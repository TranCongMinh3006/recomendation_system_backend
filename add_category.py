'''
file này để add category lv0 vào trường category của bảng article
'''
import mysql.connector
from sys import stdout
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
    passwd='123456',
    database='vnexpress'
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
    #   CẦN SỬA LẠI PASSWORD VỚI TÊN DATABASE Ở ĐÂY!!
)
curr = conn.cursor()

curr.execute("select articleID, category.categoryID FROM article_category INNER JOIN category ON article_category.categoryID= category.categoryID where level = 0;")
ids = curr.fetchall()

i = 0
for id in ids:
    curr.execute(
        "update articles set category = %s where articleID = %s", (id[1], id[0]))
    conn.commit()
    i += 1
    stdout.write("\rFinish writing %d records to db :) !" % i)
    stdout.flush()
