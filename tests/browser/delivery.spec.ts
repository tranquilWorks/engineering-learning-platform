import { test, expect, chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const path = '/courses/dsp-radar/modules/84-run-the-end-to-end-radar-processing-capstone';
test('source equations, revision disclosure, plot ranges and mobile keyboard navigation', async ({ page }) => {
  await page.goto(path);
  await expect(page.locator('.js-plotly-plot').first()).toBeVisible();
  await expect(page.locator('.katex').first()).toBeVisible();
  await expect(page.locator('.katex-error')).toHaveCount(0);
  await expect(page.locator('.revision-diagnostics details')).not.toHaveAttribute('open');
  await page.locator('.plot-values summary').first().click();
  await expect(page.locator('.plot-values table').first()).toBeVisible();
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(page.locator('.sidebar')).toHaveAttribute('inert');
  await page.getByRole('button', { name: 'Open navigation', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Close navigation', exact: true })).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button', { name: 'Open navigation', exact: true })).toBeFocused();
  await expect(page.locator('.sidebar')).toHaveAttribute('inert');
});
test('stale revision response is rejected visibly', async ({ page }) => {
  await page.route('**/modules/*/run', async route => {
    const response = await route.fetch();
    const payload = await response.json();
    payload.module_revision.content_digest = '0'.repeat(64);
    await route.fulfill({ response, json: payload });
  });
  await page.goto(path);
  await expect(page.locator('.runtime-error')).toContainText('stale content revision');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(0);
});
test('delayed old run cannot replace a changed parameter or next lesson', async ({ page }) => {
  let intercepted = false;
  await page.route('**/modules/*/run', async route => {
    if (intercepted) { await route.continue(); return; }
    intercepted = true;
    const response = await route.fetch();
    const payload = await response.json();
    payload.metrics[0].label = 'STALE SENTINEL';
    await new Promise(resolve => setTimeout(resolve, 2000));
    await route.fulfill({ response, json: payload }).catch(() => {});
  });
  await page.goto(path);
  await expect.poll(() => intercepted).toBe(true);
  const select = page.locator('.desktop-controls select').first();
  const options = await select.locator('option').evaluateAll(options => options.map(option => (option as HTMLOptionElement).value));
  await select.selectOption(options[1]);
  await expect(page.locator('.js-plotly-plot').first()).toBeVisible();
  await page.waitForTimeout(2300);
  await expect(page.getByText('STALE SENTINEL')).toHaveCount(0);
  await page.locator('.module-nav-list button').first().click();
  await expect(page.locator('.module-hero h1')).not.toContainText('end-to-end');
  await expect(page.locator('.js-plotly-plot').first()).toBeVisible();
  await expect(page.getByText('STALE SENTINEL')).toHaveCount(0);
});

test('rendered math preserves literal code and currency', async ({ page }) => {
  await page.route('**/api/v1/courses/*/modules/*', async route => {
    if (route.request().method() !== 'GET') return route.continue();
    const response = await route.fetch();
    const payload = await response.json();
    payload.module.blocks = [{ type: 'markdown', text: String.raw`Cost $20 and $30. Inline \(v=2\).` + '\n\n```tex\n' + String.raw`\[literal\]` + '\n```\n\n- [ ] Explain the sampling limit', source: null, title: null }];
    await route.fulfill({ response, json: payload });
  });
  await page.goto(path);
  await expect(page.locator('.prose')).toContainText('Cost $20 and $30.');
  await expect(page.locator('.prose code')).toContainText('literal');
  await expect(page.locator('.katex')).toHaveCount(1);
  await expect(page.getByRole('checkbox', { name: 'Explain the sampling limit' })).toBeDisabled();
});

test('numeric menu defaults survive JavaScript serialization', async ({ page }) => {
  await page.goto('/courses/dsp-radar/modules/17-perform-complex-downconversion-by-hand');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(4);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
  const option = page.locator('.desktop-controls').getByRole('button', { name: '216 broken probe', exact: true });
  const response = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
  await option.click();
  expect((await response).ok()).toBe(true);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
});
test('content review notes remain distinct from execution failures', async ({ page }) => {
  await page.goto('/courses/vehicle-dynamics/modules/13-map-engine-torque-through-gearing');
  await expect(page.getByRole('note')).toContainText('Under revision');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(4);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
  await page.goto('/courses/robotics-autonomy/modules/26-compose-rotations-and-poses-on-so-3-and-se-3');
  await expect(page.getByRole('note')).toHaveCount(0);
  await page.getByText('Lesson review and evidence', {exact:true}).click();
  await expect(page.locator('.lesson-quality')).toContainText('Scoped model revision:');
  await expect(page.locator('.lesson-quality')).toContainText('does not certify the whole course');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
});

test('equation scrolling is keyboard reachable on a mobile lesson', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.route('**/api/v1/courses/robotics-autonomy/modules/*', async route => {
    const response = await route.fetch();
    const payload = await response.json();
    payload.markdown_sources['lesson.md'] += '\n\n$$\\text{' + 'scrollable equation '.repeat(20) + '}$$';
    await route.fulfill({ response, json: payload });
  });
  await page.goto('/courses/robotics-autonomy/modules/01-drive-a-differential-robot-with-wheel-speeds');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations.filter(v => ['serious', 'critical'].includes(v.impact))).toEqual([]);
  const equations = page.locator('.katex[tabindex="0"]');
  expect(await equations.count()).toBeGreaterThan(0);
  await equations.first().focus();
  await expect(equations.first()).toBeFocused();
  await equations.first().press('ArrowRight');
  await expect.poll(() => equations.first().evaluate(node => node.scrollLeft)).toBeGreaterThan(0);
});

