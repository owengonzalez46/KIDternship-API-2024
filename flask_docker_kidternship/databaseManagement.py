import psycopg2
import uuid
import random
import os

from flask import jsonify
from psycopg2 import sql, Error

databaseHost =  os.getenv('DATABASE_HOST')
databasePort =  os.getenv('DATABASE_PORT')
databasename = os.getenv('DATABASE_NAME')
authacct =  os.getenv('DATABASE_USER')
authacctpwd =  os.getenv('DATABASE_PASS')

def searchDatabase(query):
    try:
        # Establish the database connection
        with psycopg2.connect(
            host=databaseHost,
            port=databasePort,
            user=authacct,
            password=authacctpwd,
            database=databasename
        ) as databaseConnection:
            # Create a cursor object
            with databaseConnection.cursor() as databaseCursor:
                # Execute the SQL query
                databaseCursor.execute(query)
                
                # Fetch all results
                databaseResults = databaseCursor.fetchall()
                
                # Get column names
                colnames = [desc[0] for desc in databaseCursor.description]
                
                # Convert to list of dictionaries
                results = [dict(zip(colnames, row)) for row in databaseResults]
                
                # Validate a row was actually returned
                if bool(results):
                    return results
                return None
    except Error as e:
        print(f"Error: {e}")
        return None
    
def insertIntoDatabaseSuccessful(query):
    try:
        with psycopg2.connect(
            host=databaseHost,
            port=databasePort,
            user=authacct,
            password=authacctpwd,
            database=databasename
        ) as conn:
            with conn.cursor() as cursor:
                # Execute the SQL query
                cursor.execute(query)

                # Commit inserted/updated rows
                conn.commit()
                return True
    except Error as e:
        print(f"Error: {e}")
        return False

def getAllMenuItems():
    searchQuery = "SELECT * FROM menu;"
    return searchDatabase(searchQuery)

def getOnlyMenuItems():
    searchQuery = "SELECT menuitem FROM menu;"
    return searchDatabase(searchQuery)

def getOnlyOrderIds():
    searchQuery = "SELECT orderid FROM orders;"
    return searchDatabase(searchQuery)


def getMenuItemsDetails(detailCategory, orderItem):
    searchQuery = "SELECT " + detailCategory + " FROM public.menu WHERE menuitem=\'" + orderItem + "\';"
    return searchDatabase(searchQuery)
    
def getAllMenuItemsForCategory(category):
    searchQuery = "SELECT * FROM menu WHERE category=\'" + category + "\';"
    return searchDatabase(searchQuery)

def getAllOrders():
    searchQuery = "SELECT * FROM orders;"
    return searchDatabase(searchQuery)

def getSpecificOrder(orderNumber):
    searchQuery = "SELECT * FROM orders WHERE orderid= \'" + orderNumber + "\';"
    return searchDatabase(searchQuery)

# Function to insert a new product into the database
def insertOrder(orderItem, flavor, size, temp):
    notes = ''
    orderId = str(random.randrange(100000,200000)) # Generate a new UUID
    insertQuery = "INSERT INTO orders (orderid, status, item, flavor, size, temperature, notes) VALUES (\'" + str(orderId) + "\', \'Open\', \'" + str(orderItem) + "\', \'" + str(flavor) + "\', \'" + str(size) + "\', \'" + str(temp) + "\', \'" + str(notes) + "\');"
    return orderId, insertIntoDatabaseSuccessful(insertQuery)

# Function to update order in the database
def updateOrder(orderNumber, status):
    updateQuery = "UPDATE orders SET status=\'" + str(status) + "\' WHERE orderid=\'" + str(orderNumber) + "\';"
    return insertIntoDatabaseSuccessful(updateQuery)

# Function to insert a new product into the database
def insertWordIntoCloud(words):
    word_uuid = str(uuid.uuid4())  # Generate a new UUID
    insertQuery = "INSERT INTO wordcloud (uuid, words) VALUES (\'" + str(word_uuid) + "\', \'" + str(words['word']) + "\');"
    return insertIntoDatabaseSuccessful(insertQuery)
    
def getWordsFromCloud():
    try:
        with psycopg2.connect(
            host=databaseHost,
            port=databasePort,
            user=authacct,
            password=authacctpwd,
            database=databasename
        ) as conn:
            with conn.cursor() as cursor:
                select_query = "SELECT words FROM wordcloud;"
                cursor.execute(select_query)
                rows = cursor.fetchall()
                words = ' '.join([row[0] for row in rows])
                return words
    except Exception as e:
        print(f"Error: {e}")
        return None

