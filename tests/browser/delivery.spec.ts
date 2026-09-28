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
  await page.goto('/courses/robotics-autonomy/modules/26-compose-rotations-and-poses-on-so-3-and-se-3');
  await expect(page.getByRole('note')).toContainText('Under revision');
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
