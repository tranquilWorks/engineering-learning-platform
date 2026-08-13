import { Activity, BookOpen, ChevronRight, FlaskConical, Home, Menu, X } from "lucide-react";
import { useState, type ReactNode } from "react";
import type { CourseSummary } from "../types";
import { navigate, type Route } from "../lib/routing";

interface Props {
  catalog: CourseSummary[];
  route: Route;
  children: ReactNode;
}

export function AppShell({ catalog, route, children }: Props) {
  const [open, setOpen] = useState(false);
  const activeCourse = route.kind === "home" ? null : catalog.find((item) => item.id === route.courseId);
  return (
    <div className="app-shell">
      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
        <div className="brand" role="banner">
          <span className="brand-mark"><Activity size={20} /></span>
          <div><strong>Engineering Lab</strong><span>Interactive learning</span></div>
          <button className="sidebar-close" type="button" onClick={() => setOpen(false)} aria-label="Close navigation"><X /></button>
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
      <div className="main-column">
        <header className="mobile-header">
          <button type="button" onClick={() => setOpen(true)} aria-label="Open navigation"><Menu /></button>
          <span>Engineering Learning Platform</span>
        </header>
        <main>{children}</main>
      </div>
      {open ? <button className="sidebar-scrim" type="button" onClick={() => setOpen(false)} aria-label="Close navigation overlay" /> : null}
    </div>
  );
}
