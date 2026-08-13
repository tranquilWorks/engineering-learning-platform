import ReactMarkdown from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

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

export function Markdown({ children, courseId, moduleId }: Props) {
  return (
    <div className="prose">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          img: ({ src, alt, ...props }) => (
            <img {...props} src={src ? moduleAsset(courseId, moduleId, src) : undefined} alt={alt ?? ""} loading="lazy" />
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
