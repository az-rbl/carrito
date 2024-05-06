from flask import Flask, request, jsonify
import threading
import carrito as carrito
import redis
import carrito
import os
from dotenv import load_dotenv


load_dotenv()

load_dotenv()
app = Flask(__name__)
print(os.environ.get("DATABASE_URL"))
conn = redis.from_url(os.environ.get("DATABASE_URL"))

@app.route('/cart', methods=['POST'])
def add_to_cart():
    item_id = request.json['item_id']
    quantity = request.json['quantity']
    user_id = request.json.get('user_id')  

    carrito.add_to_cart(conn, user_id,item_id,quantity)
    return jsonify({"message": f"Cart:{user_id} changed. item:{item_id} = {quantity}"}), 200


@app.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.json["user_id"]
    cart = carrito.fetch_cart(conn, user_id)
    return jsonify(str(cart)), 200

@app.route('/cart', methods=['DELETE'])
def del_cart():
    user_id = request.json["user_id"]
    carrito.delete_cart(conn,user_id)
    return jsonify({"message": f"Cart {user_id} deleted"})


if __name__ == '__main__':
    thread = threading.Thread(target=carrito.clean_full_sessions, args=(conn,), daemon=True)
    thread.start()
    app.run(debug=False)