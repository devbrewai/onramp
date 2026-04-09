# 7. Per-module mypy override for PyMuPDF stubs

Date: 2026-04-09

## Status

Accepted

## Context

PyMuPDF ships `py.typed` but has incomplete type annotations — `open()`, `close()`, and `Pixmap.tobytes()` are untyped. Under `mypy --strict`, calling these raises `no-untyped-call` errors. No `types-PyMuPDF` stub package exists on PyPI. The maintainers have deprioritized completing annotations (GitHub issue #2883).

Three options:
1. **Inline `# type: ignore[no-untyped-call]`** on each call — noisy across 3+ call sites
2. **Custom local `.pyi` stubs** — full type safety but maintenance burden on library updates
3. **Per-module mypy override** — scoped relaxation, zero code noise

## Decision

Add a `[[tool.mypy.overrides]]` section in `pyproject.toml` that disables `disallow_untyped_calls` only for `app.services.converter` — the single module that interfaces with PyMuPDF.

```toml
[[tool.mypy.overrides]]
module = "app.services.converter"
disallow_untyped_calls = false
```

## Consequences

- `mypy --strict` stays enabled globally — all our code is fully typed
- Only the converter module's calls to PyMuPDF are relaxed, not the entire codebase
- The override is documented with a comment explaining the upstream gap
- If PyMuPDF completes their annotations, we can delete the override block
- Any future untyped calls accidentally added to `converter.py` won't be caught — acceptable trade-off since it's a small, stable module
