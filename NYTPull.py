import requests #
import json
import argparse
import mysql.connector
from datetime import datetime

def main(searchTerm):
    articles = pullAPI(searchTerm)
    SQLOps(articles)
    print("Operation complete!")
    quit()

def pullAPI(searchTerm):
    #Pulls data from NYT API
    #print("Requesting data from API")
    outData = []
    rawData = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?q={0}&api-key=gZreZ448g68VaNlNzJ2eM0iFiD4F1oBV'.format(searchTerm))
    searchTime = datetime.now()
    jsonData = rawData.json()
    x = 1
    articles = []
    for item in jsonData['response']['docs']:
        if len(articles) <= 4:
            articleDict = {}
            articleDict['headline'] = item['headline']['print_headline']
            articleDict['url'] = item['web_url']
            articleDict['pubDate'] = item['pub_date']
            articleDict['searchTerm'] = searchTerm
            articleDict['searchTime'] = searchTime
            articles.append(articleDict)
    #print("{0} articles found!".format(len(articles)))
    return articles

def SQLOps(articles):
    #Handles all SQL operations
    conn = mysql.connector.connect(host='localhost', user='oneSource', password='123abc987zyx')
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS OneSource;")
    conn.database = 'OneSource'
    targetTableCheck(conn)
    writeData(conn, articles)
    conn.close()

def targetTableCheck(conn):
    #Ensure that the table exists, and has the proper columns
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES LIKE "NYTPull";')
    result = cursor.fetchall()
    if len(result) == 1:
        #The table exists, verify that it has the correct layout
        print("Table Found! Checking that it's correct...")
        cursor.execute('SHOW COLUMNS FROM NYTPull;')
        goodCols = 0
        colNames = ['headline', 'url', 'pubDate', 'searchTerm', 'searchTime']
        for item in cursor:
            if item[0] == 'id' and item[1] == b'int':
                goodCols = goodCols+1
            elif item[0] in colNames and item[1] == b'varchar(255)':
                goodCols = goodCols+1
        if goodCols == 6:
            #Table has correct layout
            #print("Table is good!")
            return
        else:
            #Table has wrong layout
            print("Table is bad! Deleting it and recreating it.")
            cursor.execute("DROP TABLE NYTPull;")
            createTable(conn)
            return

    elif len(result) == 0:
        #Table does not exist
        print("Table not found! Creating it...")
        createTable(conn)
        return

    else:
        #There are multiple tables detected - Don't know which one to use. Not proceeding.
        print("Something has gone horribly wrong!")
        quit()

def createTable(conn):
    #If table doesn't exist, or is of the wrong layout, go ahead and create it
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE NYTPull (id INT AUTO_INCREMENT PRIMARY KEY, headline VARCHAR(255), url VARCHAR(255), pubDate VARCHAR(255), searchTerm VARCHAR(255), searchTime VARCHAR(255));""")
    return

def writeData(conn, articles):
    #Write article data to table
    print("Writing data...")
    cursor = conn.cursor()
    for article in articles:
        #print(article['headline'])
        cursor.execute("""INSERT INTO NYTPull (headline, url, pubDate, searchTerm, searchTime) VALUES ('{headline}', '{url}', '{pubDate}', '{searchTerm}', '{searchTime}');""".format(headline = article['headline'], url = article['url'], pubDate = article['pubDate'], searchTerm = article['searchTerm'], searchTime = article['searchTime']))
        conn.commit()
    return

parser = argparse.ArgumentParser(description='Enter a Keyword.')
parser.add_argument('keyword', help = "Enter your search term", type=str)
args = parser.parse_args()
main(args.keyword)
