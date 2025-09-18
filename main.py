#!/usr/bin/env python3
"""
Точка входа в программу для работы с вакансиями hh.ru
"""

from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.file_workers.json_saver import JSONSaver
from src.utils.helpers import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)


def handle_search_vacancies(hh_api: HeadHunterAPI, json_saver: JSONSaver) -> None:
    """Обработка поиска вакансий"""
    search_query = input("Введите поисковый запрос: ").strip()
    if not search_query:
        print("❌ Поисковый запрос не может быть пустым")
        return

    print("🔍 Ищем вакансии на hh.ru...")

    # Загружаем вакансии через API
    raw_vacancies = hh_api.get_vacancies(search_query)

    if not raw_vacancies:
        print("❌ Не удалось загрузить вакансии или вакансии не найдены")
        return

    # Преобразуем в объекты Vacancy
    vacancies_list = Vacancy.cast_to_object_list(raw_vacancies)

    if not vacancies_list:
        print("❌ Не удалось преобразовать данные вакансий")
        return

    # Сохраняем вакансии
    added_count = 0
    for vacancy in vacancies_list:
        if json_saver.add_vacancy(vacancy):
            added_count += 1

    if added_count > 0:
        print(f"✅ Добавлено {added_count} новых вакансий")
    else:
        print("ℹ️  Новые вакансии не найдены или все уже есть в базе")


def handle_show_vacancies(json_saver: JSONSaver) -> None:
    """Обработка показа вакансий"""
    vacancies = json_saver.get_vacancies()
    if not vacancies:
        print("❌ В базе нет вакансий. Сначала загрузите их через пункт 1")
        return

    print_vacancies(vacancies)


def handle_filter_vacancies(json_saver: JSONSaver) -> None:
    """Обработка фильтрации вакансий"""
    vacancies = json_saver.get_vacancies()
    if not vacancies:
        print("❌ В базе нет вакансий. Сначала загрузите их через пункт 1")
        return

    print("🔍 Фильтрация вакансий:")
    print("ℹ️  Нажмите Enter для пропуска параметра")

    keyword = input("Ключевое слово: ").strip() or None
    min_salary = input("Минимальная зарплата: ").strip() or None
    max_salary = input("Максимальная зарплата: ").strip() or None
    experience = input("Опыт работы: ").strip() or None
    employment = input("Тип занятости: ").strip() or None
    address = input("Город: ").strip() or None

    # Применяем фильтры
    filtered = vacancies

    if keyword:
        filtered = filter_vacancies(filtered, [keyword])

    if min_salary or max_salary:
        if min_salary and max_salary:
            salary_range = f"{min_salary}-{max_salary}"
        elif min_salary:
            salary_range = f"{min_salary}-"
        elif max_salary:
            salary_range = f"-{max_salary}"
        else:
            salary_range = None

        if salary_range:
            filtered = get_vacancies_by_salary(filtered, salary_range)

    if experience:
        filtered = [v for v in filtered if experience.lower() in v.experience.lower()]

    if employment:
        filtered = [v for v in filtered if employment.lower() in v.employment.lower()]

    if address:
        filtered = [v for v in filtered if address.lower() in v.address.lower()]

    print(f"✅ Найдено {len(filtered)} вакансий:")
    print_vacancies(filtered)


def handle_top_vacancies(json_saver: JSONSaver) -> None:
    """Обработка топа вакансий"""
    vacancies = json_saver.get_vacancies()
    if not vacancies:
        print("❌ В базе нет вакансий. Сначала загрузите их через пункт 1")
        return

    try:
        top_n = int(input("Введите количество вакансий для топа: ").strip())
        if top_n <= 0:
            print("❌ Количество должно быть положительным числом")
            return

        salary_range = input("Введите диапазон зарплат (например: 100000-150000, Enter для пропуска): ").strip() or None

        filtered = get_vacancies_by_salary(vacancies, salary_range)
        if not filtered:
            print("❌ Вакансии с указанным диапазоном зарплат не найдены")
            return

        sorted_vac = sort_vacancies(filtered)
        top_vac = get_top_vacancies(sorted_vac, top_n)

        print(f"🏆 Топ {len(top_vac)} вакансий по зарплате:")
        print_vacancies(top_vac)

    except ValueError:
        print("❌ Неверный формат числа")


def handle_clear_vacancies(json_saver: JSONSaver) -> None:
    """Обработка очистки вакансий"""
    if json_saver.get_vacancies_count() == 0:
        print("ℹ️  База данных уже пустая")
        return

    confirm = input("❓ Вы уверены, что хотите очистить все вакансии? (y/n): ").strip().lower()
    if confirm == "y":
        json_saver.clear_all()
        print("✅ Все вакансии удалены")
    else:
        print("ℹ️  Операция отменена")


def user_interaction() -> None:
    """
    Функция взаимодействия с пользователем через консоль
    """
    try:
        json_saver = JSONSaver()
        hh_api = HeadHunterAPI()
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        return

    print("=" * 50)
    print("Добро пожаловать в программу поиска вакансий с hh.ru!")
    print("=" * 50)

    while True:
        try:
            vacancies_count = json_saver.get_vacancies_count()
            print(f"\nТекущее количество вакансий в базе: {vacancies_count}")

            if vacancies_count == 0:
                print("⚠️  База данных пустая. Сначала загрузите вакансии через пункт 1")

            print("\nМеню:")
            print("1. 📥 Поиск и загрузка вакансий с hh.ru")
            print("2. 📋 Показать все сохраненные вакансии")
            print("3. 🔍 Фильтровать вакансии")
            print("4. 🏆 Получить топ N вакансий по зарплате")
            print("5. 🗑️  Очистить все вакансии")
            print("6. 🚪 Выход")

            choice = input("Выберите действие (1-6): ").strip()

            if choice == "1":
                handle_search_vacancies(hh_api, json_saver)

            elif choice == "2":
                handle_show_vacancies(json_saver)

            elif choice == "3":
                handle_filter_vacancies(json_saver)

            elif choice == "4":
                handle_top_vacancies(json_saver)

            elif choice == "5":
                handle_clear_vacancies(json_saver)

            elif choice == "6":
                print("До свидания! Спасибо за использование программы.")
                break

            else:
                print("❌ Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
            print("Попробуйте еще раз.")


def main() -> None:
    """Основная функция программы"""
    user_interaction()


if __name__ == "__main__":
    main()
