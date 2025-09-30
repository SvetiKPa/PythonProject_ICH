# Создайте функции для:
# ● вывода самых популярных запросов
# ● вывода последних уникальных запросов

def report_popular_keywords(collection, search_type="keyword", limit=5):
    try:
        if search_type == "keyword":
            search_type_filter = "search_by_keyword"
            title = "КЛЮЧЕВЫХ СЛОВ"
        elif search_type == "category":
            search_type_filter = "search_by_category"
            title = "ЖАНРОВ"
        else:
            print("Неверный тип поиска. Используйте 'keyword' или 'category'")
            return

        pipeline = [
            {"$match": {
                "search_type": search_type_filter,
                "params.keyword": {"$exists": True, "$ne": ""}
            }},
            {"$group": {
                "_id": "$params.keyword",
                "total": {"$sum": 1},
                "successful": {"$sum": {"$cond": [{"$eq": ["$status", "successful"]}, 1, 0]}},
                "films": {"$sum": "$films_found"}
            }},
            {"$sort": {"total": -1}},
            {"$limit": limit}
        ]

        results = list(collection.aggregate(pipeline))

        print(f"\n ТОП-{limit} ПОПУЛЯРНЫХ {title}:")
        print("-" * 70)

        for i, item in enumerate(results, 1):
            print(f"{i}. '{item['_id']}'")
            print(f"Всего запросов: {item['total']}")
            print(f"Успешных: {item['successful']}")
            print(f"Всего найдено фильмов: {item['films']}")
            print()

    except Exception as e:
        print(f"Ошибка: попробуйте позже! {e}")


def report_unique_searches(collection, limit=10):
    try:
        pipeline = [
            {"$match": {
                "search_type": {"$in": ["search_by_keyword", "search_by_category"]},
                "params.keyword": {"$exists": True, "$ne": ""}
            }},
            {"$sort": {"timestamp": -1}},
            {"$group": {
                "_id": {
                    "search_type": "$search_type",
                    "keyword": "$params.keyword"
                },
                "last_search": {"$first": "$timestamp"},
                "status": {"$first": "$status"},
                "films_found": {"$first": "$films_found"}
            }},
            {"$sort": {"last_search": -1}},
            {"$limit": limit}
        ]

        results = list(collection.aggregate(pipeline))

        print(f"ПОСЛЕДНИЕ {limit} УНИКАЛЬНЫХ ЗАПРОСОВ:")
        print("-" * 50)

        for i, item in enumerate(results, 1):
            search_type = "По ключевому слову" if item['_id']['search_type'] == "search_by_keyword" else "По жанру"

            print(f"{i}. {search_type}: '{item['_id']['keyword']}'")
            print(f"   Время: {item['last_search'].strftime('%d-%m-%Y %H:%M')}")
            print(f"   Статус: {item['status']}")
            print(f"   Найдено фильмов: {item['films_found']}")
            print()

    except Exception as e:
        print(f"Ошибка: {e}")
