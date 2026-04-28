import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Retail Flex Monetization Cockpit",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Styling
# ----------------------------
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0b1220 0%, #101827 100%);
        color: #E5E7EB;
    }
    .stApp {
        background: linear-gradient(180deg, #0b1220 0%, #101827 100%);
    }
    .hero-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        min-height: 140px;
    }
    .section-card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 10px;
    }
    .takeaway {
        background: linear-gradient(135deg, rgba(239,68,68,0.18), rgba(249,115,22,0.12));
        border: 1px solid rgba(249,115,22,0.28);
        border-radius: 16px;
        padding: 14px 16px;
        margin: 10px 0 14px 0;
    }
    .tiny {
        font-size: 0.88rem;
        color: #C7D2FE;
    }
    .big-number {
        font-size: 1.9rem;
        font-weight: 700;
        color: #F9FAFB;
        margin-bottom: 4px;
    }
    .subtle {
        color: #9CA3AF;
        font-size: 0.92rem;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F9FAFB;
        margin-bottom: 0.35rem;
    }
    .hero-subtitle {
        color: #D1D5DB;
        font-size: 1.0rem;
        margin-bottom: 0.8rem;
    }
    .badge {
        display: inline-block;
        padding: 0.20rem 0.55rem;
        border-radius: 999px;
        background: rgba(59,130,246,0.14);
        border: 1px solid rgba(59,130,246,0.25);
        color: #BFDBFE;
        margin-right: 0.35rem;
        margin-bottom: 0.3rem;
        font-size: 0.82rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Data model
# ----------------------------
fit_score = {"n/a": 0, "Low": 1, "Med": 2, "High": 3, "Very high": 4}

assets = {
    "EV": {
        "icon": "🚗",
        "type": "Large time-shiftable demand",
        "control": "7–22 kW/session, plug-in dependent",
        "response": "Medium",
        "predictability": "Medium",
        "availability": "Mostly overnight",
        "strengths": [
            "Volume flexibility when plugged in",
            "Strong fit for dynamic charging and §14a",
            "Can become much more valuable with V2G",
        ],
        "limits": [
            "Plug-in uncertainty",
            "Without V2G, mainly downward / load-shifting flexibility",
            "Balancing fit weaker than batteries",
        ],
        "tagline": "Volume play",
    },
    "PV": {
        "icon": "☀️",
        "type": "Variable generation / self-consumption surface",
        "control": "Generation-led, limited direct flexibility",
        "response": "Low",
        "predictability": "Medium",
        "availability": "Daytime, weather dependent",
        "strengths": [
            "Creates self-consumption value surface",
            "Enables batteries and flexible loads to create value",
            "Strong customer bill story",
        ],
        "limits": [
            "Not flexible by itself in the same way as storage/load",
            "Curtailment rarely the main monetization route",
            "Value depends on pairing with storage or shiftable load",
        ],
        "tagline": "Enabler",
    },
    "Home battery": {
        "icon": "🔋",
        "type": "Fast bidirectional controllable flexibility",
        "control": "5–15 kWh, 3–10 kW typical",
        "response": "High",
        "predictability": "High",
        "availability": "High",
        "strengths": [
            "Broadest asset-to-market fit",
            "Strong for bill optimization and wholesale timing",
            "Best retail-fit asset for advanced monetization",
        ],
        "limits": [
            "Cycle-limited / warranty constrained",
            "Capex sensitive",
            "Value depends on spreads and utilization",
        ],
        "tagline": "Swiss army knife",
    },
    "Heat pump": {
        "icon": "🌡️",
        "type": "Thermal time-shift via building or hot-water inertia",
        "control": "2–10 kW electrical, comfort-bounded",
        "response": "Medium",
        "predictability": "High",
        "availability": "Seasonal / comfort driven",
        "strengths": [
            "Excellent for §14a and tariff-led shifting",
            "Predictable flexible demand",
            "Good supplier portfolio value",
        ],
        "limits": [
            "Bound by comfort and thermal inertia",
            "Weak fit for very fast markets",
            "Customer acceptance matters",
        ],
        "tagline": "Predictable shifter",
    },
    "EV + PV": {
        "icon": "🚗☀️",
        "type": "Shiftable EV demand plus local generation",
        "control": "Good customer bill optimization asset bundle",
        "response": "Medium",
        "predictability": "Medium",
        "availability": "Overnight EV, daytime PV",
        "strengths": [
            "Good dynamic charging + self-consumption bundle",
            "Strong customer proposition",
            "Can reduce import and improve tariff timing",
        ],
        "limits": [
            "No storage buffer without battery",
            "Still constrained by plug-in timing",
            "Limited fit for advanced ancillary monetization",
        ],
        "tagline": "Smart charging bundle",
    },
    "PV + battery": {
        "icon": "☀️🔋",
        "type": "Self-consumption lift plus storage-based timing optimization",
        "control": "Very good",
        "response": "High",
        "predictability": "High",
        "availability": "High",
        "strengths": [
            "Most bankable household bundle today",
            "Excellent bill optimization fit",
            "Strong DA / supplier-side optimization potential",
        ],
        "limits": [
            "Still spread- and capex-sensitive",
            "Battery can saturate if undersized",
            "Ancillary routes require operational maturity",
        ],
        "tagline": "Highest value density",
    },
    "EV + battery": {
        "icon": "🚗🔋",
        "type": "Shiftable load plus dedicated flexible storage",
        "control": "Strong",
        "response": "High",
        "predictability": "Medium",
        "availability": "High with battery, EV window dependent",
        "strengths": [
            "Good for bill optimization and DA timing",
            "Battery improves bankability vs EV alone",
            "Strong supplier / BRP value",
        ],
        "limits": [
            "Still weaker than PV+battery on self-consumption story",
            "Operationally more complex",
            "V2G still not assumed",
        ],
        "tagline": "Flex-rich bundle",
    },
    "EV + PV + battery": {
        "icon": "🚗☀️🔋",
        "type": "Full-stack household flexibility bundle",
        "control": "Excellent",
        "response": "High",
        "predictability": "High",
        "availability": "High",
        "strengths": [
            "Best total household flexibility proposition",
            "Supports stacked customer, supplier, and system value",
            "Strongest long-term strategic bundle",
        ],
        "limits": [
            "Highest orchestration complexity",
            "Requires good controls and proposition design",
            "Not every value stream is accessible on day one",
        ],
        "tagline": "Full-stack power home",
    },
}

channels = {
    "Bill optimization": {
        "desc": "Reduce end-customer bill through self-consumption lift, smart charging, and timed consumption.",
        "who": "Mainly customer, sometimes supplier via proposition margin",
        "difficulty": 4,
        "value": 5,
        "maturity": "Easy and real today",
        "constraints": ["Tariff structure", "Customer behavior", "Device control"],
        "takeaway": "Most accessible residential value pool.",
    },
    "Day-ahead optimization": {
        "desc": "Use day-ahead price spreads to shift charging, discharge, or flexible load timing.",
        "who": "Supplier / aggregator / customer depending on tariff model",
        "difficulty": 3,
        "value": 4,
        "maturity": "Real today",
        "constraints": ["Forecasting", "BRP integration", "Portfolio scale"],
        "takeaway": "Bankable, especially for batteries.",
    },
    "Intraday optimization": {
        "desc": "Capture short-term price volatility and forecast-error value in 15-min or continuous markets.",
        "who": "Supplier / aggregator",
        "difficulty": 2,
        "value": 4,
        "maturity": "Real but operationally harder",
        "constraints": ["Fast telemetry", "Control quality", "Operational sophistication"],
        "takeaway": "Best fit for batteries, weak fit for simpler retail assets.",
    },
    "§14a / variable grid fee": {
        "desc": "Shift load away from expensive grid windows or monetize regulated grid-fee incentives for controllable assets.",
        "who": "Mostly customer, potentially shared in proposition design",
        "difficulty": 4,
        "value": 4,
        "maturity": "Easy and real today",
        "constraints": ["Eligibility", "DSO implementation", "Customer opt-in"],
        "takeaway": "Near-term regulatory tailwind.",
    },
    "Balancing / ancillary": {
        "desc": "Provide aFRR/FCR-style reserve capacity and activation, usually via aggregation.",
        "who": "Aggregator / supplier / partner",
        "difficulty": 1,
        "value": 4,
        "maturity": "Selective and harder today",
        "constraints": ["Prequalification", "Telemetry", "Pool size", "Reliability risk"],
        "takeaway": "Real money, but not a broad first-wave retail proposition.",
    },
    "Portfolio / BRP value": {
        "desc": "Reduce procurement cost, imbalance exposure, and portfolio risk using controllable asset fleets.",
        "who": "Supplier / BRP",
        "difficulty": 3,
        "value": 5,
        "maturity": "Real today but often under-attributed",
        "constraints": ["Integrated trading + flex stack", "Internal attribution logic"],
        "takeaway": "Often one of the most underrated value pools.",
    },
    "Local / DSO flexibility": {
        "desc": "Offer congestion or local grid support value in specific places and pilots.",
        "who": "Aggregator / supplier / DSO",
        "difficulty": 1,
        "value": 2,
        "maturity": "Emerging / selective",
        "constraints": ["Location specificity", "Immature market depth", "Pilot dependence"],
        "takeaway": "Watch closely, but do not build the core case on it.",
    },
}

fit_matrix = {
    "EV": {
        "Bill optimization": "High",
        "Day-ahead optimization": "Med",
        "Intraday optimization": "Low",
        "§14a / variable grid fee": "High",
        "Balancing / ancillary": "Low",
        "Portfolio / BRP value": "Med",
        "Local / DSO flexibility": "Med",
    },
    "PV": {
        "Bill optimization": "High",
        "Day-ahead optimization": "n/a",
        "Intraday optimization": "n/a",
        "§14a / variable grid fee": "Low",
        "Balancing / ancillary": "n/a",
        "Portfolio / BRP value": "Low",
        "Local / DSO flexibility": "Low",
    },
    "Home battery": {
        "Bill optimization": "High",
        "Day-ahead optimization": "High",
        "Intraday optimization": "Med",
        "§14a / variable grid fee": "Med",
        "Balancing / ancillary": "Med",
        "Portfolio / BRP value": "High",
        "Local / DSO flexibility": "Med",
    },
    "Heat pump": {
        "Bill optimization": "Med",
        "Day-ahead optimization": "Med",
        "Intraday optimization": "Low",
        "§14a / variable grid fee": "High",
        "Balancing / ancillary": "Low",
        "Portfolio / BRP value": "Med",
        "Local / DSO flexibility": "Med",
    },
    "EV + PV": {
        "Bill optimization": "High",
        "Day-ahead optimization": "Med",
        "Intraday optimization": "Low",
        "§14a / variable grid fee": "High",
        "Balancing / ancillary": "Low",
        "Portfolio / BRP value": "Med",
        "Local / DSO flexibility": "Med",
    },
    "PV + battery": {
        "Bill optimization": "Very high",
        "Day-ahead optimization": "High",
        "Intraday optimization": "Med",
        "§14a / variable grid fee": "Med",
        "Balancing / ancillary": "Med",
        "Portfolio / BRP value": "High",
        "Local / DSO flexibility": "Med",
    },
    "EV + battery": {
        "Bill optimization": "High",
        "Day-ahead optimization": "High",
        "Intraday optimization": "Med",
        "§14a / variable grid fee": "High",
        "Balancing / ancillary": "Med",
        "Portfolio / BRP value": "High",
        "Local / DSO flexibility": "Med",
    },
    "EV + PV + battery": {
        "Bill optimization": "Very high",
        "Day-ahead optimization": "High",
        "Intraday optimization": "Med",
        "§14a / variable grid fee": "High",
        "Balancing / ancillary": "Med",
        "Portfolio / BRP value": "High",
        "Local / DSO flexibility": "High",
    },
}

archetypes = {
    "EV-only household": {
        "bundle": "EV",
        "proposition": "Cheap night charging + smart-charge app + possible §14a benefit",
        "value_stack": {
            "Bill optimization": 220,
            "§14a / variable grid fee": 140,
            "Day-ahead optimization": 50,
            "Intraday optimization": 10,
            "Balancing / ancillary": 5,
            "Portfolio / BRP value": 30,
            "Local / DSO flexibility": 5,
        },
        "strongest": ["Bill optimization", "§14a / variable grid fee"],
        "weakest": ["Intraday optimization", "Balancing / ancillary"],
    },
    "PV + battery household": {
        "bundle": "PV + battery",
        "proposition": "Maximize PV value + battery timing + grid-fee upside",
        "value_stack": {
            "Bill optimization": 420,
            "§14a / variable grid fee": 120,
            "Day-ahead optimization": 110,
            "Intraday optimization": 35,
            "Balancing / ancillary": 40,
            "Portfolio / BRP value": 60,
            "Local / DSO flexibility": 10,
        },
        "strongest": ["Bill optimization", "Day-ahead optimization"],
        "weakest": ["Local / DSO flexibility"],
    },
    "Heat pump + PV household": {
        "bundle": "Heat pump",
        "proposition": "Shift heat to cheaper hours + capture regulated grid-fee value",
        "value_stack": {
            "Bill optimization": 180,
            "§14a / variable grid fee": 150,
            "Day-ahead optimization": 55,
            "Intraday optimization": 5,
            "Balancing / ancillary": 0,
            "Portfolio / BRP value": 35,
            "Local / DSO flexibility": 10,
        },
        "strongest": ["§14a / variable grid fee", "Bill optimization"],
        "weakest": ["Balancing / ancillary", "Intraday optimization"],
    },
    "EV + PV + battery household": {
        "bundle": "EV + PV + battery",
        "proposition": "Full-stack home energy optimization with the broadest value-stack potential",
        "value_stack": {
            "Bill optimization": 620,
            "§14a / variable grid fee": 155,
            "Day-ahead optimization": 160,
            "Intraday optimization": 55,
            "Balancing / ancillary": 60,
            "Portfolio / BRP value": 90,
            "Local / DSO flexibility": 20,
        },
        "strongest": ["Bill optimization", "Day-ahead optimization", "Portfolio / BRP value"],
        "weakest": ["Local / DSO flexibility"],
    },
}

waves = [
    {
        "wave": "Wave 1",
        "title": "Bill optimization + §14a",
        "summary": "Start with the easiest customer-facing value pools and strongest regulatory tailwind.",
        "assets": ["EV", "Heat pump", "PV + battery"],
        "channels": ["Bill optimization", "§14a / variable grid fee"],
    },
    {
        "wave": "Wave 2",
        "title": "Wholesale + portfolio",
        "summary": "Layer supplier / BRP value once orchestration and pricing logic mature.",
        "assets": ["Home battery", "PV + battery", "EV + battery", "EV + PV + battery"],
        "channels": ["Day-ahead optimization", "Portfolio / BRP value", "Intraday optimization"],
    },
    {
        "wave": "Wave 3",
        "title": "Selective balancing",
        "summary": "Enter ancillary services selectively where pool scale and control quality are sufficient.",
        "assets": ["Home battery", "EV + PV + battery"],
        "channels": ["Balancing / ancillary"],
    },
    {
        "wave": "Wave 4",
        "title": "Local flex and advanced options",
        "summary": "Pursue location-specific and advanced monetization routes opportunistically.",
        "assets": ["EV + PV + battery", "Home battery"],
        "channels": ["Local / DSO flexibility"],
    },
]

mode_presets = {
    "Conservative": {"multiplier": 0.80},
    "Base": {"multiplier": 1.00},
    "Upside": {"multiplier": 1.20},
}

# ----------------------------
# Helpers
# ----------------------------
def hero_card(title, value, subtitle):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="subtle">{title}</div>
            <div class="big-number">{value}</div>
            <div class="tiny">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def make_fit_df():
    rows = []
    for asset, row in fit_matrix.items():
        for channel, label in row.items():
            rows.append({"Asset": asset, "Channel": channel, "Fit": label, "Score": fit_score[label]})
    return pd.DataFrame(rows)

def make_channel_priority_df():
    rows = []
    for name, c in channels.items():
        rows.append({
            "Channel": name,
            "Ease of monetization": c["difficulty"],
            "Value potential": c["value"],
            "Maturity": c["maturity"],
            "Bubble size": 25 + c["value"] * 12,
        })
    return pd.DataFrame(rows)

def value_stack_df(archetype_name, mode_name):
    base = archetypes[archetype_name]["value_stack"]
    multiplier = mode_presets[mode_name]["multiplier"]
    rows = []
    for k, v in base.items():
        rows.append({"Channel": k, "Annual value (€ / year)": round(v * multiplier, 1)})
    return pd.DataFrame(rows)

fit_df = make_fit_df()
priority_df = make_channel_priority_df()

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("⚙️ Story controls")
selected_mode = st.sidebar.selectbox("Scenario mode", list(mode_presets.keys()), index=1)
selected_archetype = st.sidebar.selectbox("Archetype", list(archetypes.keys()), index=3)
selected_asset = st.sidebar.selectbox("Asset explorer", list(assets.keys()), index=6)
selected_channel = st.sidebar.selectbox("Channel explorer", list(channels.keys()), index=0)

st.sidebar.markdown("---")
st.sidebar.caption("Use this app as a guided internal strategy cockpit. Start on the Overview page, then move to Hero Matrix and Value Stack Simulator.")

# ----------------------------
# Header
# ----------------------------
st.markdown('<div class="hero-title">Retail Flex Monetization Cockpit</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">A premium internal strategy dashboard for showing where residential flexibility value comes from, which assets fit which channels, and why value stacking matters.</div>',
    unsafe_allow_html=True,
)

b1, b2, b3, b4 = st.columns(4)
with b1:
    st.markdown('<span class="badge">No single flexibility market</span>', unsafe_allow_html=True)
with b2:
    st.markdown('<span class="badge">Stack value streams</span>', unsafe_allow_html=True)
with b3:
    st.markdown('<span class="badge">PV + battery strongest today</span>', unsafe_allow_html=True)
with b4:
    st.markdown('<span class="badge">Balancing = selective, harder</span>', unsafe_allow_html=True)

st.markdown(
    '<div class="takeaway"><b>Core message:</b> Retail flexibility becomes bankable when multiple value pools are layered on the same hardware. Lead with bill optimization + §14a + portfolio/wholesale value, then add balancing selectively where control and scale justify it.</div>',
    unsafe_allow_html=True,
)

# ----------------------------
# Navigation
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Hero Matrix",
    "Value Stack Simulator",
    "Roadmap & Explorer",
])

