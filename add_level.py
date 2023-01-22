from data_base import DataBase

if __name__ == '__main__':
    try:
        id = int(input("Номер уровня: "))
        count_crystal = int(input("Количество кристаллов: "))
        map_path = input("Название карты: ")
        db = DataBase()
        db.add_level(level_id=id, map_path=map_path, crystal_count=count_crystal)
    except Exception:
        print("Что-то пошло не так. Проверьте правильность введённых данных.")
