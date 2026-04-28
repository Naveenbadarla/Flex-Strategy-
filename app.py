import streamlit as st
import plotly.graph_objects as go


# =============================================================================
# 1. PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Retail Flex · Strategy Cockpit",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# 2. COLOR PALETTE & CSS
# =============================================================================

PALETTE = {
    "bg":              "#0B0F14",
    "panel":           "#141A22",
    "panel_2":         "#1B232D",
    "panel_3":         "#222B36",
    "border":          "#2A3340",
    "border_strong":   "#3A4552",
    "text_primary":    "#E6EDF3",
    "text_secondary":  "#9CA3AF",
    "text_tertiary":   "#6B7280",
    # accents
    "teal":            "#2DD4BF",
    "cyan":            "#22D3EE",
    "amber":           "#F59E0B",
    "gold":            "#FBBF24",
    "red":             "#EF4444",
    "blue":            "#60A5FA",
    "purple":          "#A78BFA",
    "green":           "#34D399",
    # suitability scale (used by heatmap and badges)
    "score_vh":        "#0D9488",   # very high — deep teal
    "score_h":         "#22C55E",   # high — emerald
    "score_m":         "#D97706",   # medium — amber
    "score_l":         "#475569",   # low — muted slate
    "score_na":        "#1F2937",   # n/a — near-bg
}


