# atlas-fit.fit

The public site for Atlas Fit: home, support, privacy and about pages, served by GitHub Pages.

- `build.py` writes `index.html`, `support/index.html`, `privacy/index.html`, `about/index.html` and `404.html`.
- `COMPANY` in `build.py` is the publisher's exact legal name (as on Sunbiz). It appears on the About page and in every footer; the build refuses to run without it. Apple checks it against the D-U-N-S record during organization enrollment.
- The privacy page is generated from the app's `docs/privacy-policy.md`, so re-run the build and push whenever that file changes:

      python3 build.py "/path/to/WorkoutLogApp/docs/privacy-policy.md"

- `CNAME` holds the custom domain. `.nojekyll` tells GitHub Pages to serve the files as they are.
