
# from itemadapter import ItemAdapter
import mysql.connector


class CrawlPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='12345',
            database='myecommerce',
        )
        self.curr = self.conn.cursor()

    def create_table(self):

        self.curr.execute(""" DROP TABLE IF EXISTS myecommerce_tb """)

        self.curr.execute(""" CREATE TABLE myecommerce_tb (

            product_id INT(50),

            product_name VARCHAR(255),
            product_link VARCHAR(255),
            product_thumbnail VARCHAR(255),
            product_price INT(50),
            rating_point FLOAT,
            total_comments INT(50),
            rating_5_star INT(50),
            rating_4_star INT(50),
            rating_3_star INT(50),
            rating_2_star INT(50),
            rating_1_star INT(50),
            platform text
            
            ) """)

    def store_db(self, item):
        self.curr.execute("""INSERT into myecommerce_tb values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                          (
                              item['product_id'],
                              item['product_name'],
                              item['product_link'],
                              item['product_thumbnail'],
                              item['product_price'],

                              item['rating_point'],
                              item['total_comments'],

                              item['rating_5_star'][0],
                              item['rating_4_star'][0],
                              item['rating_3_star'][0],
                              item['rating_2_star'][0],
                              item['rating_1_star'][0],

                              item['platform'],
                          ))

        self.conn.commit()

    def process_item(self, item, spider):
        # adapter = ItemAdapter(item)
        self.store_db(item)
        return item
