import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="تحليل المحاضرات", layout="wide")

BG_COLOR = "#0B0C2A"
CARD_COLOR = "#1F2A40"
LINE_COLOR = "#00B4D8"
ACCENT_COLOR = "#A020F0"
SOFT_COLOR = "#C77DFF"
LIGHT_COLOR = "#72EFDD"

st.markdown(
    f"""
    <style>
    body {{
        background-color: {BG_COLOR};
        color: white;
        font-family: "Cairo", sans-serif;
    }}
    .metric-card {{
        background-color: {CARD_COLOR};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: 0.3s;
        color: white;
    }}
    .metric-card:hover {{
        background-color: {ACCENT_COLOR};
        cursor: pointer;
        transform: scale(1.03);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

file_path = r"D:\TRAINING DEPT\2025\10-2025\TRAINING DEPT MANAGEMENTS\TRAINERS MONTHLY REPORT\تحليل_المحاضرات.xlsx"

@st.cache_data
def load_data():
    sheets = ["تحليل_بالمدرب", "تحليل_بالقطاع", "تحليل_باليوم", "تحليل_بالموقع", "التوتال"]
    data = {sheet: pd.read_excel(file_path, sheet_name=sheet) for sheet in sheets}

    for key in data.keys():
        df = data[key]
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        data[key] = df
    return data

data = load_data()

totals = data["التوتال"].iloc[0]
total_visits = int(totals["زيارات_تمت"])
total_trainers = int(totals["إجمالي_عدد_المتدربين"])
total_hours = float(totals["إجمالي_ساعات_التدريب"])
total_pct = round(float(totals["نسبة_تحقيق_الهدف_%"]), 1) if totals["نسبة_تحقيق_الهدف_%"] else 0

st.markdown("## لوحة التحكم - تحليل المحاضرات")

col1, col2, col3, col4 = st.columns(4)

if "view" not in st.session_state:
    st.session_state.view = "main"

with col1:
    if st.button("إجمالي الساعات"):
        st.session_state.view = "hours"
    st.markdown(f"<div class='metric-card'><h3>إجمالي الساعات</h3><h2>{total_hours:.1f}</h2></div>", unsafe_allow_html=True)

with col2:
    if st.button("عدد المتدربين"):
        st.session_state.view = "trainers"
    st.markdown(f"<div class='metric-card'><h3>عدد المتدربين</h3><h2>{total_trainers}</h2></div>", unsafe_allow_html=True)

with col3:
    if st.button("عدد الزيارات"):
        st.session_state.view = "visits"
    st.markdown(f"<div class='metric-card'><h3>عدد الزيارات</h3><h2>{total_visits}</h2></div>", unsafe_allow_html=True)

with col4:
    if st.button("نسبة الهدف"):
        st.session_state.view = "pct"
    st.markdown(f"<div class='metric-card'><h3>نسبة تحقيق الهدف</h3><h2>{total_pct}%</h2></div>", unsafe_allow_html=True)

view = st.session_state.view

df_trainers = data["تحليل_بالمدرب"]
df_sector = data["تحليل_بالقطاع"]
df_location = data["تحليل_بالموقع"]
df_day = data["تحليل_باليوم"]

if view == "hours":
    value_col = "إجمالي_ساعات_التدريب"
elif view == "trainers":
    value_col = "إجمالي_عدد_المتدربين"
elif view == "visits":
    value_col_trainers = "زيارات_تمت"
    value_col_sector = "زيارات_تمت"
    value_col_location = "إجمالي_الزيارات_تمت"
    value_col_day = "إجمالي_الزيارات_تمت"
else:  # pct
    value_col = "نسبة_تحقيق_الهدف_%"

if view != "main":
    st.markdown("---")
    st.markdown(f"## تفاصيل: {view}")

    colA, colB = st.columns(2)
    colC, colD = st.columns(2)

    if view != "visits":
        y_col = value_col
    else:
        y_col = value_col_trainers
    fig1 = px.bar(
        df_trainers,
        x="اسم_المدرب",
        y=y_col,
        text=y_col,
        color="اسم_المدرب",
        color_discrete_sequence=[LINE_COLOR, SOFT_COLOR, ACCENT_COLOR, LIGHT_COLOR]
    )
    fig1.update_traces(texttemplate='%{text}', textposition='outside')
    fig1.update_layout(title="الكباتن", plot_bgcolor=CARD_COLOR, paper_bgcolor=CARD_COLOR, font_color="white")
    colA.plotly_chart(fig1, use_container_width=True)

    y_col_sec = value_col_sector if view == "visits" else value_col
    fig2 = px.pie(
        df_sector,
        names="القطاع",
        values=y_col_sec,
        color_discrete_sequence=[LINE_COLOR, SOFT_COLOR, ACCENT_COLOR, LIGHT_COLOR],
        hover_data=[y_col_sec]
    )
    fig2.update_traces(textinfo='value+label')
    fig2.update_layout(title="القطاعات", paper_bgcolor=CARD_COLOR, font_color="white")
    colB.plotly_chart(fig2, use_container_width=True)

    if view != "pct":
        x_col_loc = value_col_location if view == "visits" else value_col
        fig3 = px.bar(
            df_location,
            y="الموقع",
            x=x_col_loc,
            orientation="h",
            text=x_col_loc,
            color_discrete_sequence=[LINE_COLOR]
        )
        fig3.update_traces(texttemplate='%{text}', textposition='outside')
        fig3.update_layout(title="المواقع", paper_bgcolor=CARD_COLOR, plot_bgcolor=CARD_COLOR, font_color="white")
        colC.plotly_chart(fig3, use_container_width=True)

        y_col_d = value_col_day if view == "visits" else value_col
        fig4 = px.line(
            df_day,
            x="تاريخ_الزيارة",
            y=y_col_d,
            markers=True,
            line_shape="spline",
            color_discrete_sequence=[LINE_COLOR]
        )
        fig4.update_layout(title="الأيام", paper_bgcolor=CARD_COLOR, plot_bgcolor=CARD_COLOR, font_color="white")
        colD.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("### جدول الأيام")
    st.dataframe(df_day.style.background_gradient(cmap="PuBu"), use_container_width=True)

    st.markdown("### جدول المواقع")
    st.dataframe(df_location.style.background_gradient(cmap="BuGn"), use_container_width=True)

else:
    st.markdown("---")
    st.markdown("## الجداول التحليلية")
    colL, colR = st.columns(2)
    with colL:
        st.markdown("### الأيام")
        st.dataframe(df_day.style.background_gradient(cmap="PuBu"), use_container_width=True)
    with colR:
        st.markdown("### المواقع")
        st.dataframe(df_location.style.background_gradient(cmap="BuGn"), use_container_width=True)
