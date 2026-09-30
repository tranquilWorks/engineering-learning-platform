import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import ts from 'typescript';

const require = createRequire(import.meta.url);
const source = fs.readFileSync(new URL('../src/components/LessonQuality.tsx', import.meta.url), 'utf8');

function renderReview(rows) {
  // Compile the unchanged trusted repository component and supply test-only JSON.
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'elp-lesson-quality-'));
  const components = path.join(directory, 'components');
  fs.mkdirSync(components);
  fs.symlinkSync(path.dirname(path.dirname(require.resolve('react/package.json'))), path.join(directory, 'node_modules'), 'dir');
  const reviewFile = path.join(directory, 'lesson-quality.json');
  const componentFile = path.join(components, 'LessonQuality.cjs');
  fs.writeFileSync(reviewFile, JSON.stringify(rows));
  const compiled = ts.transpileModule(source, {
    fileName: 'LessonQuality.tsx', reportDiagnostics: true,
    compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, esModuleInterop: true },
  });
  assert.equal(compiled.diagnostics.length, 0);
  fs.writeFileSync(componentFile, compiled.outputText);
  try {
    const { LessonQuality } = require(componentFile);
    return renderToStaticMarkup(createElement(LessonQuality, { course: 'fixture', module: 'fixture' }));
  } finally {
    delete require.cache[componentFile];
    delete require.cache[reviewFile];
    fs.rmSync(directory, { recursive: true, force: true });
  }
}

const base = { course: 'fixture', module: 'fixture', evidence_count: 5, assessment_review: null, scoped_review: null, known_issue: null };

test('an unresolved fixture issue retains its accessible review note and evidence limits', () => {
  const html = renderReview([{ ...base, known_issue: 'Force balance still needs review.' }]);
  assert.match(html, /role="note"/);
  assert.match(html, /Under revision:/);
  assert.match(html, /Force balance still needs review\./);
  assert.match(html, /presence does not establish complete subject coverage or learning effectiveness/);
  assert.match(html, /Representative learner and screen-reader validation have not been run/);
});

test('a cleared scoped review omits the stale issue note without certifying the course', () => {
  const html = renderReview([{ ...base, scoped_review: 'Independent force balance checked.' }]);
  assert.doesNotMatch(html, /role="note"|Under revision:/);
  assert.match(html, /Scoped model revision:/);
  assert.match(html, /Independent force balance checked\./);
  assert.match(html, /does not certify the whole course or learner outcomes/);
});

test('an unknown lesson invents no review or issue disclosure', () => {
  assert.equal(renderReview([]), '');
});
