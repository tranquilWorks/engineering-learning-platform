/** Normalize source TeX delimiters without rewriting Markdown code or currency. */
export function normalizeMath(source: string): string {
  // Text-mode equations in legacy lessons contain literal programming notation.
  // Escape reserved characters there without changing the authored relation.
  const literalMath = (math: string) => {
    // Scan balanced groups: programming notation such as x_{k+1} contains
    // nested braces even though the surrounding command requests literal text.
    let result = '', cursor = 0;
    for (const match of math.matchAll(/\\text\{/g)) {
      if (match.index! < cursor) continue;
      const start = match.index! + match[0].length;
      let end = start, depth = 1;
      for (; end < math.length && depth; end++) {
        if (math[end] === '\\') { end++; continue; }
        if (math[end] === '{') depth++;
        if (math[end] === '}') depth--;
      }
      if (depth) continue;
      const content = math.slice(start, end - 1).replace(/(?<!\\)([{}_#$%&^~])/g,
        (char) => char === '^' || char === '~' ? `\\${char}{}` : `\\${char}`);
      result += math.slice(cursor, match.index) + `\\text{${content}}`;
      cursor = end;
    }
    return (result + math.slice(cursor)).replace(/(?<!\\)#/g, '\\#');
  };
  const convert = (text: string) => text
    .replace(/\\\[([\s\S]*?)\\\]/g, (_, math: string) => `\n\n$$\n${literalMath(math.trim())}\n$$\n\n`)
    .replace(/\\\(([^\n]*?)\\\)/g, (_, math: string) => `$${literalMath(math.trim())}$`);
  const prose = (text: string) => {
    // Protect code spans and existing math before changing TeX delimiters.
    const tokens = /(`+)[\s\S]*?\1|\$\$[\s\S]*?\$\$|(?<!\\)\$[^\n$]+?\$/g;
    let result = '', end = 0;
    for (const token of text.matchAll(tokens)) {
      const value = /^\$[\d,.]+\s+(?:and|or|to)\s+\$$/.test(token[0])
        ? token[0].replace(/\$/g, '\\$') : token[0].startsWith('`') ? token[0] : literalMath(token[0]);
      result += convert(text.slice(end, token.index)) + value;
      end = token.index! + token[0].length;
    }
    return result + convert(text.slice(end));
  };
  let result = '', pending = '', fence: { char: string; length: number } | null = null;
  for (const line of source.match(/[^\n]*\n|[^\n]+$/g) ?? []) {
    const marker = /^ {0,3}(`{3,}|~{3,})/.exec(line)?.[1];
    if (fence) {
      result += line;
      if (marker?.[0] === fence.char && marker.length >= fence.length && /^ {0,3}[`~]+\s*$/.test(line)) fence = null;
    } else if (marker || /^(?: {4}|\t)/.test(line)) {
      result += prose(pending) + line; pending = '';
      if (marker) fence = { char: marker[0]!, length: marker.length };
    } else pending += line;
  }
  return result + prose(pending);
}
