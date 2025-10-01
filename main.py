import main_film_search
import statistic_report
import connector


def main():
    with connector.create_mysql_connection() as connection:
        cursor = connection.cursor()
        while True:
            title = "Поиск фильмов в базе данных Sakila"
            print("=" * 50)
            print(title.center(50))
            print("=" * 50)
            print(f"{'1.':<5} Поиск по названию фильма")
            print(f"{'2.':<5} Поиск по жанру и году выпуска")
            print(f"{'3.':<5} Статистика поисков")
            print(f"{'0.':<5} Выход")
            print("-" * 50)
            choice = input("Выберите действие (0-3): ").strip()

            if choice == "1":
                while True:
                    result = main_film_search.search_by_keyword(cursor)
                    res = input("Сделать еще один поиск по названию? Y/N: ").strip().lower()
                    if res in ['n', 'т', 'no', 'нет']:
                        break
            elif choice == "2":
                while True:
                    result = main_film_search.search_by_category_year(cursor)
                    res = input("Сделать еще один поиск по категории? Y/N: ").strip().lower()
                    if res in ['n', 'т', 'no', 'нет']:
                        break
            elif choice == "3":
                statistic_report.report_popular_keywords(connector.collection, "keyword", limit=10)
                print('-' * 50)
                statistic_report.report_popular_keywords(connector.collection, "category")
                res = input("Показать другие отчеты? (Y/N): ").strip().lower()
                if res in ['y', 'д', 'yes', 'да']:
                    statistic_report.report_unique_searches(connector.collection, "category", limit=3)
            elif choice == "0":
                print("Увидимся!")
                cursor.close()
                connector.client.close()
                break
            else:
                print("\n INVALID CHOICE! TRY AGAIN!")


if __name__ == "__main__":
    main()
