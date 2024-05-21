import sqlite3 as sl

con = sl.connect('Database1.db')

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Goods (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            article VARCHAR(50) NOT NULL,
            category VARCHAR(200) NOT NULL,
            charasteristic VARCHAR(500),
            picture VARCHAR(250),
            price VARCHAR(100) NOT NULL
        );
    """)

    con.execute("""
                    CREATE TABLE IF NOT EXISTS Categories (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        category VARCHAR(100) NOT NULL
                    );
                """)

    con.execute("""
                    CREATE TABLE IF NOT EXISTS GoodsCategories (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        good_id INTEGER NOT NULL,
                        category_id INTEGER NOT NULL,
                        FOREIGN KEY (good_id) REFERENCES Goods (id),
                        FOREIGN KEY (category_id) REFERENCES Categories (id)
                    );
                """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Warehouses (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            adress VARCHAR(150) NOT NULL,
            name VARCHAR(80) NOT NULL,
            geolocation VARCHAR(150) NOT NULL
         );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            contact VARCHAR(200) NOT NULL,
            comment VARCHAR(300)
        );
    """)

    con.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                order_date VARCHAR(100) NOT NULL,
                status VARCHAR(80) NOT NULL,
                price VARCHAR(100) NOT NULL,
                comment VARCHAR(500),
                FOREIGN KEY (client_id) REFERENCES Clients (id)
            );
        """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS Order_content (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    goods_id VARCHAR(500) NOT NULL,
                    count INTEGER NOT NULL,
                    sum_price VARCHAR(200) NOT NULL,
                    delivery_date VARCHAR(100) NOT NULL,
                    expiration_date VARCHAR(100) NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES Orders (id),
                    FOREIGN KEY (goods_id) REFERENCES Goods (id)
                );
            """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS Accounting (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    good_id INTEGER NOT NULL,
                    warehouse_id INTEGER NOT NULL,
                    count INTEGER NOT NULL,
                    delivery_date VARCHAR(100) NOT NULL,
                    expiration_date VARCHAR(100) NOT NULL,
                    FOREIGN KEY (good_id) REFERENCES Goods (id),
                    FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id)
                );
            """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS Write_off (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    good_id INTEGER NOT NULL,
                    warehouse_id INTEGER NOT NULL,
                    date VARCHAR(100) NOT NULL,
                    count INTEGER NOT NULL,
                    reason VARCHAR(500) NOT NULL,
                    FOREIGN KEY (good_id) REFERENCES Goods (id),
                    FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id)
                );
            """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS Receipt (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    good_id INTEGER NOT NULL,
                    warehouse_id INTEGER NOT NULL,
                    date VARCHAR(100) NOT NULL,
                    count INTEGER NOT NULL,
                    comment VARCHAR(500),
                    FOREIGN KEY (good_id) REFERENCES Goods (id),
                    FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id)
                );
            """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS Sale (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    good_id INTEGER NOT NULL,
                    warehouse_id INTEGER NOT NULL,
                    client_id INTEGER NOT NULL,
                    date VARCHAR(100) NOT NULL,
                    count INTEGER NOT NULL,
                    price VARCHAR(100) NOT NULL,
                    FOREIGN KEY (good_id) REFERENCES Goods (id),
                    FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id),
                    FOREIGN KEY (client_id) REFERENCES Clients (id)
                );
            """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS Transfer (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    good_id INTEGER NOT NULL,
                    from_warehouse_id INTEGER NOT NULL,
                    to_warehouse_id INTEGER NOT NULL,
                    date VARCHAR(100) NOT NULL,
                    count INTEGER NOT NULL,
                    comment VARCHAR(500),
                    FOREIGN KEY (good_id) REFERENCES Goods (id)
                );
            """)



