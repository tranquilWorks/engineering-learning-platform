import type { CourseSummary, ModuleDocument, RunResult } from "../types";

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      Accept: "application/json",
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
      ...init?.headers,
    },
  });
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) message = payload.detail;
    } catch {
      // Preserve the HTTP status when the response is not JSON.
    }
    throw new ApiError(message, response.status);
  }
  return (await response.json()) as T;
}

export const api = {
  catalog: (signal?: AbortSignal) => request<CourseSummary[]>("/api/v1/catalog", { signal }),
  module: (courseId: string, moduleId: string, signal?: AbortSignal) =>
    request<ModuleDocument>(
      `/api/v1/courses/${encodeURIComponent(courseId)}/modules/${encodeURIComponent(moduleId)}`,
      { signal },
    ),
  run: (
    courseId: string,
    moduleId: string,
    parameters: Record<string, unknown>,
    expectedContentDigest: string,
    signal?: AbortSignal,
  ) =>
    request<RunResult>(
      `/api/v1/courses/${encodeURIComponent(courseId)}/modules/${encodeURIComponent(moduleId)}/run`,
      {
        method: "POST",
        body: JSON.stringify({
          parameters,
          expected_content_digest: expectedContentDigest,
        }),
        signal,
      },
    ),
};
