# LBC Dashboard

This repo contains:

- `LBC_Dashboard/lbc_dashboard/` (or `lbc_dashboard/`): Streamlit ML dashboard (run locally with Python)
- `SQL_Engine_Benchmark_Dashboard/`: Streamlit SQL engine benchmark dashboard + `SQL_Engine_Benchmark_Dashboard/web/` landing page
- `lbc_dashboard.html`: standalone LBC HTML demo
- `sql_engine_benchmark.html`: standalone SQL benchmark HTML demo (sample chart)
- `web/`: main static landing page (GitHub Pages)

## Static website (GitHub Pages)

The published site comes from **`web/`** via **GitHub Actions** (workflow `Deploy GitHub Pages`). The workflow also copies **`lbc_dashboard.html`**, **`sql_engine_benchmark.html`**, and the **`SQL_Engine_Benchmark_Dashboard/web`** tree into `_site/` so the static demos and SQL landing URLs work.

**If you see a GitHub Pages 404**, it almost always means the repo is not deploying yet (or Deploy failed):

1. In the GitHub repo, go to **Settings → Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Open the **Actions** tab and confirm the latest **Deploy GitHub Pages** workflow is **green**
4. Re-run workflow if needed: **Actions → Deploy GitHub Pages → Run workflow**

After the first successful run, try:

- `https://zia207.github.io/data-visualization-dashboard/`
- LBC static demo: `https://zia207.github.io/data-visualization-dashboard/lbc_dashboard.html`
- SQL engine landing (docs + links): `https://zia207.github.io/data-visualization-dashboard/sql_engine_benchmark/`
- SQL static chart demo: `https://zia207.github.io/data-visualization-dashboard/sql_engine_benchmark.html`

## Run the Streamlit apps locally

**LBC**

```bash
cd LBC_Dashboard/lbc_dashboard
pip install -r requirements.txt
streamlit run app.py
```

**SQL Engine Benchmark**

```bash
cd SQL_Engine_Benchmark_Dashboard
pip install -r requirements.txt
streamlit run app.py
```

