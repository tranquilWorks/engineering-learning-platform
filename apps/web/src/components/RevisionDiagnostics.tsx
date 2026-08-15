import type { ContentRevision, PlatformRevision } from "../types";

interface Props {
  label: string;
  content: ContentRevision;
  platform?: PlatformRevision;
}

export function RevisionDiagnostics({ label, content, platform }: Props) {
  return (
    <aside className="revision-diagnostics" aria-label={`${label} revision diagnostics`}>
      <div className="revision-summary">
        <span>Contract v{content.schema_version}</span>
        <span>Content <code>{content.content_digest}</code></span>
      </div>
      <details>
        <summary>Exact revision details</summary>
        <dl>
          <dt>Content SHA-256</dt>
          <dd><code>{content.content_digest}</code></dd>
          <dt>Source Git commit</dt>
          <dd><code>{content.source_git_commit ?? "Unavailable (non-Git source)"}</code></dd>
          {platform ? (
            <>
              <dt>Platform version</dt>
              <dd><code>{platform.platform_version}</code></dd>
              <dt>Platform Git commit</dt>
              <dd><code>{platform.platform_git_commit ?? "Unavailable (non-Git runtime)"}</code></dd>
              <dt>Runtime content SHA-256</dt>
              <dd><code>{platform.runtime_content_digest}</code></dd>
              <dt>Runtime kind</dt>
              <dd><code>{platform.runtime_kind}</code></dd>
            </>
          ) : null}
        </dl>
      </details>
    </aside>
  );
}
