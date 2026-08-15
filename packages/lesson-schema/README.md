# Lesson schema

These generated artifacts define the current strict contract consumed by the platform.

- `course.schema.json`: catalog identity and module location.
- `module.schema.json`: runtime, controls, widgets, and ordered lesson blocks.
- `api.schema.json`: serialized catalog, module-document, request, and result shapes.
- `apps/web/src/types.ts`: serialized TypeScript API types generated in the same pass.

The Pydantic models under `apps/api/src/elp_api/models.py` are the executable source of truth. Regenerate or verify with:

```bash
PYTHONPATH=apps/api/src python3 scripts/export_schemas.py
PYTHONPATH=apps/api/src python3 scripts/export_schemas.py --check
```

CI rejects schema drift.

These files are derivatives of the executable Python models. They carry no independent compatibility promise, and version 1 is the only accepted course/module manifest version.
