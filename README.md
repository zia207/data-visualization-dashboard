# LBC Dashboard

This repo contains:

- `lbc_dashboard/`: Streamlit ML dashboard (run locally with Python)
- `lbc_dashboard.html`: standalone HTML dashboard demo
- `web/`: a small static landing page

## Static website (GitHub Pages)

The published site comes from **`web/`** via **GitHub Actions** (workflow `Deploy GitHub Pages`). The workflow also copies `lbc_dashboard.html` next to the landing page so the “Static demo” link works.

**If you see a GitHub Pages 404**, it almost always means the repo is not deploying yet (or Deploy failed):

1. In the GitHub repo, go to **Settings → Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Open the **Actions** tab and confirm the latest **Deploy GitHub Pages** workflow is **green**
4. Re-run workflow if needed: **Actions → Deploy GitHub Pages → Run workflow**

After the first successful run, try:

- `https://zia207.github.io/data-visualization-dashboard/`
- Static demo (same Pages deployment): `https://zia207.github.io/data-visualization-dashboard/lbc_dashboard.html`

## Run the Streamlit app locally

```bash
cd lbc_dashboard
pip install -r requirements.txt
streamlit run app.py
```

