# MVP DevOps Dashboard

A visually appealing, client-demo-ready DevOps dashboard built with Streamlit + Plotly.

## What this MVP includes

- Modern dark gradient UI
- High-level DevOps KPIs (deployment success, MTTR, change failure, deploy volume)
- Trend visualization for release health and performance
- Service-wise failure analysis chart
- Live ops feed table
- **Self-service controls** in sidebar for:
  - environment filtering
  - service filtering
  - lookback window
  - CSV upload (to replace demo data instantly)

## 1) Local setup

From repository root:

```bash
cd devops-dashboard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Run the dashboard

```bash
streamlit run app.py
```

Streamlit prints a local URL, typically:

- http://localhost:8501

Open that URL in your browser to visualize the look and feel.

## 3) Test/check commands

Basic lint/checks:

```bash
python -m py_compile app.py
python -m pip show streamlit plotly pandas
```

## 4) Use your own data (self-service)

Upload a CSV from the sidebar with these required columns:

- `timestamp`
- `service`
- `environment`
- `deployment_success_rate`
- `deployments`
- `mttr_minutes`
- `change_failure_rate`
- `cpu_percent`
- `latency_ms`

`timestamp` should be parseable by pandas (e.g. `2026-03-26 10:15:00`).

## 5) Demo talking points for your client bid

- "You get an **at-a-glance executive view** and **drill-down by service**."
- "Teams can **self-serve filters and data uploads** without engineering help."
- "This MVP is ready to evolve into role-based, multi-tenant, and real-time integrations (GitHub Actions/Jenkins/Datadog/Prometheus)."
