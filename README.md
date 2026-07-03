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

1. Push this repo to GitHub — live at [github.com/codeaholicguy/vuhongdoan.com](https://github.com/codeaholicguy/vuhongdoan.com)
2. GitHub Actions deploy is enabled (Settings → Pages → **GitHub Actions**)
3. **Update DNS** for `vuhongdoan.com` (currently still pointing at Adobe Portfolio):
   - Remove existing `A` / `CNAME` records for the domain
   - Add GitHub Pages `A` records:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - Or add `CNAME` → `codeaholicguy.github.io`
   - Optional: `www` → `codeaholicguy.github.io`
4. In GitHub repo **Settings → Pages**, confirm custom domain `vuhongdoan.com` shows as verified (HTTPS may take up to 24h)

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
