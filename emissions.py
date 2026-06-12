import pandas as pd
import streamlit as st
import plotly.express as px
emissions = pd.read_csv("co2_emissions_yearly.csv")




st.set_page_config(page_title="Carbon Emissions Yearly", layout="wide")
st.title("Carbon Emissions Yearly")

#sidebar
st.sidebar.title("Filters")
selected_database = st.sidebar.selectbox(
    "Select view",
    ["Countries","Emissions Per Capita","Years","Population in Millions"]
)

st.sidebar.metric("Total Countries", emissions["country"].nunique())
st.sidebar.metric("Years Covered", f"{emissions['year'].min()} - {emissions['year'].max()}")
st.sidebar.metric("Total Records", len(emissions))

# Chart->1
if selected_database == "Countries":
    st.subheader("Countries with Most Emissions")
    countries_df = emissions.groupby("country")["co2_emissions_mt"].sum().reset_index()
    countries_df = countries_df.sort_values("co2_emissions_mt", ascending=False).head(10)
    fig = px.bar(countries_df, x="co2_emissions_mt", y="country",
                 orientation="h", color="co2_emissions_mt",
                 color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True, key="countries_chart")

elif selected_database == "Emissions Per Capita":
    st.subheader("Emissions per Capita")
    per_capita_df = emissions.groupby("country")["co2_per_capita_t"].mean().reset_index()
    per_capita_df = per_capita_df.sort_values("co2_per_capita_t", ascending=False).head(10)
    fig = px.bar(per_capita_df, x="co2_per_capita_t", y="country",
                 orientation="h", color="co2_per_capita_t",
                 color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True, key="per_capita_chart")

elif selected_database == "Years":
    st.subheader("Global Emissions Over Time")
    yearly_df = emissions.groupby("year")["co2_emissions_mt"].sum().reset_index()
    fig = px.line(yearly_df, x="year", y="co2_emissions_mt",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True, key="years_chart")

elif selected_database == "Population in Millions":
    st.subheader("Population vs Emissions")
    pop_df = emissions.groupby("country")[["population_millions", "co2_emissions_mt"]].mean().reset_index()
    fig = px.scatter(pop_df, x="population_millions", y="co2_emissions_mt",
                     hover_name="country",
                     color="co2_emissions_mt",
                     color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True, key="population_chart")