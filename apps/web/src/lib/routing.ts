export type Route =
  | { kind: "home" }
  | { kind: "course"; courseId: string }
  | { kind: "module"; courseId: string; moduleId: string };

export function parseRoute(pathname = window.location.pathname): Route {
  const parts = pathname.split("/").filter(Boolean).map(decodeURIComponent);
  if (parts[0] === "courses" && parts[1] && parts[2] === "modules" && parts[3]) {
    return { kind: "module", courseId: parts[1], moduleId: parts[3] };
  }
  if (parts[0] === "courses" && parts[1]) return { kind: "course", courseId: parts[1] };
  return { kind: "home" };
}

export function hrefFor(route: Route): string {
  if (route.kind === "home") return "/";
  if (route.kind === "course") return `/courses/${encodeURIComponent(route.courseId)}`;
  return `/courses/${encodeURIComponent(route.courseId)}/modules/${encodeURIComponent(route.moduleId)}`;
}

export function navigate(route: Route): void {
  const href = hrefFor(route);
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}
