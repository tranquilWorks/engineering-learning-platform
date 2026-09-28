import reviews from '../lesson-quality.json';
export function LessonQuality({ course, module }: { course: string; module: string }) {
  const review = reviews.find(row => row.course === course && row.module === module);
  if (!review) return null;
  return <section className="lesson-quality" aria-label="Lesson review">
    {review.known_issue ? <p role="note" className="lesson-content-note"><strong>Under revision:</strong> {review.known_issue}</p> : null}
    <details><summary>Lesson review and evidence</summary>
      {review.scoped_review ? <p><strong>Scoped model revision:</strong> {review.scoped_review} Five independent numerical scenarios and physical limiting checks passed. This does not certify the whole course or learner outcomes.</p> : null}
      <p>This lesson has {review.evidence_count} retained design or numerical evidence artifacts. Their presence does not establish complete subject coverage or learning effectiveness.</p>
      <p>The current audit checks delivery and records specific content issues. Representative learner and screen-reader validation have not been run.</p>
    </details>
  </section>;
}
