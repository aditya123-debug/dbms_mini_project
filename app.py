from flask import Flask, request, jsonify,render_template
import mysql.connector

app = Flask(__name__)


# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change according to your MySQL user
        password="mh14ct9775",  # Your MySQL password
        database="pizza_store"
    )


# Add a new customer
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    db = connect_db()
    cursor = db.cursor()

    query = "INSERT INTO Customers (name, email, phone_number, address) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (data['name'], data['email'], data['phone_number'], data['address']))
    db.commit()

    return jsonify({'message': 'Customer added successfully'}), 201


# Place a new order
@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    db = connect_db()
    cursor = db.cursor()

    # Insert order
    query_order = "INSERT INTO Orders (customer_id, total_price) VALUES (%s, %s)"
    cursor.execute(query_order, (data['customer_id'], data['total_price']))
    order_id = cursor.lastrowid

    # Insert order details
    for item in data['order_items']:
        query_order_details = "INSERT INTO OrderDetails (order_id, pizza_id, topping_id, quantity) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_order_details, (order_id, item['pizza_id'], item['topping_id'], item['quantity']))

    db.commit()
    return jsonify({'message': 'Order placed successfully', 'order_id': order_id}), 201


# Fetch all orders
@app.route('/get_orders', methods=['GET'])
def get_orders():
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Orders")
    orders = cursor.fetchall()

    return jsonify(orders)


# Update an order
@app.route('/update_order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    db = connect_db()
    cursor = db.cursor()

    query = "UPDATE Orders SET total_price = %s WHERE order_id = %s"
    cursor.execute(query, (data['total_price'], order_id))
    db.commit()

    return jsonify({'message': 'Order updated successfully'})


# Delete an order
@app.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    db = connect_db()
    cursor = db.cursor()

    query = "DELETE FROM Orders WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    db.commit()

    return jsonify({'message': 'Order deleted successfully'})

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
