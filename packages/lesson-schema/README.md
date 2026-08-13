# Lesson schema

These generated JSON Schemas define the portable course-folder contract consumed by the platform.

- `course.schema.json`: catalog identity and module location.
- `module.schema.json`: runtime, controls, widgets, and ordered lesson blocks.

The Pydantic models under `apps/api/src/elp_api/models.py` are the executable source of truth. Regenerate or verify with:

```bash
PYTHONPATH=apps/api/src python3 scripts/export_schemas.py
PYTHONPATH=apps/api/src python3 scripts/export_schemas.py --check
```

CI rejects schema drift.
