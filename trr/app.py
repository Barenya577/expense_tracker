# from flask import Flask, request, jsonify
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# # MySQL configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'  # Your MySQL username
# app.config['MYSQL_PASSWORD'] = 'Nous@12345'  # Your MySQL password
# app.config['MYSQL_DB'] = 'expense_tracker'

# mysql = MySQL(app)

# @app.route('/expenses', methods=['GET'])
# def get_expenses():
#     """
#     Route to get all expenses from the database.
#     """
#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM expenses")
#     expenses = cursor.fetchall()  # Fetch all records

#     # Convert the data into a list of dictionaries
#     expense_list = [{'id': expense[0], 'category': expense[1], 'amount': expense[2], 'date': expense[3]} for expense in expenses]
    
#     cursor.close()

#     # Return the expenses as a JSON response
#     return jsonify(expense_list)
# @app.route('/expenses', methods=['POST'])
# def add_expense():
#     # Extract JSON data from the request body
#     data = request.get_json()
    
#     # Check if data exists
#     if not data:
#         return jsonify({'error': 'Invalid or missing JSON data'}), 400

#     # Extract values from JSON data
#     category = data.get('category')
#     amount = data.get('amount')
#     date = data.get('date')

#     # Ensure values are valid
#     if not category or not amount or not date:
#         return jsonify({'error': 'Missing required fields'}), 400

#     # Insert into the MySQL database
#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (%s, %s, %s)", (category, amount, date))
#     conn.commit()  # Commit the transaction to save data
#     expense_id = cursor.lastrowid  # Get the ID of the inserted row
#     cursor.close()

#     return jsonify({
#         'id': expense_id,
#         'category': category,
#         'amount': amount,
#         'date': date
#     }), 201  # Return a response with the inserted data


# @app.route('/expenses/<int:id>', methods=['DELETE'])
# def delete_expense(id):
#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM expenses WHERE id=%s", (id,))
#     conn.commit()
#     cursor.close()

#     return jsonify({'message': 'Expense deleted successfully'})

# @app.route('/expenses/<int:id>', methods=['PUT'])
# def update_expense(id):
#     category = request.json.get('category')
#     amount = request.json.get('amount')
#     date = request.json.get('date')

#     if not category or not amount or not date:
#         return jsonify({'error': 'Invalid data'}), 400

#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute("""
#         UPDATE expenses
#         SET category=%s, amount=%s, date=%s
#         WHERE id=%s
#     """, (category, amount, date, id))
#     conn.commit()
#     cursor.close()

#     return jsonify({'id': id, 'category': category, 'amount': amount, 'date': date})

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS  # <-- Import Flask-CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'Nous@12345'  # Your MySQL password
app.config['MYSQL_DB'] = 'expense_tracker'

mysql = MySQL(app)

@app.route('/expenses', methods=['GET'])
def get_expenses():
    """
    Route to get all expenses from the database.
    """
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()  # Fetch all records

    # Convert the data into a list of dictionaries
    expense_list = [{'id': expense[0], 'category': expense[1], 'amount': expense[2], 'date': expense[3]} for expense in expenses]
    
    cursor.close()

    # Return the expenses as a JSON response
    return jsonify(expense_list)

@app.route('/expenses', methods=['POST'])
def add_expense():
    # Extract JSON data from the request body
    data = request.get_json()
    
    # Check if data exists
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    # Extract values from JSON data
    category = data.get('category')
    amount = data.get('amount')
    date = data.get('date')

    # Ensure values are valid
    if not category or not amount or not date:
        return jsonify({'error': 'Missing required fields'}), 400

    # Insert into the MySQL database
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (%s, %s, %s)", (category, amount, date))
    conn.commit()  # Commit the transaction to save data
    expense_id = cursor.lastrowid  # Get the ID of the inserted row
    cursor.close()

    return jsonify({
        'id': expense_id,
        'category': category,
        'amount': amount,
        'date': date
    }), 201  # Return a response with the inserted data


@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=%s", (id,))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Expense deleted successfully'})

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    category = request.json.get('category')
    amount = request.json.get('amount')
    date = request.json.get('date')

    if not category or not amount or not date:
        return jsonify({'error': 'Invalid data'}), 400

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET category=%s, amount=%s, date=%s
        WHERE id=%s
    """, (category, amount, date, id))
    conn.commit()
    cursor.close()

    return jsonify({'id': id, 'category': category, 'amount': amount, 'date': date})

if __name__ == '__main__':
    app.run(debug=True)
