import sqlite3


class Database:
    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
        self.__cur = self.__conn.cursor()

    def set_data(self, table_name, data, img):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.__cur.execute(query, data)
        self.__conn.commit()

    def get_data(self, table_name, row_id):
        query = f"SELECT * FROM {table_name} WHERE id=?"
        self.__cur.execute(query, (row_id,))
        row = self.__cur.fetchall()
        if row:
            return row[1]
        else:
            return None

    def warehouse_selection(self, warehouse_id):
        query = f"""SELECT 
                        Goods.id AS "id",
                        Goods.name AS "имя",
                        Goods.article AS "артикул",
                        Goods.category AS "категория",
                        SUM(Accounting.quantity) AS "количество",
                        Goods.price AS "цена"
                    FROM 
                        Goods
                    LEFT JOIN 
                        Accounting ON Goods.id = Accounting.good_id
                    WHERE
                        Accounting.warehouse_id={warehouse_id}
                    GROUP BY 
                        Goods.id"""

        cursor = self.__cur.execute(query)
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names


    """
     для записи изображения в базу данных, необходимо открыть его через
    with с препиской rb, а затем добавить его в бд через sql-запрос
    """

    def table_filling(self, table_name):
        switch = {"Goods": f"""SELECT 
                                    Goods.id AS "id",
                                    Goods.name AS "имя",
                                    Goods.article AS "артикул",
                                    Goods.category AS "категория",
                                    SUM(Accounting.count) AS "количество",
                                    Goods.price AS "цена"
                                FROM 
                                    Goods
                                LEFT JOIN 
                                    Accounting ON Goods.id = Accounting.good_id
                                GROUP BY 
                                    Goods.id""",

                  "Warehouses": f"""SELECT 
                                        id AS "id", 
                                        name AS "имя", 
                                        adress AS "адрес", 
                                        geolocation AS "геолокация", 
                                        coordinates AS "координаты"
                                    FROM 
                                        Warehouses""",

                  "Orders": f"""SELECT
                                    id AS "id",  
                                    order_date AS "дата", 
                                    client_id AS "id клиента",
                                    status AS "статус", 
                                    price AS "стоимость"
                                FROM 
                                    Orders""",

                  "Clients": f"""SELECT 
                                    Clients.id AS "id",
                                    Clients.name AS "имя",
                                    Clients.contact AS "контактные данные",
                                    COUNT(Orders.id) AS "количество заказов"
                                FROM 
                                    Clients
                                LEFT JOIN 
                                    Orders ON Clients.id = Orders.client_id
                                GROUP BY 
                                    Clients.id"""
                  }
        # print(switch[table_name])
        cursor = self.__cur.execute(switch[table_name])
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names
        # вернуть список из строк таблицы базы данных для заполнения qtablewidget

    # def table_filling(self, table_name):
    #     cursor = self.__cur.execute(f"SELECT * FROM {table_name}")
    #     data = cursor.fetchall()
    #     column_names = [description[0] for description in cursor.description]
    #     return data, column_names
    #     # вернуть список из строк таблицы базы данных для заполнения qtablewidget

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

    def own_query(self, query, data):
        if data:
            cursor = self.__cur.execute(query, data)
            print(cursor.fetchall(), '\n', query, '\n', data)
            return cursor.fetchall()
        else:
            cursor = self.__cur.execute(query)
            print(cursor)
            return cursor.fetchall()

    def close(self):
        self.__conn.close()


class Filter(Database):
    def __init__(self, params, db_name):
        super().__init__(db_name)
        self.filter_params = params


if __name__ == "__main__":
    db = Database("Database1.db")
    print(db.table_filling('Goods'))
    # with open(r'C:\Users\Алесь\PycharmProjects\PROJECT_1\goodsImages\1645328776175687133.jpg', 'rb') as photo:
    #     photo = photo.read()
    #     db.own_query(f'''
    #         INSERT INTO Goods (name, article, category, charasteristic, picture, price) VALUES (?, ?, ?, ?, ?, ?)
    #     ''', data=['dildo "the rock"',
    #                'Огромный член, распечатанный на 3Д принтере. Порвёт даже самую бывалую шкуру. всем рекомендовано к покупке!',
    #                'toys for adult',
    #                'размер: XXXXL; цвет: серый; постобработка: об дырку само слижется; ограничения: 21+',
    #                photo,
    #                'бесценен'])
    # print(db.get_data('Goods', 0))




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


