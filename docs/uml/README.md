# UML Diagrams

This folder contains sequence and class diagrams (Mermaid) used to document the main API flows.

Files:
- Source (.md / .mmd): `docs/uml/*.md` and `docs/uml/*.mmd` contain Mermaid code blocks.
- Pre-generated images: `docs/uml/*.svg` and `docs/uml/*.png` (committed for convenience).
- HTML previews: `docs/uml/*.html` — open in browser to view and export.

How to regenerate images locally:

1) Install Node.js and mermaid-cli

```bash
# install mermaid-cli (global) or use npx
npm i -g @mermaid-js/mermaid-cli
# render a file
mmdc -i sequence_get_api_logs.mmd -o sequence_get_api_logs.svg
```

2) If you prefer no-install option, open the corresponding `.html` preview (e.g. `sequence_get_api_logs.html`) and use the browser's DevTools to copy/save the SVG or export PNG.

Notes:
- I added `sequence_get_api_logs.md/.mmd` and `class_api_log.md` and generated corresponding `.svg`/`.png` files and `.html` previews.
- If you want, I can add a small automation script (Makefile or npm script) to regenerate all diagrams.
