import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

df  = px.data.gapminder()
col1, col2, col3 = st.columns([5,5,20])

with col3:
    st.title("Demo")

year_col, continent_col, log_x_col = st.columns([5,5,5])

with year_col:
    year_choice = st.slider(
        "Año",
        min_value=1952,
        max_value=2007,
        step = 5,
        value = 2007
    )

with continent_col:
    continent_choice = st.selectbox(
        "Continente",
        tuple(['Todos'] + list(df["continent"].unique()))
    )


with log_x_col:
    log_x_choice = st.checkbox("Log X axis")

if continent_choice != "Todos":
    filtered_df = df[df["continent"]==continent_choice]
    filtered_df = filtered_df[filtered_df["year"]==year_choice]

else:
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df["year"]==year_choice]

fig = px.scatter(
    filtered_df,
    x = "gdpPercap",
    y = 'lifeExp',
    size = "pop",
    color = "continent",
    hover_name = "country",
    log_x = log_x_choice,
    size_max = 60
)

fig.update_layout(title = "PBI vs Expectativa de vida")

st.plotly_chart(fig, use_container_width=True)