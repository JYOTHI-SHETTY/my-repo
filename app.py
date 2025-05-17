import pymysql
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from db import get_db_connection, get_post
import logging
logging.basicConfig(level=logging.DEBUG)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'jaanu shetty'

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute('SELECT * FROM posts')  # Use the cursor to execute the query
    posts = cursor.fetchall()  # Fetch all rows from the result
    cursor.close()  # Close the cursor
    conn.close()  # Close the connection
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()  # Create a cursor object
            cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)', (title, content))  # Use %s for MySQL
            conn.commit()  # Commit the transaction
            cursor.close()  # Close the cursor
            conn.close()  # Close the connection
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = %s', (id,))
    post = cursor.fetchone()

    if post is None:
        abort(404)

    if request.method == 'POST':  # Only update on POST
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            cursor.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s', (title, content, id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Post updated successfully!')
            return redirect(url_for('index'))  # Redirect to prevent form resubmission

    conn.close()
    return render_template('edit.html', post=post)
           

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))  # Use %s for MySQL
    conn.commit()  # Commit the transaction
    cursor.close()  # Close the cursor
    conn.close()  # Close the connection
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))  # Fetch the post by ID
    post = cursor.fetchone()  # Fetch one row
    cursor.close()  # Close the cursor
    conn.close()  # Close the connection

    if post is None:
        abort(404)  # Return a 404 error if the post is not found

    return render_template('post.html', post=post)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute('SELECT * FROM posts')  # Use the cursor to execute the query
    posts = cursor.fetchall()  # Fetch all rows from the result
    cursor.close()  # Close the cursor
    conn.close()  # Close the connection
    return render_template('dashboard.html', posts=posts)


app.config["DEBUG"] = True

if __name__=='__main__':
    app.run()