# ----------------------------
# Tab 1: Overview
# ----------------------------
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        hero_card("Monetization channels", "7", "Distinct value pools with different access cost and bankability")
    with c2:
        hero_card("Best retail bundle", "PV + Battery", "Highest value density and strongest broad fit")
    with c3:
        hero_card("Most accessible channels", "Bill + §14a", "Best first-wave propositions")
    with c4:
        hero_card("Most operationally demanding", "Balancing", "Selective route, not a universal first step")

    left, right = st.columns([1.1, 1])

    with left:
        st.subheader("Where the money is")
        channel_rank = pd.DataFrame([
            {
                "Channel": k,
                "Value potential": v["value"],
                "Ease of access": v["difficulty"],
            }
            for k, v in channels.items()
        ]).sort_values("Value potential", ascending=True)

        fig = px.bar(
            channel_rank,
            x="Value potential",
            y="Channel",
            orientation="h",
            color="Ease of access",
            text="Value potential",
            color_continuous_scale="Sunset",
            height=460,
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Illustrative value potential",
            yaxis_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
            coloraxis_colorbar_title="Ease",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Strongest household bundles")
        bundle_scores = []
        for asset_name in list(fit_matrix.keys()):
            row = fit_matrix[asset_name]
            total = sum(fit_score[v] for v in row.values())
            bundle_scores.append({"Bundle": asset_name, "Composite fit score": total})
        bundle_df = pd.DataFrame(bundle_scores).sort_values("Composite fit score", ascending=False)

        fig2 = px.bar(
            bundle_df.head(6),
            x="Composite fit score",
            y="Bundle",
            orientation="h",
            text="Composite fit score",
            color="Composite fit score",
            color_continuous_scale="Tealgrn",
            height=460,
        )
        fig2.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Composite market-fit score",
            yaxis_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Executive takeaways")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div class="section-card">
            <b>1. Start where value is densest</b><br><br>
            PV + battery and EV + PV + battery produce the richest value stack because they combine customer bill value, timing value, and supplier-side optionality.
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="section-card">
            <b>2. Do not overbuild around a single channel</b><br><br>
            The strongest retail proposition usually does not rely on just FCR, just intraday, or just tariff savings. It stacks multiple moderate pools.
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="section-card">
            <b>3. Separate “possible” from “bankable”</b><br><br>
            A route can be technically feasible but commercially weak once telemetry, reliability, market access, and customer behavior are considered.
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Tab 2: Hero Matrix
# ----------------------------
with tab2:
    st.subheader("Asset × monetization fit matrix")
    st.caption("Use the selectors below the heatmap to inspect why a fit is strong, medium, low, or not applicable.")

    pivot = fit_df.pivot(index="Asset", columns="Channel", values="Score").loc[list(fit_matrix.keys()), list(channels.keys())]

    heat = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=["#1f2937", "#2563eb", "#14b8a6", "#84cc16", "#f59e0b"],
        height=560,
    )
    heat.update_traces(
        hovertemplate="Asset: %{y}<br>Channel: %{x}<br>Fit score: %{z}<extra></extra>"
    )
    heat.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        coloraxis_colorbar_title="Fit score",
    )
    st.plotly_chart(heat, use_container_width=True)

    a_col, c_col = st.columns([1, 1])
    with a_col:
        asset_pick = st.selectbox("Inspect asset", list(fit_matrix.keys()), index=6, key="matrix_asset")
    with c_col:
        channel_pick = st.selectbox("Inspect channel", list(channels.keys()), index=0, key="matrix_channel")

    fit_selected = fit_matrix[asset_pick][channel_pick]
    asset_info = assets[asset_pick]
    channel_info = channels[channel_pick]

    e1, e2 = st.columns([1, 1])
    with e1:
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;">{asset_info['icon']} {asset_pick}</h4>
            <div class="subtle">{asset_info['tagline']}</div><br>
            <b>Fit to {channel_pick}:</b> {fit_selected}<br><br>
            <b>Why this fit:</b><br>
            {asset_info['type']} with {asset_info['control'].lower()} tends to make this asset {fit_selected.lower()} for this route.
        </div>
        """, unsafe_allow_html=True)
    with e2:
        constraint_text = ", ".join(channel_info["constraints"])
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;">Commercial interpretation</h4>
            <b>Channel maturity:</b> {channel_info['maturity']}<br>
            <b>Main value logic:</b> {channel_info['desc']}<br><br>
            <b>Main constraints:</b> {constraint_text}<br><br>
            <b>Takeaway:</b> {channel_info['takeaway']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="takeaway"><b>Read this matrix like a portfolio strategy map:</b> bill optimization, §14a, and portfolio value are broadly accessible; wholesale is strongest for batteries; balancing is real but selective; local / DSO value is promising but not yet the foundation of a broad retail case.</div>',
        unsafe_allow_html=True,
    )

# ----------------------------
# Tab 3: Value Stack Simulator
# ----------------------------
with tab3:
    st.subheader("Value stack simulator")
    st.caption("Illustrative annual value stack for a selected household archetype. Use this to explain why value stacking matters more than any single revenue stream.")

    v1, v2 = st.columns([1, 1])
    with v1:
        archetype_name = st.selectbox("Choose archetype", list(archetypes.keys()), index=3, key="stack_arch")
    with v2:
        mode_name = st.radio("Scenario mode", list(mode_presets.keys()), horizontal=True, index=1, key="stack_mode")

    stack_df = value_stack_df(archetype_name, mode_name)
    stack_df["Channel"] = pd.Categorical(stack_df["Channel"], categories=list(channels.keys()), ordered=True)
    stack_df = stack_df.sort_values("Annual value (€ / year)", ascending=False)

    total_value = stack_df["Annual value (€ / year)"].sum()
    proposition = archetypes[archetype_name]["proposition"]
    strongest = ", ".join(archetypes[archetype_name]["strongest"])
    weakest = ", ".join(archetypes[archetype_name]["weakest"])

    k1, k2, k3 = st.columns(3)
    with k1:
        hero_card("Illustrative annual stack", f"€{total_value:,.0f}", f"{archetype_name} | {mode_name}")
    with k2:
        hero_card("Strongest value routes", strongest, "Most compelling monetization channels in this bundle")
    with k3:
        hero_card("Commercial proposition", proposition, "Suggested internal positioning")

    left, right = st.columns([1.1, 0.9])
    with left:
        fig = px.bar(
            stack_df.sort_values("Annual value (€ / year)", ascending=True),
            x="Annual value (€ / year)",
            y="Channel",
            orientation="h",
            text="Annual value (€ / year)",
            color="Annual value (€ / year)",
            color_continuous_scale="Turbo",
            height=470,
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Illustrative annual value (€ / year)",
            yaxis_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        pie = px.pie(
            stack_df,
            names="Channel",
            values="Annual value (€ / year)",
            hole=0.52,
            height=470,
        )
        pie.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
            legend=dict(orientation="h", y=-0.1),
        )
        st.plotly_chart(pie, use_container_width=True)

    st.markdown(f"""
    <div class="section-card">
        <b>How to explain this live:</b><br><br>
        This archetype is strongest in <b>{strongest}</b>. Its weakest channels are <b>{weakest}</b>. The key insight is that the total proposition becomes commercially meaningful only when multiple moderate value pools are combined rather than relying on a single “hero” market.
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# Tab 4: Roadmap & Explorer
# ----------------------------
with tab4:
    top_left, top_right = st.columns([1.05, 0.95])

    with top_left:
        st.subheader("Easy vs hard monetization map")
        bubble = px.scatter(
            priority_df,
            x="Ease of monetization",
            y="Value potential",
            size="Bubble size",
            color="Maturity",
            text="Channel",
            height=470,
        )
        bubble.update_traces(textposition="top center")
        bubble.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(range=[0.5, 4.5], tickvals=[1, 2, 3, 4], title="Ease of monetization"),
            yaxis=dict(range=[1, 5.5], tickvals=[1, 2, 3, 4, 5], title="Value potential"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
        )
        st.plotly_chart(bubble, use_container_width=True)

    with top_right:
        st.subheader("Go-to-market roadmap")
        for wave in waves:
            st.markdown(f"""
            <div class="section-card">
                <b>{wave['wave']} — {wave['title']}</b><br><br>
                {wave['summary']}<br><br>
                <b>Assets:</b> {", ".join(wave['assets'])}<br>
                <b>Channels:</b> {", ".join(wave['channels'])}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Asset explorer and channel explorer")
    left, right = st.columns(2)

    with left:
        info = assets[selected_asset]
        strengths = "".join([f"<li>{s}</li>" for s in info["strengths"]])
        limits = "".join([f"<li>{s}</li>" for s in info["limits"]])
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;">{info['icon']} {selected_asset}</h4>
            <div class="subtle">{info['tagline']}</div><br>
            <b>Flex type:</b> {info['type']}<br>
            <b>Control:</b> {info['control']}<br>
            <b>Response speed:</b> {info['response']}<br>
            <b>Predictability:</b> {info['predictability']}<br>
            <b>Availability:</b> {info['availability']}<br><br>
            <b>Strengths</b>
            <ul>{strengths}</ul>
            <b>Limitations</b>
            <ul>{limits}</ul>
        </div>
        """, unsafe_allow_html=True)

    with right:
        ch = channels[selected_channel]
        st.markdown(f"""
        <div class="section-card">
            <h4 style="margin-top:0;">{selected_channel}</h4>
            <b>What it is:</b> {ch['desc']}<br><br>
            <b>Who captures value:</b> {ch['who']}<br>
            <b>Maturity:</b> {ch['maturity']}<br>
            <b>Main takeaway:</b> {ch['takeaway']}<br><br>
            <b>Main constraints:</b> {", ".join(ch['constraints'])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="takeaway"><b>Commercial sequencing message:</b> start with the routes that are easiest to explain to customers and easiest to operationalize internally. Then layer supplier-side value and only later the more operationally demanding system-service routes.</div>',
        unsafe_allow_html=True,
    )
