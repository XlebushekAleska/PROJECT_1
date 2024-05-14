import sqlite3


class Database:
    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
        self.__cur = self.__conn.cursor()

    # свойство-геттер

    @property
    def db_data(self):
        return self.db_data

    @db_data.setter
    def db_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.__cur.execute(query, data)
        self.__conn.commit()

    @db_data.getter
    def db_data(self, table_name, row_id):
        query = f"SELECT * FROM {table_name} WHERE id=?"
        self.__cur.execute(query, (row_id,))
        row = self.__cur.fetchone()
        if row:
            return row[1]
        else:
            return None



    def table_filling(self, table_name):
        cursor = self.__cur.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names
        # вернуть список из строк таблицы базы данных для заполнения qtablewidget


    def operations(self):
        # возвращает тип операции, дату операции, id скалада
        transfer_query = f"""
                            SELECT transfer_date, from_warehouse_id, to_warehouse_id FROM Transfer 
                          """

        sale_query = f"""
                        SELECT sale_date, warehouse_id FROM Sale 
                      """

        receipt_query = f"""
                            SELECT receipt_date, warehouse_id FROM Receipt 
                        """

        write_off_query = f"""
                            SELECT write_off_date, warehouse_id FROM Write_off 
                           """

        cursor = self.__cur.execute(transfer_query)
        transfer_data = ('transfer', cursor.fetchall())
        cursor = self.__cur.execute(sale_query)
        sale_data = ('sale', cursor.fetchall())
        cursor = self.__cur.execute(receipt_query)
        receipt_data = ('receipt', cursor.fetchall())
        cursor = self.__cur.execute(write_off_query)
        write_off_data = ('write_off', cursor.fetchall())

        return transfer_data, sale_data, receipt_data, write_off_data



    def close(self):
        self.__conn.close()


if __name__ == "__main__":
    db = Database("Database1.db")





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
