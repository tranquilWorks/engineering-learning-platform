from pathlib import Path

from elp_api.catalog import CourseCatalog


def test_demo_course_is_discovered() -> None:
    root = Path(__file__).resolve().parents[3]
    catalog = CourseCatalog([root / "courses"])
    courses = catalog.summaries()
    assert {"platform-showcase", "demo-radar"} <= {course.id for course in courses}
    radar = next(course for course in courses if course.id == "demo-radar")
    assert radar.modules[0].id == "30-measure-range-from-echo-delay"
    assert radar.modules[0].interactive is True
    assert len(radar.revision.content_digest) == 64
    assert len(radar.modules[0].revision.content_digest) == 64


def test_document_resolves_markdown() -> None:
    root = Path(__file__).resolve().parents[3]
    catalog = CourseCatalog([root / "courses"])
    document = catalog.document("demo-radar", "30-measure-range-from-echo-delay")
    assert "lesson.md" in document.markdown_sources
    assert "round-trip" in document.markdown_sources["lesson.md"].lower()
    assert document.module_revision == document.course.modules[0].revision
    assert document.platform_revision.runtime_kind == "python-in-process"
