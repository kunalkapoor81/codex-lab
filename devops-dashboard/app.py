import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="DevOps Command Center",
    page_icon="🚀",
    layout="wide",
)


@st.cache_data
def generate_sample_data(hours: int = 48) -> pd.DataFrame:
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    timestamps = [now - timedelta(hours=i) for i in range(hours)][::-1]

    rows = []
    for ts in timestamps:
        success_rate = max(92, min(100, random.gauss(97.8, 1.1)))
        deploys = max(0, int(random.gauss(2.4, 1.5)))
        mttr = max(5, random.gauss(28, 10))
        change_failure = max(0.2, min(8.0, random.gauss(2.5, 1.2)))
        cpu = max(25, min(95, random.gauss(63, 14)))
        latency = max(80, random.gauss(210, 55))

        rows.append(
            {
                "timestamp": ts,
                "service": random.choice(["payments", "orders", "auth", "inventory"]),
                "environment": random.choice(["prod", "stage"]),
                "deployment_success_rate": round(success_rate, 2),
                "deployments": deploys,
                "mttr_minutes": round(mttr, 1),
                "change_failure_rate": round(change_failure, 2),
                "cpu_percent": round(cpu, 1),
                "latency_ms": round(latency, 1),
            }
        )

    return pd.DataFrame(rows)


st.markdown(
    """
    <style>
    :root {
        --bg-start: #0b1220;
        --bg-mid: #111827;
        --bg-end: #172554;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --card-bg: rgba(15, 23, 42, 0.78);
        --card-border: rgba(148, 163, 184, 0.35);
    }
    .stApp {
        background: linear-gradient(125deg, var(--bg-start) 0%, var(--bg-mid) 45%, var(--bg-end) 100%);
        color: var(--text-primary);
    }
    .block-container {
        padding-top: 1.1rem;
        max-width: 1400px;
    }
    p, li, .stCaption, label, .st-emotion-cache-10trblm, .st-emotion-cache-16idsys {
        color: var(--text-secondary) !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.96));
        border-right: 1px solid rgba(148, 163, 184, 0.25);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    div[data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 12px;
        box-shadow: 0 10px 24px rgba(2, 6, 23, 0.35);
        backdrop-filter: blur(10px);
    }
    h1, h2, h3 {
        color: var(--text-primary) !important;
        letter-spacing: 0.2px;
    }
    .stAlert {
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚀 MVP DevOps Dashboard")
st.caption("Modern, self-service command center for release health, reliability, and ops visibility.")

with st.sidebar:
    st.header("⚙️ Self-Service Controls")
    uploaded = st.file_uploader("Upload CSV (optional)", type=["csv"])
    lookback = st.slider("Lookback window (hours)", min_value=12, max_value=168, value=48, step=12)
    environment = st.multiselect("Environment", ["prod", "stage"], default=["prod", "stage"])
    services = st.multiselect(
        "Services",
        ["payments", "orders", "auth", "inventory"],
        default=["payments", "orders", "auth", "inventory"],
    )

if uploaded:
    df = pd.read_csv(uploaded)
    required_cols = {
        "timestamp",
        "service",
        "environment",
        "deployment_success_rate",
        "deployments",
        "mttr_minutes",
        "change_failure_rate",
        "cpu_percent",
        "latency_ms",
    }
    missing = required_cols - set(df.columns)
    if missing:
        st.error(f"CSV is missing required columns: {sorted(missing)}")
        st.stop()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
else:
    df = generate_sample_data(lookback)

filtered = df[df["environment"].isin(environment) & df["service"].isin(services)].copy()

if filtered.empty:
    st.warning("No data for the selected filters. Adjust sidebar controls.")
    st.stop()

latest = filtered.sort_values("timestamp").tail(1)

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
kpi_1.metric("Deploy Success", f"{latest['deployment_success_rate'].iloc[0]:.1f}%")
kpi_2.metric("Hourly Deployments", int(latest["deployments"].iloc[0]))
kpi_3.metric("MTTR", f"{latest['mttr_minutes'].iloc[0]:.1f} min")
kpi_4.metric("Change Failure", f"{latest['change_failure_rate'].iloc[0]:.1f}%")

left, right = st.columns([1.6, 1])

with left:
    trend = (
        filtered.groupby("timestamp", as_index=False)[
            ["deployment_success_rate", "latency_ms", "cpu_percent"]
        ]
        .mean()
        .sort_values("timestamp")
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=trend["timestamp"],
            y=trend["deployment_success_rate"],
            mode="lines+markers",
            name="Success %",
            line=dict(color="#22c55e", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=trend["timestamp"],
            y=trend["latency_ms"] / 3,
            mode="lines",
            name="Latency (scaled)",
            line=dict(color="#38bdf8", width=2, dash="dot"),
        )
    )
    fig.update_layout(
        title="Release Health & Performance Trend",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.72)",
        font=dict(color="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    failure_by_service = (
        filtered.groupby("service", as_index=False)["change_failure_rate"].mean().sort_values(
            "change_failure_rate", ascending=False
        )
    )
    bar = px.bar(
        failure_by_service,
        x="service",
        y="change_failure_rate",
        color="change_failure_rate",
        color_continuous_scale=["#22d3ee", "#3b82f6", "#6366f1", "#a855f7"],
        title="Change Failure by Service",
    )
    bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.72)",
        font=dict(color="#e2e8f0"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(bar, use_container_width=True)

st.subheader("📋 Live Ops Feed")
feed = filtered.sort_values("timestamp", ascending=False).head(12)
st.dataframe(
    feed[[
        "timestamp",
        "service",
        "environment",
        "deployment_success_rate",
        "deployments",
        "mttr_minutes",
        "change_failure_rate",
        "cpu_percent",
        "latency_ms",
    ]],
    use_container_width=True,
    hide_index=True,
)

st.info(
    "Tip: Upload your pipeline/export CSV with the same columns to instantly customize this dashboard for your client demo."
)
