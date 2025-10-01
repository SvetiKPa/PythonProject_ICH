
def load_statistic(collection, load_dict):
    try:
        if not load_dict:
            print("Ошибка: Пустой словарь для загрузки")
            return False

        result = collection.insert_one(load_dict)
        #print(f"Успешно добавлен документ с ID: {result.inserted_id}")
        return result.inserted_id

    except Exception as e:
        print(f"Ошибка при добавлении документа: {e}")
        return False