test('wide code blocks and lesson tables support keyboard scrolling', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/courses/dsp-radar/modules/58-implement-track-initiation-confirmation-coasting-and-deletion');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(5);
  const code = page.getByRole('group', { name: 'Code block', exact: true }).filter({ hasText: 'inactive -> tentative' });
  await expect(code).toHaveAttribute('tabindex', '0');
  expect(await code.evaluate(node => node.scrollWidth > node.clientWidth)).toBe(true);
  await code.focus();
  await code.press('ArrowRight');
  await expect.poll(() => code.evaluate(node => node.scrollLeft)).toBeGreaterThan(0);
  const axe = await new AxeBuilder({ page }).analyze();
  expect(axe.violations.filter(v => ['critical','serious'].includes(v.impact || ''))).toEqual([]);
  await page.locator('.plot-values summary').first().click();
  const ranges = page.locator('.plot-values .table-scroll').first();
  await ranges.focus();
  await expect(ranges).toBeFocused();
});

test('long inline expressions and metric names wrap within mobile lessons', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const lesson of [
    'controls-gnc/modules/07-see-stability-margin-in-time-and-frequency',
    'controls-gnc/modules/21-generate-a-feasible-trajectory',
    'vehicle-dynamics/modules/08-separate-understeer-from-oversteer',
  ]) {
    await page.goto('/courses/' + lesson);
    await expect(page.locator('.js-plotly-plot').first()).toBeVisible();
    await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth)).toBe(390);
    await page.locator('.plot-values summary').first().click();
    await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth)).toBe(390);
  }
});

test('authored axis and colorbar units appear in the rendered charts', async ({ page }) => {
  await page.goto('/courses/dsp-radar/modules/11-make-fft-bins-concrete');
  const bins = page.locator('.js-plotly-plot').first();
  await expect(bins.locator('.xtitle')).toHaveText('Signed frequency (Hz)');
  await expect(bins.locator('.ytitle')).toHaveText('Normalized magnitude (V)');
  await expect(page.locator('.y2title')).toHaveText('Bin spacing (Hz)');
  await page.goto('/courses/dsp-radar/modules/70-create-an-fmcw-range-doppler-map');
  await expect(page.locator('.cbtitle').filter({ hasText: /^dB$/ }).first()).toBeVisible();
});


