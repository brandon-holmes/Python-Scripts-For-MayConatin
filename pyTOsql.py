#pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(  host ='localhost',
                                            database='maycontain',
                                            user='root',
                                            password='May@Contain')
    insert_query = """INSERT INTO restaurants (mcid, placeid,restaurantName,longitude,latitude,phone,address,website,email,catNum,catTxt,insta,price,logo,coverImg,gallery,allergyMenu,otherMenu,peanut,shellfish,egg,fish,mustard,sesame,treenuts,soy,sulphites,milk,kosher,halal,vegan,vegetarian,glutFree,glutFriendly,fahps,lastUpdated)
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s))"""
    mayConCursor = connection.cursor()
    vals=(mcid,place_id,name,longit,latit,phNum,address,website,email,catnum,catTxt,insta,priceLvl,logo,coverImg,gallery,allMenu,othMenu,peanut,shellfish,egg,fish,mustard,sesame,treenuts,soy,sulphites,milk,kosher,halal,vegan,vegetarian,glutFree,glutFriend,fahps,lastUpd)
    mayConCursor.execute(insert_query,vals)
    connection.commit()
except Error as e:
    print("Error while connecting to MySQL", e)

mayConCursor.close()
connection.close()
print("MySQL connection is closed")
    