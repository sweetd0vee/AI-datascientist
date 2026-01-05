import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.header("📈 Визуализация данных")

st.markdown("""
### Интерактивные графики и диаграммы
Создавайте красивые и информативные визуализации для анализа данных.
""")

# Проверяем наличие данных
if 'demo_data' in st.session_state:
    df = st.session_state['demo_data']
    st.success("✅ Используются демо-данные для визуализации")
else:
    # Создаем демо-данные если их нет
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=100)
    demo_data = {
        'Дата': dates,
        'Продажи': np.random.randint(100, 1000, 100),
        'Клиенты': np.random.randint(10, 200, 100),
        'Температура': np.random.uniform(15, 30, 100).round(1),
        'Категория': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Регион': np.random.choice(['Север', 'Юг', 'Восток', 'Запад'], 100),
        'Прибыль': np.random.uniform(-50, 500, 100).round(2)
    }
    df = pd.DataFrame(demo_data)
    st.session_state['demo_data'] = df
    st.info("📊 Созданы демо-данные для визуализации")

st.subheader("Данные для визуализации")
st.dataframe(df.head(10), use_container_width=True)

# Выбор типа графика
chart_type = st.selectbox(
    "Выберите тип графика",
    ["Линейный график", "Столбчатая диаграмма", "Круговая диаграмма",
     "Точечная диаграмма", "Гистограмма", "Box plot"]
)

# Выбор колонок для оси X и Y
col1, col2 = st.columns(2)
with col1:
    x_column = st.selectbox("Ось X", df.columns)
with col2:
    if chart_type != "Гистограмма" and chart_type != "Круговая диаграмма":
        y_column = st.selectbox("Ось Y", df.select_dtypes(include=[np.number]).columns)
    elif chart_type == "Гистограмма":
        y_column = st.selectbox("Ось Y (для гистограммы)", df.select_dtypes(include=[np.number]).columns)

# Дополнительные настройки
if chart_type in ["Столбчатая диаграмма", "Точечная диаграмма", "Линейный график"]:
    color_column = st.selectbox("Цветовая группировка (опционально)", ["Нет"] + list(df.columns))
    if color_column == "Нет":
        color_column = None

# Создание графика
if st.button("Создать график"):
    fig = None

    try:
        if chart_type == "Линейный график":
            if color_column:
                fig = px.line(df, x=x_column, y=y_column, color=color_column,
                              title=f"{y_column} по {x_column}")
            else:
                fig = px.line(df, x=x_column, y=y_column,
                              title=f"{y_column} по {x_column}")

        elif chart_type == "Столбчатая диаграмма":
            if color_column:
                fig = px.bar(df, x=x_column, y=y_column, color=color_column,
                             title=f"{y_column} по {x_column}")
            else:
                fig = px.bar(df, x=x_column, y=y_column,
                             title=f"{y_column} по {x_column}")

        elif chart_type == "Круговая диаграмма":
            value_counts = df[x_column].value_counts()
            fig = px.pie(values=value_counts.values, names=value_counts.index,
                         title=f"Распределение по {x_column}")

        elif chart_type == "Точечная диаграмма":
            if color_column:
                fig = px.scatter(df, x=x_column, y=y_column, color=color_column,
                                 title=f"{y_column} vs {x_column}")
            else:
                fig = px.scatter(df, x=x_column, y=y_column,
                                 title=f"{y_column} vs {x_column}")

        elif chart_type == "Гистограмма":
            fig = px.histogram(df, x=y_column, nbins=30,
                               title=f"Распределение {y_column}")

        elif chart_type == "Box plot":
            fig = px.box(df, x=x_column, y=y_column,
                         title=f"Box plot: {y_column} по {x_column}")

        if fig:
            # Настройка макета
            fig.update_layout(
                title_font_size=20,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Сохранение графика
            if st.button("Сохранить график как HTML"):
                fig.write_html("chart.html")
                st.success("График сохранен как chart.html")
    except Exception as e:
        st.error(f"Ошибка при создании графика: {e}")

# Множественные графики
st.subheader("📊 Множественные графики")
if st.checkbox("Показать несколько графиков одновременно"):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    selected_cols = st.multiselect(
        "Выберите колонки для отображения",
        numeric_cols.tolist(),
        default=numeric_cols.tolist()[:3] if len(numeric_cols) > 3 else numeric_cols.tolist()
    )

    if selected_cols:
        fig_multi = go.Figure()
        for col in selected_cols:
            fig_multi.add_trace(go.Scatter(
                x=df.index,
                y=df[col],
                mode='lines',
                name=col
            ))

        fig_multi.update_layout(
            title="Сравнение нескольких показателей",
            xaxis_title="Индекс",
            yaxis_title="Значение",
            hovermode='x unified'
        )
        st.plotly_chart(fig_multi, use_container_width=True)

# Статистические графики
st.subheader("📈 Статистические графики")
stats_option = st.selectbox(
    "Выберите статистический график",
    ["Корреляционная матрица", "Распределение данных", "Q-Q plot"]
)

if st.button("Показать статистический график"):
    if stats_option == "Корреляционная матрица":
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            fig_corr = px.imshow(corr_matrix,
                                 text_auto=True,
                                 aspect="auto",
                                 title="Корреляционная матрица")
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.warning("Недостаточно числовых колонок для корреляционной матрицы")

    elif stats_option == "Распределение данных":
        selected_col = st.selectbox(
            "Выберите колонку для анализа распределения",
            df.select_dtypes(include=[np.number]).columns
        )
        if selected_col:
            fig_dist = px.histogram(df, x=selected_col, nbins=30,
                                    marginal="box",
                                    title=f"Распределение {selected_col}")
            st.plotly_chart(fig_dist, use_container_width=True)