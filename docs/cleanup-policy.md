# Conservative Cleanup Policy

Content intelligence workflows often need a cleanup pass after OCR or
transcription. The cleanup step should improve readability while preserving the
source's meaning, structure, and uncertainty.

## Rules

- Correct obvious OCR or transcription errors.
- Preserve the original order of ideas.
- Keep uncertainty markers such as `[unclear]`.
- Do not add facts, examples, equations, citations, or claims.
- Do not remove source identifiers needed for auditability.
- Keep generated artifacts tied to a manifest record.

## Public Demo Pattern

The public demos simulate cleanup with deterministic replacements. A private
workflow can replace that deterministic step with a reviewed model-assisted
cleanup pass, but the public boundary is the same: publish only synthetic,
licensed, or reviewed derivative text.
