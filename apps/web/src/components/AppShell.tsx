import { Activity, BookOpen, ChevronRight, FlaskConical, Home, Menu, X } from "lucide-react";
import { useEffect, useRef, useState, type ReactNode } from "react";
import type { CourseSummary } from "../types";
import { hrefFor, navigate, type Route } from "../lib/routing";

interface Props {
  catalog: CourseSummary[];
  route: Route;
  children: ReactNode;
}

export function AppShell({ catalog, route, children }: Props) {
  const [open, setOpen] = useState(false);
  const [mobile, setMobile] = useState(() => window.matchMedia("(max-width: 900px)").matches);
  const opener = useRef<HTMLButtonElement>(null);
  const sidebar = useRef<HTMLElement>(null);
  const routeKey = hrefFor(route);
  const previousRoute = useRef(routeKey);
  const close = () => { setOpen(false); requestAnimationFrame(() => opener.current?.focus()); };
  useEffect(() => {
    const query = window.matchMedia("(max-width: 900px)");
    const change = () => { setMobile(query.matches); setOpen(false); };
    query.addEventListener("change", change);
    return () => query.removeEventListener("change", change);
  }, []);
  useEffect(() => {
    if (open && mobile) sidebar.current?.querySelector<HTMLButtonElement>("button")?.focus();
  }, [open, mobile]);
  useEffect(() => {
    if (previousRoute.current !== routeKey) {
      previousRoute.current = routeKey;
      requestAnimationFrame(() => {
        document.getElementById("lesson-main")?.focus();
        window.scrollTo(0, 0);
      });
    }
  }, [routeKey]);
  const activeCourse = route.kind === "home" ? null : catalog.find((item) => item.id === route.courseId);
  return (
    <div className="app-shell">
      <a className="skip-link" href="#lesson-main">Skip to lesson</a>
      <aside ref={sidebar} id="course-navigation" aria-label="Course sidebar" inert={mobile && !open} className={`sidebar ${open ? "sidebar-open" : ""}`} onKeyDown={(event) => {
        if (!mobile || !open) return;
        if (event.key === "Escape") { event.preventDefault(); close(); }
        if (event.key === "Tab") {
          const buttons = sidebar.current?.querySelectorAll<HTMLButtonElement>("button");
          const first = buttons?.[0], last = buttons?.[buttons.length - 1];
          if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
          if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
        }
      }}>
        <div className="brand">
          <span className="brand-mark"><Activity size={20} /></span>
          <div><strong>Engineering Lab</strong><span>Interactive learning</span></div>
          <button className="sidebar-close" type="button" onClick={close} aria-label="Close navigation"><X /></button>
        </div>
        <nav aria-label="Course navigation">
          <button className={`nav-home ${route.kind === "home" ? "active" : ""}`} type="button" onClick={() => { navigate({ kind: "home" }); setOpen(false); }}>
            <Home size={17} /> Course library
          </button>
          <div className="nav-label">Courses</div>
          {catalog.map((course) => (
            <div key={course.id} className="course-nav-group">
              <button
                type="button"
                className={`course-nav ${activeCourse?.id === course.id ? "active" : ""}`}
                onClick={() => { navigate({ kind: "course", courseId: course.id }); setOpen(false); }}
              >
                <BookOpen size={16} /><span>{course.title}</span><ChevronRight size={14} />
              </button>
              {activeCourse?.id === course.id ? (
                <div className="module-nav-list">
                  {course.modules.map((module) => (
                    <button
                      key={module.id}
                      className={route.kind === "module" && route.moduleId === module.id ? "active" : ""}
                      aria-current={route.kind === "module" && route.moduleId === module.id ? "page" : undefined}
                      type="button"
                      onClick={() => { navigate({ kind: "module", courseId: course.id, moduleId: module.id }); setOpen(false); }}
                    >
                      <span>{module.number ? String(module.number).padStart(2, "0") : "·"}</span>{module.title}
                    </button>
                  ))}
                </div>
              ) : null}
            </div>
          ))}
        </nav>
        <div className="sidebar-footer"><FlaskConical size={15} /> trusted numerical runtime</div>
      </aside>
      <div className="main-column" inert={mobile && open}>
        <header className="mobile-header">
          <button ref={opener} type="button" onClick={() => setOpen(true)} aria-label="Open navigation" aria-expanded={open} aria-controls="course-navigation"><Menu /></button>
          <span>Engineering Learning Platform</span>
        </header>
        <main id="lesson-main" tabIndex={-1}>{children}</main>
      </div>
      {open && mobile ? <button className="sidebar-scrim" type="button" tabIndex={-1} onClick={close} aria-label="Close navigation overlay" /> : null}
    </div>
  );
}
