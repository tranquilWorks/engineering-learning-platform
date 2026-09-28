import ReactMarkdown from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { normalizeMath } from "../lib/math";
import { memo, useEffect, useRef } from "react";

interface Props {
  children: string;
  courseId: string;
  moduleId: string;
}

function isExternal(value: string): boolean {
  return /^(?:[a-z]+:|\/|#)/i.test(value);
}

function moduleAsset(courseId: string, moduleId: string, value: string): string {
  if (isExternal(value)) return value;
  const cleaned = value.replace(/^\.\//, "").replace(/^assets\//, "");
  return `/api/v1/courses/${encodeURIComponent(courseId)}/modules/${encodeURIComponent(moduleId)}/assets/${cleaned.split("/").map(encodeURIComponent).join("/")}`;
}

export const Markdown = memo(function Markdown({ children, courseId, moduleId }: Props) {
  const root = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const node = root.current;
    if (!node) return;
    const update = () => {
      node.querySelectorAll<HTMLElement>(".katex").forEach((math) => {
        const html = math.querySelector<HTMLElement>(".katex-html");
        const width = Math.max(html?.scrollWidth ?? 0, html?.getBoundingClientRect().width ?? 0);
        const available = Math.min(node.clientWidth, math.parentElement?.clientWidth || node.clientWidth);
        const overflow = width > available + 1;
        math.classList.toggle("math-scroll", overflow);
        if (overflow) {
          math.tabIndex = 0;
          math.setAttribute("role", "group");
          math.setAttribute("aria-label", "Scrollable equation");
        } else {
          math.removeAttribute("tabindex");
          math.removeAttribute("role");
          math.removeAttribute("aria-label");
        }
      });
    };
    update();
    const observer = new ResizeObserver(update);
    observer.observe(node);
    node.querySelectorAll(".katex, .katex-display").forEach((math) => observer.observe(math));
    document.fonts.addEventListener("loadingdone", update);
    return () => {
      observer.disconnect();
      document.fonts.removeEventListener("loadingdone", update);
    };
  }, [children]);
  return (
    <div ref={root} className="prose">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          pre: ({ children }) => <pre tabIndex={0} role="group" aria-label="Code block">{children}</pre>,
          table: ({ children }) => <div className="table-scroll" tabIndex={0} role="group" aria-label="Lesson table"><table>{children}</table></div>,
          li: ({ children, className }) => (
            <li className={className}>
              {className?.includes("task-list-item") ? <label>{children}</label> : children}
            </li>
          ),
          img: ({ src, alt, ...props }) => (
            <img {...props} src={src ? moduleAsset(courseId, moduleId, src) : undefined} alt={alt ?? ""} loading="lazy" />
          ),
        }}
      >
        {normalizeMath(children)}
      </ReactMarkdown>
    </div>
  );
});
