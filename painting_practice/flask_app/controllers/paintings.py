from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.painting import Painting 

@app.route('/paintings')
def painting_dashboard():
    all_paintings = Painting.get_paintings_with_users()
    return render_template('list_painting.html',all_paintings = all_paintings)

@app.route('/paintings/new')
def new_painting():
    users = User.get_users()
    return render_template('new_painting.html', users = users)

@app.route('/create_painting', methods = ['POST'])
def create_painting():
    if Painting.is_valid(request.form):
        data = {
            'title':request.form['title'],
            'description':request.form['description'],
            'price':request.form['price'],
            'user_id':session['user_id']
        }
        Painting.create_painting(data)
        return redirect('/paintings')
    else:
        return redirect('/paintings/new')
        
# Show a painting route
@app.route('/paintings/<int:painting_id>')
def show_painting(painting_id):
    data = {
        'painting_id':painting_id
    }
    painting = Painting.get_one_painting(data)
    return render_template('show_painting.html', painting=painting)

# Edit painting routes
@app.route('/paintings/<int:painting_id>/edit')
def edit_painting(painting_id):
    users = User.get_users()
    data = {
        'painting_id': painting_id
    }
    painting = Painting.get_one_painting(data)
    return render_template('edit_painting.html', users = users, painting=painting)

@app.route('/update_painting/<int:painting_id>', methods=['POST'])
def update_painting(painting_id):
    if Painting.is_valid(request.form):
        data = {
            'painting_id':painting_id,
            'title':request.form['title'],
            'description':request.form['description'],
            'price':request.form['price'],
            'user_id':session['user_id']
        }
        Painting.update_painting_info(data)
        return redirect(f"/paintings/{painting_id}")
    else:
        return redirect(f'/paintings/{painting_id}/edit')

# Delete painting route
@app.route('/paintings/<int:painting_id>/delete')
def delete_painting(painting_id):
    data = {
        'painting_id' : painting_id
    }
    Painting.delete_one_painting(data)
    return redirect('/paintings') 