import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def get_data(self, table_name, id):
        query = f"SELECT * FROM {table_name} WHERE id=?"
        self.cur.execute(query, (id,))
        row = self.cur.fetchone()
        if row:
            return row[1]
        else:
            return None

    def set_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cur.execute(query, data)
        self.conn.commit()

    def table_filling(self, table_name):
        cursor = self.cur.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names
        # вернуть список из строк таблицы базы данных для заполнения qtablewidget


    def operations(self):
        transfer_query = f"""
            SELECT * FROM Transfer 
                JOIN Sale ON Transfer.from_warehouse_id = 

        """

        sale_query = f"""
                    SELECT * FROM Transfer 
                        JOIN Sale ON Transfer.from_warehouse_id = 

                """

        receipt_query = f"""
                            SELECT * FROM Transfer 
                                JOIN Sale ON Transfer.from_warehouse_id = 

                        """

        cursor = self.cur.execute(query)
        data = cursor.fetchall()
        # возвращает тип операции, дату операции, id скалада
        pass

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Создаем объект базы данных
    db = Database("example.db")

# from PyQt5 import QtCore, QtGui, QtWidgets
# import sqlite3 as sl
#
# con = sl.connect('Database1.accdb')
#
#
# class Database:
#     def __init__(self, db_name):
#         self.conn = sl.connect(db_name)
#         self.cur = self.conn.cursor()
#         self.cur.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, value TEXT)")
#         self.conn.commit()
#
#     def get_data(self, row_id):
#         self.cur.execute("SELECT * FROM data WHERE id=?", (row_id,))
#         row = self.cur.fetchone()
#         if row:
#             return row[1]
#         else:
#             return None
#
#     def set_data(self, id, value):
#         self.cur.execute("INSERT OR REPLACE INTO data (id, value) VALUES (?, ?)", (id, value))
#         self.conn.commit()
#
#     def data_loading(self, table_name):
#
#
#         return None
