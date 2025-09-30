
def formated_search(cursor, total_rows, current_page=1, limit=10):
    displayed_count = 0
    while displayed_count < total_rows:
        films = cursor.fetchmany(limit)

        print(f"Показано фильмов: {len(films)} из {total_rows} - порция {current_page}")
        for i, film in enumerate(films, start=1):
            film_id, film_name, category, year = film
            print(f"{displayed_count + i:2d}. {film_name:<30} - {year}")

        displayed_count += len(films)
        current_page += 1

        if displayed_count < total_rows:
            res = input(f"\nВывести следующие {min(limit, total_rows - displayed_count)} фильмов? (Y/N): ").strip().lower()
            if res in ['n', 'т', 'no']:
                break

    print(f"\nПоказано {displayed_count} из {total_rows} фильмов")


def formated_by_column(data):
    for i in range(0, len(data), 3):
        # Первый элемент в строке
        cat_id1, cat_name1 = data[i]
        line = f"{i + 1:2d}. {cat_name1:<15}"
        # Второй элемент в строке (если есть)
        if i + 1 < len(data):
            cat_id2, cat_name2 = data[i + 1]
            line += f"    {i + 2:2d}. {cat_name2:<15}"
        # Третий элемент в строке (если есть)
        if i + 2 < len(data):
            cat_id3, cat_name3 = data[i + 2]
            line += f"    {i + 3:2d}. {cat_name3}"
        print(line)
