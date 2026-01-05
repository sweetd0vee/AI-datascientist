import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

# Заголовок страницы
st.header("📊 Анализ данных и обработка файлов")

st.markdown("""
### Функционал AFQKJDSQ VTYTL;TH C DJP VJ;YJCNM
**Расшифровка:** Автоматизированная обработка файлов, качественный анализ данных, 
визуализация тенденций, трансформация и хранение с глубоким анализом файлов.

**Основные возможности:**
- 📁 Загрузка и обработка различных форматов файлов
- 🔍 Анализ и статистика данных
- 🧹 Очистка и преобразование данных
- 💾 Экспорт результатов
""")

# Разделитель
st.markdown("---")

# Создаем две колонки
col1, col2 = st.columns([2, 1])

with col1:
    # Загрузка файла
    uploaded_file = st.file_uploader(
        "Загрузите файл для анализа",
        type=['csv', 'xlsx', 'txt', 'json'],
        help="Поддерживаемые форматы: CSV, Excel, TXT, JSON"
    )

    if uploaded_file is not None:
        # Определяем тип файла и загружаем данные
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ CSV файл успешно загружен! Строк: {df.shape[0]}, Колонок: {df.shape[1]}")

            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
                st.success(f"✅ Excel файл успешно загружен! Строк: {df.shape[0]}, Колонок: {df.shape[1]}")

            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
                st.success(f"✅ JSON файл успешно загружен! Строк: {df.shape[0]}, Колонок: {df.shape[1]}")

            elif uploaded_file.name.endswith('.txt'):
                # Для текстовых файлов читаем как CSV с разделителем табуляции
                df = pd.read_csv(uploaded_file, delimiter='\t')
                st.success(f"✅ TXT файл успешно загружен! Строк: {df.shape[0]}, Колонок: {df.shape[1]}")

            # Показываем превью данных
            st.subheader("📋 Предпросмотр данных")
            st.dataframe(df.head(20), use_container_width=True)

            # Основная статистика
            st.subheader("📊 Основная статистика")
            stats_col1, stats_col2, stats_col3 = st.columns(3)

            with stats_col1:
                st.metric("Всего строк", df.shape[0])
            with stats_col2:
                st.metric("Всего колонок", df.shape[1])
            with stats_col3:
                missing_values = df.isnull().sum().sum()
                st.metric("Пропущенные значения", missing_values)

            # Детальная статистика для числовых колонок
            if df.select_dtypes(include=[np.number]).shape[1] > 0:
                st.subheader("📈 Статистика числовых данных")
                numeric_stats = df.describe()
                st.dataframe(numeric_stats, use_container_width=True)

            # Анализ пропущенных значений
            st.subheader("🔍 Анализ пропущенных значений")
            missing_df = pd.DataFrame({
                'Колонка': df.columns,
                'Тип данных': df.dtypes.values,
                'Пропущенные': df.isnull().sum().values,
                'Заполненность %': (100 - (df.isnull().sum() / len(df) * 100)).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)

            # Информация о типах данных
            st.subheader("🔧 Информация о типах данных")
            type_info = pd.DataFrame({
                'Колонка': df.columns,
                'Тип данных': df.dtypes,
                'Уникальные значения': [df[col].nunique() for col in df.columns]
            })
            st.dataframe(type_info, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Ошибка при обработке файла: {str(e)}")
    else:
        # Демо-данные если файл не загружен
        st.info("👆 Загрузите файл или используйте демо-данные для тестирования")

        if st.button("Сгенерировать демо-данные"):
            # Создаем демо-данные
            np.random.seed(42)
            dates = pd.date_range('2024-01-01', periods=100)
            demo_data = {
                'Дата': dates,
                'Продажи': np.random.randint(100, 1000, 100),
                'Клиенты': np.random.randint(10, 200, 100),
                'Температура': np.random.uniform(15, 30, 100).round(1),
                'Категория': np.random.choice(['A', 'B', 'C'], 100),
                'Прибыль': np.random.uniform(-50, 500, 100).round(2)
            }
            df = pd.DataFrame(demo_data)
            st.session_state['demo_data'] = df
            st.rerun()

        if 'demo_data' in st.session_state:
            df = st.session_state['demo_data']
            st.success(f"✅ Используются демо-данные. Строк: {df.shape[0]}, Колонок: {df.shape[1]}")

            st.subheader("📋 Предпросмотр демо-данных")
            st.dataframe(df.head(20), use_container_width=True)

with col2:
    st.subheader("⚙️ Инструменты обработки")

    # Опции для обработки данных
    if 'df' in locals() or ('demo_data' in st.session_state and uploaded_file is None):
        if uploaded_file is None and 'demo_data' in st.session_state:
            df = st.session_state['demo_data']

        # Фильтрация данных
        with st.expander("🔍 Фильтрация данных", expanded=False):
            if st.checkbox("Применить фильтр"):
                filter_column = st.selectbox("Колонка для фильтрации", df.columns)
                if df[filter_column].dtype in ['int64', 'float64']:
                    min_val = float(df[filter_column].min())
                    max_val = float(df[filter_column].max())
                    selected_range = st.slider(
                        "Диапазон значений",
                        min_val, max_val,
                        (min_val, max_val)
                    )
                    filtered_df = df[(df[filter_column] >= selected_range[0]) &
                                     (df[filter_column] <= selected_range[1])]
                else:
                    unique_values = df[filter_column].unique()
                    selected_values = st.multiselect(
                        "Выберите значения",
                        unique_values,
                        default=list(unique_values[:3]) if len(unique_values) > 3 else list(unique_values)
                    )
                    filtered_df = df[df[filter_column].isin(selected_values)]

                if st.button("Применить фильтр"):
                    df = filtered_df
                    st.success(f"✅ Данные отфильтрованы. Осталось строк: {len(df)}")

        # Очистка данных
        with st.expander("🧹 Очистка данных", expanded=False):
            if st.checkbox("Удалить дубликаты"):
                initial_rows = len(df)
                df = df.drop_duplicates()
                st.info(f"Удалено {initial_rows - len(df)} дубликатов")

            if st.checkbox("Заполнить пропущенные значения"):
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if df[col].isnull().any():
                        df[col] = df[col].fillna(df[col].median())
                st.success("✅ Пропущенные значения заполнены")

        # Преобразование данных
        with st.expander("🔄 Преобразование данных", expanded=False):
            transform_option = st.selectbox(
                "Операция",
                ["Нормализация", "Логарифмирование", "Стандартизация"]
            )

            if st.button("Применить преобразование"):
                st.info(f"Применено: {transform_option}")
                # Здесь можно добавить реальную логику преобразования

        # Экспорт данных
        with st.expander("💾 Экспорт данных", expanded=False):
            export_format = st.radio(
                "Формат экспорта",
                ["CSV", "Excel", "JSON"]
            )

            if st.button("Экспортировать данные"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                if export_format == "CSV":
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Скачать CSV",
                        data=csv,
                        file_name=f"data_export_{timestamp}.csv",
                        mime="text/csv"
                    )
                elif export_format == "Excel":
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Data')
                    st.download_button(
                        label="📥 Скачать Excel",
                        data=output.getvalue(),
                        file_name=f"data_export_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                elif export_format == "JSON":
                    json_str = df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="📥 Скачать JSON",
                        data=json_str,
                        file_name=f"data_export_{timestamp}.json",
                        mime="application/json"
                    )

# Информационная панель
st.markdown("---")
st.subheader("📈 Быстрый анализ")

if 'df' in locals() or ('demo_data' in st.session_state):
    if uploaded_file is None and 'demo_data' in st.session_state:
        df = st.session_state['demo_data']

    # Показываем ключевые метрики
    cols = st.columns(4)
    with cols[0]:
        st.metric("Всего записей", len(df))
    with cols[1]:
        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
        st.metric("Числовых колонок", numeric_cols)
    with cols[2]:
        categorical_cols = len(df.select_dtypes(include=['object']).columns)
        st.metric("Категориальных колонок", categorical_cols)
    with cols[3]:
        date_cols = len(df.select_dtypes(include=['datetime64']).columns)
        st.metric("Колонок с датами", date_cols)

# Подсказки для пользователя
with st.expander("💡 Советы по использованию", expanded=False):
    st.markdown("""
    1. **Загрузка данных**: Поддерживаются CSV, Excel, JSON и TXT файлы
    2. **Анализ**: Автоматически рассчитывается статистика для числовых данных
    3. **Очистка**: Удаляйте дубликаты и заполняйте пропущенные значения
    4. **Экспорт**: Сохраняйте обработанные данные в нужном формате
    5. **Фильтрация**: Используйте слайдеры для фильтрации числовых данных
    """)