test('repaired capstone exposes scoped review and computed requirement failure', async ({ page }) => {
  await page.goto('/courses/controls-gnc/modules/66-capstone-identify-control-estimate-and-stress-a-plant');
  await expect(page.locator('.compute-status:visible').first()).toContainText('Experiment synchronized');
  await expect(page.locator('.lesson-content-note')).toHaveCount(0);
  await page.getByText('Lesson review and evidence', { exact: true }).click();
  await expect(page.getByText('Scoped model revision:', { exact: true })).toBeVisible();
  const rank = page.getByRole('row').filter({ hasText: 'Calibration regressor rank' });
  await expect(rank).toContainText('pass');
  const response = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
  await page.locator('.control-panel:visible').getByRole('checkbox').check();
  expect((await response).ok()).toBe(true);
  await expect(rank).toContainText('fail');
  await expect(page.locator('.runtime-error')).toHaveCount(0);
});

test('repaired bounded plots keep drawn SVG curves after failure and reset', async ({ page }) => {
  await page.goto('/courses/vehicle-dynamics/modules/64-run-a-forward-backward-lap-time-simulation');
  const controls = page.locator('.control-panel:visible');
  const assertDrawn = async () => {
    await expect(page.locator('.compute-status:visible').first()).toContainText('Experiment synchronized');
    await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
    for (const plot of await page.locator('.js-plotly-plot').all()) {
      await expect(plot.locator('.scatterlayer .trace path').first()).toBeVisible();
      expect(await plot.evaluate((node: any) => node.data.every((trace: any) => trace.type === 'scatter'))).toBe(true);
    }
    await expect(page.locator('.js-plotly-plot').getByText(/WebGL/i)).toHaveCount(0);
  };
  await assertDrawn();
  for (const action of [() => controls.getByRole('checkbox').check(), () => controls.getByRole('button', { name: 'Reset parameters' }).click()]) {
    const response = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
    await action();
    expect((await response).ok()).toBe(true);
    await assertDrawn();
  }
});

test('existing WebGL lesson draws unchanged curves when WebGL is disabled', async ({ baseURL }) => {
  const browser = await chromium.launch({ args: ['--disable-webgl'] });
  try {
    const page = await browser.newPage();
    const response = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
    await page.goto(baseURL + '/courses/controls-gnc/modules/01-watch-a-mass-spring-damper-respond');
    const result = await (await response).json();
    await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
    for (const [index, plot] of (await page.locator('.js-plotly-plot').all()).entries()) {
      await expect(plot.locator('.scatterlayer .trace path').first()).toBeVisible();
      const drawn = await plot.evaluate((node: any) => node.data.map((trace: any) => ({ type: trace.type, x: trace.x, y: trace.y })));
      const authored = Object.values(result.plots)[index] as any;
      expect(authored.data.every((trace: any) => trace.type === 'scattergl')).toBe(true);
      expect(drawn).toEqual(authored.data.map((trace: any) => ({ type: 'scatter', x: trace.x, y: trace.y })));
      const legend = await plot.locator('.legend').boundingBox();
      const axisTitle = await plot.locator('.xtitle').boundingBox();
      expect(legend && axisTitle && axisTitle.y + axisTitle.height < legend.y).toBeTruthy();
      if (index === 1) {
        const topAxis = await plot.locator('.x2title').boundingBox();
        const chartTitle = await plot.locator('.gtitle').boundingBox();
        expect(topAxis && chartTitle && chartTitle.y + chartTitle.height < topAxis.y).toBeTruthy();
      }
    }
    await expect(page.locator('.js-plotly-plot').getByText(/WebGL/i)).toHaveCount(0);
  } finally { await browser.close(); }
});

test('chart initialization failure falls back even after a successful context probe', async ({ page }) => {
  await page.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (kind: any, options?: any): any {
      // The capability probe has no options. Chart initialization requests
      // options and fails: exercise real Plotly fallback, never mock run data.
      if ((kind === 'webgl' || kind === 'experimental-webgl') && options) return null;
      return original.call(this, kind, options);
    } as typeof original;
  });
  await page.goto('/courses/controls-gnc/modules/01-watch-a-mass-spring-damper-respond');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
  for (const plot of await page.locator('.js-plotly-plot').all()) {
    await expect(plot.locator('.scatterlayer .trace path').first()).toBeVisible();
  }
  await expect(page.locator('.no-webgl')).toHaveCount(0);
  await expect(page.locator('.error-inline')).toHaveCount(0);
});


