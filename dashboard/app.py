import json
import math
import os
import textwrap
from pathlib import Path

import streamlit as st
import plotly.express as px

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - fallback for older SDKs
    OpenAI = None
    import openai
else:  # pragma: no cover
    openai = None  # type: ignore

try:  # pragma: no cover - Python ≥ 3.11
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - fallback para versiones anteriores
    import tomli as tomllib  # type: ignore


APP_DIR = Path(__file__).resolve().parent
SECRET_CANDIDATES = [
    APP_DIR / ".streamlit" / "secrets.toml",
    APP_DIR.parent / ".streamlit" / "secrets.toml",
    Path.home() / ".streamlit" / "secrets.toml",
]


def load_secret_from_files() -> dict[str, str]:
    """Lee la primera coincidencia de secrets.toml y devuelve sus pares clave/valor."""
    for candidate in SECRET_CANDIDATES:
        if candidate.exists():
            try:
                data = tomllib.loads(candidate.read_text(encoding="utf-8"))
                return {k: str(v) for k, v in data.items()}
            except Exception:
                continue
    return {}

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

        .chat-wrapper {{
            position: sticky;
            top: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .chat-card {{
            background: {PALETTE['surface']};
            border-radius: 20px;
            border: 1px solid rgba(15, 23, 42, 0.07);
            box-shadow: 0 24px 50px rgba(15, 23, 42, 0.08);
            padding: 1.6rem 1.8rem;
        }}

        .chat-title {{
            margin: 0;
            font-size: 1.1rem;
            font-weight: 600;
            color: {PALETTE['primary']};
        }}

        .chat-caption {{
            margin: 0.4rem 0 1.2rem 0;
            font-size: 0.88rem;
            color: rgba(15, 23, 42, 0.66);
        }}

        [data-testid="stChatMessageUser"] > div,
        [data-testid="stChatMessageAssistant"] > div {{
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(15, 23, 42, 0.05);
            border-radius: 16px;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.05);
        }}

        [data-testid="stChatInput"] {{
            background: {PALETTE['surface']};
            border-top: 1px solid rgba(15, 23, 42, 0.06);
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Utilidades para el chat con LLM ---------------------------------------------------------

def build_gapminder_context(df) -> dict:
    """Genera un resumen serializable en JSON del dataframe filtrado."""

    def _safe_number(value):
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if math.isnan(number) or math.isinf(number):
            return None
        return number

    context: dict[str, object] = {
        "meta": {
            "rows": int(df.shape[0]),
            "unique_countries": int(df["country"].nunique()) if "country" in df.columns else None,
            "continent_distribution": {},
        },
        "numeric_stats": [],
        "top_countries_by_population": [],
        "sample_rows": [],
    }

    if "continent" in df.columns and not df.empty:
        context["meta"]["continent_distribution"] = {
            str(name): int(count)
            for name, count in df["continent"].value_counts().sort_index().items()
        }

    if context["meta"]["rows"] == 0:
        context["meta"]["note"] = "El dataframe filtrado está vacío para los filtros actuales."
        return context

    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        stats = df[col].agg(["mean", "median", "min", "max"])
        context["numeric_stats"].append(
            {
                "column": col,
                "mean": _safe_number(stats.get("mean")),
                "median": _safe_number(stats.get("median")),
                "min": _safe_number(stats.get("min")),
                "max": _safe_number(stats.get("max")),
            }
        )

    if not df.empty:
        sample_json = df.head(5).to_json(orient="records")
        context["sample_rows"] = json.loads(sample_json)

        full_json = df.to_json(orient="records")
        try:
            context["dataset_records"] = json.loads(full_json)
        except json.JSONDecodeError:
            context["dataset_records"] = []

    key_columns = {"country", "continent", "lifeExp", "gdpPercap", "pop"}
    if key_columns.issubset(df.columns):
        top_df = df.sort_values("pop", ascending=False).head(5)
        context["top_countries_by_population"] = json.loads(top_df.to_json(orient="records"))
    else:
        top_df = df.head(5)
        context["top_countries_by_population"] = json.loads(top_df.to_json(orient="records"))

    return context


def ask_gapminder_llm(question: str, df) -> str:
    """Consulta el modelo de OpenAI con contexto del dataframe filtrado."""
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        file_secrets = load_secret_from_files()
        api_key = file_secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "No se encontró la clave de API de OpenAI. Configura `OPENAI_API_KEY` en tus "
            "variables de entorno o en `st.secrets` para habilitar la conversación."
        )

    context_data = build_gapminder_context(df)
    try:
        payload = json.dumps(
            {"context": context_data, "question": question},
            ensure_ascii=False,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        return f"No se pudo preparar el contexto para el modelo: {exc}"

    system_prompt = (
        "Eres un analista de datos que trabaja con información de Gapminder. "
        "Responde en español con explicaciones claras, apoyándote únicamente en el contexto "
        "entregado. Si la pregunta no puede resolverse con los datos filtrados, acláralo."
    )

    try:
        if OpenAI is not None:  # SDK nuevo
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "system",
                        "content": [
                            {"type": "input_text", "text": system_prompt}
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": payload}
                        ],
                    },
                ],
                temperature=0.2,
            )
            answer = getattr(response, "output_text", "").strip()
        else:  # SDK clásico
            openai.api_key = api_key
            completion = openai.ChatCompletion.create(  # type: ignore[attr-defined]
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": payload,
                    },
                ],
                temperature=0.2,
            )
            answer = completion["choices"][0]["message"]["content"].strip()

    except Exception as exc:  # pragma: no cover - manejo de red/SDK
        return f"No se pudo obtener una respuesta del modelo: {exc}"

    return answer or "El modelo no devolvió contenido."

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
    coloraxis_colorbar=dict(title="Esperanza de vida"),
)
heatmap_fig.update_xaxes(side="top")

