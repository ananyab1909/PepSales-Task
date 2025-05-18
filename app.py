from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from config import MONGO_URI
import uuid,json
from models.mongo import mongo
from services.email_service import send_email
from services.sms_service import send_sms
from services.inapp_service import store_in_app
from kafka import KafkaProducer

app = Flask(__name__)
app.app_context().push()
app.config["MONGO_URI"] = MONGO_URI
mongo.init_app(app)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    required_fields = ["name", "email", "phone"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already registered"}), 409
    if mongo.db.users.find_one({"phone": data["phone"]}):
        return jsonify({"error": "Phone already registered"}), 409

    user_id = str(uuid.uuid4())

    mongo.db.users.insert_one({
        "_id": user_id,
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"]
    })

    return jsonify({"message": "User created", "user_id": user_id}), 201

@app.route("/notifications", methods=["POST"])
def send_notification():
    data = request.json
    msg_type = data.get("type")          
    message = data.get("message")
    recipient = data.get("recipient")    
    if not all([msg_type, recipient, message]):
        return jsonify({"error": "Missing fields"}), 400

    if msg_type == "email":
        user = mongo.db.users.find_one({"email": recipient})
    elif msg_type == "sms":
        user = mongo.db.users.find_one({"phone": recipient})
    elif msg_type == "inapp":
        user = mongo.db.users.find_one({"_id": recipient})
    else:
        return jsonify({"error": "Invalid notification type"}), 400

    if not user:
        return jsonify({"error": "Recipient not found"}), 404

    notification_payload = {
        "type": msg_type,
        "recipient": recipient,
        "message": message
    }

    producer.send("messages", notification_payload)
    producer.flush()

    return jsonify({"status": f"{msg_type} notification queued"}), 200


@app.route("/users/<user_id>/notifications", methods=["GET"])
def get_user_notifications(user_id):
    if not mongo.db.users.find_one({"_id": user_id}):
        return jsonify({"error": "User not found"}), 404

    notifications = mongo.db.messages.find({"user_id": user_id})
    return jsonify([{
        "type": n["type"],
        "message": n["message"]
    } for n in notifications]), 200

if __name__ == "__main__":
    app.run(debug=True)
