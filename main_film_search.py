import connector
import formatter
import log_writer
import datetime

COUNT_FILMS_BY_KEYWORD = """SELECT count(film_id)
                            FROM film
                            WHERE title LIKE %s """
GET_FILMS_BY_KEYWORD = """SELECT film.film_id, film.title, category.name, film.release_year
                          FROM film
                                   JOIN film_category ON film_category.film_id = film.film_id
                                   JOIN category ON film_category.category_id = category.category_id
                          WHERE title LIKE %s
                          ORDER BY release_year desc, film.title"""

COUNT_FILMS_BY_CATEGORY_YEAR = """SELECT count(film.film_id)
                                  FROM film
                                           JOIN film_category ON film_category.film_id = film.film_id
                                           JOIN category ON film_category.category_id = category.category_id
                                  WHERE category.category_id = %s
                                    AND film.release_year BETWEEN %s AND %s
                                  ORDER BY release_year DESC"""

GET_FILMS_BY_CATEGORY_YEAR = """SELECT film.film_id, film.title, category.name, film.release_year
                                FROM film
                                         JOIN film_category ON film_category.film_id = film.film_id
                                         JOIN category ON film_category.category_id = category.category_id
                                WHERE category.category_id = %s
                                  AND film.release_year BETWEEN %s AND %s
                                ORDER BY release_year DESC, film.title"""

GET_MIN_MAX_YEAR = """SELECT MIN(release_year), MAX(release_year)
                      FROM film
                               JOIN film_category ON film_category.film_id = film.film_id
                               JOIN category ON film_category.category_id = category.category_id
                      WHERE category.category_id = %s"""


def get_category_code(data):
    selected_category = input("Выберите жанр(или номер): ").strip()
    selected_code = ""
    genre_name = ""
    if selected_category.isdigit():
        index = int(selected_category) - 1
        if 0 <= index < len(data):
            selected_code = data[index][0]
            genre_name = data[index][1]
    else:
        for code, name in data:
            if name.lower() == selected_category.lower():
                selected_code = code
                genre_name = name
                break
    # print(selected_code)
    return selected_code, genre_name


def get_min_max_years(cursor, code):
    """Получает минимальный и максимальный год  в БД"""
    cursor.execute(GET_MIN_MAX_YEAR, (code,))
    return cursor.fetchone()


def custom_year(min_year, max_year):
    while True:
        try:
            year_input = input("Введите диапазон лет (например: 2005-2012 или 2010): ")
            if '-' in year_input:
                start_year, end_year = map(int, year_input.split('-'))
                if start_year > end_year:
                    start_year, end_year = end_year, start_year
            else:
                start_year = end_year = int(year_input)

            if not (1900 <= start_year <= 2050 and 1900 <= end_year <= 2050):
                print("Год должен быть в диапазоне 1900-2050")
                continue

            if start_year > max_year or end_year < min_year:
                print(f"В базе нет фильмов за указанный период. Доступные годы: {min_year}-{max_year}")
                continue

            return start_year, end_year

        except ValueError:
            print("Введите корректный формат: '2005-2012' или '2010'")
        except Exception as e:
            print(f"Ошибка ввода: {e}")


def execute_search(cursor, count_query, sql_query, search_pattern, txt):
    cursor.execute(count_query, search_pattern)
    total_rows = cursor.fetchone()[0]

    if total_rows == 0:
        status = "empty"
        print("Фильмы не найдены")
        return total_rows, status

    status = "successful"
    print(f"Всего найдено фильмов: {total_rows}")
    cursor.execute(sql_query, search_pattern)
    formatter.formated_search(cursor, total_rows, txt)
    # print(total_rows, status)
    return total_rows, status


def search_by_keyword(cursor):
    "Поиск по ключевому слову"
    function_name = "search_by_keyword"
    search_word = input("Введите поисковое слово(а): ").strip()

    if not search_word:
        print("Поисковый запрос не может быть пустым")
        return False

    search_pattern = (f"%{search_word}%",)
    params = {"keyword": search_word}
    result = execute_search(cursor, COUNT_FILMS_BY_KEYWORD, GET_FILMS_BY_KEYWORD, search_pattern, search_word)
    total_rows, status = result

    log_data = {
        "timestamp": datetime.datetime.now(),
        "status": status,
        "search_type": function_name,
        "params": params,
        'films_found': total_rows,
    }
    # print(log_data)
    log_writer.load_statistic(connector.collection, log_data)
    return True


def search_by_category_year(cursor):
    function_name = "search_by_category"
    cursor.execute("SELECT category_id, name FROM category")
    categories_data = cursor.fetchall()

    print("Доступные жанры: ")
    formatter.formated_by_column(categories_data)

    selected_code, genre_name = get_category_code(categories_data)
    while not selected_code:
        print("Введите корректные данные")
        selected_code, genre_name = get_category_code(categories_data)

    year1, year2 = get_min_max_years(cursor, selected_code)
    print(f"\nДля жанра {genre_name} найдены фильмы с {year1} по {year2} год")

    res = input(f"Вывести за года {year1} - {year2}? (Y) / (или свой выбор лет) (N) ").strip().lower()
    search_year1, search_year2 = year1, year2
    if res not in ['y', 'н', 'yes', 'да', '']:
        search_year1, search_year2 = custom_year(year1, year2)
    print(f"Будет выполнен поиск за период: {search_year1}-{search_year2}")

    search_pattern = (selected_code, search_year1, search_year2)
    params = {
        "keyword": genre_name,
        "year_from": search_year1,
        "year_to": search_year2
    }
    result = execute_search(cursor, COUNT_FILMS_BY_CATEGORY_YEAR, GET_FILMS_BY_CATEGORY_YEAR, search_pattern,
                            genre_name)

    total_rows, status = result
    # print(f"По категории --{genre_name}-- {search_year1}-{search_year2} всего найдено фильмов: {total_rows}")

    log_data = {
        "timestamp": datetime.datetime.now(),
        "status": status,
        "search_type": function_name,
        "params": params,
        'films_found': total_rows,
    }
    log_writer.load_statistic(connector.collection, log_data)
    return True