test('authored checkpoint navigation exposes real cumulative evidence on desktop and mobile', async ({ page }) => {
  for (const width of [1440, 390]) {
    await page.setViewportSize({width, height:1000});
    for (const module of ['20-estimate-tone-frequency-and-phase-from-noisy-samples', '84-run-the-end-to-end-radar-processing-capstone']) {
      const response = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
      await page.goto('/courses/dsp-radar/modules/' + module);
      expect((await response).ok()).toBe(true);
      await page.locator('.compute-status:visible').first().filter({hasText:'Experiment synchronized'}).waitFor();
      const nav = page.getByRole('navigation', {name:'Lesson sections'});
      const checkpointLink = nav.getByRole('link', {name:'Course checkpoint', exact:true});
      await checkpointLink.focus();
      await page.keyboard.press('Enter');
      const heading = page.getByRole('heading', {name:'Course checkpoint', exact:true});
      await expect(heading).toBeInViewport();
      const section = heading.locator('..');
      await expect(section.getByRole('heading', {name:/Cumulative assessment DSP-A/})).toBeVisible();
      await expect(section).toContainText('No learner score or completion is stored.');
      if (module.startsWith('84')) await expect(section).toContainText('fixed baseline');
      await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth)).toBe(width);
      const checkpointHash = await page.evaluate(() => location.hash);
      const conceptLink = nav.getByRole('link', {name:'Concept', exact:true});
      const conceptId = await conceptLink.getAttribute('href');
      await conceptLink.focus();
      await page.keyboard.press('Enter');
      await expect(page.locator(conceptId!)).toBeInViewport();
      await page.goBack();
      await expect.poll(() => page.evaluate(() => location.hash)).toBe(checkpointHash);
      await expect(heading).toBeInViewport();
      await page.goForward();
      await expect(page.locator(conceptId!)).toBeInViewport();
      await checkpointLink.click();
      await expect(heading).toBeInViewport();
      if (module.startsWith('20')) {
        const nextResponse = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
        await page.getByRole('button', {name:'Next module'}).click();
        await expect(page).toHaveURL(/modules\/21-/);
        await expect(page.locator('#lesson-main')).toBeFocused();
        await expect.poll(() => page.evaluate(() => scrollY)).toBe(0);
        expect((await nextResponse).ok()).toBe(true);
      }
    }
  }
});


test('trajectory feasibility fast path preserves real desktop and mobile fault recovery', async ({ page }) => {
  for (const width of [1440, 390]) {
    await page.setViewportSize({width, height:1000});
    const response = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
    await page.goto('/courses/robotics-autonomy/modules/58-optimize-a-trajectory-through-obstacle-constraints');
    const initial = await response;
    expect(initial.ok()).toBe(true);
    const baseline = await initial.json();
    expect(baseline.diagnostics.signature[2]).toBe(0);
    const controls = page.locator('.control-panel:visible');
    const drawn = async () => {
      await expect(page.locator('.compute-status:visible').first()).toContainText('Experiment synchronized');
      await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
      for (const plot of await page.locator('.js-plotly-plot').all()) {
        // A horizontal SVG line has zero-height geometry despite a visible stroke.
        await expect(plot.locator('.scatterlayer .trace path.point').first()).toBeVisible();
        await expect(plot.locator('.scatterlayer .trace path.js-line').first()).toHaveAttribute('d', /M.+L/);
      }
      await expect(page.locator('.runtime-error')).toHaveCount(0);
    };
    await drawn();
    const failedResponse = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
    await controls.getByRole('checkbox').check();
    const failed = await failedResponse;
    expect(failed.ok()).toBe(true);
    expect((await failed.json()).diagnostics.signature[2]).toBeGreaterThan(0);
    await drawn();
    const recoveredResponse = page.waitForResponse(r => r.url().endsWith('/run') && r.request().method() === 'POST');
    await controls.getByRole('button', {name:'Reset parameters'}).click();
    const recovered = await recoveredResponse;
    expect(recovered.ok()).toBe(true);
    expect((await recovered.json()).diagnostics.signature).toEqual(baseline.diagnostics.signature);
    await drawn();
  }
});