main_col, chat_col = st.columns([2, 1], gap="large")

with main_col:
    st.markdown("<div class='chart-grid chart-grid--primary'>", unsafe_allow_html=True)
    with st.container():
        st.markdown(
            """
            <div class="chart-card">
                <h3 class="chart-title">Relación PBI vs. esperanza de vida</h3>
                <p class="chart-caption">Cada burbuja representa un país; el tamaño responde a la población del año seleccionado.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(scatter_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-grid chart-grid--secondary'>", unsafe_allow_html=True)
    with st.container():
        st.markdown(
            """
            <div class="chart-card">
                <h3 class="chart-title">Distribución de esperanza de vida</h3>
                <p class="chart-caption">Visualiza cómo se distribuyen los países según la esperanza de vida para el filtro aplicado.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(hist_fig, use_container_width=True)

    with st.container():
        st.markdown(
            """
            <div class="chart-card">
                <h3 class="chart-title">PBI per cápita promedio por continente</h3>
                <p class="chart-caption">Compara el nivel económico medio de cada continente para el año seleccionado.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    with st.container():
        st.markdown(
            """
            <div class="chart-card">
                <h3 class="chart-title">Heatmap de esperanza de vida</h3>
                <p class="chart-caption">Explora la evolución promedio por continente entre 1952 y 2007. Se ajusta al continente filtrado.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with chat_col:
    st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

    chat_signature = f"year={year_choice}|continent={continent_choice}|log={log_x_choice}"
    if st.session_state.get("_chat_signature") != chat_signature:
        st.session_state["chat_messages"] = []
        st.session_state["_chat_signature"] = chat_signature

    st.markdown(
        """
        <div class="chat-card">
            <h3 class="chat-title">Pregúntale al analista virtual</h3>
            <p class="chat-caption">Consulta al modelo sobre los indicadores visibles; se alimenta del dataframe filtrado actual.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.get("chat_messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu pregunta sobre Gapminder…"):
        st.session_state.setdefault("chat_messages", []).append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando al modelo…"):
                response_text = ask_gapminder_llm(prompt, filtered_df)
            st.markdown(response_text)

        st.session_state["chat_messages"].append({"role": "assistant", "content": response_text})

    st.markdown("</div>", unsafe_allow_html=True)
