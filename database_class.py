import sqlite3


class Database:
    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
        self.__cur = self.__conn.cursor()
        self.__conn.create_function("test_function", 1, test2)

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

    def delete_data(self, table_name, row_id):
        query = (f'''DELETE FROM
                         {table_name}
                     WHERE
                         {table_name}.id = {row_id}''')

        cursor = self.__cur.execute(query)
        self.__conn.commit()
        return cursor.fetchall()

    def change_data(self, table_name: str, row_id: int, data: dict):
        query = (f'''UPDATE {table_name}
                     SET\n
                 ''')
        for key, value in data.items():
            query += f'"{key}" = "{value}",\n'
        query = query[:-2] + f'\nWHERE id = {row_id}'
        print(query)
        self.__cur.execute(query)
        self.__conn.commit()

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
                        Goods.id
                    """

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
                                   Goods.id
                               """,

                  "Warehouses": f"""SELECT 
                                        id AS "id", 
                                        name AS "имя", 
                                        adress AS "адрес", 
                                        geolocation AS "геолокация"
                                    FROM 
                                        Warehouses
                                    """,

                  "Orders": f"""SELECT
                                    id AS "id",  
                                    order_date AS "дата", 
                                    client_id AS "id клиента",
                                    status AS "статус", 
                                    price AS "стоимость"
                                FROM 
                                    Orders
                                """,

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
                                     Clients.id
                                 """,

                  "Write_off": f"""SELECT 
                                       id AS "id",
                                       good_id AS "id товара",
                                       warehouse_id AS "id склада",
                                       date AS "дата",
                                       count AS "количество",
                                       reason AS "причина"                                        
                                   FROM 
                                       Write_off
                                   """,

                  "Receipt": f"""SELECT 
                                     id AS "id",
                                     good_id AS "id товара",
                                     warehouse_id AS "id склада",
                                     date AS "дата",
                                     count AS "количество",
                                     comment AS "комментарий"                                        
                                 FROM 
                                     Receipt
                                 """,

                  "Sale": f"""SELECT 
                                     id AS "id",
                                     good_id AS "id товара",
                                     warehouse_id AS "id склада",
                                     client_id AS "id клиента",
                                     date AS "дата",
                                     count AS "количество",
                                     price AS "цена"                                        
                                 FROM 
                                     Sale
                                 """,

                  "Transfer": f"""SELECT 
                                  id AS "id",
                                  good_id AS "id товара",
                                  from_warehouse_id AS "id склада из...",
                                  to_warehouse_id AS "id склада в...",
                                  date AS "дата",
                                  count AS "количество",
                                  comment AS "комментарий"                                        
                              FROM 
                                  Transfer
                              """,
                  }
        # print(switch[table_name])
        cursor = self.__cur.execute(switch[table_name])
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names
        # вернуть список из строк таблицы базы данных для заполнения qtablewidget

    def filter_goods(self, min_price: float = None, max_price: float = None, min_count: int = None,
                     max_count: int = None,
                     name: str = None, article: str = None, category: str = None, warehouse_id: int = None):

        query = ("""SELECT 
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
                    """)

        if min_price and max_price:
            query += f'\nWHERE Goods.price BETWEEN {min_price} and {max_price},'
        elif min_price:
            query += f'\nWHERE Goods.price > {min_price},'
        elif max_price:
            query += f'\nWHERE Goods.price < {max_price},'
        if min_count and max_count:
            query += f'\nWHERE Accounting.count BETWEEN {min_count} and {max_count},'
        elif min_count:
            query += f'\nWHERE Accounting.count > {min_count},'
        elif max_count:
            query += f'\nWHERE Accounting.count < {max_count},'
        if name:
            query += f'\nWHERE Goods.name == "{name}",'
        if article:
            query += f'\nWHERE Goods.article == "{article}",'
        if category:
            query += f'\nWHERE Goods.category = {category},'
        if warehouse_id:
            query += f'\nWhere Accounting.wharehouse_id == {warehouse_id},'

        query = query[:-1] + '\nGROUP BY Goods.id'
        print(query)
        cursor = self.__cur.execute(query)
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names

    def filter_wharehouses(self, name: str = None, adress: str = None):
        query = (f"""SELECT 
                         id AS "id", 
                         name AS "имя", 
                         adress AS "адрес", 
                         geolocation AS "геолокация"
                     FROM 
                         Warehouses
                     """)

        if name:
            query += f'\nWHERE name == "{name}",'

        if adress:
            query += f'\nWHERE adress == "{adress}",'

        query = query[:-1]

        cursor = self.__cur.execute(query)
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names

    def filter_clients(self, min_orders_count: int = None, max_orders_count: int = None, name: str = None):
        query = (f"""SELECT 
                        Clients.id AS "id",
                        Clients.name AS "имя",
                        Clients.contact AS "контактные данные",
                        COUNT(Orders.id) AS "количество заказов"
                    FROM 
                        Clients
                    LEFT JOIN 
                        Orders ON Clients.id = Orders.client_id
                    GROUP BY 
                        Clients.id
                    """)

        if min_orders_count and max_orders_count:
            query += f'\nWHERE COUNT(Orders.id) BETWEEN {min_orders_count} AND {max_orders_count},'
        elif min_orders_count:
            query += f'\nWHERE COUNT(Orders.id) > {min_orders_count},'
        elif max_orders_count:
            query += f'\nWHERE COUNT(Orders.id) < {max_orders_count},'
        if name:
            query += f'\nWHERE Clients.name == "{name}",'

        query = query[:-1] + '\nGROUP BY Clients.id'

        cursor = self.__cur.execute(query)
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names

    def filter_orders(self, first_date: str = None, last_date: str = None, status: str = None,
                      first_price: float = None, last_price: float = None, name: str = None):
        query = (f"""SELECT
                         id AS "id",  
                         order_date AS "дата", 
                         client_id AS "id клиента",
                         status AS "статус", 
                         price AS "стоимость"
                     FROM 
                         Orders
                     LEFT JOIN
                        Clients ON Orders.client_id = Clients.id
                     """)

        if first_date and last_date:
            query += f'\nWHERE Orders.order_date BETWEEN {first_date} AND {last_date},'
        elif first_date:
            query += f'\nWHERE Orders.order_date > {first_date},'
        elif last_date:
            query += f'\nWHERE Orders.order_date < {last_date},'
        if status:
            query += f'\nWHERE Orders.status == "{status}",'
        if first_price and last_price:
            query += f'\nWHERE Orders.price BETWEEN {first_price} AND {last_price},'
        elif first_price:
            query += f'\nWHERE Orders.price > {first_price},'
        elif last_price:
            query += f'\nWHERE Orders.price < {last_price},'
        if name:
            query += f'\nWHERE Clients.name == "{name}",'

        query = query[:-1]

        cursor = self.__cur.execute(query)
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return data, column_names

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


def test2(x: str) -> str:
    '''
    питоновская функция в sql
    :return:
    '''

    if len(x) > 10:
        return x[:10]
    else:
        return x


if __name__ == "__main__":
    db = Database("Database1.db")
    # db.set_data('Goods', ['wef', 'rfw', 'rfwr', 'frwf', None, '123'])

    # db.change_data('Goods', 4, {'name': 'варежки',
    #                             'article': 'нереальные перчатки крутого гэнгсты. в них тебя будут бояться и уважать все алкаши с района',
    #                             'category': 'одежда; верхняя одежда',
    #                             'charasteristic': 'размер: S; цвет: чёрный панк',
    #                             'picture': None,
    #                             'price': '20'
    #                             })

    db.set_data('Goods', ['перчатки', 'нереальные перчатки крутого гэнгсты. в них тебя будут бояться и уважать все алкаши с района', 'одежда', 'размер: S; цвет: чёрный панк', None, '20'])

    # print(db.filter_goods())

    # db.delete_data('Goods', 2)

    #
    # print(db.get_column_names('Goods'))
    # db.set_data(table_name='Goods', data=['шляпа', 'головной убор крестьянина, которому позавидует любой барин',
    #                                       'головные уборы; одежда', 'размер: L; цвет: светлый; матриал: солома', None,
    #                                       '15'])

    # print(db.get_data('Goods', 1))
    # print(db.get_column_names('Goods'))

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
