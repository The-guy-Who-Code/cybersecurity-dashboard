import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CyberSecurity Threat Analysis", layout="wide")
st.title("CyberSecurity Threat Analysis")
st.markdown("Analysis of global cybersecurity threats, vulnerabilities and malicious activity")

# load data
df_threat = pd.read_csv("1_otx_threat_intel.csv")
df_cve = pd.read_csv("2_cve_vulnerabilities.csv")
df_domains = pd.read_csv("3_malicious_domains.csv")
df_ips = pd.read_csv("4_malicious_ips.csv")

# sidebar
st.sidebar.title("Filters")
selected_dataset = st.sidebar.selectbox(
    "Select Dataset",
    ["Malicious IPs", "Vulnerabilities", "Threat Intel", "Domains"]
)
st.sidebar.metric("Total IPs", len(df_ips))
st.sidebar.metric("Total CVEs", len(df_cve))
st.sidebar.metric("Total Threats", len(df_threat))
st.sidebar.metric("Total Domains", len(df_domains))

# charts — only show selected
if selected_dataset == "Malicious IPs":
    st.subheader("Countries with Most Malicious IPs")
    country_df = df_ips["Country"].value_counts().head(10).reset_index()
    country_df.columns = ["Country", "count"]
    fig = px.bar(country_df, x="count", y="Country",
                 orientation="h", color="count",
                 color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True, key="ip_chart")

elif selected_dataset == "Vulnerabilities":
    st.subheader("Vendors with Most Vulnerabilities")
    vendor_df = df_cve["vendorProject"].value_counts().head(10).reset_index()
    vendor_df.columns = ["vendor", "count"]
    fig = px.bar(vendor_df, x="count", y="vendor",
                 orientation="h", color="count",
                 color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True, key="cve_chart")

elif selected_dataset == "Threat Intel":
    st.subheader("Most Targeted Industries")
    industry_df = df_threat["Industries"].value_counts().head(11).reset_index()
    industry_df.columns = ["Industry", "count"]
    industry_df = industry_df[industry_df["Industry"] != "Unknown"]
    fig = px.bar(industry_df, x="count", y="Industry",
                 orientation="h", color="count",
                 color_continuous_scale="Greens")
    st.plotly_chart(fig, use_container_width=True, key="threat_chart")

elif selected_dataset == "Domains":
    st.subheader("Malicious Domains - Ransomware Usage")
    ransomware_df = df_cve["knownRansomwareCampaignUse"].value_counts().reset_index()
    ransomware_df.columns = ["type", "count"]
    fig = px.pie(ransomware_df, values="count", names="type",
                 color_discrete_sequence=["#ff4444", "#333333"])
    st.plotly_chart(fig, use_container_width=True, key="domain_chart")