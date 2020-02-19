import sqlite3  # import sqlite database module for python

# establish connection to data.db file, create a new db file if not
# previously exist
conn = sqlite3.connect("data.db")
c = conn.cursor()  # create cursor object of the connection


def dbSetup():
    with conn:  # context manager will handle conn.commit and conn.close after each sql commands execution

        # create 5 tables in data.db , each with several different values to
        # store (in columns)
        c.execute("""CREATE TABLE IF NOT EXISTS UserTable (userFirstName TEXT,userLastName TEXT,userID TEXT,userPassword TEXT,userGender TEXT)""")

        c.execute(""" 
            CREATE TABLE IF NOT EXISTS BudgetRecordTable (
            userID TEXT,
            yearMonth_ TEXT,
            type TEXT,
            date_ TEXT,
            particular TEXT,
            reference TEXT,
            amount TEXT)
            """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS AlarmTable (
            userID TEXT,
            datetime_ TEXT,
            datetimeToRing TEXT,
            title TEXT,
            particular TEXT)
            """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS CalendarTable (
            userID TEXT,
            date_ TEXT,
            detail TEXT)
            """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS MemoTable(
            userID TEXT,
            datetime_ TEXT,
            title TEXT,
            detail TEXT)
            """)
