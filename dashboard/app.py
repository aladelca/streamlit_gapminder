import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Demo Gapminder", page_icon="📊", layout="wide")

# Dataset base
_df = px.data.gapminder()

# Paleta minimalista
PALETTE = {
    "background": "#F7F9FC",
    "surface": "#FFFFFF",
    "primary": "#0F172A",
    "accent": "#38BDF8",
    "muted": "#94A3B8",
}

st.markdown(
    f"""
    <style>
        body {{
            font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: {PALETTE['background']};
            color: {PALETTE['primary']};
        }}

        [data-testid="stAppViewContainer"] {{
            background: {PALETTE['background']};
            padding-bottom: 3rem;
        }}

        [data-testid="block-container"] {{
            max-width: 1100px;
            padding-top: 3rem;
        }}

        .hero-card {{
            background: {PALETTE['surface']};
            border-radius: 24px;
            padding: 2.2rem 2.8rem;
            border: 1px solid rgba(15, 23, 42, 0.06);
            box-shadow: 0 30px 70px rgba(15, 23, 42, 0.08);
        }}

        .hero-eyebrow {{
            font-size: 0.75rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: {PALETTE['muted']};
        }}

        .hero-title {{
            margin: 0.45rem 0 0.6rem 0;
            font-size: 2.5rem;
            font-weight: 700;
            color: {PALETTE['primary']};
        }}

        .hero-subtitle {{
            margin: 0;
            color: rgba(15, 23, 42, 0.7);
            font-size: 1rem;
        }}

        .controls-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-top: 2.5rem;
        }}

        .control-card {{
            background: {PALETTE['surface']};
            border-radius: 18px;
            padding: 1.6rem 1.8rem;
            border: 1px solid rgba(15, 23, 42, 0.06);
            box-shadow: 0 20px 55px rgba(15, 23, 42, 0.06);
        }}

        .control-label {{
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {PALETTE['muted']};
            margin-bottom: 0.75rem;
            display: block;
        }}

        .chart-grid {{
            display: grid;
            gap: 1.5rem;
            margin-top: 3rem;
        }}

        .chart-grid--primary {{
            grid-template-columns: 1fr;
        }}

        .chart-grid--secondary {{
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        }}

        .chart-card {{
            background: {PALETTE['surface']};
            border-radius: 22px;
            padding: 1.8rem 2rem;
            border: 1px solid rgba(15, 23, 42, 0.06);
            box-shadow: 0 28px 60px rgba(15, 23, 42, 0.07);
        }}

        .chart-title {{
            margin: 0;
            font-size: 1.15rem;
            font-weight: 600;
            color: {PALETTE['primary']};
        }}

        .chart-caption {{
            margin: 0.35rem 0 1.2rem 0;
            font-size: 0.9rem;
            color: rgba(15, 23, 42, 0.65);
        }}

        div[data-baseweb="select"] > div {{
            border-radius: 12px !important;
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: rgba(56, 189, 248, 0.08);
        }}

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="select"] > div:focus-within {{
            border-color: rgba(56, 189, 248, 0.9);
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25);
        }}

        [data-testid="stSlider"] > div {{
            padding-top: 0 !important;
        }}

        [data-testid="stSlider"] div[data-baseweb="slider"] > div:nth-child(1) {{
            background: rgba(15, 23, 42, 0.08);
            height: 6px;
        }}

        [data-testid="stSlider"] div[data-baseweb="slider"] > div:nth-child(2) {{
            background: linear-gradient(90deg, {PALETTE['accent']}, {PALETTE['primary']});
            height: 6px;
        }}

        [data-testid="stSlider"] div[role="slider"] {{
            border: 0 !important;
            background: {PALETTE['surface']};
            box-shadow: 0 0 0 6px rgba(56, 189, 248, 0.3);
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Encabezado con estética minimalista
_, header_col, _ = st.columns([1, 6, 1])
with header_col:
    st.markdown(
        """
        <div class="hero-card">
            <span class="hero-eyebrow">Gapminder</span>
            <h1 class="hero-title">Panorama Demográfico</h1>
            <p class="hero-subtitle">Explora la relación entre PBI per cápita y esperanza de vida filtrando por año y continente.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='controls-grid'>", unsafe_allow_html=True)

col_year, col_continent, col_scale = st.columns(3)

with col_year:
    st.markdown("<div class='control-card'>", unsafe_allow_html=True)
    st.markdown("<span class='control-label'>Año</span>", unsafe_allow_html=True)
    year_choice = st.slider(
        "Año",
        min_value=1952,
        max_value=2007,
        step=5,
        value=2007,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_continent:
    st.markdown("<div class='control-card'>", unsafe_allow_html=True)
    st.markdown("<span class='control-label'>Continente</span>", unsafe_allow_html=True)
    continent_choice = st.selectbox(
        "Continente",
        tuple(["Todos"] + sorted(_df["continent"].unique())),
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_scale:
    st.markdown("<div class='control-card'>", unsafe_allow_html=True)
    st.markdown("<span class='control-label'>Escala</span>", unsafe_allow_html=True)
    log_x_choice = st.toggle("Usar escala logarítmica", value=False)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if continent_choice != "Todos":
    filtered_df = _df[_df["continent"] == continent_choice]
    filtered_df = filtered_df[filtered_df["year"] == year_choice]
else:
    filtered_df = _df[_df["year"] == year_choice]

# Figuras
scatter_fig = px.scatter(
    filtered_df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=log_x_choice,
    size_max=60,
    labels={
        "gdpPercap": "PBI per cápita",
        "lifeExp": "Esperanza de vida",
        "continent": "Continente",
    },
    color_discrete_sequence=px.colors.qualitative.Set2,
)
scatter_fig.update_layout(
    plot_bgcolor=PALETTE["surface"],
    paper_bgcolor=PALETTE["surface"],
    font=dict(color=PALETTE["primary"]),
    margin=dict(l=20, r=20, t=60, b=40),
    legend_title="Continente",
)
scatter_fig.update_traces(marker=dict(line=dict(width=0.5, color="white")))

hist_fig = px.histogram(
    filtered_df,
    x="lifeExp",
    nbins=20,
    opacity=0.85,
    labels={"lifeExp": "Esperanza de vida"},
    color_discrete_sequence=[PALETTE["accent"]],
)
hist_fig.update_layout(
    plot_bgcolor=PALETTE["surface"],
    paper_bgcolor=PALETTE["surface"],
    font=dict(color=PALETTE["primary"]),
    margin=dict(l=20, r=20, t=60, b=40),
    showlegend=False,
    bargap=0.08,
)

continent_summary = (
    _df[_df["year"] == year_choice]
    .groupby("continent", as_index=False)["gdpPercap"]
    .mean()
    .sort_values("gdpPercap", ascending=False)
)
continent_summary["Seleccionado"] = continent_summary["continent"].eq(continent_choice)

bar_fig = px.bar(
    continent_summary,
    x="continent",
    y="gdpPercap",
    color="Seleccionado",
    color_discrete_map={
        True: PALETTE["accent"],
        False: PALETTE["muted"],
    },
    labels={"continent": "Continente", "gdpPercap": "PBI per cápita"},
)
bar_fig.update_layout(
    plot_bgcolor=PALETTE["surface"],
    paper_bgcolor=PALETTE["surface"],
    font=dict(color=PALETTE["primary"]),
    margin=dict(l=20, r=20, t=60, b=40),
    showlegend=False,
)

heat_source = _df[_df["year"].between(1952, 2007)]
if continent_choice != "Todos":
    heat_source = heat_source[heat_source["continent"] == continent_choice]

heatmap_table = (
    heat_source
    .pivot_table(index="continent", columns="year", values="lifeExp", aggfunc="mean")
    .sort_index()
)
heatmap_table = heatmap_table.reindex(sorted(heatmap_table.columns), axis=1)
heatmap_table.columns = heatmap_table.columns.astype(str)

heatmap_fig = px.imshow(
    heatmap_table,
    aspect="auto",
    color_continuous_scale="Blues",
    labels={"color": "Esperanza de vida", "x": "Año", "y": "Continente"},
)
heatmap_fig.update_layout(
    plot_bgcolor=PALETTE["surface"],
    paper_bgcolor=PALETTE["surface"],
    font=dict(color=PALETTE["primary"]),
    margin=dict(l=20, r=20, t=60, b=40),
    coloraxis_colorbar=dict(title="Años"),
)
heatmap_fig.update_xaxes(side="top")

st.markdown("<div class='chart-grid chart-grid--primary'>", unsafe_allow_html=True)
with st.container():
    st.markdown(
        """
        <div class="chart-card">
            <h3 class="chart-title">Relación PBI vs. esperanza de vida</h3>
            <p class="chart-caption">Cada burbuja representa un país; el tamaño responde a la población del año seleccionado.</p>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(scatter_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='chart-grid chart-grid--secondary'>", unsafe_allow_html=True)
with st.container():
    st.markdown(
        """
        <div class="chart-card">
            <h3 class="chart-title">Distribución de esperanza de vida</h3>
            <p class="chart-caption">Visualiza cómo se distribuyen los países según la esperanza de vida para el filtro aplicado.</p>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(hist_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown(
        """
        <div class="chart-card">
            <h3 class="chart-title">PBI per cápita promedio por continente</h3>
            <p class="chart-caption">Compara el nivel económico medio de cada continente para el año seleccionado.</p>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(bar_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown(
        """
        <div class="chart-card">
            <h3 class="chart-title">Heatmap de esperanza de vida</h3>
            <p class="chart-caption">Explora la evolución promedio por continente entre 1952 y 2007. Se ajusta al continente filtrado.</p>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