test('Controls sigma-point checkpoint preserves the covariance distinction and actual fault', async ({ page }) => {
  await page.goto('/courses/controls-gnc/modules/55-transform-uncertainty-with-an-unscented-kalman-filter');
  await expect(page.locator('.module-hero h1')).toContainText('Transform Gaussian Uncertainty with Sigma Points');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
  await page.setViewportSize({width:390,height:844});
  const jump=page.getByRole('navigation',{name:'Lesson sections'}).getByRole('link',{name:'Course checkpoint',exact:true});
  await jump.focus(); await page.keyboard.press('Enter');
  await expect(page.getByRole('heading',{name:'Course checkpoint',exact:true})).toBeInViewport();
  await expect(page.getByRole('heading',{name:'P55 evidence task',exact:true})).toBeVisible();
  await expect(page.locator('.prose').last()).toContainText('central covariance correction');
  const toggle=page.locator('.control-panel:visible input[type=checkbox]');
  const response=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.check(); const broken=await (await response).json();
  expect(broken.diagnostics.mean).toBeCloseTo(.64,10);
  expect(broken.diagnostics.variance).toBeCloseTo(0,10);
  const recoveredResponse=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.uncheck(); const recovered=await (await recoveredResponse).json();
  expect(recovered.diagnostics.variance).toBeCloseTo(.8192,10);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
});

test('Controls MPC browser executes a bounded plan and exposes unconstrained violation', async ({ page }) => {
  await page.goto('/courses/controls-gnc/modules/49-control-a-constrained-plant-with-model-predictive-control');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
  const toggle=page.locator('.control-panel:visible input[type=checkbox]');
  const response=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.check();const broken=await (await response).json();
  expect(broken.diagnostics.signature[1]).toBeGreaterThan(0);
  const recovery=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.uncheck();const healthy=await (await recovery).json();
  expect(healthy.diagnostics.first_plan).toHaveLength(6);
  expect(Math.max(...healthy.diagnostics.input.map(Math.abs))).toBeLessThanOrEqual(.8);
  expect(Math.max(...healthy.diagnostics.kkt_residuals)).toBeLessThan(1e-8);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
});

test('Navigation exclusion checkpoint executes a fresh seven-row fit', async ({ page }) => {
  await page.goto('/courses/controls-gnc/modules/62-monitor-navigation-integrity-and-exclude-faulty-measurements');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
  await page.setViewportSize({width:390,height:844});
  const jump=page.getByRole('navigation',{name:'Lesson sections'}).getByRole('link',{name:'Course checkpoint',exact:true});
  await jump.focus();await page.keyboard.press('Enter');
  await expect(page.getByRole('heading',{name:'Course checkpoint',exact:true})).toBeInViewport();
  const toggle=page.locator('.control-panel:visible input[type=checkbox]');
  const response=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.check();const broken=await (await response).json();
  expect(broken.diagnostics.retained_rows).toHaveLength(8);
  const recovery=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.uncheck();const recovered=await (await recovery).json();
  expect(recovered.diagnostics.retained_rows).toHaveLength(7);
  expect(recovered.diagnostics.retained_rows).not.toContain(2);
  expect(recovered.diagnostics.signature[2]).toBeLessThan(broken.diagnostics.signature[2]);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
});

