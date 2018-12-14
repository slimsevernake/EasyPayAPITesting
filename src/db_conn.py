import psycopg2

from src.params import address_id, user_id, inspector_id


class DBConnection(object):
    def __init__(self):
        self.session = psycopg2.connect(dbname="easypay_db", user="postgres",
                                        password="postgres", host="localhost")
        self.cursor = None

    def __enter__(self):
        self.cursor = self.session.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def count_of_visits(self, date):
        self.cursor.execute("SELECT COUNT(*) FROM schedules "
                            "WHERE event_date = '%s' AND "
                            "address_id = %d AND user_id = %d;" %
                            (date, address_id, inspector_id))
        return self.cursor.fetchone()[0]

    def check_role(self):
        self.cursor.execute("SELECT role FROM users WHERE user_id = %d;" %
                            user_id)
        return self.cursor.fetchone()[0]

    def no_inspector(self):
        self.cursor.execute("SELECT COUNT(*) FROM utilities_users "
                            "WHERE user_id = %d;" %
                            inspector_id)
        return self.cursor.fetchone()[0] == 0

    def add_inspector(self):
        if self.no_inspector():
            self.cursor.execute("INSERT INTO utilities_users "
                                "(utility_id, user_id) VALUES (2, %d);" %
                                inspector_id)
            self.session.commit()


def check(role):
    with DBConnection() as db:
        return db.check_role() == role


def no_inspector():
    with DBConnection() as db:
        if db.no_inspector():
            db.add_inspector()
            return True
        return db.no_inspector()


def get_current_count_of_visits(date):
    with DBConnection() as db:
        return db.count_of_visits(date)
