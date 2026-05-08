# LBC Dashboard

This repo contains:

- `lbc_dashboard/`: Streamlit ML dashboard (run locally with Python)
- `lbc_dashboard.html`: standalone HTML dashboard demo
- `web/`: a small static landing page

## Static website (GitHub Pages)

The website is deployed from the `web/` folder via GitHub Actions. The deploy workflow also copies `lbc_dashboard.html` into the published site so the “Static demo” link works.

After the first successful run, your site URL will be:

- `https://zia207.github.io/data-visualization-dashboard/`

## Run the Streamlit app locally

```bash
cd lbc_dashboard
pip install -r requirements.txt
streamlit run app.py
```

