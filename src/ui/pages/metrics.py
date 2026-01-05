import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import hashlib

st.header("🔧 Инструменты и утилиты")

st.markdown("""
### Набор полезных инструментов для работы с данными
Различные утилиты для преобразования, анализа и работы с данными.
""")

# Создаем табы для различных инструментов
tool_tabs = st.tabs(["📝 Текст", "🔢 Числа", "📅 Даты", "🔄 Конвертер", "🔐 Безопасность"])

with tool_tabs[0]:  # Текст
    st.subheader("Текстовые инструменты")

    text_input = st.text_area("Введите текст", height=150)

    if text_input:
        col1, col2 = st.columns(2)

        with col1:
            st.write("📊 Статистика текста:")
            st.write(f"• Символов: {len(text_input)}")
            st.write(f"• Слов: {len(text_input.split())}")
            st.write(f"• Строк: {len(text_input.splitlines())}")

            if st.button("Удалить дубликаты строк"):
                lines = text_input.splitlines()
                unique_lines = list(dict.fromkeys(lines))
                st.text_area("Результат", "\n".join(unique_lines), height=150)

        with col2:
            operation = st.selectbox(
                "Операция с текстом",
                ["Верхний регистр", "Нижний регистр", "Удалить пробелы",
                 "Обратный порядок", "SHA-256 хеш"]
            )

            if st.button("Применить"):
                if operation == "Верхний регистр":
                    result = text_input.upper()
                elif operation == "Нижний регистр":
                    result = text_input.lower()
                elif operation == "Удалить пробелы":
                    result = text_input.replace(" ", "")
                elif operation == "Обратный порядок":
                    result = text_input[::-1]
                elif operation == "SHA-256 хеш":
                    result = hashlib.sha256(text_input.encode()).hexdigest()

                st.text_area("Результат", result, height=150)

with tool_tabs[1]:  # Числа
    st.subheader("Числовые инструменты")

    num_input = st.text_area("Введите числа (через запятую или с новой строки)", height=100)

    if num_input:
        try:
            # Парсим числа
            numbers = []
            for item in num_input.replace(',', '\n').split():
                try:
                    numbers.append(float(item))
                except:
                    continue

            if numbers:
                df_numbers = pd.DataFrame(numbers, columns=['Числа'])

                col1, col2 = st.columns(2)

                with col1:
                    st.write("📈 Базовая статистика:")
                    st.write(f"• Количество: {len(numbers)}")
                    st.write(f"• Сумма: {sum(numbers):.2f}")
                    st.write(f"• Среднее: {np.mean(numbers):.2f}")
                    st.write(f"• Медиана: {np.median(numbers):.2f}")
                    st.write(f"• Минимум: {min(numbers):.2f}")
                    st.write(f"• Максимум: {max(numbers):.2f}")
                    st.write(f"• Стандартное отклонение: {np.std(numbers):.2f}")

                with col2:
                    st.write("🔧 Операции:")
                    operation = st.selectbox(
                        "Выберите операцию",
                        ["Нормализация", "Логарифм", "Квадратный корень", "Округление"]
                    )

                    if st.button("Выполнить операцию"):
                        if operation == "Нормализация":
                            min_val = min(numbers)
                            max_val = max(numbers)
                            if max_val != min_val:
                                normalized = [(x - min_val) / (max_val - min_val) for x in numbers]
                                st.write("Нормализованные значения:")
                                st.write(normalized)

                        elif operation == "Логарифм":
                            log_numbers = [np.log(x) if x > 0 else None for x in numbers]
                            st.write("Натуральные логарифмы:")
                            st.write(log_numbers)

                        elif operation == "Квадратный корень":
                            sqrt_numbers = [np.sqrt(x) if x >= 0 else None for x in numbers]
                            st.write("Квадратные корни:")
                            st.write(sqrt_numbers)

                        elif operation == "Округление":
                            decimals = st.slider("Количество знаков", 0, 10, 2)
                            rounded = [round(x, decimals) for x in numbers]
                            st.write("Округленные значения:")
                            st.write(rounded)

        except Exception as e:
            st.error(f"Ошибка обработки чисел: {e}")

