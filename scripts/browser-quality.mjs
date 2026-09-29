/** Real browser audit against the baked container, never mocked lesson results. */
import { chromium, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import crypto from 'node:crypto';
const base = process.env.ELP_BROWSER_URL || 'http://127.0.0.1:8767';
const out = 'docs/course-quality';
fs.mkdirSync(out, { recursive: true });
const catalog = await (await fetch(`${base}/api/v1/catalog`)).json();
const browser = await chromium.launch({ headless: true });
const rows = [], interactions = [], screenshots = [];
const saveReport = () => {
  const file = process.env.ELP_BROWSER_REPORT || `${out}/browser-report.json`;
  fs.writeFileSync(`${file}.tmp`, JSON.stringify({ validation_level: 'automated_chromium', browser_version: browser.version(), base, experiment_request_concurrency: 1, page_inspection_concurrency: 1, concurrent_capacity_claimed: false, rows, interactions, screenshots, manual_screen_reader: 'not_run', representative_learners: 'not_run' }, null, 2) + '\n');
  fs.renameSync(`${file}.tmp`, file);
};
const selected = process.env.ELP_BROWSER_COURSE;
const selectedModule = process.env.ELP_BROWSER_MODULE;
const semanticSelection = { 'controls-gnc': [36, 38, 42, 43, 45, 46, 47, 48, 49, 50, 51, 55, 66, 67, 68], 'robotics-autonomy': [68, 69], 'vehicle-dynamics': [61, 62, 63, 64, 65, 66, 67] };
const cumulative = new Set([10, 20, 28, 40, 52, 60, 68, 74, 83, 84]);
const isCumulative = (course, module) => course.id === 'dsp-radar' && cumulative.has(module.number);
const isRevised = (course, module) => semanticSelection[course.id]?.includes(module.number) ?? false;
for (const [viewport, size] of Object.entries({ desktop: { width: 1440, height: 1000 }, mobile: { width: 390, height: 844 } })) {
  const context = await browser.newContext({ viewport: size });
  // Inspect complete pages and pace real experiment requests like one learner.
  // No request parameters, response bodies, runtime limits or assertions change.
  let runTurn = Promise.resolve();
  await context.route('**/run', async route => {
    const previous = runTurn;
    let release;
    runTurn = new Promise(resolve => { release = resolve; });
    await previous;
    try {
      await route.continue();
      await route.request().response();
    } finally { release(); }
  });
  for (const course of catalog.filter(c => !selected || c.id === selected)) {
    const page = await context.newPage();
    page.setDefaultTimeout(30000);
    let errors = [];
    page.on('pageerror', e => errors.push(e.message));
    for (const module of course.modules.filter(m => !selectedModule || m.id === selectedModule)) {
      errors = [];
      const row = { course: course.id, module: module.id, viewport, status: 'failed' };
      try {
        const path = `/courses/${course.id}/modules/${module.id}`;
        const doc = await (await fetch(`${base}/api/v1${path}`)).json();
        row.content_digest = doc.module_revision.content_digest;
        await page.goto(`${base}${path}`);
        const expectedPlots = doc.module.blocks.reduce((count, b) => count + (b.type === 'plot' ? 1 : b.type === 'plot_grid' ? b.plots.length : 0), 0);
        await page.waitForFunction(count => document.querySelectorAll('.js-plotly-plot').length === count && !document.querySelector('.plot-empty') && !document.querySelector('.runtime-error'), expectedPlots, { timeout: 60000 });
        await page.locator('.compute-status:visible').first().filter({ hasText: 'Experiment synchronized' }).waitFor({ timeout: 60000 });
        await page.waitForTimeout(100);
        const axe = await new AxeBuilder({ page }).analyze();
        row.violations = axe.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target) }));
        row.plot_count = await page.locator('.js-plotly-plot').count();
        row.metric_count = await page.locator('.metric').count();
        row.math_count = await page.locator('.katex').count();
        row.math_errors = await page.locator('.katex-error').count();
        row.plot_errors = await page.locator('.error-inline:visible').allTextContents();
        row.unsupported_webgl = await page.locator('.js-plotly-plot').getByText(/WebGL/i).count();
        row.title_errors = await page.locator('.js-plotly-plot').evaluateAll(nodes => nodes.flatMap((node, index) => {
          const failures = [];
          const check = (input, rendered, path) => {
            if (!input || typeof input !== 'object' || Array.isArray(input) || input.visible === false || input.showscale === false) return;
            for (const [key, value] of Object.entries(input)) {
              if (key === 'title') {
                const expected = typeof value === 'string' ? value : value?.text;
                if (expected && rendered?.title?.text !== expected) failures.push(`${index}:${path}.title`);
              } else if (value && typeof value === 'object' && !Array.isArray(value)) check(value, rendered?.[key], `${path}.${key}`);
            }
          };
          check(node.layout, node._fullLayout, 'layout');
          node.data?.forEach((trace, i) => {
            if (trace.showscale !== false) check(trace.colorbar, node._fullData?.[i]?.colorbar, `trace${i}.colorbar`);
          });
          return failures;
        }));
        row.horizontal_overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
        row.errors = errors;
        row.mobile_navigation_hidden = viewport !== 'mobile' || await page.locator('.sidebar').getAttribute('inert') !== null;
        if (errors.length || row.plot_errors.length || row.unsupported_webgl || row.title_errors.length || row.horizontal_overflow || row.math_errors || !row.mobile_navigation_hidden || row.violations.some(v => ['serious', 'critical'].includes(v.impact))) throw new Error('Delivery or automated accessibility assertion failed');
        const source = Object.values(doc.markdown_sources).join('\n');
        if (/\\\[|\\\(|\$\$/.test(source) && !row.math_count) throw new Error('Authored equations were not rendered');
        if (doc.module.blocks.some(b => b.type === 'metrics') && !row.metric_count) throw new Error('Missing metrics');
        if (course.id === 'dsp-radar') {
          row.drawn_plots = await page.locator('.js-plotly-plot').evaluateAll(nodes => nodes.filter(node => node.querySelector('.scatterlayer .trace path, .heatmaplayer image, .barlayer path, .contourlayer path')).length);
          if (row.drawn_plots !== expectedPlots) throw new Error('DSP plot lacks drawn trace/image evidence');
          const jump = page.getByRole('navigation', {name:'Lesson sections'}).getByRole('link', {name:'Course checkpoint', exact:true});
          await jump.click();
          const heading = page.getByRole('heading', {name:'Course checkpoint', exact:true});
          await expect(heading).toBeInViewport();
          row.checkpoint_in_viewport = true;
          const checkpoint = heading.locator('..');
          const content = await checkpoint.textContent();
          row.checkpoint = content.includes(`DSP-F${String(module.number).padStart(2,'0')}`) && content.includes('Check your reasoning.') && content.includes('No learner score or completion is stored.');
          if (!row.checkpoint) throw new Error('Missing authored checkpoint or learner boundary');
          row.cumulative = isCumulative(course, module) ? content.includes('Cumulative assessment DSP-A') && content.includes('Assessment rubric.') : null;
          if (isCumulative(course, module)) {
            if (!row.cumulative) throw new Error('Missing cumulative task/rubric');
            const file = `${out}/assessment-dsp-${module.number}-${viewport}.png`;
            await checkpoint.screenshot({path:file});
            screenshots.push({path:file,sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')});
          }
        }
        if (course.id === 'controls-gnc' && [36,38,42,43,45,46,47,48,49,50,51,55].includes(module.number)) {
          const jump = page.getByRole('navigation', {name:'Lesson sections'}).getByRole('link', {name:'Course checkpoint', exact:true});
          await jump.click();
          const heading = page.getByRole('heading', {name:'Course checkpoint', exact:true});
          await expect(heading).toBeInViewport();
          const content = await heading.locator('..').textContent();
          if (!content.includes(`P${module.number} evidence task`) || !content.includes('Reasoning rubric') || !content.includes('no learner score is stored')) throw new Error('Missing Controls evidence task, rubric or learner boundary');
          row.checkpoint_in_viewport = true;
          row.checkpoint = true;
        }
        row.status = 'passed';
        if (module === course.modules.at(-1)) {
          const file = `${out}/${course.id}-${viewport}.png`;
          await page.screenshot({ path: file });
          screenshots.push({ path: file, sha256: crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex') });
        }
        if (module === course.modules[0] || isRevised(course, module) || isCumulative(course, module)) {
          const controls = page.locator('.control-panel:visible');
          const before = await page.locator('.metric').allTextContents();
          const choice = controls.locator('select').first();
          const slider = controls.locator('input[type=range]').first();
          const segmented = controls.locator('.segmented button[aria-pressed="false"]').first();
          const toggle = controls.locator('input[type=checkbox]').last();
          const act = { course: course.id, module: module.id, viewport, reset: false, control_changed: false, failure_recovery: 'not_available' };
          const waitRun = async action => {
            const response = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
            await action(); const r = await response; if (!r.ok()) throw new Error('Control run failed');
            const payload = await r.json();
            await page.locator('.compute-status:visible').first().filter({ hasText: 'Experiment synchronized' }).waitFor();
            await page.waitForTimeout(100); return payload;
          };
          if (await slider.count()) { await waitRun(async () => { await slider.focus(); await slider.press('ArrowRight'); }); act.control_changed = true; }
          else if (await choice.count()) { const options = await choice.locator('option').evaluateAll(x => x.map(o => o.value)); await waitRun(() => choice.selectOption(options.find(v => v !== doc.default_parameters[doc.module.controls.find(c => c.type === 'select').id]))); act.control_changed = true; }
          else if (await segmented.count()) { await waitRun(() => segmented.click()); act.control_changed = true; }
          if (await toggle.count()) {
            const initial = await toggle.isChecked();
            const broken = await waitRun(() => toggle.setChecked(!initial));
            const recovered = await waitRun(() => toggle.setChecked(initial));
            act.failure_recovery = JSON.stringify(broken.plots) !== JSON.stringify(recovered.plots) || JSON.stringify(broken.metrics) !== JSON.stringify(recovered.metrics) ? 'passed' : 'no_observable_change';
          }
          await waitRun(() => controls.getByRole('button', { name: 'Reset parameters' }).click());
          act.reset = JSON.stringify(before) === JSON.stringify(await page.locator('.metric').allTextContents());
          act.post_interaction_plot_errors = await page.locator('.error-inline, .runtime-error').allTextContents();
          act.unsupported_webgl = await page.locator('.js-plotly-plot').getByText(/WebGL/i).count();
          if (isRevised(course, module)) {
            // These bounded line plots use SVG: require actual drawn curves,
            // not merely a Plotly container, axes, or serialized result.
            act.drawn_svg_plots = await page.locator('.js-plotly-plot').evaluateAll(nodes => nodes.filter(node => node.querySelector('.scatterlayer .trace path')).length);
            if (act.drawn_svg_plots !== expectedPlots) throw new Error('Revised plot has no drawn SVG trace');
          }
          if (act.unsupported_webgl || act.post_interaction_plot_errors.length) throw new Error('Post-interaction plot rendering failed');
          interactions.push(act);
          if (isRevised(course, module)) {
            const file = `${out}/revision-${course.id}-${module.number}-${viewport}.png`;
            await page.screenshot({ path: file, fullPage: true });
            screenshots.push({ path: file, sha256: crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex') });
          }
          if (!act.reset || !act.control_changed || act.failure_recovery === 'no_observable_change') throw new Error('Representative interaction failed');
        }
      } catch (error) { row.status = 'failed'; row.failure = String(error); row.runtime_errors = await page.locator('.runtime-error, .error-inline').allTextContents(); row.errors = errors; }
      rows.push(row);
      saveReport();
      console.log(`${rows.length} ${viewport} ${course.id}/${module.id} ${row.status}${row.failure ? ' ' + row.failure : ''}`);
    }
    await page.close();
  }
  await context.close();
}
await browser.close();
if (rows.some(r => r.status !== 'passed')) process.exitCode = 1;