CUSTOM_CSS = f"""
<style>
    /* App shell */
    .stApp {{ background-color: {PALETTE['bg']}; }}
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1380px;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {PALETTE['panel']};
        border-right: 1px solid {PALETTE['border']};
    }}
    section[data-testid="stSidebar"] .stRadio > label {{
        color: {PALETTE['text_tertiary']} !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }}
    section[data-testid="stSidebar"] [role="radiogroup"] label p {{
        font-size: 0.92rem !important;
        font-weight: 500;
    }}

    /* Typography */
    h1, h2, h3, h4 {{
        color: {PALETTE['text_primary']};
        font-weight: 500;
        letter-spacing: -0.01em;
    }}
    h1 {{ font-size: 2.0rem; font-weight: 600; margin-bottom: 0.2rem; }}
    h2 {{ font-size: 1.35rem; margin-top: 1.5rem; }}
    h3 {{ font-size: 1.05rem; margin-top: 1rem; }}

    .stApp, .stMarkdown, .stMarkdown p {{ color: {PALETTE['text_primary']}; }}
    .stMarkdown p {{ line-height: 1.65; }}

    /* Subtitle under H1 */
    .subtitle {{
        color: {PALETTE['text_secondary']};
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }}

    /* Cards */
    .card {{
        background: {PALETTE['panel']};
        border: 1px solid {PALETTE['border']};
        border-radius: 10px;
        padding: 1.1rem 1.35rem;
        margin-bottom: 0.9rem;
    }}
    .card-emph {{
        background: {PALETTE['panel_2']};
        border-left: 3px solid {PALETTE['teal']};
    }}

    /* Metric cards */
    .metric-card {{
        background: {PALETTE['panel']};
        border: 1px solid {PALETTE['border']};
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        height: 100%;
    }}
    .metric-label {{
        color: {PALETTE['text_tertiary']};
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .metric-value {{
        color: {PALETTE['text_primary']};
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 0.4rem;
        line-height: 1.2;
    }}
    .metric-sub {{
        color: {PALETTE['text_secondary']};
        font-size: 0.82rem;
        margin-top: 0.4rem;
    }}

    /* Headline strip */
    .headline-strip {{
        background: {PALETTE['panel_2']};
        border: 1px solid {PALETTE['border']};
        border-left: 3px solid {PALETTE['teal']};
        padding: 0.85rem 1.2rem;
        border-radius: 8px;
        margin: 0.3rem 0 1.5rem 0;
        color: {PALETTE['text_primary']};
        font-weight: 500;
        font-size: 1.0rem;
    }}

    /* Badges */
    .badge {{
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-right: 4px;
    }}
    .badge-vh {{ background: {PALETTE['score_vh']}; color: #ffffff; }}
    .badge-h  {{ background: {PALETTE['score_h']};  color: #052e16; }}
    .badge-m  {{ background: {PALETTE['score_m']};  color: #2c1605; }}
    .badge-l  {{ background: {PALETTE['score_l']};  color: #E5E7EB; }}
    .badge-na {{ background: {PALETTE['score_na']}; color: {PALETTE['text_tertiary']}; }}

    /* Tags */
    .tag {{
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 4px;
        background: {PALETTE['panel_3']};
        border: 1px solid {PALETTE['border']};
        color: {PALETTE['text_secondary']};
        font-size: 0.76rem;
        margin: 2px 4px 2px 0;
    }}
    .tag-strong {{ color: {PALETTE['teal']}; border-color: {PALETTE['teal']}55; }}
    .tag-warn   {{ color: {PALETTE['amber']}; border-color: {PALETTE['amber']}55; }}

    /* Insight box */
    .insight {{
        background: {PALETTE['panel_2']};
        border-left: 3px solid {PALETTE['gold']};
        padding: 0.9rem 1.2rem;
        border-radius: 6px;
        margin: 1rem 0;
        color: {PALETTE['text_primary']};
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    .insight-label {{
        color: {PALETTE['gold']};
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
        display: block;
    }}

    /* Score bars */
    .score-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0.3rem 0;
        font-size: 0.85rem;
    }}
    .score-label {{
        color: {PALETTE['text_secondary']};
        width: 130px;
        font-size: 0.82rem;
    }}
    .score-bar-bg {{
        flex: 1;
        height: 6px;
        background: {PALETTE['panel_3']};
        border-radius: 3px;
        overflow: hidden;
    }}
    .score-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, {PALETTE['teal']} 0%, {PALETTE['cyan']} 100%);
        border-radius: 3px;
    }}
    .score-num {{
        color: {PALETTE['text_secondary']};
        font-size: 0.78rem;
        width: 24px;
        text-align: right;
    }}

    /* Wave card */
    .wave-card {{
        background: {PALETTE['panel']};
        border: 1px solid {PALETTE['border']};
        border-left: 3px solid {PALETTE['teal']};
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
    }}
    .wave-num {{
        color: {PALETTE['teal']};
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }}
    .wave-title {{
        color: {PALETTE['text_primary']};
        font-size: 1.05rem;
        font-weight: 500;
        margin: 0.25rem 0 0.4rem 0;
    }}

    /* Section divider */
    .section-divider {{
        height: 1px;
        background: {PALETTE['border']};
        margin: 1.6rem 0 1.2rem 0;
    }}

    /* Streamlit overrides */
    .stSelectbox label, .stRadio label, .stMultiSelect label, .stSlider label {{
        color: {PALETTE['text_secondary']} !important;
        font-weight: 500;
        font-size: 0.85rem !important;
    }}
    .stSelectbox > div > div {{
        background: {PALETTE['panel']} !important;
        border-color: {PALETTE['border']} !important;
    }}

    /* Hide Streamlit chrome */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# 3. DATA — ASSETS
# =============================================================================
# Each asset captures: capability scores (0–5), strengths/limits, best/weak
# channels, and a one-line summary for cards. Capability scores feed the radar.

ASSETS: dict[str, dict] = {
    "ev_1way": {
        "name": "EV (1-way)",
        "short": "EV",
        "tagline": "Volume play",
        "marker": "▮",
        "flex_type": "Shiftable demand",
        "power_kw": "7–22",
        "energy_kwh": "40–100",
        "scores": {
            "controllability": 4,
            "response_speed": 3,
            "predictability": 2,
            "availability": 2,
            "cycle_freedom": 4,
        },
        "strengths": [
            "Large overnight shiftable load",
            "Clean dynamic-tariff customer story",
            "Aggregate volume scales linearly with EV penetration",
        ],
        "limits": [
            "Plug-in uncertainty (typical 50–70 % overnight)",
            "Symmetric balancing services need V2G",
            "OEM control API fragmentation",
        ],
        "best": ["bill", "grid_fee"],
        "weak": ["fcr", "afrr", "id"],
        "summary": (
            "Volume play. Overnight charging under dynamic tariffs and §14a is "
            "the cleanest residential entry; balancing services require V2G or "
            "asymmetric pools."
        ),
    },
    "ev_v2g": {
        "name": "EV (V2G)",
        "short": "EV V2G",
        "tagline": "Future heavyweight",
        "marker": "▮↔",
        "flex_type": "Bidirectional storage on wheels",
        "power_kw": "7–22 (bidirectional)",
        "energy_kwh": "40–100",
        "scores": {
            "controllability": 5,
            "response_speed": 4,
            "predictability": 2,
            "availability": 2,
            "cycle_freedom": 3,
        },
        "strengths": [
            "Battery-equivalent flex when plugged in",
            "Strategically positioned for 2027+ value pools",
            "Genuine local-flex value (residential street density)",
        ],
        "limits": [
            "Hardware penetration <5 % of new EVs in 2026",
            "ISO 15118-20 standards still maturing",
            "Cycle warranty and OEM partnerships gating",
        ],
        "best": ["bill", "da", "grid_fee", "local", "brp"],
        "weak": ["id"],
        "summary": (
            "Strategic option, not a near-term P&L driver. Real revenue unlocks "
            "from ~2027 as hardware and standards mature; invest in pilots and "
            "OEM partnerships now."
        ),
    },
    "pv": {
        "name": "Rooftop PV",
        "short": "PV",
        "tagline": "Enabler, not flex",
        "marker": "☀",
        "flex_type": "Variable generation",
        "power_kw": "3–15",
        "energy_kwh": "—",
        "scores": {
            "controllability": 1,
            "response_speed": 1,
            "predictability": 3,
            "availability": 3,
            "cycle_freedom": 5,
        },
        "strengths": [
            "Largest residential value pool today (self-cons. uplift)",
            "Forecastable on a daily basis",
            "Pairs with every flex asset",
        ],
        "limits": [
            "Not a flexible asset on its own — only curtailable",
            "Value depends on co-located load or storage",
            "Output is weather-bound, not dispatch-bound",
        ],
        "best": ["bill"],
        "weak": ["da", "id", "afrr", "fcr"],
        "summary": (
            "An enabler rather than pure flexibility. PV creates the "
            "self-consumption surface that batteries and loads monetize against; "
            "value is captured indirectly through pairing."
        ),
    },
    "battery": {
        "name": "Home battery",
        "short": "Battery",
        "tagline": "Swiss army knife",
        "marker": "▦",
        "flex_type": "Bidirectional storage",
        "power_kw": "3–10",
        "energy_kwh": "5–15",
        "scores": {
            "controllability": 5,
            "response_speed": 5,
            "predictability": 5,
            "availability": 5,
            "cycle_freedom": 3,
        },
        "strengths": [
            "Touches every monetization channel",
            "Fast, predictable, always available",
            "Best retail asset for daily arbitrage",
        ],
        "limits": [
            "Cycle-limited (warranty terms)",
            "State-of-charge constraints under stacking",
            "Plug-and-play units often lack open control APIs",
        ],
        "best": ["bill", "da", "brp"],
        "weak": [],
        "summary": (
            "The Swiss army knife of retail flex. Every channel is in scope, "
            "but cycle wear must be priced and proper telemetry is needed for "
            "the high-skill markets."
        ),
    },
    "hp": {
        "name": "Heat pump",
        "short": "Heat pump",
        "tagline": "Predictable shifter",
        "marker": "◐",
        "flex_type": "Thermal time-shift",
        "power_kw": "2–10",
        "energy_kwh": "(thermal buffer 1–4 h)",
        "scores": {
            "controllability": 4,
            "response_speed": 2,
            "predictability": 4,
            "availability": 4,
            "cycle_freedom": 5,
        },
        "strengths": [
            "Excellent §14a fit (>4.2 kW threshold)",
            "Predictable, weather-correlated demand",
            "Comfort-tolerant pre-heating windows",
        ],
        "limits": [
            "Slow ramp — not for FCR",
            "Comfort floor binding",
            "Thermal buffer typically 1–4 hours",
        ],
        "best": ["grid_fee", "bill", "da"],
        "weak": ["fcr", "id"],
        "summary": (
            "Predictable shifter. Strongest fit with §14a and day-ahead "
            "pre-heating; not suitable for fast services."
        ),
    },
    "ev_pv": {
        "name": "EV + PV",
        "short": "EV+PV",
        "tagline": "Solar mobility",
        "marker": "▮+☀",
        "flex_type": "Shiftable load + generation",
        "power_kw": "7–22 + 3–15",
        "energy_kwh": "40–100",
        "scores": {
            "controllability": 4,
            "response_speed": 3,
            "predictability": 3,
            "availability": 3,
            "cycle_freedom": 4,
        },
        "strengths": [
            "Direct PV-to-EV charging is a marketable story",
            "Daytime charging when PV surplus available",
            "Clean §14a + dynamic tariff stack",
        ],
        "limits": [
            "EV often absent during PV peak (commuter pattern)",
            "No fast-service capability without battery",
            "Dependent on smart-charge logic at the wallbox",
        ],
        "best": ["bill", "grid_fee"],
        "weak": ["fcr", "afrr"],
        "summary": (
            "Strong customer narrative, modest commercial uplift over EV alone. "
            "Most value comes from PV self-consumption when the EV happens to "
            "be home."
        ),
    },
    "pv_battery": {
        "name": "PV + battery",
        "short": "PV+Bat",
        "tagline": "Highest-density retail bundle",
        "marker": "☀+▦",
        "flex_type": "Generation + storage",
        "power_kw": "3–15 + 3–10",
        "energy_kwh": "5–15",
        "scores": {
            "controllability": 5,
            "response_speed": 5,
            "predictability": 5,
            "availability": 5,
            "cycle_freedom": 3,
        },
        "strengths": [
            "Highest annual value density per home",
            "Self-consumption + arbitrage + grid-fee stack",
            "Always-on battery underpins fast services",
        ],
        "limits": [
            "Largest hardware capex of all bundles",
            "§14a discharge constraints can clip stacking",
            "Cycle wear must be optimized across channels",
        ],
        "best": ["bill", "da", "brp"],
        "weak": [],
        "summary": (
            "The headline pairing. Highest customer-facing value, cleanest "
            "story, full channel access. Lead with this segment in go-to-market."
        ),
    },
    "ev_battery": {
        "name": "EV + battery",
        "short": "EV+Bat",
        "tagline": "Mobility + always-on flex",
        "marker": "▮+▦",
        "flex_type": "Shiftable load + storage",
        "power_kw": "7–22 + 3–10",
        "energy_kwh": "40–100 + 5–15",
        "scores": {
            "controllability": 5,
            "response_speed": 5,
            "predictability": 4,
            "availability": 4,
            "cycle_freedom": 3,
        },
        "strengths": [
            "Battery covers EV plug-in gaps for fast services",
            "Two §14a-eligible loads",
            "Strong portfolio predictability",
        ],
        "limits": [
            "Without PV, bill story is less differentiated",
            "Capex high without PV self-consumption layer",
            "Cycle allocation between channels needs governance",
        ],
        "best": ["bill", "da", "grid_fee", "brp"],
        "weak": [],
        "summary": (
            "Robust commercial profile. Battery delivers fast services while "
            "EV provides bulk shifting; less natural retail story than the PV "
            "pairing without solar."
        ),
    },
    "ev_pv_battery": {
        "name": "EV + PV + battery",
        "short": "Full stack",
        "tagline": "Home as a power plant",
        "marker": "▮+☀+▦",
        "flex_type": "Full stack",
        "power_kw": "7–22 + 3–15 + 3–10",
        "energy_kwh": "40–100 + 5–15",
        "scores": {
            "controllability": 5,
            "response_speed": 5,
            "predictability": 4,
            "availability": 5,
            "cycle_freedom": 3,
        },
        "strengths": [
            "Maximum value-stack potential",
            "Strongest customer proposition (energy autonomy)",
            "Future-proof against V2G and dynamic tariffs",
        ],
        "limits": [
            "Highest hardware capex",
            "Optimization complexity (SoC arbitration)",
            "Smaller addressable base today (early-adopter segment)",
        ],
        "best": ["bill", "da", "grid_fee", "local", "brp"],
        "weak": [],
        "summary": (
            "Top of the stack. All channels accessible; revenue density per "
            "home is highest. Smaller addressable base today but the "
            "lighthouse segment for premium propositions."
        ),
    },
}


# =============================================================================
# 4. DATA — MONETIZATION CHANNELS
# =============================================================================

CHANNELS: dict[str, dict] = {
    "bill": {
        "name": "Customer bill optimization",
        "short": "Bill opt",
        "icon": "€",
        "category": "Customer",
        "what": (
            "Reduce the customer's energy bill through PV self-consumption "
            "uplift, dynamic-tariff arbitrage, and load shifting away from "
            "expensive import hours."
        ),
        "mechanism": "Spread between retail import tariff and avoided cost",
        "captured_by": "Customer (or supplier via premium tariff / savings share)",
        "best_assets": ["pv_battery", "ev_pv_battery", "battery", "ev_pv"],
        "constraints": [
            "Value flows to customer unless packaged into a margin product",
            "Capped by retail tariff ceiling and PV feed-in alternative",
            "Smart-meter rollout still incomplete",
        ],
        "scores": {
            "value_potential":         5,
            "ease_of_access":          5,
            "operational_complexity":  2,
            "scalability":             5,
        },
        "maturity": "Mature — easy and real today",
        "realism": "easy_real",
    },
    "da": {
        "name": "Day-ahead wholesale",
        "short": "DA",
        "icon": "↔",
        "category": "Wholesale",
        "what": (
            "Charge / discharge / shift load to capture EPEX day-ahead price "
            "spreads. Daily peak–trough typically €30–80/MWh, higher in "
            "volatile months."
        ),
        "mechanism": "Daily price spread arbitrage",
        "captured_by": "Supplier / aggregator (sometimes shared with customer)",
        "best_assets": ["battery", "pv_battery", "ev_battery", "ev_pv_battery"],
        "constraints": [
            "Requires forecasting and BRP integration",
            "Spread is shrinking in some hours as flex penetrates",
            "Pass-through tariff or supplier-side optimization needed",
        ],
        "scores": {
            "value_potential":         3,
            "ease_of_access":          3,
            "operational_complexity":  3,
            "scalability":             5,
        },
        "maturity": "Mature — bankable today",
        "realism": "real_hard",
    },
    "id": {
        "name": "Intraday wholesale",
        "short": "ID",
        "icon": "⟳",
        "category": "Wholesale",
        "what": (
            "Trading 15-min and continuous intraday products around forecast "
            "errors and short-term system shocks. High €/MWh per cycle, "
            "lower volume."
        ),
        "mechanism": "Sub-hourly arbitrage and re-hedging",
        "captured_by": "Supplier / aggregator (specialized trading desk)",
        "best_assets": ["battery", "pv_battery", "ev_pv_battery"],
        "constraints": [
            "Demands fast control and near-real-time telemetry",
            "Fragmented OEM control APIs are a real blocker",
            "Plug-and-play units rarely reach this pool",
        ],
        "scores": {
            "value_potential":         3,
            "ease_of_access":          2,
            "operational_complexity":  4,
            "scalability":             3,
        },
        "maturity": "Real but operationally hard",
        "realism": "real_hard",
    },
    "grid_fee": {
        "name": "§14a / variable grid fees",
        "short": "§14a",
        "icon": "▥",
        "category": "Regulatory",
        "what": (
            "§14a EnWG: DSOs may dim controllable loads >4.2 kW in exchange "
            "for a regulated grid-fee discount (Modul 1 flat, Modul 2 percentage, "
            "Modul 3 time-variable). Time-variable network tariffs being rolled "
            "out 2025–2028."
        ),
        "mechanism": "Regulated grid-fee discount for opt-in controllability",
        "captured_by": "Customer (regulated discount)",
        "best_assets": ["hp", "ev_battery", "ev_pv_battery", "ev_1way"],
        "constraints": [
            "Discount is regulated, not market-driven",
            "DSO-specific implementation across ~870 DSOs",
            "Customer must opt in (Modul 2/3)",
        ],
        "scores": {
            "value_potential":         3,
            "ease_of_access":          5,
            "operational_complexity":  2,
            "scalability":             5,
        },
        "maturity": "Active since 2024 — regulatory tailwind",
        "realism": "easy_real",
    },
    "afrr": {
        "name": "aFRR (balancing)",
        "short": "aFRR",
        "icon": "⏱",
        "category": "Ancillary",
        "what": (
            "Automatic frequency restoration reserve. 30s ramp, capacity + "
            "activation revenue, asymmetric bids possible. Pre-qualification "
            "and pool size are gating."
        ),
        "mechanism": "Capacity remuneration plus activation revenue",
        "captured_by": "Aggregator / TSO (revenue share with supplier or customer)",
        "best_assets": ["battery", "pv_battery", "ev_v2g", "ev_battery"],
        "constraints": [
            "1 MW minimum bid (poolable); hundreds–thousands of assets needed",
            "Telemetry obligations and severe non-delivery penalties",
            "Best entered via aggregator partnership, not greenfield",
        ],
        "scores": {
            "value_potential":         4,
            "ease_of_access":          2,
            "operational_complexity":  5,
            "scalability":             3,
        },
        "maturity": "Real but operationally hard",
        "realism": "real_hard",
    },
    "fcr": {
        "name": "FCR (balancing)",
        "short": "FCR",
        "icon": "⚡",
        "category": "Ancillary",
        "what": (
            "Frequency containment reserve. Symmetric, very fast, 4-hour "
            "blocks. Historically €2–5k/MW/week; capacity prices have "
            "compressed materially as battery capacity scales."
        ),
        "mechanism": "Capacity remuneration for symmetric fast response",
        "captured_by": "Aggregator / TSO",
        "best_assets": ["battery", "pv_battery", "ev_v2g"],
        "constraints": [
            "Symmetric requirement — needs bidirectional capability",
            "Increasingly crowded as front-of-meter batteries scale",
            "Cycle wear must be priced",
        ],
        "scores": {
            "value_potential":         3,
            "ease_of_access":          1,
            "operational_complexity":  5,
            "scalability":             2,
        },
        "maturity": "Mature but compressing",
        "realism": "real_hard",
    },
    "local": {
        "name": "Local / DSO flexibility",
        "short": "Local",
        "icon": "◎",
        "category": "Network",
        "what": (
            "Local congestion relief, redispatch contributions, DSO flex "
            "tenders. Highly location-specific. Prices set by tender or "
            "bilateral negotiation."
        ),
        "mechanism": "Tender or bilateral payment for location-specific dispatch",
        "captured_by": "Aggregator / supplier with DSO contract",
        "best_assets": ["ev_v2g", "ev_pv_battery", "battery"],
        "constraints": [
            "Markets are nascent in Germany",
            "Not yet a scalable revenue stream",
            "Highly heterogeneous across DSOs",
        ],
        "scores": {
            "value_potential":         2,
            "ease_of_access":          1,
            "operational_complexity":  4,
            "scalability":             2,
        },
        "maturity": "Emerging — selective pilots only",
        "realism": "emerging",
    },
    "brp": {
        "name": "Portfolio / BRP value",
        "short": "BRP",
        "icon": "◧",
        "category": "Internal",
        "what": (
            "Internal value to the supplier / BRP — better hedging, lower "
            "imbalance exposure, reduced peak procurement, smoother "
            "forecasts. Often invisible on the customer-facing P&L but real "
            "on the procurement P&L."
        ),
        "mechanism": "Reduced procurement and imbalance cost",
        "captured_by": "Supplier (procurement / trading P&L)",
        "best_assets": ["battery", "pv_battery", "ev_pv_battery", "ev_battery"],
        "constraints": [
            "Value is hard to attribute cleanly internally",
            "Requires integrated trading + flex platform",
            "Often underweighted in business cases",
        ],
        "scores": {
            "value_potential":         4,
            "ease_of_access":          3,
            "operational_complexity":  3,
            "scalability":             5,
        },
        "maturity": "Mature — the underrated channel",
        "realism": "easy_real",
    },
}


# =============================================================================
# 5. DATA — ASSET × CHANNEL FIT MATRIX
# =============================================================================
# Score scale: 4 = Very High, 3 = High, 2 = Medium, 1 = Low, 0 = Not applicable.
# Bankable flag = is this fit commercially realistic today (vs theoretical).

def _fit(score: int, rationale: str, bankable: bool = True) -> dict:
    return {"score": score, "rationale": rationale, "bankable": bankable}


# Channel order used everywhere for consistency
CHANNEL_ORDER = ["bill", "da", "id", "grid_fee", "afrr", "fcr", "local", "brp"]
ASSET_ORDER = [
    "ev_1way", "ev_v2g", "pv", "battery", "hp",
    "ev_pv", "pv_battery", "ev_battery", "ev_pv_battery",
]

FIT_MATRIX: dict[tuple[str, str], dict] = {

    # --- EV (1-way) -----------------------------------------------------------
    ("ev_1way", "bill"):     _fit(3, "Overnight charging under a dynamic tariff captures the retail-to-wholesale spread. Cleanest customer-facing flex story for an EV."),
    ("ev_1way", "da"):       _fit(2, "Smart-charge optimization works, but plug-in uncertainty and 7–22 kW power cap the realized arbitrage per session."),
    ("ev_1way", "id"):       _fit(1, "Plug-in randomness and slow control loops make sub-hourly trading marginal without aggregation infrastructure."),
    ("ev_1way", "grid_fee"): _fit(3, "Wallbox >4.2 kW qualifies for §14a Modul 1 (≈€110–190/yr discount). Clean regulatory tailwind."),
    ("ev_1way", "afrr"):     _fit(1, "Down-only (curtail charging) only — symmetric services need V2G. Reliability sub-90 % without large pools.", bankable=False),
    ("ev_1way", "fcr"):      _fit(1, "Symmetric requirement makes 1-way EVs a poor structural fit. Theoretically possible via curtailment-only schemes, not commercial.", bankable=False),
    ("ev_1way", "local"):    _fit(2, "Geographic concentration in residential streets makes EVs interesting for DSO congestion, but markets are immature."),
    ("ev_1way", "brp"):      _fit(2, "Forecastable in aggregate, useful for portfolio shaping. Per-asset value modest."),

    # --- EV (V2G) -------------------------------------------------------------
    ("ev_v2g", "bill"):      _fit(3, "Discharge into peak hours on top of 1-way bill optimization. Depends on tariff structures rewarding export."),
    ("ev_v2g", "da"):        _fit(3, "Battery-equivalent arbitrage when plugged in. Plug-in remains the binding constraint."),
    ("ev_v2g", "id"):        _fit(2, "Fast bidirectional response is technically feasible; call-rate uncertainty limits commercial entry."),
    ("ev_v2g", "grid_fee"):  _fit(3, "Same §14a logic as 1-way, with extra discharge optionality."),
    ("ev_v2g", "afrr"):      _fit(2, "Symmetric capacity feasible; OEM control APIs and cycle warranty are gating factors."),
    ("ev_v2g", "fcr"):       _fit(2, "Same as aFRR. Reliability requires aggregation across hundreds of vehicles."),
    ("ev_v2g", "local"):     _fit(3, "Bidirectional response is genuinely valuable for local congestion; commercial pathways forming."),
    ("ev_v2g", "brp"):       _fit(3, "High portfolio value: bidirectional, large pool, diurnal predictability."),

    # --- PV alone -------------------------------------------------------------
    ("pv", "bill"):     _fit(3, "Self-consumption uplift is the largest residential value pool. Strictly speaking not 'flex' but a value source."),
    ("pv", "da"):       _fit(0, "PV is not flexible; it can only be curtailed. No arbitrage role on its own."),
    ("pv", "id"):       _fit(0, "Same as DA — not a controllable load."),
    ("pv", "grid_fee"): _fit(1, "PV alone is generation, not a controllable load. Minor §14a relevance."),
    ("pv", "afrr"):     _fit(0, "Not relevant for residential PV.", bankable=False),
    ("pv", "fcr"):      _fit(0, "Not relevant.", bankable=False),
    ("pv", "local"):    _fit(1, "Curtailment for grid support is technically possible but rarely monetized at retail scale."),
    ("pv", "brp"):      _fit(1, "Forecastable but uncontrollable — portfolio value is generation hedge, not flex."),

    # --- Home battery ---------------------------------------------------------
    ("battery", "bill"):     _fit(3, "Strong: pairs with PV self-consumption, dynamic-tariff arbitrage, and peak shaving."),
    ("battery", "da"):       _fit(3, "Best retail asset for daily arbitrage. Cycle-limited but predictable."),
    ("battery", "id"):       _fit(2, "Native fast response — but intraday access requires control infrastructure that plug-and-play units often lack."),
    ("battery", "grid_fee"): _fit(2, "Battery >4.2 kW qualifies; §14a discharge constraints can clip stacking with other channels."),
    ("battery", "afrr"):     _fit(2, "Native technical fit; pool size, pre-qualification, and cycle-wear pricing required."),
    ("battery", "fcr"):      _fit(2, "Strong technical fit; market increasingly crowded as front-of-meter batteries scale."),
    ("battery", "local"):    _fit(2, "Locally placed batteries help DSO congestion; markets are nascent."),
    ("battery", "brp"):      _fit(3, "The most reliable, predictable, dispatchable retail asset for portfolio value."),

    # --- Heat pump ------------------------------------------------------------
    ("hp", "bill"):     _fit(2, "Thermal time-shift gives modest bill reduction under dynamic tariffs. Comfort-bounded."),
    ("hp", "da"):       _fit(2, "Pre-heating / pre-cooling within the thermal envelope captures ~1–3 hour spreads."),
    ("hp", "id"):       _fit(1, "Slow ramp limits intraday relevance; only marginal."),
    ("hp", "grid_fee"): _fit(3, "Excellent §14a fit: >4.2 kW threshold easy to meet, predictable shifting, clear customer story."),
    ("hp", "afrr"):     _fit(1, "Slow ramp (minutes); only marginal on slow products and only via large pools."),
    ("hp", "fcr"):      _fit(0, "Response too slow; comfort floor binding.", bankable=False),
    ("hp", "local"):    _fit(2, "Thermal load deferral is useful for evening peak DSO support."),
    ("hp", "brp"):      _fit(2, "Predictable seasonal demand. Useful for procurement shaping."),

    # --- EV + PV --------------------------------------------------------------
    ("ev_pv", "bill"):     _fit(3, "Direct PV-to-EV charging story plus dynamic tariff layer. EV often absent during PV peak (commuter pattern) caps the uplift."),
    ("ev_pv", "da"):       _fit(2, "EV smart-charge logic captures DA spreads; no fast-service capability."),
    ("ev_pv", "id"):       _fit(1, "Same constraints as 1-way EV."),
    ("ev_pv", "grid_fee"): _fit(3, "§14a Modul 1 on the wallbox; PV is regulatorily separate."),
    ("ev_pv", "afrr"):     _fit(1, "Curtailment-only without V2G or battery."),
    ("ev_pv", "fcr"):      _fit(1, "Same as 1-way EV."),
    ("ev_pv", "local"):    _fit(2, "Geographic clustering useful for DSO; market access still maturing."),
    ("ev_pv", "brp"):      _fit(2, "Improved predictability vs EV alone, modest portfolio uplift."),

    # --- PV + battery ---------------------------------------------------------
    ("pv_battery", "bill"):     _fit(4, "Highest-value retail bundle for bill optimization: PV self-consumption uplift + battery arbitrage + peak shave + dynamic tariff."),
    ("pv_battery", "da"):       _fit(3, "Battery-driven arbitrage is reliable and bankable."),
    ("pv_battery", "id"):       _fit(2, "Battery is fast enough; control infrastructure determines bankability."),
    ("pv_battery", "grid_fee"): _fit(2, "Eligible; §14a interventions can reduce battery utilization for other channels."),
    ("pv_battery", "afrr"):     _fit(2, "Battery enables aFRR; aggregation pool is the enabler."),
    ("pv_battery", "fcr"):      _fit(2, "Same as battery alone."),
    ("pv_battery", "local"):    _fit(2, "Battery + PV pairing is locally useful, especially in PV-heavy LV networks."),
    ("pv_battery", "brp"):      _fit(3, "High predictability + dispatchability. Strong portfolio value."),

    # --- EV + battery ---------------------------------------------------------
    ("ev_battery", "bill"):     _fit(3, "Strong without PV but lower bill density; battery covers EV plug-in gaps."),
    ("ev_battery", "da"):       _fit(3, "Battery provides reliable arbitrage; EV adds bulk shifting capacity."),
    ("ev_battery", "id"):       _fit(2, "Battery is the workhorse; same infrastructure constraints as battery alone."),
    ("ev_battery", "grid_fee"): _fit(3, "Two §14a-eligible loads; clean regulatory stack."),
    ("ev_battery", "afrr"):     _fit(2, "Battery enables symmetric service; EV adds asymmetric capacity when plugged."),
    ("ev_battery", "fcr"):      _fit(2, "Battery-driven; EV optionally augments via V2G."),
    ("ev_battery", "local"):    _fit(2, "Useful in residential-density networks, especially with V2G EV."),
    ("ev_battery", "brp"):      _fit(3, "Best predictability of any non-PV bundle. High portfolio value."),

    # --- EV + PV + battery (full stack) ---------------------------------------
    ("ev_pv_battery", "bill"):     _fit(4, "Maximum bill density: PV self-consumption + battery arbitrage + EV smart-charge + dynamic tariff."),
    ("ev_pv_battery", "da"):       _fit(3, "Battery-driven; full stack supports aggressive arbitrage strategies."),
    ("ev_pv_battery", "id"):       _fit(2, "Battery is fast enough; intraday bankability hinges on control infrastructure."),
    ("ev_pv_battery", "grid_fee"): _fit(3, "Two §14a-eligible loads (HP-class wallbox + battery)."),
    ("ev_pv_battery", "afrr"):     _fit(2, "Battery enables aFRR; full stack improves call-rate reliability."),
    ("ev_pv_battery", "fcr"):      _fit(2, "Battery-driven, with V2G option for additional symmetric capacity."),
    ("ev_pv_battery", "local"):    _fit(3, "Strongest local-flex profile due to bidirectional bundle and on-site generation."),
    ("ev_pv_battery", "brp"):      _fit(3, "Highest portfolio value per home: dispatchable + predictable + diversified."),
}


# =============================================================================
# 6. DATA — CUSTOMER ARCHETYPES (with illustrative annual value stacks in EUR)
# =============================================================================
# Three scenarios per archetype (conservative / base / upside). Numbers are
# illustrative and intended for storytelling, not financial modelling.

# Channel labels for the value-stack (in display order, bottom to top)
VALUE_STACK_ORDER = [
    "bill", "grid_fee", "da", "id", "afrr", "fcr", "local", "brp",
]

# Who captures the value (used for color-coding / narrative)
VALUE_CAPTURE = {
    "bill":     {"who": "Customer",   "color": PALETTE["teal"]},
    "grid_fee": {"who": "Customer",   "color": PALETTE["cyan"]},
    "da":       {"who": "Supplier",   "color": PALETTE["blue"]},
    "id":       {"who": "Supplier",   "color": PALETTE["purple"]},
    "afrr":     {"who": "Aggregator", "color": PALETTE["amber"]},
    "fcr":      {"who": "Aggregator", "color": PALETTE["gold"]},
    "local":    {"who": "Aggregator", "color": PALETTE["red"]},
    "brp":      {"who": "Supplier",   "color": PALETTE["green"]},
}

ARCHETYPES: dict[str, dict] = {
    "ev_only": {
        "name": "EV-only household",
        "asset_id": "ev_1way",
        "icon": "▮",
        "flex": "5–15 kWh per overnight charge; 7–11 kW shiftable load",
        "strongest": ["bill", "grid_fee"],
        "weakest":   ["fcr", "afrr", "id"],
        "proposition": (
            "Cheap night charging + ~€150/year grid-fee discount + simple "
            "smart-charge app. Clean entry product for EV owners."
        ),
        "why_matters": (
            "Largest near-term volume play. EV penetration is the supply-side "
            "tailwind for retail flex through 2030."
        ),
        "stack": {
            "conservative": {"bill": 150, "grid_fee": 110, "da": 0,   "id": 0, "afrr": 0,  "fcr": 0, "local": 0, "brp": 20},
            "base":         {"bill": 220, "grid_fee": 150, "da": 30,  "id": 0, "afrr": 0,  "fcr": 0, "local": 0, "brp": 35},
            "upside":       {"bill": 320, "grid_fee": 190, "da": 60,  "id": 0, "afrr": 30, "fcr": 0, "local": 0, "brp": 50},
        },
    },
    "pv_battery": {
        "name": "PV + battery household",
        "asset_id": "pv_battery",
        "icon": "☀+▦",
        "flex": "Self-consumption optimization + 5–10 kWh storage arbitrage",
        "strongest": ["bill", "da", "grid_fee", "brp"],
        "weakest":   ["fcr"],
        "proposition": (
            "Maximize your PV value + dynamic-tariff arbitrage + grid discount, "
            "all in one app. The headline retail-flex bundle."
        ),
        "why_matters": (
            "Highest annual value density per home. Lead segment for the "
            "go-to-market — easiest control, cleanest story."
        ),
        "stack": {
            "conservative": {"bill": 200, "grid_fee": 110, "da": 50,  "id": 0,   "afrr": 0,   "fcr": 0,  "local": 0,  "brp": 30},
            "base":         {"bill": 350, "grid_fee": 150, "da": 100, "id": 30,  "afrr": 50,  "fcr": 30, "local": 10, "brp": 50},
            "upside":       {"bill": 500, "grid_fee": 190, "da": 150, "id": 70,  "afrr": 120, "fcr": 60, "local": 25, "brp": 80},
        },
    },
    "hp_pv": {
        "name": "Heat pump + PV household",
        "asset_id": "hp",
        "icon": "◐+☀",
        "flex": "Thermal time-shift (1–4 h) + PV self-consumption pairing",
        "strongest": ["grid_fee", "bill", "da"],
        "weakest":   ["fcr", "id"],
        "proposition": (
            "Smart heating that shifts to cheap hours + lower grid fees + "
            "free heat from your PV. Modernization-tailwind segment."
        ),
        "why_matters": (
            "Heating-modernization volume opportunity. §14a is a structural "
            "tailwind regardless of market conditions."
        ),
        "stack": {
            "conservative": {"bill": 100, "grid_fee": 110, "da": 30,  "id": 0, "afrr": 0,  "fcr": 0, "local": 0,  "brp": 20},
            "base":         {"bill": 175, "grid_fee": 150, "da": 55,  "id": 0, "afrr": 0,  "fcr": 0, "local": 5,  "brp": 35},
            "upside":       {"bill": 250, "grid_fee": 190, "da": 80,  "id": 0, "afrr": 20, "fcr": 0, "local": 15, "brp": 60},
        },
    },
    "full_stack": {
        "name": "EV + PV + battery (full stack)",
        "asset_id": "ev_pv_battery",
        "icon": "▮+☀+▦",
        "flex": "Full-stack flexibility across all timescales",
        "strongest": ["bill", "da", "grid_fee", "brp"],
        "weakest":   [],
        "proposition": (
            "Energy autonomy + dynamic optimization + ancillary upside — "
            "your home as a power plant. Lighthouse segment proposition."
        ),
        "why_matters": (
            "Smaller addressable base today but the highest revenue density "
            "and the lighthouse for premium products."
        ),
        "stack": {
            "conservative": {"bill": 400, "grid_fee": 110, "da": 100, "id": 0,   "afrr": 50,  "fcr": 0,   "local": 0,  "brp": 50},
            "base":         {"bill": 600, "grid_fee": 150, "da": 175, "id": 50,  "afrr": 100, "fcr": 30,  "local": 15, "brp": 80},
            "upside":       {"bill": 800, "grid_fee": 190, "da": 250, "id": 100, "afrr": 150, "fcr": 60,  "local": 35, "brp": 120},
        },
    },
}


# =============================================================================
# 7. DATA — GO-TO-MARKET WAVES
# =============================================================================

WAVES: list[dict] = [
    {
        "wave": 1,
        "name": "Capture customer-facing value",
        "timing": "Now — 12 months",
        "channels": ["bill", "grid_fee"],
        "assets":   ["pv_battery", "ev_pv_battery", "hp", "ev_pv"],
        "why": (
            "Customer-facing, regulator-supported, low operational complexity. "
            "Bankable margin from day one. Anchor the customer story before "
            "anything else."
        ),
        "capabilities": [
            "Dynamic tariff product",
            "PV self-consumption analytics",
            "§14a Modul 1/2 enrolment",
            "Smart-meter integration where available",
        ],
        "why_not_earlier": "It already starts now.",
        "why_not_later":   "Channel is already moving — late entrants face thinner margins and switching headwinds.",
    },
    {
        "wave": 2,
        "name": "Layer wholesale optimization",
        "timing": "12–24 months",
        "channels": ["da", "brp"],
        "assets":   ["battery", "pv_battery", "ev_battery", "ev_pv_battery"],
        "why": (
            "Day-ahead first, intraday for batteries. High scalability per unit "
            "of platform investment. Portfolio value should be captured in "
            "parallel — it's often the larger of the two."
        ),
        "capabilities": [
            "BRP integration / balance-group setup",
            "Forecasting and optimization engine",
            "Trading desk linkage",
            "Internal value attribution to procurement P&L",
        ],
        "why_not_earlier": "Without a customer base and asset pool, wholesale capture is sub-scale.",
        "why_not_later":   "Spreads compress as more flex enters; movers capture the curve.",
    },
    {
        "wave": 3,
        "name": "Selective balancing services",
        "timing": "24–36 months",
        "channels": ["afrr", "fcr"],
        "assets":   ["battery", "pv_battery", "ev_v2g"],
        "why": (
            "Only with home batteries (and later V2G), only at sufficient pool "
            "scale, only with proper aggregation infrastructure. FCR is "
            "crowded; aFRR has more room."
        ),
        "capabilities": [
            "Pre-qualification with TSO",
            "1 MW+ aggregated pool",
            "Telemetry and SLA-grade control",
            "Aggregator partnership or own stack",
        ],
        "why_not_earlier": "Pool size, telemetry, and pre-qualification are gating; FCR prices have already compressed.",
        "why_not_later":   "V2G fleet penetration unlocks an additional supply layer mid-cycle.",
    },
    {
        "wave": 4,
        "name": "Local flex + V2G optionality",
        "timing": "36 months+",
        "channels": ["local"],
        "assets":   ["ev_v2g", "ev_pv_battery"],
        "why": (
            "Watch local flex markets — location-specific pilots only. Position "
            "for V2G via OEM partnerships and standards work. Real revenue "
            "from V2G unlocks ~2027+."
        ),
        "capabilities": [
            "DSO partnerships and local-tender capability",
            "ISO 15118-20 readiness and V2G hardware roadmap",
            "Bidirectional commercial models",
            "Strategic OEM relationships",
        ],
        "why_not_earlier": "Markets aren't deep enough; V2G hardware penetration <5 % in 2026.",
        "why_not_later":   "Optionality investment now de-risks the post-2027 revenue pool.",
    },
]


# =============================================================================
# 8. PLOTLY DEFAULT THEME
# =============================================================================

def base_layout(**kwargs) -> dict:
    """Default Plotly layout for the dark theme."""
    layout = dict(
        paper_bgcolor=PALETTE["bg"],
        plot_bgcolor=PALETTE["bg"],
        font=dict(
            family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            color=PALETTE["text_primary"],
            size=12,
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            gridcolor=PALETTE["border"],
            zerolinecolor=PALETTE["border"],
            color=PALETTE["text_secondary"],
        ),
        yaxis=dict(
            gridcolor=PALETTE["border"],
            zerolinecolor=PALETTE["border"],
            color=PALETTE["text_secondary"],
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=PALETTE["border"],
            font=dict(color=PALETTE["text_secondary"], size=11),
        ),
    )
    layout.update(kwargs)
    return layout


# =============================================================================
# 9. HELPER FUNCTIONS
# =============================================================================

SCORE_LABELS = {4: "VH", 3: "H", 2: "M", 1: "L", 0: "—"}
SCORE_FULL   = {4: "Very high", 3: "High", 2: "Medium", 1: "Low", 0: "Not applicable"}
SCORE_CSS    = {4: "vh", 3: "h", 2: "m", 1: "l", 0: "na"}
SCORE_COLOR  = {
    4: PALETTE["score_vh"],
    3: PALETTE["score_h"],
    2: PALETTE["score_m"],
    1: PALETTE["score_l"],
    0: PALETTE["score_na"],
}


def badge(score: int) -> str:
    """Return an HTML badge for a score."""
    return f'<span class="badge badge-{SCORE_CSS[score]}">{SCORE_LABELS[score]}</span>'


def tag(text: str, kind: str = "") -> str:
    """Return an HTML tag pill."""
    cls = f"tag tag-{kind}" if kind else "tag"
    return f'<span class="{cls}">{text}</span>'


def metric_card(label: str, value: str, sub: str = "") -> str:
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-sub">{sub}</div>
    </div>
    """


