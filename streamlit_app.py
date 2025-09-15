
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Нефтяной Дашборд", layout="wide")
st.title("📦 Нефтяной Дашборд – 2025")

# Load corrected data
df = pd.read_excel("Баланс_нефти_объединенный_исправлен.xlsx")
df["Дата"] = pd.to_datetime(df["Дата"], errors='coerce')

# Convert relevant columns to numeric
for col in [
    "Сдача нефти  на терминал",
    "Сдача нефти в КТО",
    "НПС Макат",
    "ПСП Карсак"
]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Sidebar: Month filter
months = sorted(df["Месяц"].dropna().unique())
selected_month = st.sidebar.selectbox("Выберите месяц", months)
filtered_df = df[df["Месяц"] == selected_month]

st.subheader(f"📆 Данные за {selected_month}")

# Monthly totals for validation
kto_total = filtered_df["Сдача нефти в КТО"].sum()
terminal_total = filtered_df["Сдача нефти  на терминал"].sum()

if kto_total > terminal_total:
    st.error(f"❌ В {selected_month} объем в КТО ({kto_total:.2f}) превышает объем на терминал ({terminal_total:.2f})")

# Plot 1: Terminal delivery
st.markdown("### 📈 Сдача нефти на терминал")
fig1 = px.line(filtered_df, x="Дата", y="Сдача нефти  на терминал")
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Delivery to KTO
st.markdown("### 🛢️ Сдача нефти в КТО (НПС Макат + ПСП Карсак)")
fig2 = px.line(filtered_df, x="Дата", y="Сдача нефти в КТО")
st.plotly_chart(fig2, use_container_width=True)

# Plot 3: KTO Components
st.markdown("### 🧪 Компоненты КТО: НПС Макат и ПСП Карсак")
fig3 = px.bar(filtered_df, x="Дата", y=["НПС Макат", "ПСП Карсак"])
st.plotly_chart(fig3, use_container_width=True)

# Data table
st.markdown("### 📋 Таблица данных")
st.dataframe(filtered_df)
