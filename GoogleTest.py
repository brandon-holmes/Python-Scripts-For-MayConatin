#MISSING FROM GOOGLE:
#Taken from CSV
    #Logo(restaurant logo not google logo)
    #Cover Image(Pictures availasble though google)
    #Category (numbers and text)
    #Instagram
    #Gallery (see cover image)
    #Allergy menu / Regular Menu
    #All allergy info (ratings, kosher, halal etc, Date of allergy menu, FAHPS)
    #Last updated (date)
    #Email
    #City (kinda)
    #MCID (AAA###)
    #Notes


#pip install googlemaps

import csv
from googleplaces import GooglePlaces
import mysql.connector
from mysql.connector import Error

#Change CSV file below 
CSV_FILE = "Restaurants.csv"
#API Key here, should make env var at some point 
API_KEY = 'AIzaSyCquce8w2Ax_gKSA1hc43SjSjVRCIYZqVk' 
google_places = GooglePlaces(API_KEY)
#Open CSV file and loop through each row in the file
#Gets values needed to be stored in the SQL database

#Change Values for Database here
#database should be the name of your MySQL database(not to be confused with table or connection name)
#password is your root password for MySQL
#DEFAULT VALUES: host: "localhost", user: "root", table: "restaurants"
dataBase = "maycontainsql"
password = "May@Contain"

with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            #Place_ID (Seperate cuz special)
            place_id = row['PlaceID']

            #Images ( Logos, Instagram, etc...)
            logo = row['Logo']
            coverImg = row['Cover Image']
            insta = row['Instagram']
            gallery = row['Gallery']

            #Allergy info (Allergen Ratings, Menus, Updated date, Kosher, GlutenFree, etc... )
            allMenu = row['Allergy Information']
            othMenu = row['Other Menu']
            peanut = int(row['Peanut'])
            shellfish = int(row['Shellfish'])
            egg = int(row['Egg'])
            fish = int(row['Fish'])
            mustard = int(row['Mustard'])
            sesame = int(row['Sesame'])
            treeNuts = int(row['Tree Nuts'])
            soy = int(row['Soy'])
            sulphites = int(row['Sulphites'])
            milk = int(row['Milk'])
            #True/False values, blanks interpretted as false
            kosher = bool(row['Kosher'])
            halal = bool(row['Halal'])
            vegan = bool(row['Vegan'])
            vegetarian = bool(row['Vegetarian'])
            glutFree = bool(row['GlutenFree'])
            dairyFree = bool(row['DairyFree'])
            glutFriend = bool(row['GlutenFriendly'])
            lastUpd = row['LastUpdated']

            #Misc info (Email, Categories, ID, Fahps)
            email = row['Email']
            catNum = row['Category (Numerical)']
            catTxt = row ['Category']
            mcid = row['MCID (AAA###)']
            fahps = row['Food Allergy Handling Protocols']
            #Google info 
            place = google_places.get_place(place_id)

            #Details
            details = str(place.details)
            #Name 
            name = place.name
            #Phone number
            phNum = place.local_phone_number
            #Address formatted:(street, City, province/state Postal-Code, Country)
            address = place.formatted_address
            #Website (general website for individual location)
            website = place.website
            #GeoLocat (LONG AND LAT parsed from this)
            geoLocat =str(place.geo_location)
            geoArr = geoLocat.split("\'")
            latit = float(geoArr[3])
            longit = float(geoArr[7])
            #Price calulations
            word = str(details)
            priceIndx = word.find('price_level')
            priceLvlTemp = word[priceIndx+14]# this will always retrieve the number after price level
            try:
                priceLvl = int(priceLvlTemp)
            except:
                priceLvl = -1
            try:
                #CHANGE HARDCODE DATABASE SETTINGS HERE
                #host will be localhost when running on private machine
                #Database is the main database where your table is store (table name can be changed down below)
                #user and password are the main username and password you set for MYSQL
                connection = mysql.connector.connect(  host ='localhost',
                                                database= dataBase,
                                                user='root',
                                                password= password)
                                                #Change table name directly below (the first thing after INSERT INTO is table name)
                insert_query = """INSERT INTO restaurants (mcid,placeid,restaurantName,longitude,latitude,phone,address,website,email,catNum,catTxt,insta,price,logo,coverImg,gallery,allergyMenu,otherMenu,peanut,shellfish,egg,fish,mustard,sesame,treenuts,soy,sulphites,milk,kosher,halal,vegan,vegetarian,glutFree,glutFriendly,fahps,lastUpdated)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                #after successful connection replace "%s" of values above with values of previously retrieved variables from google/csv file.
                mayConCursor = connection.cursor()
                vals=(mcid,place_id,name,longit,latit,phNum,address,website,email,catNum,catTxt,insta,priceLvl,logo,coverImg,gallery,allMenu,othMenu,peanut,shellfish,egg,fish,mustard,sesame,treeNuts,soy,sulphites,milk,kosher,halal,vegan,vegetarian,glutFree,glutFriend,fahps,lastUpd)
                #execute and commit query and values with confimation 
                mayConCursor.execute(insert_query,vals)
                connection.commit()
                print("Successfully added: "+ name +", MCID:"+mcid)
            except Error as e:
                print("Error while connecting or committing to MySQL", e)
        except:
            print("WARNING: \n-----------------\n ERROR WITH: " + name+", MCID:"+mcid+", Place_ID: "+place_id+", FAILED TO COMMIT, CHECK VALUES\n-----------------")
