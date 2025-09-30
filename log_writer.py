import datetime

def create_log_data(search_type, params, total_rows, all_films=None):
    status = "successful"
    if total_rows == 0 :
        status = "empty"

    log_data = {
        "timestamp": datetime.datetime.now(),
        "status": status,
        "search_type": search_type,
        "params": params,
        "results_count": total_rows,
        'films_found': total_rows,
        "search_film": {"info": all_films or []}
    }
    return log_data


def load_statistic(collection, load_dict):
    try:
        if not load_dict:
            print("Ошибка: Пустой словарь для загрузки")
            return False

        result = collection.insert_one(load_dict)
#        print(f"Успешно добавлен документ с ID: {result.inserted_id}")
        return result.inserted_id

    except Exception as e:
        print(f"Ошибка при добавлении документа: {e}")
        return False

