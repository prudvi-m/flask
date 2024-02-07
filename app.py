from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to initialize the SQLite database
def initialize_database():
    conn = sqlite3.connect('todo.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
initialize_database()

# Route to get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()
    conn.close()
    return jsonify([dict(todo) for todo in todos])

# Route to create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    new_todo = request.json
    task = new_todo.get('task')
    status = new_todo.get('status')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (task, status) VALUES (?, ?)', (task, status))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo created successfully"}), 201

# Route to update a todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    updated_todo = request.json
    task = updated_todo.get('task')
    status = updated_todo.get('status')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE todos SET task=?, status=? WHERE id=?', (task, status, todo_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo updated successfully"})


# Route to delete a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id=?', (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
