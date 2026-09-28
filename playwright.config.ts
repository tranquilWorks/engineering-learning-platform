import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/browser', workers: 1, timeout: 90000,
  outputDir: '.state/browser-tests', reporter: 'list',
  use: { baseURL: process.env.ELP_BROWSER_URL || 'http://127.0.0.1:8767', viewport: { width: 1440, height: 1000 } },
});
