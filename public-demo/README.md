# Static public showcase

The showcase is a read-only Vue build with synthetic sample data. It uses the same lessons and precomputed examples produced by the Community Lab engine. A static server serves its HTML, assets and one snapshot file. Opening a sample uses browser memory. Learners may store course progress and theme preferences in their browser.

After installing the locked development dependencies with `uv sync --locked` and `npm --prefix frontend ci`, run the build below.

```bash
make showcase
python3 -m http.server 4173 --bind 127.0.0.1 --directory public-demo
```

Open <http://127.0.0.1:4173/dist/>. Publish the contents of `public-demo/dist` to a static host or GitHub Pages. The relative asset paths and hash navigation support a project subdirectory. A local HTTP server is required to load the snapshot. Hosting is optional.
