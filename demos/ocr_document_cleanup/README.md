# OCR Document Cleanup Demo

This demo is a public-safe simulation of a PDF/image-notes OCR cleanup workflow.
It mirrors the reusable shape of a private workflow:

```text
source pages
-> OCR text
-> conservative cleanup
-> manifest
-> corpus segments
```

Run from the repository root:

```bash
python3 demos/ocr_document_cleanup/run_demo.py
```

Generated outputs:

- `sample_outputs/ocr_document_cleanup/manifest.json`
- `sample_outputs/ocr_document_cleanup/cleaned_notes.md`
- `sample_outputs/ocr_document_cleanup/corpus.json`
- `sample_outputs/ocr_document_cleanup/workflow_summary.md`

The demo does not call Mathpix, OpenAI, `pdftoppm`, or any network service.
