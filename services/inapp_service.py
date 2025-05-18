from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pymongo.errors import PyMongoError
from models.mongo import mongo

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(PyMongoError),
    reraise=True
)
def store_in_app(db, user_id, message):
    print(f"Storing IN-APP notification for {user_id}: {message}")
    db.messages.insert_one({
        "user_id": user_id,
        "type": "inapp",
        "message": message
    })
    print("In-app notification stored in DB.")
