# Lesson schema

These schemas define the portable course-folder contract consumed by the platform.

- `course.schema.json`: catalog identity and module location.
- `module.schema.json`: runtime, controls, and ordered lesson blocks.

The Pydantic models under `apps/api/src/elp_api/models.py` are the executable source during the foundation phase. Milestone M2 adds generated schema consistency tests so the JSON Schema and Python models cannot drift.
