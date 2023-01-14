import sqlite3

from dataclasses import dataclass


@dataclass
class Level:
    id: int
    map_path: str
    count_crystal: int


@dataclass
class UserLevelProgress:
    id: int
    stars: int


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("data\\db.db")
        self.cur = self.con.cursor()

    def get_all_level_user_progress(self) -> list[UserLevelProgress]:
        q = """
            select level_id, stars from user_level_progress;
            """

        res = self.cur.execute(q).fetchall()
        ls = []
        for lvl in res:
            id, stars = lvl
            ls.append(UserLevelProgress(id=id, stars=stars))
        return ls

    def get_level(self, level_id):
        q = """
            select id, map_path, crystal_count from level where id=?;
            """
        id, map_path, crystal_count = self.cur.execute(q, (level_id,)).fetchone()
        return Level(id=id, map_path=map_path, count_crystal=crystal_count)

    def update_user_level_progress(self, level_id, stars):
        q = f"""
            select stars from user_level_progress where level_id=?;
            """
        (previous_result,) = self.cur.execute(q, (level_id,)).fetchone()

        stars = max(stars, previous_result)

        update = """
                UPDATE user_level_progress
                SET stars = ?
                where level_id = ?
                """
        self.cur.execute(
            update,
            (
                stars,
                level_id,
            ),
        )
        self.con.commit()

    def add_level(self, level_id, map_path, crystal_count):
        q_check = f"""
                select id from level where id=?
                """
        check = self.cur.execute(q_check, (level_id,)).fetchall()
        if check:
            print("[ERROR] Такой уровень уже существует!")
            s = input("Перезаписать уровень? yes/no: ")
            if s.lower() == "yes":
                delete_q = """
                           DELETE from level
                           WHERE id = ?
                           """
                self.cur.execute(delete_q, (level_id,))
                delete_q = """
                            DELETE from user_level_progress
                            WHERE level_id = ?
                            """
                self.cur.execute(delete_q, (level_id,))
                self.con.commit()
            else:
                return
        insert = """
                insert into level(id, map_path, crystal_count) VALUES (?, ?, ?);
                """
        self.cur.execute(insert, (level_id, map_path, crystal_count))
        insert = """
                insert into user_level_progress(level_id, stars) VALUES (?, ?);
                """
        self.cur.execute(insert, (level_id, 0))
        self.con.commit()
        print("[INFO] Готово!")

    def remove_progress(self):
        q = """
            select id from level
        """
        levels_id = self.cur.execute(q).fetchall()
        for level_id in levels_id:
            update = """
                            UPDATE user_level_progress
                            SET stars = ?
                            where level_id = ?
                            """
            self.cur.execute(
                update,
                (
                    0,
                    *level_id,
                ),
            )
        self.con.commit()
        print("[INFO] Прогресс сброшен")


if __name__ == "__main__":
    db = DataBase()
    # db.add_level(3, r"data\map3.tmx", 10)
    # db.remove_progress()