def insight_box(text: str, label: str = "Insight") -> str:
    return f"""
    <div class="insight">
      <span class="insight-label">{label}</span>
      {text}
    </div>
    """


def score_bar(label: str, score: int, max_score: int = 5) -> str:
    pct = int(round(score / max_score * 100))
    return f"""
    <div class="score-row">
      <div class="score-label">{label}</div>
      <div class="score-bar-bg"><div class="score-bar-fill" style="width:{pct}%"></div></div>
      <div class="score-num">{score}/{max_score}</div>
    </div>
    """


def channel_chip(channel_id: str, kind: str = "") -> str:
    """Return a tag for a channel by id."""
    return tag(CHANNELS[channel_id]["short"], kind=kind)


def headline(text: str) -> str:
    return f'<div class="headline-strip">{text}</div>'


# =============================================================================
# 10. PAGE: 1. EXECUTIVE OVERVIEW
# =============================================================================

def render_overview() -> None:
    st.markdown("# Retail flexibility — strategy cockpit")
    st.markdown(
        '<div class="subtitle">Where the value lies in monetizing flexibility '
        'from EVs, rooftop PV, home batteries, and heat pumps in German / '
        'European retail energy markets.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        headline(
            "There is no single flexibility market. Seven distinct value pools "
            "exist — and the bankable proposition is built by stacking three "
            "or four of them on the same hardware."
        ),
        unsafe_allow_html=True,
    )

    # Top metric row -----------------------------------------------------------
    cols = st.columns(4)
    with cols[0]:
        st.markdown(
            metric_card("Monetization channels", "7", "Bill · DA · ID · §14a · aFRR · FCR · Local · BRP"),
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            metric_card("Most scalable", "Bill · §14a · BRP", "Accessible across almost all asset classes"),
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            metric_card("Hardest today", "FCR · Local", "Crowded / nascent · pool & telemetry gating"),
            unsafe_allow_html=True,
        )
    with cols[3]:
        st.markdown(
            metric_card("Strongest bundle", "PV + battery", "Highest value density per home"),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Three-column key messages ------------------------------------------------
    st.markdown("## Three messages to anchor the conversation")

    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
            <div class="card card-emph">
              <div class="metric-label">Message 01</div>
              <h3 style="margin-top:0.4rem;">Stacking, not chasing</h3>
              <p style="color:{PALETTE['text_secondary']}; font-size:0.92rem;">
              The bankable proposition is rarely from one channel. It comes
              from layering bill optimization, §14a, wholesale, and (selectively)
              balancing on the same hardware.
              </p>
            </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
            <div class="card card-emph">
              <div class="metric-label">Message 02</div>
              <h3 style="margin-top:0.4rem;">Lead with PV + battery</h3>
              <p style="color:{PALETTE['text_secondary']}; font-size:0.92rem;">
              Highest value density, cleanest customer story, regulatory
              tailwind via §14a. Layer heat pumps next, then EVs at volume,
              then position for V2G.
              </p>
            </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
            <div class="card card-emph">
              <div class="metric-label">Message 03</div>
              <h3 style="margin-top:0.4rem;">BRP value is underrated</h3>
              <p style="color:{PALETTE['text_secondary']}; font-size:0.92rem;">
              For vertically integrated suppliers, portfolio / BRP value is
              often the largest internal P&L lever — and the one most
              consistently overlooked in flex business cases.
              </p>
            </div>
        """, unsafe_allow_html=True)

    # Big-picture summary chart ------------------------------------------------
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## The framework at a glance")

    # Build a compact summary heatmap
    z = []
    text = []
    for asset_id in ASSET_ORDER:
        row, row_t = [], []
        for ch_id in CHANNEL_ORDER:
            f = FIT_MATRIX[(asset_id, ch_id)]
            row.append(f["score"])
            row_t.append(SCORE_LABELS[f["score"]])
        z.append(row)
        text.append(row_t)

    fig = go.Figure(go.Heatmap(
        z=z,
        text=text,
        texttemplate="%{text}",
        textfont=dict(size=11, color=PALETTE["text_primary"]),
        x=[CHANNELS[c]["short"] for c in CHANNEL_ORDER],
        y=[ASSETS[a]["short"] for a in ASSET_ORDER],
        colorscale=[
            [0.00, PALETTE["score_na"]],
            [0.249, PALETTE["score_na"]],
            [0.25, PALETTE["score_l"]],
            [0.499, PALETTE["score_l"]],
            [0.50, PALETTE["score_m"]],
            [0.749, PALETTE["score_m"]],
            [0.75, PALETTE["score_h"]],
            [0.99, PALETTE["score_h"]],
            [1.0, PALETTE["score_vh"]],
        ],
        zmin=0, zmax=4,
        showscale=False,
        xgap=3, ygap=3,
        hovertemplate="<b>%{y}</b><br>Channel: %{x}<br>Suitability: %{text}<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        height=360,
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(side="top", color=PALETTE["text_secondary"], tickfont=dict(size=11)),
        yaxis=dict(autorange="reversed", color=PALETTE["text_secondary"], tickfont=dict(size=11)),
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        insight_box(
            "Read the matrix as: <strong>bill optimization, §14a, and BRP value</strong> "
            "are broadly accessible across asset classes. <strong>Wholesale</strong> "
            "is reliably high only for batteries. <strong>Balancing</strong> is "
            "honest medium at best for retail. <strong>Local / DSO</strong> is "
            "promising but not yet bankable.",
            label="How to read this",
        ),
        unsafe_allow_html=True,
    )


# =============================================================================
# 11. PAGE: 2. ASSET FLEXIBILITY EXPLORER
# =============================================================================

def render_assets() -> None:
    st.markdown("# Asset flexibility explorer")
    st.markdown(
        '<div class="subtitle">What kind of flexibility each retail asset '
        'actually offers — and where its limits sit.</div>',
        unsafe_allow_html=True,
    )

    # Asset selector
    asset_id = st.selectbox(
        "Select asset",
        options=ASSET_ORDER,
        format_func=lambda a: f"{ASSETS[a]['marker']}  {ASSETS[a]['name']} — {ASSETS[a]['tagline']}",
        key="asset_explorer_select",
    )
    asset = ASSETS[asset_id]

    st.markdown(headline(asset["summary"]), unsafe_allow_html=True)

    # Two-column layout: capability radar + details
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.markdown("### Capability profile")

        # Radar chart for capabilities
        labels = ["Controllability", "Response speed", "Predictability", "Availability", "Cycle freedom"]
        values = [
            asset["scores"]["controllability"],
            asset["scores"]["response_speed"],
            asset["scores"]["predictability"],
            asset["scores"]["availability"],
            asset["scores"]["cycle_freedom"],
        ]
        # close the loop
        values_loop = values + [values[0]]
        labels_loop = labels + [labels[0]]

        fig = go.Figure(go.Scatterpolar(
            r=values_loop,
            theta=labels_loop,
            fill="toself",
            line=dict(color=PALETTE["teal"], width=2),
            fillcolor="rgba(45, 212, 191, 0.18)",
            hovertemplate="%{theta}: %{r}/5<extra></extra>",
        ))
        fig.update_layout(**base_layout(
            height=340,
            polar=dict(
                bgcolor=PALETTE["bg"],
                radialaxis=dict(
                    range=[0, 5],
                    showline=False,
                    gridcolor=PALETTE["border"],
                    tickfont=dict(color=PALETTE["text_tertiary"], size=10),
                ),
                angularaxis=dict(
                    gridcolor=PALETTE["border"],
                    tickfont=dict(color=PALETTE["text_secondary"], size=11),
                ),
            ),
            showlegend=False,
            margin=dict(l=60, r=60, t=20, b=20),
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Quick facts
        st.markdown(f"""
            <div class="card">
              <div class="metric-label">Quick facts</div>
              <div style="margin-top:0.6rem;">
                <div style="margin:0.3rem 0;"><span style="color:{PALETTE['text_tertiary']}; font-size:0.78rem;">Flex type</span><br><strong>{asset['flex_type']}</strong></div>
                <div style="margin:0.3rem 0;"><span style="color:{PALETTE['text_tertiary']}; font-size:0.78rem;">Power</span><br><strong>{asset['power_kw']} kW</strong></div>
                <div style="margin:0.3rem 0;"><span style="color:{PALETTE['text_tertiary']}; font-size:0.78rem;">Energy</span><br><strong>{asset['energy_kwh']}</strong></div>
              </div>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        # Strengths
        st.markdown("### Strengths")
        for s in asset["strengths"]:
            st.markdown(f"<div style='padding:0.3rem 0; color:{PALETTE['text_primary']};'>"
                        f"<span style='color:{PALETTE['teal']}; margin-right:8px;'>▸</span>{s}</div>",
                        unsafe_allow_html=True)

        # Limits
        st.markdown("### Limits")
        for l in asset["limits"]:
            st.markdown(f"<div style='padding:0.3rem 0; color:{PALETTE['text_primary']};'>"
                        f"<span style='color:{PALETTE['amber']}; margin-right:8px;'>▸</span>{l}</div>",
                        unsafe_allow_html=True)

        # Best / weak channels
        st.markdown("### Channel fit")
        best_html = " ".join(channel_chip(c, kind="strong") for c in asset["best"])
        weak_html = " ".join(channel_chip(c, kind="warn") for c in asset["weak"]) if asset["weak"] else "<span style='color:#6B7280; font-size:0.85rem;'>none material</span>"
        st.markdown(f"<div style='margin:0.3rem 0;'><span style='color:{PALETTE['text_tertiary']}; font-size:0.78rem;'>STRONG FIT</span><br>{best_html}</div>",
                    unsafe_allow_html=True)
        st.markdown(f"<div style='margin:0.3rem 0;'><span style='color:{PALETTE['text_tertiary']}; font-size:0.78rem;'>WEAK FIT</span><br>{weak_html}</div>",
                    unsafe_allow_html=True)

    # Channel suitability detail strip
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Suitability across all monetization channels")

    cols = st.columns(len(CHANNEL_ORDER))
    for i, ch_id in enumerate(CHANNEL_ORDER):
        f = FIT_MATRIX[(asset_id, ch_id)]
        score = f["score"]
        ch = CHANNELS[ch_id]
        with cols[i]:
            st.markdown(f"""
                <div style="background:{PALETTE['panel']}; border:1px solid {PALETTE['border']}; border-top:3px solid {SCORE_COLOR[score]}; border-radius:8px; padding:0.7rem 0.6rem; text-align:center; height:100%;">
                  <div style="color:{PALETTE['text_tertiary']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.06em;">{ch['short']}</div>
                  <div style="color:{SCORE_COLOR[score]}; font-size:1.05rem; font-weight:600; margin-top:0.4rem;">{SCORE_LABELS[score]}</div>
                  <div style="color:{PALETTE['text_secondary']}; font-size:0.72rem; margin-top:0.3rem;">{SCORE_FULL[score]}</div>
                </div>
            """, unsafe_allow_html=True)


# =============================================================================
# 12. PAGE: 3. MONETIZATION CHANNELS EXPLORER
# =============================================================================

def render_channels() -> None:
    st.markdown("# Monetization channels explorer")
    st.markdown(
        '<div class="subtitle">Seven value pools — different counterparties, '
        'price levels, access costs, and operational realities.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        headline(
            "Not all channels are equally bankable. The most accessible ones "
            "(bill, §14a, BRP) often have the best risk-adjusted return; the "
            "most lucrative-sounding ones (FCR, aFRR) carry the highest "
            "operational overhead."
        ),
        unsafe_allow_html=True,
    )

    # Channel selector
    ch_id = st.selectbox(
        "Select channel",
        options=CHANNEL_ORDER,
        format_func=lambda c: f"{CHANNELS[c]['icon']}  {CHANNELS[c]['name']}",
        key="channel_explorer_select",
    )
    channel = CHANNELS[ch_id]

    # Realism color bar
    realism_color = {
        "easy_real":  PALETTE["green"],
        "real_hard":  PALETTE["amber"],
        "emerging":   PALETTE["red"],
    }[channel["realism"]]
    realism_label = {
        "easy_real":  "Easy and real today",
        "real_hard":  "Real but operationally hard",
        "emerging":   "Emerging / selective",
    }[channel["realism"]]

    st.markdown(f"""
        <div class="card" style="border-left:3px solid {realism_color};">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
            <h3 style="margin:0;">{channel['name']}</h3>
            <span style="background:{realism_color}22; color:{realism_color}; padding:0.25rem 0.75rem; border-radius:4px; font-size:0.78rem; font-weight:600;">{realism_label}</span>
          </div>
          <p style="color:{PALETTE['text_primary']}; margin:0.5rem 0; line-height:1.65;">{channel['what']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Two-column: scores and details
    col_left, col_right = st.columns([1, 1.15])

    with col_left:
        st.markdown("### Channel scorecard")
        st.markdown(score_bar("Value potential",        channel["scores"]["value_potential"]), unsafe_allow_html=True)
        st.markdown(score_bar("Ease of access",         channel["scores"]["ease_of_access"]), unsafe_allow_html=True)
        st.markdown(score_bar("Operational complexity", channel["scores"]["operational_complexity"]), unsafe_allow_html=True)
        st.markdown(score_bar("Scalability",            channel["scores"]["scalability"]), unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card" style="margin-top:1rem;">
              <div class="metric-label">Maturity</div>
              <div style="font-weight:500; margin-top:0.4rem;">{channel['maturity']}</div>
              <div class="metric-label" style="margin-top:0.9rem;">Value captured by</div>
              <div style="font-weight:500; margin-top:0.4rem;">{channel['captured_by']}</div>
              <div class="metric-label" style="margin-top:0.9rem;">Mechanism</div>
              <div style="color:{PALETTE['text_secondary']}; font-size:0.9rem; margin-top:0.4rem;">{channel['mechanism']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### Best-fit assets")
        best_html = " ".join(
            f'<span class="tag tag-strong">{ASSETS[a]["short"]}</span>'
            for a in channel["best_assets"]
        )
        st.markdown(f"<div style='margin:0.3rem 0 1rem 0;'>{best_html}</div>", unsafe_allow_html=True)

        st.markdown("### Key constraints")
        for c in channel["constraints"]:
            st.markdown(f"<div style='padding:0.35rem 0; color:{PALETTE['text_primary']};'>"
                        f"<span style='color:{PALETTE['amber']}; margin-right:8px;'>▸</span>{c}</div>",
                        unsafe_allow_html=True)

    # Compare-all-channels strip
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### How this channel compares to the other six")

    fig = go.Figure()
    for metric in ["value_potential", "ease_of_access", "operational_complexity", "scalability"]:
        labels = {
            "value_potential":         "Value potential",
            "ease_of_access":          "Ease of access",
            "operational_complexity":  "Op. complexity",
            "scalability":             "Scalability",
        }
        colors = {
            "value_potential":         PALETTE["teal"],
            "ease_of_access":          PALETTE["green"],
            "operational_complexity":  PALETTE["amber"],
            "scalability":             PALETTE["blue"],
        }
        fig.add_trace(go.Bar(
            x=[CHANNELS[c]["short"] for c in CHANNEL_ORDER],
            y=[CHANNELS[c]["scores"][metric] for c in CHANNEL_ORDER],
            name=labels[metric],
            marker=dict(color=colors[metric]),
            hovertemplate="%{y}/5<extra></extra>",
        ))
    fig.update_layout(**base_layout(
        height=320,
        barmode="group",
        bargap=0.25,
        yaxis=dict(range=[0, 5.3], title="", color=PALETTE["text_secondary"], gridcolor=PALETTE["border"]),
        xaxis=dict(title="", color=PALETTE["text_secondary"]),
        legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)", bordercolor=PALETTE["border"], font=dict(color=PALETTE["text_secondary"])),
        margin=dict(l=20, r=20, t=60, b=40),
    ))
    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# 13. PAGE: 4. ASSET-TO-MARKET FIT HEATMAP (CENTERPIECE)
# =============================================================================

def render_heatmap() -> None:
    st.markdown("# Asset-to-market fit")
    st.markdown(
        '<div class="subtitle">The centerpiece view. Which assets fit which '
        'monetization channels — and why.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        headline(
            "Hover any cell for the rationale. Use the selectors below to "
            "drill into the commercial logic and bankability assessment."
        ),
        unsafe_allow_html=True,
    )

    # Build heatmap data with rich hovertext
    z = []
    hover = []
    text = []
    for asset_id in ASSET_ORDER:
        row_z, row_h, row_t = [], [], []
        for ch_id in CHANNEL_ORDER:
            f = FIT_MATRIX[(asset_id, ch_id)]
            row_z.append(f["score"])
            row_t.append(SCORE_LABELS[f["score"]])
            bankable_str = "Bankable today" if f["bankable"] else "Theoretical only"
            row_h.append(
                f"<b>{ASSETS[asset_id]['name']}</b> × <b>{CHANNELS[ch_id]['name']}</b><br>"
                f"<span style='color:#9CA3AF'>Suitability: <b>{SCORE_FULL[f['score']]}</b> ({bankable_str})</span><br><br>"
                f"{f['rationale']}"
            )
        z.append(row_z)
        hover.append(row_h)
        text.append(row_t)

    fig = go.Figure(go.Heatmap(
        z=z,
        text=text,
        customdata=hover,
        texttemplate="%{text}",
        textfont=dict(size=12, color=PALETTE["text_primary"], family="-apple-system, sans-serif"),
        x=[CHANNELS[c]["short"] for c in CHANNEL_ORDER],
        y=[ASSETS[a]["short"] for a in ASSET_ORDER],
        colorscale=[
            [0.00, PALETTE["score_na"]],
            [0.249, PALETTE["score_na"]],
            [0.25, PALETTE["score_l"]],
            [0.499, PALETTE["score_l"]],
            [0.50, PALETTE["score_m"]],
            [0.749, PALETTE["score_m"]],
            [0.75, PALETTE["score_h"]],
            [0.99, PALETTE["score_h"]],
            [1.0, PALETTE["score_vh"]],
        ],
        zmin=0, zmax=4,
        showscale=False,
        xgap=4, ygap=4,
        hovertemplate="%{customdata}<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        height=520,
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(side="top", color=PALETTE["text_secondary"], tickfont=dict(size=12)),
        yaxis=dict(autorange="reversed", color=PALETTE["text_secondary"], tickfont=dict(size=12)),
        hoverlabel=dict(
            bgcolor=PALETTE["panel_2"],
            bordercolor=PALETTE["border_strong"],
            font=dict(color=PALETTE["text_primary"], size=12, family="-apple-system, sans-serif"),
            align="left",
        ),
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Legend strip
    legend_items = [
        ("Very high", PALETTE["score_vh"]),
        ("High",      PALETTE["score_h"]),
        ("Medium",    PALETTE["score_m"]),
        ("Low",       PALETTE["score_l"]),
        ("Not appl.", PALETTE["score_na"]),
    ]
    legend_html = '<div style="display:flex; gap:18px; align-items:center; margin:0.4rem 0 1.5rem 0; font-size:0.85rem; color:#9CA3AF;">'
    for label, color in legend_items:
        legend_html += (
            f'<span style="display:inline-flex; align-items:center; gap:6px;">'
            f'<span style="display:inline-block; width:18px; height:14px; background:{color}; border-radius:3px;"></span>{label}</span>'
        )
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    # Drill-down panel ---------------------------------------------------------
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Cell drill-down")
    st.markdown(
        f'<div style="color:{PALETTE["text_secondary"]}; font-size:0.9rem; margin-bottom:0.8rem;">'
        f'Pick any asset × channel combination to see the full commercial logic.</div>',
        unsafe_allow_html=True,
    )

    sel_cols = st.columns(2)
    with sel_cols[0]:
        d_asset = st.selectbox(
            "Asset",
            options=ASSET_ORDER,
            format_func=lambda a: ASSETS[a]["name"],
            key="drill_asset",
        )
    with sel_cols[1]:
        d_channel = st.selectbox(
            "Channel",
            options=CHANNEL_ORDER,
            format_func=lambda c: CHANNELS[c]["name"],
            key="drill_channel",
        )

    f = FIT_MATRIX[(d_asset, d_channel)]
    score = f["score"]
    bankable_label = "Bankable today" if f["bankable"] else "Theoretical only"
    bankable_color = PALETTE["green"] if f["bankable"] else PALETTE["amber"]

    st.markdown(f"""
        <div class="card" style="border-left:4px solid {SCORE_COLOR[score]};">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <h3 style="margin:0;">{ASSETS[d_asset]['name']} × {CHANNELS[d_channel]['name']}</h3>
            <div>
              <span class="badge badge-{SCORE_CSS[score]}">{SCORE_LABELS[score]} · {SCORE_FULL[score]}</span>
              <span style="background:{bankable_color}22; color:{bankable_color}; padding:0.22rem 0.6rem; border-radius:4px; font-size:0.72rem; font-weight:600; margin-left:6px;">{bankable_label}</span>
            </div>
          </div>
          <p style="color:{PALETTE['text_primary']}; line-height:1.7; margin:0.6rem 0;">{f['rationale']}</p>

          <div class="section-divider" style="margin:1rem 0;"></div>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.2rem;">
            <div>
              <div class="metric-label">Channel mechanism</div>
              <p style="color:{PALETTE['text_secondary']}; font-size:0.88rem; margin-top:0.4rem;">{CHANNELS[d_channel]['mechanism']}</p>
            </div>
            <div>
              <div class="metric-label">Value captured by</div>
              <p style="color:{PALETTE['text_secondary']}; font-size:0.88rem; margin-top:0.4rem;">{CHANNELS[d_channel]['captured_by']}</p>
            </div>
          </div>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# 14. PAGE: 5. VALUE STACK SIMULATOR
# =============================================================================

def render_value_stack() -> None:
    st.markdown("# Value stack simulator")
    st.markdown(
        '<div class="subtitle">Illustrative annual value, layer by layer, '
        'for representative customer archetypes.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        headline(
            "Single-channel monetization is rarely enough. The real proposition "
            "stacks bill optimization, §14a, wholesale, and (selectively) "
            "balancing on the same hardware. This simulator shows that visually."
        ),
        unsafe_allow_html=True,
    )

    # Controls
    col_a, col_b = st.columns([2, 1])
    with col_a:
        archetype_id = st.selectbox(
            "Customer archetype",
            options=list(ARCHETYPES.keys()),
            format_func=lambda a: f"{ARCHETYPES[a]['icon']}  {ARCHETYPES[a]['name']}",
            key="vs_archetype",
        )
    with col_b:
        st.markdown(
            f'<div style="color:{PALETTE["text_tertiary"]}; font-size:0.78rem; margin-top:1.7rem;">'
            f'Numbers are <strong>illustrative</strong> — for narrative, not financial modelling.</div>',
            unsafe_allow_html=True,
        )

    archetype = ARCHETYPES[archetype_id]

    # Stacked bar across three scenarios ---------------------------------------
    scenarios = ["conservative", "base", "upside"]
    scenario_labels = ["Conservative", "Base", "Upside"]

    fig = go.Figure()
    for ch_id in VALUE_STACK_ORDER:
        values = [archetype["stack"][s].get(ch_id, 0) for s in scenarios]
        if sum(values) == 0:
            continue
        fig.add_trace(go.Bar(
            x=scenario_labels,
            y=values,
            name=CHANNELS[ch_id]["short"],
            marker=dict(color=VALUE_CAPTURE[ch_id]["color"]),
            hovertemplate=(
                f"<b>{CHANNELS[ch_id]['name']}</b><br>"
                f"Captured by: {VALUE_CAPTURE[ch_id]['who']}<br>"
                f"€%{{y}}/yr<extra></extra>"
            ),
        ))
    totals = [sum(archetype["stack"][s].values()) for s in scenarios]
    fig.add_trace(go.Scatter(
        x=scenario_labels,
        y=[t + max(totals) * 0.04 for t in totals],
        text=[f"€{t}" for t in totals],
        mode="text",
        textfont=dict(color=PALETTE["text_primary"], size=14, family="-apple-system, sans-serif"),
        showlegend=False,
        hoverinfo="skip",
    ))
    fig.update_layout(**base_layout(
        height=440,
        barmode="stack",
        bargap=0.35,
        yaxis=dict(title="€ / year", color=PALETTE["text_secondary"], gridcolor=PALETTE["border"]),
        xaxis=dict(color=PALETTE["text_secondary"]),
        legend=dict(orientation="h", y=-0.18, x=0, bgcolor="rgba(0,0,0,0)", font=dict(color=PALETTE["text_secondary"])),
        margin=dict(l=20, r=20, t=20, b=80),
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Who captures what (split by capturer)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Who captures the value")

    base_stack = archetype["stack"]["base"]
    by_capturer = {"Customer": 0, "Supplier": 0, "Aggregator": 0}
    for ch_id, val in base_stack.items():
        who = VALUE_CAPTURE[ch_id]["who"]
        by_capturer[who] = by_capturer.get(who, 0) + val
    total_base = sum(by_capturer.values())

    cols = st.columns(3)
    capturer_colors = {
        "Customer":   PALETTE["teal"],
        "Supplier":   PALETTE["blue"],
        "Aggregator": PALETTE["amber"],
    }
    for i, (who, val) in enumerate(by_capturer.items()):
        pct = int(round(val / total_base * 100)) if total_base else 0
        with cols[i]:
            st.markdown(f"""
                <div class="metric-card" style="border-top:3px solid {capturer_colors[who]};">
                  <div class="metric-label">{who} (base)</div>
                  <div class="metric-value">€{val}</div>
                  <div class="metric-sub">{pct}% of stack</div>
                </div>
            """, unsafe_allow_html=True)

    # Proposition + commercial relevance
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"""
            <div class="card card-emph">
              <div class="metric-label">Proposition</div>
              <p style="font-size:1.0rem; line-height:1.65; color:{PALETTE['text_primary']}; margin-top:0.5rem;">
              "{archetype['proposition']}"
              </p>
            </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
            <div class="card">
              <div class="metric-label">Why this archetype matters</div>
              <p style="color:{PALETTE['text_secondary']}; line-height:1.65; margin-top:0.5rem;">
              {archetype['why_matters']}
              </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(
        insight_box(
            "<strong>The stacking effect:</strong> in the base scenario, removing "
            "any single channel leaves a meaningful but rarely sufficient "
            f"proposition. The total <strong>€{sum(base_stack.values())}/yr</strong> "
            "across channels is what justifies the operational stack — telemetry, "
            "BRP setup, customer ops, aggregator partnerships.",
            label="Why stacking matters",
        ),
        unsafe_allow_html=True,
    )


# =============================================================================
# 15. PAGE: 6. EASY-VS-HARD 2x2
# =============================================================================

def render_2x2() -> None:
    st.markdown("# Easy vs hard to monetize")
    st.markdown(
        '<div class="subtitle">Strategic prioritization of the seven '
        'monetization channels. Bubble size = relative addressable pool.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        headline(
            "Upper-right is where to lead — high value, easy access. Upper-left "
            "is where to invest selectively — high value, but operationally "
            "demanding. Lower-left needs patience, not capital."
        ),
        unsafe_allow_html=True,
    )

    # Compute axis values:
    #   x = ease (5 - operational_complexity adjusted by ease_of_access)
    #   y = value potential
    #   size = relative addressable pool (proxy)
    # Pool size proxy by maturity / scalability:
    pool_proxy = {
        "bill":     50, "da":   38, "id":  18, "grid_fee": 45,
        "afrr":     22, "fcr":  16, "local": 8, "brp":     42,
    }
    maturity_color = {
        "easy_real":  PALETTE["green"],
        "real_hard":  PALETTE["amber"],
        "emerging":   PALETTE["red"],
    }

    fig = go.Figure()
    for ch_id, ch in CHANNELS.items():
        # Ease score: higher ease_of_access, lower complexity = easier
        ease = (ch["scores"]["ease_of_access"] + (6 - ch["scores"]["operational_complexity"])) / 2
        value = ch["scores"]["value_potential"]
        fig.add_trace(go.Scatter(
            x=[ease],
            y=[value],
            mode="markers+text",
            marker=dict(
                size=pool_proxy[ch_id],
                color=maturity_color[ch["realism"]],
                opacity=0.78,
                line=dict(color=PALETTE["bg"], width=2),
            ),
            text=[ch["short"]],
            textposition="middle center",
            textfont=dict(color="#0B0F14", size=11, family="-apple-system, sans-serif", weight=700),
            name=ch["short"],
            customdata=[[ch["name"], ch["maturity"], ch["captured_by"]]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "<span style='color:#9CA3AF'>Value potential: %{y}/5 · Ease: %{x:.1f}/5</span><br>"
                "Maturity: %{customdata[1]}<br>"
                "Captured by: %{customdata[2]}<extra></extra>"
            ),
            showlegend=False,
        ))

    # Quadrant lines + labels
    fig.add_shape(type="line", x0=3, y0=0, x1=3, y1=5.5,
                  line=dict(color=PALETTE["border"], width=1, dash="dot"))
    fig.add_shape(type="line", x0=0, y0=3, x1=5.5, y1=3,
                  line=dict(color=PALETTE["border"], width=1, dash="dot"))

    quadrant_labels = [
        (4.5, 5.2, "LEAD",            PALETTE["teal"]),
        (1.5, 5.2, "INVEST SELECTIVELY", PALETTE["amber"]),
        (4.5, 0.4, "EASY BUT THIN",   PALETTE["text_tertiary"]),
        (1.5, 0.4, "WATCH",           PALETTE["text_tertiary"]),
    ]
    for x, y, label, color in quadrant_labels:
        fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>",
                           showarrow=False,
                           font=dict(color=color, size=10, family="-apple-system, sans-serif"))

    fig.update_layout(**base_layout(
        height=520,
        xaxis=dict(
            range=[0, 5.5], title="Ease of monetization →",
            color=PALETTE["text_secondary"], gridcolor=PALETTE["border"],
            tickvals=[1, 2, 3, 4, 5],
        ),
        yaxis=dict(
            range=[0, 5.5], title="Value potential →",
            color=PALETTE["text_secondary"], gridcolor=PALETTE["border"],
            tickvals=[1, 2, 3, 4, 5],
        ),
        margin=dict(l=60, r=40, t=40, b=60),
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Maturity legend
    cols = st.columns(3)
    legend = [
        ("Easy and real today",     PALETTE["green"], "Bill · §14a · BRP"),
        ("Real but operationally hard", PALETTE["amber"], "DA · ID · aFRR · FCR"),
        ("Emerging / selective",    PALETTE["red"],   "Local / DSO"),
    ]
    for i, (label, color, channels) in enumerate(legend):
        with cols[i]:
            st.markdown(f"""
                <div class="card" style="border-top:3px solid {color};">
                  <div style="color:{color}; font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;">{label}</div>
                  <div style="color:{PALETTE['text_secondary']}; font-size:0.88rem; margin-top:0.5rem;">{channels}</div>
                </div>
            """, unsafe_allow_html=True)


# =============================================================================
# 16. PAGE: 7. CUSTOMER ARCHETYPES
# =============================================================================

def render_archetypes() -> None:
    st.markdown("# Customer archetypes")
    st.markdown(
        '<div class="subtitle">Four representative households — what flexibility '
        'they offer, where the value lands, and the proposition that fits.</div>',
        unsafe_allow_html=True,
    )

    # Archetype cards in a 2x2 grid
    archetype_ids = list(ARCHETYPES.keys())
    for row_start in [0, 2]:
        cols = st.columns(2)
        for i, idx in enumerate([row_start, row_start + 1]):
            archetype_id = archetype_ids[idx]
            archetype = ARCHETYPES[archetype_id]
            base_total = sum(archetype["stack"]["base"].values())
            up_total   = sum(archetype["stack"]["upside"].values())

            best_chips = " ".join(
                f'<span class="tag tag-strong">{CHANNELS[c]["short"]}</span>'
                for c in archetype["strongest"]
            )
            weak_chips = " ".join(
                f'<span class="tag tag-warn">{CHANNELS[c]["short"]}</span>'
                for c in archetype["weakest"]
            ) if archetype["weakest"] else f'<span style="color:{PALETTE["text_tertiary"]}; font-size:0.85rem;">none material</span>'

            with cols[i]:
                st.markdown(f"""
                    <div class="card" style="border-left:3px solid {PALETTE['teal']};">
                      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.6rem;">
                        <div>
                          <div style="color:{PALETTE['teal']}; font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;">{archetype['icon']} &nbsp;Archetype</div>
                          <h3 style="margin:0.2rem 0 0 0;">{archetype['name']}</h3>
                        </div>
                        <div style="text-align:right;">
                          <div style="color:{PALETTE['text_tertiary']}; font-size:0.7rem; text-transform:uppercase;">Annual stack (base)</div>
                          <div style="color:{PALETTE['text_primary']}; font-size:1.4rem; font-weight:600; margin-top:0.2rem;">€{base_total}</div>
                          <div style="color:{PALETTE['text_tertiary']}; font-size:0.78rem;">up to €{up_total} (upside)</div>
                        </div>
                      </div>

                      <div style="color:{PALETTE['text_secondary']}; font-size:0.88rem; margin-bottom:0.8rem;">
                        <strong style="color:{PALETTE['text_primary']};">Flex offered:</strong> {archetype['flex']}
                      </div>

                      <div style="margin-bottom:0.5rem;">
                        <span style="color:{PALETTE['text_tertiary']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.06em;">Strongest channels</span><br>
                        <div style="margin-top:0.3rem;">{best_chips}</div>
                      </div>
                      <div style="margin-bottom:0.8rem;">
                        <span style="color:{PALETTE['text_tertiary']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.06em;">Weakest channels</span><br>
                        <div style="margin-top:0.3rem;">{weak_chips}</div>
                      </div>

                      <div style="background:{PALETTE['panel_2']}; border-radius:6px; padding:0.7rem 0.9rem; margin-top:0.5rem;">
                        <div style="color:{PALETTE['gold']}; font-size:0.68rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.3rem;">Proposition</div>
                        <div style="color:{PALETTE['text_primary']}; font-size:0.92rem; line-height:1.55;">"{archetype['proposition']}"</div>
                      </div>
                    </div>
                """, unsafe_allow_html=True)

    # Comparison chart of all four
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Total annual value comparison (base scenario)")

    arch_names = [ARCHETYPES[a]["name"] for a in archetype_ids]
    fig = go.Figure()
    for ch_id in VALUE_STACK_ORDER:
        values = [ARCHETYPES[a]["stack"]["base"].get(ch_id, 0) for a in archetype_ids]
        if sum(values) == 0:
            continue
        fig.add_trace(go.Bar(
            y=arch_names,
            x=values,
            name=CHANNELS[ch_id]["short"],
            orientation="h",
            marker=dict(color=VALUE_CAPTURE[ch_id]["color"]),
            hovertemplate=f"<b>{CHANNELS[ch_id]['name']}</b><br>€%{{x}}/yr<extra></extra>",
        ))
    fig.update_layout(**base_layout(
        height=350,
        barmode="stack",
        xaxis=dict(title="€ / year", color=PALETTE["text_secondary"], gridcolor=PALETTE["border"]),
        yaxis=dict(autorange="reversed", color=PALETTE["text_secondary"]),
        legend=dict(orientation="h", y=-0.22, x=0, bgcolor="rgba(0,0,0,0)", font=dict(color=PALETTE["text_secondary"])),
        margin=dict(l=20, r=20, t=20, b=80),
    ))
    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# 17. PAGE: 8. GO-TO-MARKET ROADMAP
# =============================================================================

def render_roadmap() -> None:
    st.markdown("# Go-to-market roadmap")
    st.markdown(
        '<div class="subtitle">Sequence the build. Lead where value is dense '
        'and access is cheap; layer harder channels as the platform matures.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        headline(
            "Wave 1 wins the customer. Wave 2 wins the platform. Wave 3 buys "
            "operational scale. Wave 4 protects the optionality."
        ),
        unsafe_allow_html=True,
    )

    # Timeline visualization
    fig = go.Figure()
    timing_starts = [0, 12, 24, 36]
    timing_ends   = [12, 24, 36, 48]
    wave_colors = [PALETTE["teal"], PALETTE["green"], PALETTE["amber"], PALETTE["purple"]]
    wave_labels = [f"Wave {w['wave']} · {w['name']}" for w in WAVES]

    for i, w in enumerate(WAVES):
        fig.add_trace(go.Bar(
            y=[wave_labels[i]],
            x=[timing_ends[i] - timing_starts[i]],
            base=[timing_starts[i]],
            orientation="h",
            marker=dict(color=wave_colors[i]),
            hovertemplate=f"<b>{w['name']}</b><br>Timing: {w['timing']}<extra></extra>",
            showlegend=False,
            text=w["timing"],
            textposition="inside",
            textfont=dict(color="#0B0F14", size=11, family="-apple-system, sans-serif"),
            insidetextanchor="middle",
        ))

    fig.update_layout(**base_layout(
        height=280,
        barmode="overlay",
        xaxis=dict(
            title="Months from now",
            color=PALETTE["text_secondary"],
            gridcolor=PALETTE["border"],
            range=[0, 50],
            tickvals=[0, 12, 24, 36, 48],
        ),
        yaxis=dict(autorange="reversed", color=PALETTE["text_secondary"], tickfont=dict(size=11)),
        margin=dict(l=20, r=20, t=20, b=60),
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Wave detail cards
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Wave details")

    for i, w in enumerate(WAVES):
        channel_chips = " ".join(
            f'<span class="tag tag-strong">{CHANNELS[c]["short"]}</span>'
            for c in w["channels"]
        )
        asset_chips = " ".join(
            f'<span class="tag">{ASSETS[a]["short"]}</span>'
            for a in w["assets"]
        )
        capabilities = "".join(
            f'<div style="padding:0.25rem 0; color:{PALETTE["text_primary"]}; font-size:0.9rem;">'
            f'<span style="color:{wave_colors[i]}; margin-right:8px;">▸</span>{c}</div>'
            for c in w["capabilities"]
        )

        st.markdown(f"""
            <div class="wave-card" style="border-left-color:{wave_colors[i]};">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                <div>
                  <div class="wave-num" style="color:{wave_colors[i]};">Wave {w['wave']} · {w['timing']}</div>
                  <div class="wave-title">{w['name']}</div>
                </div>
              </div>
              <p style="color:{PALETTE['text_secondary']}; line-height:1.6; margin-bottom:0.8rem;">{w['why']}</p>

              <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.2rem;">
                <div>
                  <div class="metric-label">Channels in this wave</div>
                  <div style="margin-top:0.4rem;">{channel_chips}</div>
                  <div class="metric-label" style="margin-top:0.8rem;">Lead assets</div>
                  <div style="margin-top:0.4rem;">{asset_chips}</div>
                </div>
                <div>
                  <div class="metric-label">Capabilities required</div>
                  <div style="margin-top:0.3rem;">{capabilities}</div>
                </div>
              </div>

              <div class="section-divider" style="margin:1rem 0 0.7rem 0;"></div>

              <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.2rem; font-size:0.85rem;">
                <div>
                  <span style="color:{PALETTE['text_tertiary']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.06em;">Why not earlier</span><br>
                  <span style="color:{PALETTE['text_secondary']};">{w['why_not_earlier']}</span>
                </div>
                <div>
                  <span style="color:{PALETTE['text_tertiary']}; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.06em;">Why not later</span><br>
                  <span style="color:{PALETTE['text_secondary']};">{w['why_not_later']}</span>
                </div>
              </div>
            </div>
        """, unsafe_allow_html=True)

    # Closing message
    st.markdown(
        insight_box(
            "<strong>The crisp commercial message:</strong> the flexibility "
            "opportunity is real but operationally heterogeneous. Win by "
            "stacking three to four value streams on the same hardware — "
            "not by chasing the highest-priced single channel. Lead with "
            "bill + §14a + wholesale; layer balancing only at scale; treat "
            "local flex and V2G as strategic options, not core revenue.",
            label="Takeaway",
        ),
        unsafe_allow_html=True,
    )


# =============================================================================
# 18. SIDEBAR + ROUTER
# =============================================================================

PAGES = {
    "1 · Executive overview":        render_overview,
    "2 · Asset flexibility":         render_assets,
    "3 · Monetization channels":     render_channels,
    "4 · Asset × market heatmap":    render_heatmap,
    "5 · Value stack simulator":     render_value_stack,
    "6 · Easy vs hard 2×2":          render_2x2,
    "7 · Customer archetypes":       render_archetypes,
    "8 · Go-to-market roadmap":      render_roadmap,
}


def main() -> None:
    with st.sidebar:
        st.markdown(f"""
            <div style="padding:0.5rem 0 1.5rem 0;">
              <div style="color:{PALETTE['teal']}; font-size:0.72rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase;">◆  Strategy Cockpit</div>
              <div style="color:{PALETTE['text_primary']}; font-size:1.05rem; font-weight:500; margin-top:0.4rem; line-height:1.35;">Retail flexibility<br>monetization</div>
              <div style="color:{PALETTE['text_tertiary']}; font-size:0.8rem; margin-top:0.4rem;">Germany · Europe</div>
            </div>
        """, unsafe_allow_html=True)

        page = st.radio(
            "Section",
            options=list(PAGES.keys()),
            label_visibility="visible",
        )

        st.markdown(f"""
            <div style="position:absolute; bottom:1.5rem; left:1rem; right:1rem; padding-top:1rem; border-top:1px solid {PALETTE['border']};">
              <div style="color:{PALETTE['text_tertiary']}; font-size:0.72rem; line-height:1.5;">
                Internal storytelling tool.<br>
                Numbers are illustrative — for narrative, not financial modelling.
              </div>
            </div>
        """, unsafe_allow_html=True)

    PAGES[page]()


if __name__ == "__main__":
    main()
