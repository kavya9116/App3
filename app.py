"""
Indian Government Budget Analysis Dashboard
=============================================
An interactive Streamlit application for analyzing and comparing
the Union Budget of India across ministries and financial years
(2013-14 to 2023-24).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Budget Analyzer",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Hero header */
    .hero-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    }
    .hero-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-header p {
        color: #a5b4fc;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid rgba(165, 180, 252, 0.15);
        border-radius: 12px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.2);
    }
    .metric-card .label {
        color: #a5b4fc;
        font-size: 0.78rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 0.3rem;
    }
    .metric-card .delta {
        font-size: 0.82rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    .delta-positive { color: #34d399; }
    .delta-negative { color: #f87171; }

    /* Section titles */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e0e7ff;
        margin: 2rem 0 1rem;
        padding-left: 0.6rem;
        border-left: 4px solid #6366f1;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1e1b4b 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown label,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #c7d2fe;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid rgba(165, 180, 252, 0.15);
        border-radius: 12px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Budget Data (₹ Crores) ──────────────────────────────────────────────────
# Source: Union Budget of India – Expenditure Budget documents (2013-14 to 2023-24)
# Values are Budget Estimates in ₹ Crores (approximate)
BUDGET_DATA = {
    "Ministry/Department": [
        "Defence",
        "Home Affairs",
        "Rural Development",
        "Education",
        "Health & Family Welfare",
        "Agriculture & Farmers Welfare",
        "Railways",
        "Road Transport & Highways",
        "Finance",
        "Urban Development / Housing",
        "Women & Child Development",
        "Social Justice & Empowerment",
        "Commerce & Industry",
        "IT & Telecommunications",
        "Science & Technology",
        "Environment & Forests",
        "Consumer Affairs & Food",
        "Labour & Employment",
        "Petroleum & Natural Gas",
        "Textiles",
    ],
    "2013-14": [
        203672, 73370, 73560, 71306, 30246, 27049, 26000, 31819, 16000, 22522,
        18585, 6725, 3492, 15280, 8348, 2430, 92789, 5753, 7520, 6120,
    ],
    "2014-15": [
        229000, 78780, 80043, 74846, 33278, 28358, 29000, 34345, 17200, 24140,
        20440, 7234, 3836, 16920, 8940, 2678, 102030, 6180, 8420, 6500,
    ],
    "2015-16": [
        246727, 84490, 84589, 69074, 33152, 24909, 40000, 45842, 18900, 27200,
        17408, 7734, 4213, 18440, 9580, 2900, 114990, 6350, 9200, 5120,
    ],
    "2016-17": [
        249099, 87830, 101120, 72394, 38524, 44485, 45000, 52447, 20100, 29530,
        17408, 8600, 4630, 20100, 10340, 2720, 120000, 6530, 10400, 5234,
    ],
    "2017-18": [
        262390, 93370, 110333, 79686, 47353, 51026, 55000, 61000, 22500, 32300,
        22095, 9719, 5103, 22400, 11440, 2675, 150000, 7115, 12400, 6165,
    ],
    "2018-19": [
        282733, 100281, 115437, 85010, 54667, 57600, 53000, 71000, 24500, 36750,
        24700, 10500, 5470, 24900, 12540, 2850, 171000, 7700, 14200, 7148,
    ],
    "2019-20": [
        305296, 113952, 119874, 94854, 62660, 57600, 66000, 83016, 26800, 40740,
        29165, 11600, 5861, 27000, 13600, 3100, 185000, 8230, 16100, 7637,
    ],
    "2020-21": [
        323053, 121527, 120147, 99312, 67112, 131531, 70000, 91823, 28500, 45570,
        28068, 11428, 6192, 29500, 14500, 3180, 201500, 8680, 18400, 7890,
    ],
    "2021-22": [
        363140, 134234, 133690, 93224, 73932, 131531, 110055, 118101, 32100, 54581,
        24435, 11901, 6827, 53108, 16000, 3030, 254300, 10136, 21200, 3631,
    ],
    "2022-23": [
        385370, 145236, 138203, 104278, 86201, 132514, 140367, 199108, 35600, 63200,
        25172, 13002, 7521, 79490, 16712, 3079, 271515, 11078, 23800, 3631,
    ],
    "2023-24": [
        405582, 155515, 159964, 112899, 89155, 127470, 241397, 271282, 38400, 79150,
        25449, 13855, 8210, 97579, 16361, 3079, 297000, 12058, 26200, 4417,
    ],
}

# ─── Build DataFrame ─────────────────────────────────────────────────────────
df = pd.DataFrame(BUDGET_DATA)
years = [c for c in df.columns if c != "Ministry/Department"]

# Long-form for Plotly
df_long = df.melt(
    id_vars="Ministry/Department",
    value_vars=years,
    var_name="Year",
    value_name="Budget (₹ Cr)",
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Dashboard Controls")
    st.markdown("---")

    selected_years = st.multiselect(
        "📅 Select Financial Years",
        options=years,
        default=years,
        help="Choose one or more budget years to analyze.",
    )

    all_ministries = sorted(df["Ministry/Department"].unique())
    selected_ministries = st.multiselect(
        "🏛️ Select Ministries",
        options=all_ministries,
        default=all_ministries[:10],
        help="Pick ministries to include in comparisons.",
    )

    st.markdown("---")
    chart_theme = st.selectbox(
        "🎨 Chart Color Theme",
        ["Viridis", "Plasma", "Inferno", "Turbo", "Sunset", "Tealrose"],
        index=0,
    )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#6366f1; font-size:0.75rem;'>"
        "Built with ❤️ using Streamlit & Plotly<br>"
        "Data: Union Budget of India</div>",
        unsafe_allow_html=True,
    )

# colour sequence for plotly
COLOR_SEQ_MAP = {
    "Viridis": px.colors.sequential.Viridis,
    "Plasma": px.colors.sequential.Plasma,
    "Inferno": px.colors.sequential.Inferno,
    "Turbo": px.colors.sequential.Turbo,
    "Sunset": px.colors.sequential.Sunset,
    "Tealrose": px.colors.diverging.Tealrose,
}
color_seq = COLOR_SEQ_MAP.get(chart_theme, px.colors.sequential.Viridis)

# ─── Filter Data ──────────────────────────────────────────────────────────────
mask = df["Ministry/Department"].isin(selected_ministries)
df_filtered = df.loc[mask, ["Ministry/Department"] + selected_years]
df_long_filtered = df_long[
    (df_long["Ministry/Department"].isin(selected_ministries))
    & (df_long["Year"].isin(selected_years))
]

# ─── Hero Header ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-header">
        <h1>🇮🇳 Indian Union Budget Analyzer</h1>
        <p>Ministry-wise Budget Allocation Analysis · FY 2013-14 to 2023-24</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── KPI Cards ────────────────────────────────────────────────────────────────
if selected_years and selected_ministries:
    latest_year = max(selected_years)
    earliest_year = min(selected_years)
    total_latest = df_filtered[latest_year].sum()
    total_earliest = df_filtered[earliest_year].sum()
    growth_pct = ((total_latest - total_earliest) / total_earliest) * 100 if total_earliest else 0
    top_ministry = df_filtered.loc[
        df_filtered[latest_year].idxmax(), "Ministry/Department"
    ]
    top_amount = df_filtered[latest_year].max()
    avg_budget = df_filtered[latest_year].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="label">Total Budget ({latest_year})</div>
                <div class="value">₹{total_latest:,.0f} Cr</div>
                <div class="delta {'delta-positive' if growth_pct >= 0 else 'delta-negative'}">
                    {'▲' if growth_pct >= 0 else '▼'} {abs(growth_pct):.1f}% vs {earliest_year}
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="label">Top Ministry ({latest_year})</div>
                <div class="value" style="font-size:1.1rem">{top_ministry}</div>
                <div class="delta delta-positive">₹{top_amount:,.0f} Cr</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="label">Avg Ministry Budget</div>
                <div class="value">₹{avg_budget:,.0f} Cr</div>
                <div class="delta" style="color:#a5b4fc">{len(selected_ministries)} ministries</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""<div class="metric-card">
                <div class="label">Years Covered</div>
                <div class="value">{len(selected_years)}</div>
                <div class="delta" style="color:#a5b4fc">{earliest_year} → {latest_year}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Tabs ─────────────────────────────────────────────────────────────────
    tabs = st.tabs([
        "📈 Trend Analysis",
        "📊 Year-on-Year Comparison",
        "🍩 Share Breakdown",
        "🔥 Heatmap",
        "🏆 Rankings",
        "📋 Data Table",
    ])

    # ── Tab 1: Trend Analysis ─────────────────────────────────────────────────
    with tabs[0]:
        st.markdown('<div class="section-title">Budget Trend Over Years</div>', unsafe_allow_html=True)

        fig_trend = px.line(
            df_long_filtered,
            x="Year",
            y="Budget (₹ Cr)",
            color="Ministry/Department",
            markers=True,
            color_discrete_sequence=color_seq,
            hover_data={"Budget (₹ Cr)": ":,.0f"},
        )
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.45, xanchor="center", x=0.5,
                font=dict(size=10),
            ),
            height=550,
            margin=dict(t=30, b=120),
            hovermode="x unified",
        )
        fig_trend.update_xaxes(showgrid=True, gridcolor="rgba(99,102,241,0.1)")
        fig_trend.update_yaxes(showgrid=True, gridcolor="rgba(99,102,241,0.1)")
        st.plotly_chart(fig_trend, use_container_width=True)

        # Growth rate area chart
        st.markdown('<div class="section-title">Year-over-Year Growth Rate (%)</div>', unsafe_allow_html=True)
        growth_rows = []
        for _, row in df_filtered.iterrows():
            ministry = row["Ministry/Department"]
            vals = [row[y] for y in selected_years]
            for i in range(1, len(vals)):
                prev = vals[i - 1]
                curr = vals[i]
                gr = ((curr - prev) / prev * 100) if prev else 0
                growth_rows.append({
                    "Ministry/Department": ministry,
                    "Year": selected_years[i],
                    "Growth (%)": round(gr, 2),
                })
        if growth_rows:
            df_growth = pd.DataFrame(growth_rows)
            fig_growth = px.bar(
                df_growth,
                x="Year",
                y="Growth (%)",
                color="Ministry/Department",
                barmode="group",
                color_discrete_sequence=color_seq,
                hover_data={"Growth (%)": ":.1f"},
            )
            fig_growth.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.55, xanchor="center", x=0.5,
                    font=dict(size=10),
                ),
                height=500,
                margin=dict(t=20, b=140),
            )
            st.plotly_chart(fig_growth, use_container_width=True)

    # ── Tab 2: Year-on-Year Comparison ────────────────────────────────────────
    with tabs[1]:
        st.markdown('<div class="section-title">Compare Two Financial Years</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            year_a = st.selectbox("Year A", selected_years, index=0, key="ya")
        with col_b:
            default_b_idx = len(selected_years) - 1 if len(selected_years) > 1 else 0
            year_b = st.selectbox(
                "Year B",
                selected_years,
                index=default_b_idx,
                key="yb",
            )

        if year_a == year_b:
            st.info("ℹ️ Please select two different years to compare.")
        comp_df = df_filtered[["Ministry/Department"]].copy()
        comp_df[year_a] = df_filtered[year_a].values
        comp_df[year_b + " "] = df_filtered[year_b].values  # space suffix avoids duplicate col if same year
        comp_df["Change (₹ Cr)"] = comp_df[year_b + " "] - comp_df[year_a]
        comp_df["Change (%)"] = np.where(
            comp_df[year_a] != 0,
            (comp_df["Change (₹ Cr)"] / comp_df[year_a] * 100).round(1),
            0.0,
        )
        comp_df = comp_df.sort_values("Change (%)", ascending=True)

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            y=comp_df["Ministry/Department"],
            x=comp_df[year_a],
            name=year_a,
            orientation="h",
            marker_color="#6366f1",
        ))
        fig_comp.add_trace(go.Bar(
            y=comp_df["Ministry/Department"],
            x=comp_df[year_b + " "],
            name=year_b,
            orientation="h",
            marker_color="#22d3ee",
        ))
        fig_comp.update_layout(
            barmode="group",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=max(450, len(selected_ministries) * 45),
            margin=dict(l=200, t=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        # Waterfall of changes
        st.markdown('<div class="section-title">Budget Change Waterfall</div>', unsafe_allow_html=True)
        comp_sorted = comp_df.sort_values("Change (₹ Cr)", ascending=False)
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            x=comp_sorted["Ministry/Department"],
            y=comp_sorted["Change (₹ Cr)"],
            textposition="outside",
            text=[f"₹{v:,.0f}" for v in comp_sorted["Change (₹ Cr)"]],
            connector=dict(line=dict(color="rgba(99,102,241,0.3)")),
            increasing=dict(marker=dict(color="#34d399")),
            decreasing=dict(marker=dict(color="#f87171")),
        ))
        fig_wf.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
            margin=dict(t=20, b=120),
            xaxis_tickangle=-45,
            yaxis_title="Change (₹ Crores)",
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    # ── Tab 3: Share Breakdown ────────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<div class="section-title">Ministry-wise Share of Budget</div>', unsafe_allow_html=True)

        pie_year = st.select_slider("Select Year for Pie Chart", options=selected_years, value=selected_years[-1])
        pie_df = df_filtered[["Ministry/Department", pie_year]].copy()
        pie_df = pie_df.sort_values(pie_year, ascending=False)

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            fig_pie = px.pie(
                pie_df,
                names="Ministry/Department",
                values=pie_year,
                color_discrete_sequence=color_seq,
                hole=0.0,
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label", textfont_size=10)
            fig_pie.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=500,
                margin=dict(t=20, b=20),
                title=dict(text=f"Pie Chart – {pie_year}", font=dict(size=14)),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_p2:
            fig_donut = px.pie(
                pie_df,
                names="Ministry/Department",
                values=pie_year,
                color_discrete_sequence=color_seq,
                hole=0.45,
            )
            fig_donut.update_traces(textposition="inside", textinfo="percent+label", textfont_size=10)
            fig_donut.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=500,
                margin=dict(t=20, b=20),
                title=dict(text=f"Donut Chart – {pie_year}", font=dict(size=14)),
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Stacked area
        st.markdown('<div class="section-title">Stacked Area – Budget Share Over Time</div>', unsafe_allow_html=True)
        fig_area = px.area(
            df_long_filtered,
            x="Year",
            y="Budget (₹ Cr)",
            color="Ministry/Department",
            groupnorm="percent",
            color_discrete_sequence=color_seq,
        )
        fig_area.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
            yaxis_title="Share (%)",
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.55, xanchor="center", x=0.5,
                font=dict(size=10),
            ),
            margin=dict(t=20, b=140),
        )
        st.plotly_chart(fig_area, use_container_width=True)

    # ── Tab 4: Heatmap ───────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown('<div class="section-title">Budget Allocation Heatmap</div>', unsafe_allow_html=True)

        heat_data = df_filtered.set_index("Ministry/Department")[selected_years]
        fig_heat = px.imshow(
            heat_data.values,
            labels=dict(x="Year", y="Ministry", color="₹ Crores"),
            x=selected_years,
            y=heat_data.index.tolist(),
            color_continuous_scale=chart_theme.lower() if chart_theme.lower() in [
                "viridis", "plasma", "inferno", "turbo"
            ] else "viridis",
            aspect="auto",
        )
        fig_heat.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=max(450, len(selected_ministries) * 38),
            margin=dict(l=220, t=20),
        )
        fig_heat.update_xaxes(side="top")
        st.plotly_chart(fig_heat, use_container_width=True)

        # Growth heatmap
        st.markdown('<div class="section-title">Growth Rate Heatmap (%)</div>', unsafe_allow_html=True)
        # Manual pct_change along columns (axis=1 was removed in pandas 2.2+)
        shifted = heat_data.shift(axis=1)
        growth_matrix = ((heat_data - shifted) / shifted * 100)
        growth_matrix = growth_matrix.iloc[:, 1:]  # drop first NaN col
        if not growth_matrix.empty:
            fig_gheat = px.imshow(
                growth_matrix.values.round(1),
                labels=dict(x="Year", y="Ministry", color="Growth %"),
                x=growth_matrix.columns.tolist(),
                y=growth_matrix.index.tolist(),
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                aspect="auto",
            )
            fig_gheat.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(450, len(selected_ministries) * 38),
                margin=dict(l=220, t=20),
            )
            fig_gheat.update_xaxes(side="top")
            st.plotly_chart(fig_gheat, use_container_width=True)

    # ── Tab 5: Rankings ──────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<div class="section-title">Ministry Budget Rankings</div>', unsafe_allow_html=True)

        rank_year = st.select_slider(
            "Select Year for Ranking", options=selected_years, value=selected_years[-1], key="rank_slider"
        )
        rank_df = (
            df_filtered[["Ministry/Department", rank_year]]
            .sort_values(rank_year, ascending=True)
            .reset_index(drop=True)
        )

        fig_rank = px.bar(
            rank_df,
            x=rank_year,
            y="Ministry/Department",
            orientation="h",
            color=rank_year,
            color_continuous_scale=color_seq,
            text=[f"₹{v:,.0f} Cr" for v in rank_df[rank_year]],
        )
        fig_rank.update_traces(textposition="outside", textfont_size=11)
        fig_rank.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=max(450, len(selected_ministries) * 42),
            margin=dict(l=220, t=20, r=100),
            coloraxis_showscale=False,
            xaxis_title="Budget (₹ Crores)",
            yaxis_title="",
        )
        st.plotly_chart(fig_rank, use_container_width=True)

        # Bump chart (rank over time)
        st.markdown('<div class="section-title">Rank Position Over the Years</div>', unsafe_allow_html=True)
        rank_over_time = []
        for y in selected_years:
            temp = df_filtered[["Ministry/Department", y]].copy()
            temp["Rank"] = temp[y].rank(ascending=False).astype(int)
            temp["Year"] = y
            temp = temp.rename(columns={y: "Budget"})
            rank_over_time.append(temp)
        if rank_over_time:
            df_rank_time = pd.concat(rank_over_time, ignore_index=True)
            fig_bump = px.line(
                df_rank_time,
                x="Year",
                y="Rank",
                color="Ministry/Department",
                markers=True,
                color_discrete_sequence=color_seq,
                hover_data={"Budget": ":,.0f"},
            )
            fig_bump.update_yaxes(autorange="reversed", dtick=1)
            fig_bump.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=550,
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5,
                    font=dict(size=10),
                ),
                margin=dict(t=20, b=140),
                yaxis_title="Rank (1 = Highest Budget)",
            )
            st.plotly_chart(fig_bump, use_container_width=True)

    # ── Tab 6: Data Table ────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<div class="section-title">Raw Budget Data (₹ Crores)</div>', unsafe_allow_html=True)

        display_df = df_filtered.copy()
        # Add total row
        total_row = {"Ministry/Department": "📊 TOTAL"}
        for y in selected_years:
            total_row[y] = display_df[y].sum()
        total_df = pd.concat([display_df, pd.DataFrame([total_row])], ignore_index=True)

        st.dataframe(
            total_df.style.format(
                {y: "₹{:,.0f}" for y in selected_years}
            ).set_properties(**{"text-align": "right"}).set_properties(
                subset=["Ministry/Department"], **{"text-align": "left", "font-weight": "bold"}
            ),
            use_container_width=True,
            height=min(600, (len(total_df) + 1) * 38),
        )

        csv = total_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="india_budget_analysis.csv",
            mime="text/csv",
        )

else:
    st.warning("⚠️ Please select at least one year and one ministry from the sidebar to start analysis.")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#6366f1; font-size:0.8rem; padding:1rem;'>"
    "📊 Indian Union Budget Analyzer &nbsp;|&nbsp; Data covers FY 2013-14 to 2023-24 &nbsp;|&nbsp; "
    "Values in ₹ Crores (Budget Estimates)"
    "</div>",
    unsafe_allow_html=True,
)
