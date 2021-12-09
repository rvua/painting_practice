from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
  
class Painting:
    db = 'painting_practice_schema'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}
    
    @classmethod
    def create_painting(cls, data):
        query = "INSERT INTO paintings (title, description, price, user_id, created_at, updated_at) VALUES (%(title)s, %(description)s, %(price)s, %(user_id)s, NOW(), NOW())"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def get_paintings_with_users(cls):
        query = "SELECT * from paintings LEFT JOIN users ON user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        paintings = []
        for row in results:
            painting = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            painting.user = user.User(user_data)
            paintings.append(painting)
        return paintings
    
    @classmethod
    def get_one_painting(cls, data):
        query = "SELECT * from paintings LEFT JOIN users ON user_id = users.id WHERE paintings.id = %(painting_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        painting = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at']
        }
        painting.user = user.User(user_data)
        return painting
    
    @classmethod
    def update_painting_info(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, user_id = %(user_id)s, updated_at = NOW() WHERE id = %(painting_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return 

    @classmethod
    def delete_one_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(painting_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return 
    
    @staticmethod 
    def is_valid(painting):
        is_valid = True
        if len(painting['title']) < 3:
            is_valid = False
            flash('Title must be at least 2 characters long')
        if painting['title'] == '':
            is_valid = False
            flash('Title Required')
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at leasr 10 characters long.")
        if painting['description'] == '':
            is_valid = False
            flash('Decription Required')
        if len(painting['price']) < 1:
            is_valid = False
            flash('Price must be greater than 0') 
        if painting['title'] == '':
            is_valid = False
            flash('Price Required')
        return is_valid