with tool_tabs[2]:  # Даты
    st.subheader("Инструменты для работы с датами")

    col1, col2 = st.columns(2)

    with col1:
        st.write("📅 Калькулятор дат")

        start_date = st.date_input("Начальная дата", datetime.now())
        days_to_add = st.number_input("Дней для добавления", value=7, min_value=-365, max_value=365)
        weeks_to_add = st.number_input("Недель для добавления", value=0, min_value=-52, max_value=52)

        if st.button("Рассчитать"):
            result_date = start_date + timedelta(days=days_to_add + weeks_to_add * 7)
            st.success(f"Результат: {result_date.strftime('%d.%m.%Y')}")

            # Дополнительная информация
            st.write(f"• День недели: {result_date.strftime('%A')}")
            st.write(f"• Номер недели: {result_date.isocalendar()[1]}")
            st.write(f"• Квартал: {(result_date.month - 1) // 3 + 1}")

    with col2:
        st.write("⏱️ Разница между датами")

        date1 = st.date_input("Первая дата", datetime.now())
        date2 = st.date_input("Вторая дата", datetime.now() + timedelta(days=30))

        if st.button("Рассчитать разницу"):
            difference = abs((date2 - date1).days)
            st.info(f"Разница: {difference} дней")
            st.write(f"• Недель: {difference // 7}")
            st.write(f"• Месяцев (приблизительно): {difference // 30}")
            st.write(f"• Лет (приблизительно): {difference // 365}")

with tool_tabs[3]:  # Конвертер
    st.subheader("Конвертер единиц измерения")

    conv_type = st.selectbox(
        "Тип конвертации",
        ["Длина", "Вес", "Температура", "Объем", "Скорость"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        value = st.number_input("Значение", value=1.0, step=0.1)

    with col2:
        if conv_type == "Длина":
            from_unit = st.selectbox("Из", ["Метры", "Километры", "Миллиметры", "Дюймы", "Футы"])
            to_unit = st.selectbox("В", ["Метры", "Километры", "Миллиметры", "Дюймы", "Футы"])
        elif conv_type == "Вес":
            from_unit = st.selectbox("Из", ["Килограммы", "Граммы", "Фунты", "Унции"])
            to_unit = st.selectbox("В", ["Килограммы", "Граммы", "Фунты", "Унции"])
        elif conv_type == "Температура":
            from_unit = st.selectbox("Из", ["Цельсий", "Фаренгейт", "Кельвин"])
            to_unit = st.selectbox("В", ["Цельсий", "Фаренгейт", "Кельвин"])
        elif conv_type == "Объем":
            from_unit = st.selectbox("Из", ["Литры", "Миллилитры", "Галлоны", "Кубические метры"])
            to_unit = st.selectbox("В", ["Литры", "Миллилитры", "Галлоны", "Кубические метры"])
        elif conv_type == "Скорость":
            from_unit = st.selectbox("Из", ["км/ч", "м/с", "мили/ч", "узлы"])
            to_unit = st.selectbox("В", ["км/ч", "м/с", "мили/ч", "узлы"])

    with col3:
        if st.button("Конвертировать"):
            result = value  # Здесь должна быть реальная логика конвертации

            # Простая демонстрация конвертации
            conversion_factors = {
                "Длина": {"Метры": 1, "Километры": 0.001, "Миллиметры": 1000, "Дюймы": 39.37, "Футы": 3.281},
                "Вес": {"Килограммы": 1, "Граммы": 1000, "Фунты": 2.205, "Унции": 35.274}
            }

            if conv_type in conversion_factors:
                if from_unit in conversion_factors[conv_type] and to_unit in conversion_factors[conv_type]:
                    # Конвертируем в базовую единицу, затем в целевую
                    base_value = value / conversion_factors[conv_type][from_unit]
                    result = base_value * conversion_factors[conv_type][to_unit]

            st.metric("Результат", f"{result:.4f} {to_unit}")

with tool_tabs[4]:  # Безопасность
    st.subheader("Инструменты безопасности")

    security_option = st.selectbox(
        "Выберите инструмент",
        ["Генератор паролей", "Хеширование", "Base64 кодирование"]
    )

    if security_option == "Генератор паролей":
        col1, col2 = st.columns(2)

        with col1:
            length = st.slider("Длина пароля", 8, 32, 12)
            use_upper = st.checkbox("Заглавные буквы", True)
            use_lower = st.checkbox("Строчные буквы", True)
            use_digits = st.checkbox("Цифры", True)
            use_special = st.checkbox("Специальные символы", True)

        with col2:
            if st.button("Сгенерировать пароль"):
                import random
                import string

                characters = ""
                if use_upper:
                    characters += string.ascii_uppercase
                if use_lower:
                    characters += string.ascii_lowercase
                if use_digits:
                    characters += string.digits
                if use_special:
                    characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

                if characters:
                    password = ''.join(random.choice(characters) for _ in range(length))
                    st.success("Сгенерированный пароль:")
                    st.code(password, language="text")

                    # Оценка сложности пароля
                    complexity = 0
                    if use_upper: complexity += 1
                    if use_lower: complexity +=