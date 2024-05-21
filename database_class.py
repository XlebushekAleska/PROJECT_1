import sqlite3


class Database:
    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
        self.__conn.create_function("test_function", 1, test2)
        self.__cur = self.__conn.cursor()

    def apply_filter(self, filter_function):
        data = filter_function(self.__cur)
        column_names = [description[0] for description in self.__cur.description]
        return data, column_names

    def get_column_names(self, table_name: str):
        self.__cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
        return [description[0] for description in self.__cur.description]

    def set_data(self, table_name: str, data: list):
        self.__cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
        column_names = [description[0] for description in self.__cur.description]
        column_names.remove('id')
        placeholders = ', '.join('?' for _ in range(len(data)))
        column_names = ', '.join(column_names)
        print(placeholders)
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        print(query)
        self.__cur.execute(query, data)
        self.__conn.commit()

    def get_data(self, table_name, row_id):
        query = f"SELECT * FROM {table_name} WHERE id=?"
        self.__cur.execute(query, (row_id,))
        row = self.__cur.fetchall()[0]
        column_names = [description[0] for description in self.__cur.description]
        if row:
            return row, column_names
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
                                     Clients.id""",

                  "Write_off": f"""SELECT 
                                       id AS "id",
                                       good_id AS "id товара",
                                       warehouse_id AS "id склада",
                                       date AS "дата",
                                       count AS "количество",
                                       reason AS "причина"                                        
                                   FROM 
                                       Write_off""",

                  "Receipt": f"""SELECT 
                                     id AS "id",
                                     good_id AS "id товара",
                                     warehouse_id AS "id склада",
                                     date AS "дата",
                                     count AS "количество",
                                     comment AS "комментарий"                                        
                                 FROM 
                                     Receipt""",

                  "Sale": f"""SELECT 
                                     id AS "id",
                                     good_id AS "id товара",
                                     warehouse_id AS "id склада",
                                     client_id AS "id клиента",
                                     date AS "дата",
                                     count AS "количество",
                                     price AS "цена"                                        
                                 FROM 
                                     Sale""",

                  "Transfer": f"""SELECT 
                                  id AS "id",
                                  good_id AS "id товара",
                                  from_warehouse_id AS "id склада из...",
                                  to_warehouse_id AS "id склада в...",
                                  date AS "дата",
                                  count AS "количество",
                                  comment AS "комментарий"                                        
                              FROM 
                                  Transfer""",
                  }
        # print(switch[table_name])
        cursor = self.__cur.execute(switch[table_name])
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names
        # вернуть список из строк таблицы базы данных для заполнения qtablewidget

    def operations(self):
        # возвращает тип операции, дату операции, id скалада
        transfer_query = f"""
                            SELECT date, good_id, from_warehouse_id FROM Transfer 
                          """
        sale_query = f"""
                        SELECT date, good_id, warehouse_id FROM Sale 
                      """
        receipt_query = f"""
                            SELECT date, good_id, warehouse_id FROM Receipt 
                        """
        write_off_query = f"""
                            SELECT date, good_id, warehouse_id FROM Write_off 
                           """
        cursor = self.__cur.execute(transfer_query)
        transfer_data = [('transfer',) + row for row in cursor.fetchall()]
        cursor = self.__cur.execute(sale_query)
        sale_data = [('sale',) + row for row in cursor.fetchall()]
        cursor = self.__cur.execute(receipt_query)
        receipt_data = [('receipt',) + row for row in cursor.fetchall()]
        cursor = self.__cur.execute(write_off_query)
        write_off_data = [('write_off',) + row for row in cursor.fetchall()]

        return transfer_data + sale_data + receipt_data + write_off_data, ('операция', 'дата', 'id товара', 'id склада')

    def own_query(self, query, data=None, fetch=True):
        """
        Метод для выполнения нестандартных SQL-запросов к базе данных.

        :param query: SQL-запрос
        :param data: Данные для подстановки в запрос (необязательно)
        :param fetch: Флаг, указывающий, нужно ли извлечь данные из курсора (по умолчанию True)
        :return: Результат выполнения запроса (если fetch=True) или None (если fetch=False)
        """
        if data:
            cursor = self.__cur.execute(query, data)
        else:
            cursor = self.__cur.execute(query)

        if fetch:
            result = cursor.fetchall()
            # print(result, '\n', query, '\n', data)
            return result
        else:
            self.__conn.commit()
            return None

    def close(self):
        self.__conn.close()

    def test(self):
        """
        питоновская функция в sql
        :return:
        """
        data = self.__conn.execute("""
                    SELECT test_function(charasteristic) FROM Goods
                    """)
        print(data.fetchall())

    # def operations(self)


def test2(x: str) -> str:
    '''
    питоновская функция в sql
    :return:
    '''

    if len(x) > 10:
        return x[:10]
    else:
        return x


def filter_goods_by_category_and_price(category: str, min_price: float, max_price: float):
    def inner(cursor):
        query = """
            SELECT * FROM Goods 
            WHERE category LIKE ? A ND price BETWEEN ? AND ?
        """
        cursor.execute(query, (f"%{category}%", min_price, max_price))
        return cursor.fetchall()
    return inner


def filter_clients_by_name(name: str):
    def inner(cursor):
        query = """
            SELECT * FROM Clients 
            WHERE name LIKE ?
        """
        cursor.execute(query, (f"%{name}%",))
        return cursor.fetchall()
    return inner


def filter_orders(name: str):
    def inner(cursor):
        query = """
            SELECT * FROM Clients 
            WHERE name LIKE ?
        """
        cursor.execute(query, (f"%{name}%",))
        return cursor.fetchall()
    return inner


def filter_wharehouses(name: str):
    def inner(cursor):
        query = """
            SELECT * FROM Clients 
            WHERE name LIKE ?
        """
        cursor.execute(query, (f"%{name}%",))
        return cursor.fetchall()
    return inner


if __name__ == "__main__":
    db = Database("Database1.db")

    print(db.get_column_names('Goods'))
    db.set_data(table_name='Goods', data=['шляпа', 'головной убор крестьянина, которому позавидует любой барин',
                                          'головные уборы; одежда', 'размер: L; цвет: светлый; матриал: солома', None, '15'])

    # print(db.get_data('Goods', 1))
    print(db.get_column_names('Goods'))


    # print(db.table_filling("Receipt"))
    # print(db.operations())
    # db.test()

    # print(db.table_filling('Goods'))
    # print(db.table_filling('Warehouses'))
    # print(db.table_filling('Orders'))
    # print(db.table_filling('Clients'))

    # with open(r'C:\Users\Алесь\PycharmProjects\PROJECT_1\goodsImages\1645328776175687133.jpg', 'rb') as photo:
    #     photo = photo.read()
    #     db.own_query(query=f'''
    #         INSERT INTO Goods (name, article, category, charasteristic, picture, price) VALUES (?, ?, ?, ?, ?, ?)
    #     ''', data=['дубинка "the rock"',
    #                'Дубинка угабуги, распечатанная на 3Д принтере. Грозное оружие в походе даже на самого'
    #                ' крупного мамонта. Всем угабугам рекомендовано к покупке!',
    #                'toys for ugabuga',
    #                'размер: XXXXL; цвет: серый; постобработка: о мамонта само сотрётся; ограничения: отсутствуют',
    #                photo,
    #                '300'], fetch=False)
    #
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


# with open(r'C:\Users\Алесь\PycharmProjects\PROJECT_1\goodsImages\1645328776175687133.jpg', 'rb') as photo:
#     photo = photo.read()
#     db.own_query(query=f'''
#         INSERT INTO Goods (name, article, category, charasteristic, picture, price) VALUES (?, ?, ?, ?, ?, ?)
#     ''', data=['dildo "the rock"',
#                'Огромный член, распечатанный на 3Д принтере. Порвёт даже самую бывалую шкуру. всем рекомендовано к покупке!',
#                'toys for adult',
#                'размер: XXXXL; цвет: серый; постобработка: об дырку само слижется; ограничения: 21+',
#                photo,
#                'бесценен'])
# print(db.get_data('Goods', 0))



# шлак

# class Filter(Database):
#     def __init__(self, params, db_name):
#         super().__init__(db_name)
#         self.filter_params = params