test('Robotics geometry draws a real dual-power fault and recovers', async ({ page }) => {
  await page.goto('/courses/robotics-autonomy/modules/27-map-twists-screws-and-wrenches-with-adjoint-transforms');
  await expect(page.locator('.js-plotly-plot')).toHaveCount(2);
  const toggle=page.locator('.control-panel:visible input[type=checkbox]');
  const response=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.check();const broken=await (await response).json();
  expect(broken.diagnostics.signature[0]).toBeGreaterThan(.01);
  const recovery=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
  await toggle.uncheck();const recovered=await (await recovery).json();
  expect(recovered.diagnostics.signature[0]).toBeLessThan(1e-12);
  expect(recovered.diagnostics.powers.every((p:number)=>Math.abs(p-.69)<1e-12)).toBe(true);
  await expect.poll(()=>page.locator('.js-plotly-plot').evaluateAll(nodes=>nodes.filter(n=>n.querySelector('.scatterlayer .trace path')).length)).toBe(2);
  await expect(page.locator('.runtime-error')).toHaveCount(0);
});

test('zero-angle and zero-gain limits retain visible plotted points', async ({ page }) => {
  const cases = [
    ['controls-gnc/57-transform-frames-quaternions-and-sensor-alignment', 0, 'angles', 'yaw_angle_deg', 'ArrowLeft', 7],
    ['robotics-autonomy/28-build-spatial-jacobians-and-diagnose-singularities', 0, 'angles_rad', 'elbow_angle_deg', 'Home', 1],
    ['robotics-autonomy/29-resolve-redundancy-with-null-space-motion', 1, 'gains', 'null_gain_per_s', 'Home', 1],
  ] as const;
  for (const [path,index,key,parameter,button,presses] of cases) {
    await page.goto('/courses/'+path.split('/')[0]+'/modules/'+path.split('/')[1]);
    await page.locator('.compute-status:visible').first().filter({hasText:'Experiment synchronized'}).waitFor();
    const slider=page.locator('.control-panel:visible input[type=range]').nth(index);
    const response=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST' && r.request().postDataJSON().parameters[parameter]===0);
    await slider.focus();
    for(let press=0;press<presses;press++) await slider.press(button);
    const result=await (await response).json();
    expect(result.diagnostics[key].every((v:number)=>v===0)).toBe(true);
    await expect.poll(()=>page.locator('.js-plotly-plot').evaluateAll(nodes=>nodes.filter(n=>n.querySelector('.scatterlayer .trace .point')).length)).toBe(2);
    await expect(page.locator('.runtime-error')).toHaveCount(0);
  }
});


test('Vehicle bicycle balance and damping availability are exposed in the actual lesson', async ({ page }) => {
  for (const width of [1440, 390]) {
    await page.setViewportSize({width, height:1000});
    await page.goto('/courses/vehicle-dynamics/modules/07-use-the-bicycle-model');
    await expect(page.locator('.compute-status:visible').first()).toContainText('Experiment synchronized');
    await expect(page.locator('.metric').filter({hasText:'Force-balance residual'})).toContainText('N');
    const checkpoint = page.getByRole('navigation',{name:'Lesson sections'}).getByRole('link',{name:'Course checkpoint',exact:true});
    await checkpoint.click();
    await expect(page.getByRole('heading',{name:'Course checkpoint',exact:true})).toBeInViewport();
    await expect(page.getByText('P07 evidence task',{exact:true})).toBeVisible();
    const controls=page.locator('.control-panel:visible');
    const toggle=controls.locator('input[type=checkbox]').last();
    const response=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
    await toggle.check();
    const bad=await (await response).json();
    expect(Math.abs(bad.diagnostics.physical.force_balance_residual_n)).toBeGreaterThan(59000);
    expect(Math.abs(bad.diagnostics.physical.yaw_balance_residual_nm)).toBeGreaterThan(17000);
    const recovered=page.waitForResponse(r=>r.url().endsWith('/run') && r.request().method()==='POST');
    await toggle.uncheck();
    expect(Math.abs((await (await recovered).json()).diagnostics.physical.force_balance_residual_n)).toBeLessThan(1e-10);
    await page.goto('/courses/vehicle-dynamics/modules/10-see-damping-change-transient-motion');
    await expect(page.locator('.compute-status:visible').first()).toContainText('Experiment synchronized');
    await page.locator('.control-panel:visible input[type=checkbox]').last().check();
    await expect(page.locator('.metric').filter({hasText:'Four slow-pole time constants'})).toContainText('Unavailable');
    await expect(page.locator('.runtime-error')).toHaveCount(0);
  }
});
