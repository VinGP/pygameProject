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


if __name__ == "__main__":
    db = DataBase()
    print(db.get_all_level_user_progress())
    print(db.get_level(1))
    db.update_user_level_progress(1, 2)
    print(db.get_all_level_user_progress())
