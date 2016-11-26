#!/usr/bin/python
import psycopg2
import sys
import json
import pprint
import re
from datetime import datetime

'''
Turn "on Wednesday, November 23rd, 2016" to "Wednesday, November 23, 2016"
'''
def parseDate(s):                                             
    return re.sub(r'(\d)(st|nd|rd|th)', r'\1', s[3:])
 
def main():

    ############### load JSON (warning: statements.JSON has duplicates of (...almost...) every statement) ###############
    # "almost" because of scraper hiccups

    fname = "statements.json"
    statements = []

    with open(fname) as js:
        data = js.read()
        if not data:
            print("no data")
        # Deserialize str or unicode instance to a Python object
        statements = json.loads(data)

    ############### connect to postgres ###############
 
    print("Connecting to database\n ->%s" % ('politifact_db'))
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(host='localhost', dbname='politifact_db', user='bella', password='')
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print("Connected!\n")


    ############### create table 'statements' with ###############

    cursor.execute(
        """CREATE TABLE statements (
            id              SERIAL,
            statement       text, 
            statement_link  text, 
            ruling          text, 
            ruling_text     text, 
            time            date, 
            source          text, 
            source_image    text
        );"""
         
    )

 
    # execute our Query
    for statement in statements:
        cursor.execute(
            """INSERT INTO statements (statement, statement_link, ruling, ruling_text, time, source, source_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s);""",
            (   statement['statement'],
                statement['statement_link'], 
                statement['ruling'], 
                statement['ruling_text'], 
                datetime.strptime(parseDate(statement['time']), '%A, %B %d, %Y').date(), 
                statement['source'], 
                statement['source_image']
            )
        ) 

    # remove all duplicates
    cursor.execute(
        """DELETE FROM statements
            WHERE id IN (SELECT id
                            FROM (SELECT id,
                                            ROW_NUMBER() OVER (PARTITION BY statement, statement_link ORDER BY id) AS rnum
                                  FROM statements) t
                            WHERE t.rnum > 1);"""
    )

    # cursor.execute("SELECT * FROM statements;")
    # # retrieve the records from the database
    # records = cursor.fetchall()
 
    # Make the changes to the database persistent
    conn.commit()
    
    # Close communication with the database
    cursor.close()
    conn.close()
    

if __name__ == "__main__":
    main()

