# Static public showcase

The showcase serves a static Vue build with synthetic samples, precomputed detection results, timelines, and browser-local reports. Pages hosts HTML, CSS, JavaScript, media, and JSON. Case notes and learning progress use browser storage.

```bash
uv sync --locked
npm --prefix frontend ci
make showcase
python3 -m http.server 4173 --bind 127.0.0.1 --directory public-demo
```

Open <http://127.0.0.1:4173/dist/>. Relative asset paths and hash navigation support a project subdirectory. The CI browser job also attaches a `read-only-showcase` archive after it passes the subpath smoke tests.

## Enable GitHub Pages

1. Review and merge the candidate to `main` through its pull requests. Review [.github/workflows/pages.yml](../.github/workflows/pages.yml) before first deployment.
2. As a repository admin, open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**.
3. In **Actions**, open **Publish read-only showcase to GitHub Pages**, click **Run workflow**, and select `main`. The workflow also runs on changes to the static build inputs on `main`.
4. Wait for the build and deploy jobs, then open the URL recorded in the `github-pages` environment. Check the Technique Map, the MFA example, and the browser network panel. Expected traffic consists of static reads from the showcase origin.

Pages deployment requires the repository Pages configuration and the reviewed workflow on the default branch. Current status is tracked in the [validation report](../reports/validation-summary.md).
