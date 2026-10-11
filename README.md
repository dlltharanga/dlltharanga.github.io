# dlltharanga.github.io

My career data lives in **`resume.json`**, the single source of truth for my CV, LinkedIn profile and this website.

## How it works
1. Edit `resume.json`.
2. Push to `main`.
3. GitHub Actions runs `build.py`, which generates:
   - `index.html` (deployed to https://dlltharanga.github.io)
   - `linkedin.md` (ready-to-paste LinkedIn text, in the build artifact)

## Structure
| Path | Purpose |
|---|---|
| `resume.json` | Career data ([JSON Resume](https://jsonresume.org) format, with `x-` extensions) |
| `build.py` | Generates the site and LinkedIn copy (no dependencies) |
| `site/` | Styles, script and preview image |
| `.github/workflows/build.yml` | Build and deploy to GitHub Pages |

Run locally: `python build.py`, then open `dist/index.html`.
