import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(query, (username,)) # (variable, ) <-- this is used to create a tuple
        row = result.fetchone() # gets the first row out of the result set
        if row: # this is creating a user object that will create a column/attribute specified in the __init__ method
            user = cls(*row) # ([0], row[1], row[2]) this matches the parameters from the __init__ method, but is the same as (*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod 
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user