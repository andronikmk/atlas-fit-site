# atlas-fit.fit

The public site for Atlas Fit: home, support and privacy pages, served by GitHub Pages.

- `build.py` writes `index.html`, `support/index.html`, `privacy/index.html` and `404.html`.
- The privacy page is generated from the app's `docs/privacy-policy.md`, so re-run the build and push whenever that file changes:

      python3 build.py "/path/to/WorkoutLogApp/docs/privacy-policy.md"

- `CNAME` holds the custom domain. `.nojekyll` tells GitHub Pages to serve the files as they are.
