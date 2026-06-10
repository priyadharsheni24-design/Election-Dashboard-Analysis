import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page config ---
st.set_page_config(page_title="India Election EDA", page_icon="🗳️", layout="wide")

# --- Custom CSS for a friendly look ---
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f172a; }
            /*All default text */
             html, body, [class*="css"], p, div, span, label {
        color: #e2e8f0 ;
    }
            


    /* Metric card style */
    [data-testid="metric-container"] {
        background:#1e293b ;
        border-radius: 14px;
        padding: 18px;
        box-shadow: none;
        border-left: 5px solid #818cf8;
    }
            [data-testid="metric-container"] * { color: #e2e8f0 !important; }
    [data-testid="stMetricValue"] { color: #ffffff ; font-size: 28px !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 ; }


    /* Section headers */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #818cf8;
        margin: 28px 0 8px 0;
        padding-left: 12px;
        border-left: 4px solid #818cf8;
    }

    /* Info box */
    .info-box {
        background: #1e293b;
        border-radius: 10px;
        padding: 12px 14px;
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 14px;
        border: 1px solid #334155;

    }

    /* Winner card */
    .winner-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        border-left: 4px solid #22c55e;
        border-top: 1px solid #334155;
        border-right: 1px solid #334155;
        border-bottom: 1px solid #334155;
    }

    /* Turnout bar */
    .turnout-row {
        background:#1e293b ;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
         border: 1px solid #334155;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1b4b !important;
    }
    [data-testid="stSidebar"] * { color: #c7d2fe !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #ffffff !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: #a5b4fc !important;
        font-size: 13px !important;
    }
    [data-testid="stSidebar"] hr { border-color: #4338ca !important; }

    /* Selectbox and multiselect dropdowns */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-color: #334155 !important;
    }

    /* Page title */
    h1 { color: #ffffff !important; }
    h2, h3 { color: #c7d2fe !important; }

    /* Divider */
    hr { border-color: #334155 !important; }

</style>
""", unsafe_allow_html=True)

# --- Load data ---
df = pd.read_csv(r"C:\Users\priya\Downloads\lok_sabha (1).csv")
# 2026 State Assembly Results
results_2026 = pd.DataFrame({
    "state":        ["Tamil Nadu", "West Bengal", "Kerala", "Assam"],
    "winner_2026":  ["TVK",        "BJP",         "UDF/INC", "BJP"],
    "winner_2021":  ["DMK",        "TMC",         "LDF/CPI(M)", "BJP"],
    "seats_2026":   [108,           206,            82,           82],
    "seats_2021":   [159,           215,            99,           60],
    "total_seats":  [234,           294,            140,          126],
    "upset":        [True,          True,           True,         False]
})


# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("## 🗳️ Election Filter")
    st.markdown("---")

    selected_year = st.selectbox("📅 Election Year",
                                  sorted(df["year"].unique(), reverse=True))
    selected_year = int(selected_year)

    states = ["All States"] + sorted(df["state"].unique().tolist())
    selected_state = st.selectbox("🗺️ State", states)

    # Filter first before showing party options
    filtered_temp = df[df["year"] == selected_year]
    if selected_state != "All States":
        filtered_temp = filtered_temp[filtered_temp["state"] == selected_state]

    parties = sorted(filtered_temp["party"].unique().tolist())
    selected_parties = st.multiselect("🏛️ Party", options=parties, default=parties)

    st.markdown("---")
    st.markdown(f"<small>Showing data for <b>{selected_year}</b></small>", unsafe_allow_html=True)

# ===================== FILTER DATA =====================
filtered = filtered_temp.copy()
if selected_parties:
    filtered = filtered[filtered["party"].isin(selected_parties)]

winners = filtered[filtered["winner"] == 1]

# ===================== HEADER =====================
st.markdown("# 🗳️ India Lok Sabha — Election Dashboard")
label = selected_state if selected_state != "All States" else "All States"
st.markdown(f"<div class='info-box'>📍 Showing results for <b>{label}</b> · Election Year: <b>{selected_year}</b> · Parties selected: <b>{len(selected_parties)}</b></div>", unsafe_allow_html=True)
  
if len(filtered) == 0:
    st.markdown(f"""
    <div style='background:#451a03; border-radius:12px; padding:20px;
                border:1px solid #f59e0b; text-align:center; margin:20px 0;'>
        <div style='font-size:28px; margin-bottom:8px'>🗳️</div>
        <div style='font-size:18px; font-weight:700; color:#fcd34d; margin-bottom:8px'>
            No Election in {label} in {selected_year}
        </div>
        <div style='font-size:14px; color:#fde68a; line-height:1.6'>
            {selected_state} did not have an election in {selected_year}.<br>
            Elections in {selected_year} were held only in
            <b>{'Delhi' if selected_year == 2025 else 'Tamil Nadu, West Bengal, Kerala and Assam' if selected_year == 2026 else 'all states'}</b>.<br><br>
            👈 Please select a different state or year from the sidebar.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
# ===================== METRIC CARDS =====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏆 Total Seats", len(winners["constituency"].unique()))
col2.metric("📊 Avg Turnout", f"{filtered['turnout_pct'].mean():.1f}%")
col3.metric("🏛️ Parties", filtered["party"].nunique())
col4.metric("🗳️ Total Votes", f"{filtered['votes'].sum():,}")

st.markdown("---")

# ===================== CHART ROW 1 =====================
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("<div class='section-title'>🏆 Seats Won by Party</div>", unsafe_allow_html=True)
    st.markdown("<div class='info-box'>Each bar shows how many seats a party won. Longer bar = more seats won.</div>", unsafe_allow_html=True)
    seats = winners.groupby("party").size().reset_index(name="seats")
    seats = seats.sort_values("seats", ascending=False)
    fig1 = px.bar(seats, x="seats", y="party", orientation="h",
                  color="seats", color_continuous_scale="Blues",
                  text="seats")
    fig1.update_traces(textposition="inside",textfont=dict(color="#ffffff", size=13))
    fig1.update_layout(
       plot_bgcolor="#1e293b", paper_bgcolor="#1e293b",
    font=dict(color="#e2e8f0"),
    yaxis=dict(autorange="reversed", tickfont=dict(color="#e2e8f0")),
    xaxis=dict(tickfont=dict(color="#e2e8f0"), gridcolor="#334155"),
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=10, b=10),
    height=350 
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown("<div class='section-title'>🥧 Vote Share by Party</div>", unsafe_allow_html=True)
    st.markdown("<div class='info-box'>The bigger the slice, the more total votes that party received across all constituencies.</div>", unsafe_allow_html=True)
    vote_share = filtered.groupby("party")["votes"].sum().reset_index()
    fig2 = px.pie(vote_share, names="party", values="votes",
                  hole=0.45,
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_traces(textposition="inside", textinfo="label+percent",textfont=dict(color="#ffffff", size=12))
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        height=350,
        font=dict(color="#e2e8f0")
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===================== TOP 10 WINNERS - FRIENDLY CARDS =====================
st.markdown("<div class='section-title'>🥇 Top 10 Winners by Victory Margin</div>", unsafe_allow_html=True)
st.markdown("<div class='info-box'>Victory margin = difference in votes between the winner and the runner-up. A bigger margin means a more dominant win.</div>", unsafe_allow_html=True)

top10 = winners.nlargest(10, "margin").reset_index(drop=True)

# Show as a visual progress-bar style table
medal = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
max_margin = top10["margin"].max()

for i, row in top10.iterrows():
    pct = int((row["margin"] / max_margin) * 100)
    st.markdown(f"""
    <div class='winner-card'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px'>
            <span style='font-weight:700; font-size:15px'>{medal[i]} {row['candidate']}</span>
            <span style='background:#d1fae5; color:#065f46; padding:3px 10px; border-radius:20px; font-size:13px; font-weight:600'>{row['party']}</span>
        </div>
        <div style='font-size:13px; color:#6b7280; margin-bottom:6px'>📍 {row['constituency']}, {row['state']}</div>
        <div style='background:#f3f4f6; border-radius:8px; height:10px; width:100%'>
            <div style='background:#10b981; height:10px; border-radius:8px; width:{pct}%'></div>
        </div>
        <div style='font-size:12px; color:#374151; margin-top:4px'>Won by <b>{row['margin']:,} votes</b></div>
    </div>
    """, unsafe_allow_html=True)

# ===================== STATE-WISE TURNOUT - FRIENDLY =====================
st.markdown("<div class='section-title'>📍 State-wise Voter Turnout</div>", unsafe_allow_html=True)
st.markdown("<div class='info-box'>Turnout % = percentage of registered voters who actually came and voted. Higher % means more people participated in that state.</div>", unsafe_allow_html=True)

turnout = filtered.groupby("state")["turnout_pct"].mean().reset_index()
turnout = turnout.sort_values("turnout_pct", ascending=False).reset_index(drop=True)
max_t = turnout["turnout_pct"].max()

for _, row in turnout.iterrows():
    pct = row["turnout_pct"]
    bar_w = int((pct / max_t) * 100)
    color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 60 else "#ef4444"
    label_color = "#065f46" if pct >= 70 else "#92400e" if pct >= 60 else "#991b1b"
    bg_color = "#d1fae5" if pct >= 70 else "#fef3c7" if pct >= 60 else "#fee2e2"
    st.markdown(f"""
    <div class='turnout-row'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:5px'>
            <span style='font-weight:600; font-size:14px'>📍 {row['state']}</span>
            <span style='background:{bg_color}; color:{label_color}; padding:2px 10px; border-radius:20px; font-size:13px; font-weight:700'>{pct:.1f}%</span>
        </div>
        <div style='background:#f3f4f6; border-radius:6px; height:8px'>
            <div style='background:{color}; height:8px; border-radius:6px; width:{bar_w}%'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='font-size:12px; color:#9ca3af; margin-top:8px'>🟢 Above 70% — Good &nbsp;&nbsp; 🟡 60–70% — Average &nbsp;&nbsp; 🔴 Below 60% — Low</div>", unsafe_allow_html=True)
# ===================== 2026 SHOCK RESULTS =====================
if selected_year == 2026:
     
    st.markdown("<div class='section-title'>⚡ 2026 State Assembly — Shock Results</div>",
            unsafe_allow_html=True)
    st.markdown("<div class='info-box'>May 4, 2026 assembly results shocked India — three states changed hands in one day. TVK won Tamil Nadu in its debut election, BJP ended TMC's 15-year rule in West Bengal, and Congress-led UDF returned to power in Kerala.</div>",
            unsafe_allow_html=True)
if selected_year == 2026:       
    st.markdown("---")         
    col1, col2, col3, col4 = st.columns(4)   
    for _, row in results_2026.iterrows():   
        pass         

# --- Upset cards ---
if int(selected_year) == 2026:
    col1, col2, col3, col4 = st.columns(4)
    cards = [
      (col1, "🎬 Tamil Nadu", "TVK", "108 / 234 seats", "DMK lost power", "#052e16", "#22c55e", "#86efac"),
      (col2, "🌸 West Bengal", "BJP", "206 / 294 seats", "TMC lost after 15 yrs", "#052e16", "#22c55e", "#86efac"),
      (col3, "🌴 Kerala", "UDF/INC", "82 / 140 seats", "LDF lost power", "#052e16", "#22c55e", "#86efac"),
      (col4, "🦏 Assam", "BJP", "82 / 126 seats", "Hat-trick win", "#1e1b4b", "#818cf8", "#c7d2fe"),
]
    for col, title, winner, seats, note, bg, col1c, col2c in cards:
       col.markdown(f"""
       <div style='background:{bg}; border-radius:12px; padding:16px;
                border:1px solid #334155; text-align:center;'>
            <div style='font-size:13px; color:#94a3b8; margin-bottom:4px'>{title}</div>
            <div style='font-size:22px; font-weight:700; color:{col1c}'>{winner}</div>
            <div style='font-size:12px; color:{col2c}; margin-top:4px'>{seats}</div>
            <div style='font-size:11px; color:#64748b; margin-top:6px'>{note}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# --- Before vs After bar chart ---
if int(selected_year) == 2026:
    st.markdown("<div class='section-title'>📊 Seats Won — 2021 vs 2026</div>",
            unsafe_allow_html=True)
    st.markdown("<div class='info-box'>Each state shows two bars — previous election winner in blue, 2026 winner in green. The dramatic drop in TMC and DMK bars shows how big the swings were.</div>",
            unsafe_allow_html=True)

    before_after = pd.DataFrame({
        "state":   ["Tamil Nadu","Tamil Nadu","West Bengal","West Bengal","Kerala","Kerala","Assam","Assam"],
        "party":   ["DMK (2021)","TVK (2026)","TMC (2021)","BJP (2026)","LDF (2021)","UDF (2026)","BJP (2021)","BJP (2026)"],
        "seats":   [159,          108,          215,          206,          99,          82,          60,           82],
        "year":    ["2021",       "2026",       "2021",       "2026",       "2021",      "2026",      "2021",       "2026"]
})

    fig_ba = px.bar(before_after, x="state", y="seats", color="year",
                barmode="group", text="seats",
                color_discrete_map={"2021": "#3b82f6", "2026": "#22c55e"},
                title="Ruling party seat count — before and after 2026")
    fig_ba.update_traces(textposition="inside",
                     textfont=dict(color="#ffffff", size=13))
    fig_ba.update_layout(
       plot_bgcolor="#1e293b", paper_bgcolor="#1e293b",
       font=dict(color="#e2e8f0"),
       xaxis=dict(tickfont=dict(color="#e2e8f0"), gridcolor="#334155"),
       yaxis=dict(tickfont=dict(color="#e2e8f0"), gridcolor="#334155",
               title="Seats won"),
       legend=dict(font=dict(color="#e2e8f0"), bgcolor="#1e293b"),
       margin=dict(l=10, r=10, t=40, b=10),
       height=380
)
    st.plotly_chart(fig_ba, use_container_width=True)

# --- Swing meter ---
if int(selected_year) == 2026: 
    st.markdown("<div class='section-title'>🔄 Seat Swing — How Many Seats Changed</div>",
            unsafe_allow_html=True)
    st.markdown("<div class='info-box'>Swing = seats gained by the new winner compared to previous election. Bigger bar = more dramatic change. Red means the previous ruling party lost heavily.</div>",
            unsafe_allow_html=True)

    results_2026["swing"] = abs(results_2026["seats_2026"] - results_2026["seats_2021"])
    results_2026["color"] = results_2026["upset"].map({True: "#ef4444", False: "#22c55e"})
    max_swing = results_2026["swing"].max()

    for _, row in results_2026.iterrows():
        bar_w = int((row["swing"] / max_swing) * 100)
        dot = "🔴" if row["upset"] else "🟢"
        tag = "UPSET" if row["upset"] else "RETAINED"
        tag_bg = "#450a0a" if row["upset"] else "#14532d"
        tag_color = "#fca5a5" if row["upset"] else "#86efac"
        st.markdown(f"""
        <div style='background:#1e293b; border-radius:12px; padding:14px 16px;
                margin-bottom:10px; border:1px solid #334155;'>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px'>
            <span style='font-weight:600; font-size:14px; color:#f1f5f9'>
                {dot} {row['state']} — {row['winner_2021']} → {row['winner_2026']}
            </span>
            <span style='background:{tag_bg}; color:{tag_color}; padding:2px 10px;
                         border-radius:20px; font-size:12px; font-weight:700'>{tag}</span>
        </div>
        <div style='background:#0f172a; border-radius:6px; height:10px;'>
            <div style='background:{row["color"]}; height:10px; border-radius:6px;
                        width:{bar_w}%'></div>
        </div>
        <div style='font-size:12px; color:#94a3b8; margin-top:5px'>
            Swing of <b style='color:#e2e8f0'>{row['swing']} seats</b> &nbsp;·&nbsp;
            New winner holds <b style='color:#e2e8f0'>{row['seats_2026']}/{row['total_seats']}</b> seats
        </div>
    </div>
    """, unsafe_allow_html=True)