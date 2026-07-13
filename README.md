# elia-apps.github.io

The landing site for **Elia** — a small family of calm, private, offline-first
apps for pregnancy, birth, and the early days with your baby.

Live at **https://elia-apps.github.io**

## Structure

```
.
├── index.html              # Landing page (hero, apps, philosophy, story)
├── 404.html                # Friendly not-found page
├── apps/
│   ├── contractions/       # Elia Contractions — a calm companion for birth
│   │   └── index.html
│   └── feeding/            # Elia Feeding — a calm feeding log for the first days
│       └── index.html
├── assets/
│   ├── css/styles.css      # Shared design system (light + dark)
│   └── img/favicon.svg     # Brand mark
└── .nojekyll               # Serve files as-is (no Jekyll processing)
```

## Design

Plain HTML/CSS/JS — no build step. Colors, tone, and copy follow the Elia brand
and design docs. The palette and dark mode live as CSS custom properties in
`assets/css/styles.css`; each app page can override the accent (Contractions =
rose, Feeding = honey).

## Adding a new app

1. Copy `apps/feeding/index.html` to `apps/<slug>/index.html` and edit the copy.
2. Add a matching `.app-card` to the `#apps` grid in `index.html`.
3. Pick an accent via the per-page `<style>` override (or reuse rose).

## Local preview

Any static server works, e.g.:

```
python3 -m http.server 8000
```

Then open http://localhost:8000
