import { useEffect, useMemo, useRef, useState } from "react";
import { AlertTriangle, ArrowRight, BookOpen, CheckCircle2, CircleDashed, FlaskConical, LoaderCircle, Play, SlidersHorizontal } from "lucide-react";
import { api } from "./lib/api";
import { navigate, parseRoute, type Route } from "./lib/routing";
import type { CourseSummary, ModuleDocument, RunResult } from "./types";
import { AppShell } from "./components/AppShell";
import { BlockRenderer } from "./components/BlockRenderer";
import { Controls } from "./components/Controls";

function useRoute(): Route {
  const [route, setRoute] = useState<Route>(() => parseRoute());
  useEffect(() => {
    const handler = () => setRoute(parseRoute());
    window.addEventListener("popstate", handler);
    return () => window.removeEventListener("popstate", handler);
  }, []);
  return route;
}

function ErrorPanel({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <section className="state-panel error-state">
      <AlertTriangle size={24} />
      <div><h1>Unable to load the learning experience</h1><p>{message}</p></div>
      {onRetry ? <button type="button" className="secondary-button" onClick={onRetry}>Retry</button> : null}
    </section>
  );
}

function HomePage({ catalog }: { catalog: CourseSummary[] }) {
  const moduleCount = catalog.reduce((total, course) => total + course.modules.length, 0);
  return (
    <div className="page page-home">
      <section className="hero">
        <span className="hero-kicker"><FlaskConical size={15} /> executable engineering curriculum</span>
        <h1>Build intuition by changing the system.</h1>
        <p>Short explanations, explicit predictions, live controls, MATLAB-class visualizations, and immediate numerical feedback—all in one professional learning surface.</p>
        <div className="hero-stats">
          <div><strong>{catalog.length}</strong><span>courses discovered</span></div>
          <div><strong>{moduleCount}</strong><span>modules available</span></div>
          <div><strong>1</strong><span>self-hosted port</span></div>
        </div>
      </section>
      <section className="library-section">
        <div className="section-heading"><span className="eyebrow">Course library</span><h2>Choose a learning path</h2></div>
        <div className="course-grid">
          {catalog.map((course) => (
            <button key={course.id} type="button" className="course-card" onClick={() => navigate({ kind: "course", courseId: course.id })}>
              <div className="course-card-icon"><BookOpen /></div>
              <div className="course-card-copy"><h3>{course.title}</h3><p>{course.description}</p></div>
              <div className="course-card-meta"><span>{course.modules.length} module{course.modules.length === 1 ? "" : "s"}</span><ArrowRight size={17} /></div>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

function CoursePage({ course }: { course: CourseSummary }) {
  return (
    <div className="page">
      <header className="course-header">
        <span className="eyebrow">Course</span>
        <h1>{course.title}</h1>
        <p>{course.description}</p>
        <div className="tag-row">{course.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
      </header>
      <section className="module-list-section">
        <div className="section-heading"><span className="eyebrow">Curriculum</span><h2>{course.modules.length} learning modules</h2></div>
        <div className="module-list">
          {course.modules.map((module, index) => (
            <button key={module.id} type="button" className="module-row" onClick={() => navigate({ kind: "module", courseId: course.id, moduleId: module.id })}>
              <span className="module-number">{module.number ? String(module.number).padStart(2, "0") : String(index + 1).padStart(2, "0")}</span>
              <span className="module-copy"><strong>{module.title}</strong><small>{module.summary}</small></span>
              <span className={`module-status ${module.interactive ? "interactive" : "static"}`}>{module.interactive ? <SlidersHorizontal size={14} /> : <CircleDashed size={14} />}{module.interactive ? "Interactive" : "Static"}</span>
              <ArrowRight size={18} />
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

function ModulePage({ courseId, moduleId }: { courseId: string; moduleId: string }) {
  const [document, setDocument] = useState<ModuleDocument | null>(null);
  const [parameters, setParameters] = useState<Record<string, unknown>>({});
  const [result, setResult] = useState<RunResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const runSequence = useRef(0);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true); setError(null); setDocument(null); setResult(null);
    api.module(courseId, moduleId, controller.signal)
      .then((value) => { setDocument(value); setParameters(value.default_parameters); })
      .catch((reason: unknown) => { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : "Module load failed"); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [courseId, moduleId]);

  useEffect(() => {
    if (!document || document.module.runtime.kind === "static") return;
    const sequence = ++runSequence.current;
    const controller = new AbortController();
    const timer = window.setTimeout(() => {
      setBusy(true); setError(null);
      api.run(courseId, moduleId, parameters, controller.signal)
        .then((value) => { if (sequence === runSequence.current) setResult(value); })
        .catch((reason: unknown) => { if (!controller.signal.aborted && sequence === runSequence.current) setError(reason instanceof Error ? reason.message : "Experiment failed"); })
        .finally(() => { if (!controller.signal.aborted && sequence === runSequence.current) setBusy(false); });
    }, 110);
    return () => { window.clearTimeout(timer); controller.abort(); };
  }, [courseId, document, moduleId, parameters]);

  const reset = () => document && setParameters(document.default_parameters);
  const currentIndex = document?.course.modules.findIndex((item) => item.id === moduleId) ?? -1;
  const nextModule = document && currentIndex >= 0 ? document.course.modules[currentIndex + 1] : undefined;

  if (loading) return <section className="state-panel"><LoaderCircle className="spin" /><div><h1>Loading module</h1><p>Discovering content and preparing the numerical runtime.</p></div></section>;
  if (!document) return <ErrorPanel message={error ?? "The requested module does not exist."} />;

  return (
    <div className="module-page">
      <header className="module-hero">
        <div className="module-breadcrumb">{document.course.title}<span>/</span>{document.module.number ? `Module ${document.module.number}` : "Module"}</div>
        <div className="module-title-row">
          <div><span className="eyebrow">Guiding question</span><h1>{document.module.title}</h1><p>{document.module.guiding_question || document.module.summary}</p></div>
          <span className={`runtime-badge ${document.module.runtime.kind}`}><Play size={14} />{document.module.runtime.kind === "python" ? "Live Python" : "Static lesson"}</span>
        </div>
        <div className="tag-row">{document.module.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
      </header>
      {error ? <div className="runtime-error"><AlertTriangle size={17} /><span>{error}</span></div> : null}
      <div className="module-layout">
        {document.module.controls.length ? (
          <aside className="desktop-controls">
            <Controls controls={document.module.controls} parameters={parameters} busy={busy} onChange={(id, value) => setParameters((current) => ({ ...current, [id]: value }))} onReset={reset} />
          </aside>
        ) : null}
        <article className="lesson-column">
          <BlockRenderer
            document={document}
            result={result}
            parameters={parameters}
            busy={busy}
            onParameter={(id, value) => setParameters((current) => ({ ...current, [id]: value }))}
            onReset={reset}
          />
          <section className="module-complete-card">
            <CheckCircle2 size={21} />
            <div><span className="eyebrow">Reflection</span><h2>Explain the cause, not only the plot.</h2><p>Before moving on, state which parameter changed, which observable responded, and which physical quantity did not.</p></div>
            {nextModule ? <button type="button" className="primary-button" onClick={() => navigate({ kind: "module", courseId, moduleId: nextModule.id })}>Next module <ArrowRight size={16} /></button> : null}
          </section>
        </article>
      </div>
    </div>
  );
}

export default function App() {
  const route = useRoute();
  const [catalog, setCatalog] = useState<CourseSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const reload = () => {
    const controller = new AbortController();
    setLoading(true); setError(null);
    api.catalog(controller.signal).then(setCatalog).catch((reason: unknown) => setError(reason instanceof Error ? reason.message : "Catalog load failed")).finally(() => setLoading(false));
    return controller;
  };
  useEffect(() => { const controller = reload(); return () => controller.abort(); }, []);
  const content = useMemo(() => {
    if (loading) return <section className="state-panel"><LoaderCircle className="spin" /><div><h1>Loading course catalog</h1><p>Discovering mounted learning content.</p></div></section>;
    if (error) return <ErrorPanel message={error} onRetry={() => reload()} />;
    if (route.kind === "home") return <HomePage catalog={catalog} />;
    const course = catalog.find((item) => item.id === route.courseId);
    if (!course) return <ErrorPanel message={`Course ${route.courseId} was not found.`} />;
    if (route.kind === "course") return <CoursePage course={course} />;
    return <ModulePage courseId={route.courseId} moduleId={route.moduleId} />;
  }, [catalog, error, loading, route]);
  return <AppShell catalog={catalog} route={route}>{content}</AppShell>;
}
