import traceback
from flask import Flask
from flask_pymongo import PyMongo
from kafka import KafkaConsumer
import json
from config import MONGO_URI
from services.email_service import send_email
from services.sms_service import send_sms
from services.inapp_service import store_in_app

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
mongo.init_app(app)

with app.app_context():
    try:
        print("Existing collections:", mongo.db.list_collection_names())
    except Exception as conn_err:
        print("Error connecting to Mongo or listing collections:")

    consumer = KafkaConsumer(
        'messages',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print("Worker is listening.")

    for msg in consumer:
        print("\nGot message:", msg)
        try:
            print("Decoded value:", msg.value)
            data = msg.value
            msg_type = data.get("type")
            recipient = data.get("recipient")
            message = data.get("message")

            if not msg_type or not recipient or not message:
                print(f"Missing fields in message: {data}")
                continue

            if msg_type == "email":
                user = mongo.db.users.find_one({"email": recipient})
            elif msg_type == "sms":
                user = mongo.db.users.find_one({"phone": recipient})
            elif msg_type == "inapp":
                user = mongo.db.users.find_one({"_id": recipient})
            else:
                print("Unknown message type:", msg_type)
                continue

            if not user:
                print(f"No user found with {msg_type} = {recipient}. Skipping.")
                continue

            user_id = user.get("_id")
            if not user_id:
                print(f"User found but missing _id field: {user}. Skipping.")
                continue

            print(f"Found user with ID: {user_id}")

            try:
                if msg_type == "email":
                    print(f"Sending email to user_id={user_id}")
                    send_email(mongo.db,user_id, message)
                elif msg_type == "sms":
                    print(f"Sending SMS to user_id={user_id}")
                    send_sms(mongo.db,user_id, message)
                elif msg_type == "inapp":
                    print(f"Storing in-app notification for user_id={user_id}")
                    store_in_app(mongo.db,user_id, message)
            except Exception as notify_err:
                print(f"Error sending/storing notification for user_id={user_id}:")
                traceback.print_exc()
                continue

        except Exception as e:
            print("Unexpected error processing message:")
