import os
import streamlit as st

# Загрузка CSS из файла
def load_css(css_path: str):
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        # Fallback к hardcoded CSS
        st.markdown("""
        <style>
            /* Минимальный CSS на случай отсутствия файла */
            .main-header {
                font-size: 2.5rem;
                color: #1E3A8A;
                text-align: center;
                padding: 20px 0;
            }
        </style>
        """, unsafe_allow_html=True)