import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="교실 냉난방 불편도 모니터링", page_icon="❄️", layout="wide")
st.title("🏫 교실 냉난방 불편도 모니터링 시스템")

DATA_FILE = "feedback_data.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["날짜", "교실", "온도(℃)", "불편도"])
    df.to_csv(DATA_FILE, index=False)

menu = st.sidebar.selectbox("메뉴 선택", ["학생 설문 입력", "관리자 대시보드"])

if menu == "학생 설문 입력":
    st.header("📋 교실 온도 및 불편도 입력")
    classroom = st.text_input("교실명을 입력하세요 (예: 2-3반)")
    temp = st.number_input("현재 교실 온도(℃)", min_value=0.0, max_value=50.0, step=0.5)
    discomfort = st.radio(
        "현재 온도에 대한 느낌을 선택하세요",
        ["너무 추움", "조금 추움", "적당", "조금 더움", "너무 더움"],
        horizontal=True
    )
    if st.button("제출하기"):
        if classroom and temp:
            new_data = pd.DataFrame({
                "날짜": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                "교실": [classroom],
                "온도(℃)": [temp],
                "불편도": [discomfort]
            })
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ 설문이 성공적으로 제출되었습니다!")
        else:
            st.warning("⚠️ 교실명과 온도를 모두 입력해주세요.")

elif menu == "관리자 대시보드":
    st.header("📊 불편도 현황 대시보드")
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        st.info("아직 제출된 데이터가 없습니다.")
    else:
        st.subheader("📅 최근 제출된 데이터")
        st.dataframe(df.tail(10))

        st.subheader("🌡 불편도 비율")
        fig = px.histogram(df, x="불편도", color="불편도", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🏫 교실별 평균 온도")
        avg_temp = df.groupby("교실")["온도(℃)"].mean().reset_index()
        fig2 = px.bar(avg_temp, x="교실", y="온도(℃)", color="온도(℃)", text_auto=".1f")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("💬 교실별 불편도 요약")
        discomfort_summary = df.groupby(["교실", "불편도"]).size().unstack(fill_value=0)
        st.dataframe(discomfort_summary)

