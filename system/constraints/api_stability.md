# API stability

- Do **not** remove or rename public HTTP paths under `/v1/` without a versioned replacement and migration notes.
- Do **not** change JSON field names or semantics of externally documented payloads (`README.md`, OpenAPI at `/docs`) without updating clients and tests in the same change.
- Prefer **additive** changes (new optional fields, new endpoints) over breaking edits.
- Desktop and packaged builds may depend on environment variables documented in `backend/app/core/settings.py` — treat renames as API changes.
