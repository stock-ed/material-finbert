#!/usr/bin/python
import psycopg2
from datetime import datetime, timedelta, date
import pandas as pd
import json
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db

def init(db):
    pass
    # do nothing;

def fTable(Followers):
    if Followers:
        table = "followers_names"
    else:
        table = "following_names"
    return table

def uTable(Followers):
    if Followers:
        table = "followers"
    else:
        table = "following"
    return table

def follow(conn, Username, Followers, User):
    pass

def get_hash_id(conn, id):
    return ""

def user(conn, config, User):
    pass

def tweets(conn, Tweet, config):
    try:
        cur = conn.cursor()

        jsondata = json.dumps(Tweet.__dict__)

        insertQuery = """INSERT INTO tweets (tweet_text, author_id, tweet_id, retweet_count, reply_count, like_count, quote_count, user_id, user_name, symbol, tweet_json) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        entry = (
            Tweet.tweet,
            Tweet.user_id_str,
            Tweet.id_str,
            Tweet.retweets_count,
            Tweet.replies_count,
            Tweet.likes_count,
            0,
            Tweet.user_id_str,
            Tweet.username,
            config.Database,
            jsondata)

        cur.execute(insertQuery, entry)
        # get the generated id back
        id = cur.fetchone()[0]
        conn.commit()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 0


def update_search_rule(conn, id):
    try:
        cdt = datetime.today()
        one_date = datetime(
            cdt.year, cdt.month, cdt.day, cdt.hour, cdt.minute, cdt.second)
        cur = conn.cursor()
        sql = 'UPDATE public.symbols SET last_searched_on = %s WHERE id = $s'
        entry = ()
        cur.execute(sql, entry)
        # get the generated id back
        result = cur.fetchone()
        if (result == None):
            return False, None
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False, None


def get_search_rules(conn):
    try:
        cur = conn.cursor()

        sql = 'SELECT id, symbol, last_searched_on FROM public.symbols WHERE is_rule_active = true'

        # sql = """SELECT data FROM studies where study_type=%s and symbol=%s and period=%s and published_on >= %s"""
        # execute the SELECT statement
        entry = ()
        cur.execute(sql, entry)
        # get the generated id back
        result = cur.fetchone()
        if (result == None):
            return False, None
        conn.commit()
        return True, result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False, None


def Conn(database):
    try:
        if database:
            connect = None
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            connect = psycopg2.connect(**params)
            return connect
        else:
            return ""
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit(0)

