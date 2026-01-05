import streamlit as st
import importlib.util
import sys
from utils import load_css
from pathlib import Path

# Настройка страницы
st.set_page_config(
    page_title="Веб-приложение по анализу данных",
    page_icon="🚀",
    layout="wide"
)


# Загрузка CSS из файла
load_css("assets/main.css")

# Заголовок приложения
st.title("🚀 Платформа для исследования данных")
st.markdown("---")


def safe_import_page(module_name, page_path):
    """Безопасная загрузка модуля страницы"""
    try:
        # Создаем спецификацию модуля
        spec = importlib.util.spec_from_file_location(module_name, page_path)
        if spec is None:
            raise ImportError(f"Не удалось загрузить спецификацию для {page_path}")

        # Создаем модуль
        module = importlib.util.module_from_spec(spec)

        # Добавляем в sys.modules для предотвращения повторной загрузки
        sys.modules[module_name] = module

        # Выполняем модуль
        spec.loader.exec_module(module)
        return module
    except FileNotFoundError:
        st.error(f"Файл {page_path} не найден")
        return None
    except Exception as e:
        st.error(f"Ошибка загрузки модуля {module_name}: {str(e)}")
        return None


# Создаем табы
tab1, tab2, tab3 = st.tabs([
    "📊 Анализ данных",
    "📈 Метрики и статистики",
    "🔧 Визуализация",
])

# Инициализация session state для обмена данными между страницами
if 'shared_data' not in st.session_state:
    st.session_state.shared_data = {
        'df': None,
        'uploaded_file': None,
        'charts': []
    }

# Загружаем содержимое каждой страницы
with tab1:
    st.subheader("📊 Анализ и обработка данных")

    # Безопасная загрузка страницы анализа данных
    page_path = Path("pages/data_analysis.py")
    if page_path.exists():
        try:
            # Динамический импорт модуля
            module_name = "data_analysis"
            spec = importlib.util.spec_from_file_location(module_name, page_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Вызываем основную функцию страницы, если она существует
            if hasattr(module, 'render'):
                module.render()
            else:
                # Если нет функции render, импортируем напрямую
                from pages.data_analysis import render

                render()
        except Exception as e:
            st.error(f"Ошибка загрузки страницы анализа данных: {e}")
            st.info("Используется базовый функционал")
            st.write("Загрузите файл для анализа данных...")
            uploaded_file = st.file_uploader("Выберите файл", type=['csv', 'xlsx'])
            if uploaded_file:
                st.session_state.shared_data['uploaded_file'] = uploaded_file
                st.success(f"Файл {uploaded_file.name} успешно загружен!")
    else:
        st.warning("Файл pages/data_analysis.py не найден")
        st.info("Создайте файл `pages/data_analysis.py` с функцией `render()`")

with tab2:
    st.subheader("📈 Метрики и статистики")

    page_path = Path("pages/metrics.py")
    if page_path.exists():
        try:
            module_name = "metrics"
            spec = importlib.util.spec_from_file_location(module_name, page_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'render'):
                module.render()
            else:
                from pages.metrics import render

                render()
        except Exception as e:
            st.error(f"Ошибка загрузки страницы метрик: {e}")

            # Показываем базовые метрики
            if st.session_state.shared_data.get('uploaded_file'):
                st.info(f"Загружен файл: {st.session_state.shared_data['uploaded_file'].name}")
            else:
                st.info("Нет загруженных данных для анализа")
    else:
        st.warning("Файл pages/metrics.py не найден")

with tab3:
    st.subheader("🔧 Визуализация данных")

    page_path = Path("pages/visualization.py")
    if page_path.exists():
        try:
            module_name = "visualization"
            spec = importlib.util.spec_from_file_location(module_name, page_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'render'):
                module.render()
            else:
                from pages.visualization import render

                render()
        except Exception as e:
            st.error(f"Ошибка загрузки страницы визуализации: {e}")

            # Базовый функционал визуализации
            st.info("Создайте интерактивные графики на основе загруженных данных")
    else:
        st.warning("Файл pages/visualization.py не найден")

# Футер приложения
st.markdown("---")
st.markdown("**Исследовательский анализ данных** v.1.0")