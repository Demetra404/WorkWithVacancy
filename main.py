from src.hh_api import HHAPI
from src.vacancy import Vacancy
from src.json_handler import JSONHandler
from src.helpers import convert_to_vacancy_objects, get_top_n_by_salary, filter_by_keyword


def main():
    """
    Основная функция для взаимодействия с пользователем.
    """
    api = HHAPI()
    file_handler = JSONHandler()

    print("Парсер вакансий с HeadHunter.ru")
    print("=" * 40)

    while True:
        print("\nДоступные действия:")
        print("1.Поиск вакансий на hh.ru")
        print("2.Топ N вакансий по зарплате")
        print("3.Фильтр вакансий по ключевому слову")
        print("4.Удалить вакансии")
        print("5.Выход")

        choice = input("\nВыберите действие (1-5): ")

        if choice == "1":
            search_vacancies(api, file_handler)
        elif choice == "2":
            show_top_vacancies(file_handler)
        elif choice == "3":
            filter_vacancies(file_handler)
        elif choice == "4":
            delete_vacancies(file_handler)
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")


def search_vacancies(api: HHAPI, file_handler: JSONHandler) -> None:
    """Поиск вакансий на hh.ru"""
    keyword = input("Введите поисковый запрос: ").strip()

    if not keyword:
        print("Запрос не может быть пустым!")
        return

    try:
        print("Ищем вакансии...")
        vacancies_data = api.get_vacancies(keyword)
        vacancies = convert_to_vacancy_objects(vacancies_data)

        for vacancy_data in vacancies_data:
            file_handler.add_vacancy({
                'title': vacancy_data.get('name'),
                'url': vacancy_data.get('alternate_url'),
                'salary': vacancy_data.get('salary'),
                'description': vacancy_data.get('snippet', {}).get('responsibility', ''),
                'requirements': vacancy_data.get('snippet', {}).get('requirement', ''),
                'employer': vacancy_data.get('employer', {}).get('name', '')
            })

        print(f"Найдено {len(vacancies)} вакансий и сохранено в файл")

        for i, vacancy in enumerate(vacancies[:5], 1):
            print(f"\n{i}. {vacancy}")

    except Exception as e:
        print(f"Ошибка: {e}")


def show_top_vacancies(file_handler: JSONHandler) -> None:
    """Показать топ N вакансий по зарплате"""
    try:
        n = int(input("Сколько вакансий показать? "))
        vacancies_data = file_handler.get_vacancies()
        vacancies = convert_to_vacancy_objects(vacancies_data)

        if not vacancies:
            print("Нет сохраненных вакансий!")
            return

        top_vacancies = get_top_n_by_salary(vacancies, n)

        print(f"\n Топ-{n} вакансий по зарплате:")
        for i, vacancy in enumerate(top_vacancies, 1):
            print(f"\n{i}. {vacancy}")

    except ValueError:
        print("Введите корректное число!")


def filter_vacancies(file_handler: JSONHandler) -> None:
    """Фильтровать вакансии по ключевому слову"""
    keyword = input("Введите ключевое слово для поиска в описании: ").strip()

    if not keyword:
        print("Ключевое слово не может быть пустым!")
        return

    vacancies_data = file_handler.get_vacancies()
    vacancies = convert_to_vacancy_objects(vacancies_data)

    filtered = filter_by_keyword(vacancies, keyword)

    print(f"\n Найдено {len(filtered)} вакансий с ключевым словом '{keyword}':")
    for i, vacancy in enumerate(filtered, 1):
        print(f"\n{i}. {vacancy}")


def delete_vacancies(file_handler: JSONHandler) -> None:
    """Удалить вакансии по критериям"""
    print("\n Удаление вакансий:")
    print("1. По названию")
    print("2. По работодателю")

    choice = input("Выберите критерий (1-2): ")

    if choice == "1":
        title = input("Введите название вакансии: ").strip()
        if title:
            file_handler.delete_vacancy({'title': title})
            print(f" Вакансии с названием '{title}' удалены")
        else:
            print(" Название не может быть пустым")
    elif choice == "2":
        employer = input("Введите название работодателя: ").strip()
        if employer:
            file_handler.delete_vacancy({'employer': employer})
            print(f" Вакансии работодателя '{employer}' удалены")
        else:
            print(" Название работодателя не может быть пустым")
    else:
        print(" Неверный выбор!")


def show_file_info(file_handler: JSONHandler) -> None:
    """Показать информацию о файле"""
    vacancies_data = file_handler.get_vacancies()
    print(f"\n Информация о файле:")
    print(f" Имя файла: {file_handler.filename}")
    print(f" Количество вакансий: {len(vacancies_data)}")

    employers = set(v.get('employer', '') for v in vacancies_data if v.get('employer'))
    print(f" Уникальных работодателей: {len(employers)}")


if __name__ == "__main__":
    main()