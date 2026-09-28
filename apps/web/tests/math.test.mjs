import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeMath } from '../src/lib/math.ts';
test('source display and inline equations normalize', () => {
  assert.equal(normalizeMath(String.raw`Speed \(v=R\omega\), then \[a=v^2/R\]`), 'Speed $v=R\\omega$, then \n\n$$\na=v^2/R\n$$\n\n');
});
test('fenced and inline code remain byte identical', () => {
  for (const code of [String.raw`\`\[x\]\``, '```tex\n\\[x\\]\n```', '~~~tex\n\\[x\\]\n~~~', '    \\[x\\]']) assert.equal(normalizeMath(code), code);
});
test('existing dollar math and currency are preserved', () => {
  for (const text of ['$x^2$ and $$y$$', '$20 and $30', String.raw`Cost \$20; \(x\)`]) {
    if (text.includes('Cost')) assert.equal(normalizeMath(text), String.raw`Cost \$20; $x$`);
    else assert.equal(normalizeMath(text), text === '$20 and $30' ? '\\$20 and \\$30' : text);
  }
});
test('multiple source equations do not merge', () => {
  assert.equal(normalizeMath(String.raw`\(x\) and \(y\)`), '$x$ and $y$');
});

test('unterminated and longer closing fences preserve literal source', () => {
  for (const code of ['```tex\n\\[x\\]\n', '~~~tex\n\\[x\\]\n~~~~\n']) assert.equal(normalizeMath(code), code);
});
test('legacy text-mode equation notation is literal and valid KaTeX', async () => {
  const { default: katex } = await import('katex');
  for (const math of [String.raw`\text{tau_g=m*g*l*sin(theta)}`, String.raw`\text{G(s)=C(sI-A)^-1B}`, 'q_dot=J# v+ (I-J#J)z']) {
    const normalized = normalizeMath(`$$${math}$$`).slice(2, -2);
    assert.doesNotThrow(() => katex.renderToString(normalized, { throwOnError: true }));
  }
  assert.equal(normalizeMath(String.raw`\`J#\``), String.raw`\`J#\``);
});

test('nested legacy text groups preserve literal braces and render', async () => {
  const { default: katex } = await import('katex');
  const source = String.raw`$$\text{P^s_k=P_k+C_k(P^s_{k+1}-P^-_{k+1})C_k^T}$$`;
  const math = normalizeMath(source).slice(2, -2);
  assert.ok(math.includes(String.raw`\{k+1\}`));
  assert.doesNotThrow(() => katex.renderToString(math, { throwOnError: true }));
});

test('every retained native lesson renders without a KaTeX parse error', async () => {
  const { globSync, readFileSync } = await import('node:fs');
  const { createElement } = await import('react');
  const { renderToStaticMarkup } = await import('react-dom/server');
  const { default: Markdown } = await import('react-markdown');
  const { default: remarkMath } = await import('remark-math');
  const { default: rehypeKatex } = await import('rehype-katex');
  const paths = [...globSync('courses/*/modules/*/lesson.md')];
  assert.ok(paths.length >= 288);
  const errors = [];
  for (const path of paths) {
    const html = renderToStaticMarkup(createElement(Markdown, {
      remarkPlugins: [remarkMath], rehypePlugins: [rehypeKatex],
      children: normalizeMath(readFileSync(path, 'utf8')),
    }));
    if (html.includes('katex-error')) errors.push(path);
  }
  assert.deepEqual(errors, []);
});
