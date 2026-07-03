# vuhongdoan.com

Static portfolio site for [Vu-Hong Doan](https://vuhongdoan.com), migrated off Adobe Portfolio and hosted on **GitHub Pages**.

## Features

- Password-protected portfolio (client-side gate, same UX as Adobe Portfolio)
- All images served locally (no `cdn.myportfolio.com` dependency)
- GitHub Actions deploy on push to `main`

## Local development

```bash
npm run serve
```

Open http://localhost:8080 — you'll be redirected to the password gate.

## Password

The gate compares a SHA-256 hash stored in `public/js/config.js`.

Generate a hash for your password:

```bash
npm run hash-password -- 'your-password-here'
```

Paste the output into `public/js/config.js` → `passwordHash`, then rebuild.

> **Note:** Client-side password protection keeps casual visitors out but is not cryptographically secure against someone reading the source. This matches how Adobe Portfolio password pages work.

## Build manually

```bash
npm run migrate   # download images → public/images/, extract content/
npm run build     # assemble site/ for deployment
```

Output is written to `site/` (gitignored).

## Deploy to GitHub Pages

1. Push this repo to GitHub (e.g. `github.com/vuhongdoan/vuhongdoan.com`)
2. In **Settings → Pages**, set source to **GitHub Actions**
3. Push to `main` — the workflow builds and deploys automatically
4. Add DNS for `vuhongdoan.com`:
   - `A` records → GitHub Pages IPs (see [GitHub docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site))
   - or `CNAME` → `<user>.github.io`

The build writes a `CNAME` file with `vuhongdoan.com`.

## Project structure

```
legacy/          Original Adobe Portfolio HTML clone
content/         Extracted page bodies (generated)
public/          CSS, JS, images source for build
site/            Built static site (generated, deployed)
scripts/
  migrate.py     Download CDN images, extract content
  build.py       Assemble HTML pages for GitHub Pages
```
