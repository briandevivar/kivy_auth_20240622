import sqlite3
import logging

from sqlite3 import Error

from models import AuthModel, UsersModel


DB_NAME = "personal_data.db"


class Db:
    __conn = None
    __cur = None

    def __init__(self):
        self.set_connection(DB_NAME)
        self.set_cursor()

    def set_connection(self, db):
        self.__conn = sqlite3.connect(db)

    def set_cursor(self):
        self.__cur = self.__conn.cursor()

    def get_connection(self):
        return self.__conn

    def get_cursor(self):
        return self.__cur

    def __del__(self):
        self.__conn.close()


class AuthTbl(Db):
    def __init__(self):
        Db.__init__(self)
        self.conn = self.get_connection()
        self.cur = self.get_cursor()
        self.create_table()

    def create_table(self):
        try:
            sql = """CREATE TABLE IF NOT EXISTS auth_tbl (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        created_at DATETIME NOT NULL,
                        updated_at DATETIME NOT NULL
                    )"""
            self.cur.execute(sql)
            self.conn.commit()
        except Error as e:
            logging.error(e)

    def insert_auth(self, username, password, user_id, created_at, updated_at):
        try:
            sql = """INSERT INTO auth_tbl (
                username, 
                password, 
                user_id, 
                created_at, 
                updated_at) VALUES (?, ?, ?, ?, ?)"""
            result = self.cur.execute(sql, (
                username,
                password,
                user_id,
                created_at,
                updated_at))
            self.conn.commit()
            return result.lastrowid or None
        except Error as e:
            logging.error(e)

    def login(self, username, password) -> AuthModel:
        try:
            sql = """SELECT * FROM auth_tbl WHERE username = ? and password = ?"""
            result = self.cur.execute(sql, (username, password)).fetchone()
            return result or None
        except Error as e:
            logging.error(e)

    def __del__(self):
        self.__conn.close()


class UsersTbl(Db):
    def __init__(self):
        Db.__init__(self)
        self.conn = self.get_connection()
        self.cur = self.get_cursor()
        self.create_table()

    def create_table(self):
        try:
            sql = """CREATE TABLE IF NOT EXISTS users_tbl (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT NOT NULL,
                        address TEXT NOT NULL,
                        birthday TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        created_at DATETIME NOT NULL,
                        updated_at DATETIME NOT NULL
                    )"""
            self.cur.execute(sql)
            self.conn.commit()
        except Error as e:
            logging.error(e)

    def insert_info(self, full_name, address, birthday, gender, created_at, updated_at):
        try:
            sql = """INSERT INTO users_tbl (
                        full_name, 
                        address, 
                        birthday, 
                        gender, 
                        created_at, 
                        updated_at) VALUES (?, ?, ?, ?, ?, ?)"""
            result = self.cur.execute(sql, (
                full_name,
                address,
                birthday,
                gender,
                created_at,
                updated_at))
            self.conn.commit()
            return result.lastrowid
        except Error as e:
            logging.error(e)

    def select_by_id(self, user_id):
        try:
            sql = """SELECT * FROM users_tbl WHERE id = ?"""
            result = self.cur.execute(sql, (user_id,)).fetchone()
            return result or None
        except Error as e:
            logging.error(e)

    def __del__(self):
        self.__conn.close()


auth_tbl = AuthTbl()
users_tbl = UsersTbl()
