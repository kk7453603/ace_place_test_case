from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time

app = Flask(__name__)


db_uri = os.environ.get('DB_URI')
client = MongoClient(db_uri)
db = client['notifications']
collection = db['users']


smtp_host = os.environ.get('SMTP_HOST')
smtp_port = int(os.environ.get('SMTP_PORT'))
smtp_login = os.environ.get('SMTP_LOGIN')
smtp_password = os.environ.get('SMTP_PASSWORD')
smtp_email = os.environ.get('SMTP_EMAIL')
smtp_name = os.environ.get('SMTP_NAME')


@app.route('/create', methods=['POST'])
def create_notification():
    try:
        data = request.json
        user_id = data.get('user_id')
        target_id = data.get('target_id')
        key = data.get('key')
        notification_data = data.get('data')

        user = get_user(user_id)
        if not user:
            email = request.args.get('email')
            if not email:
                return jsonify({"success": False, "message": "Email is required"}), 400
            user = create_user(user_id, email)

        notification = {
            "id": get_next_notification_id(user),
            "timestamp": get_current_timestamp(),
            "is_new": True,
            "user_id": user['_id'],
            "key": key,
            "target_id": target_id,
            "data": notification_data
        }
        insert_notification(notification)

        if key == 'registration' or key == 'new_login':
            send_email(user, notification)

        return jsonify({"success": True}), 201
    except PyMongoError as e:
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route('/list', methods=['GET'])
def get_notifications():
    try:
        user_id = request.args.get('user_id')
        skip = int(request.args.get('skip', '0'))
        limit = int(request.args.get('limit', '10'))

        user = get_user(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        notifications = list(collection.find({"user_id": user['_id']}).
                             skip(skip).
                             limit(limit).
                             sort("timestamp", -1))

        total_notifications = collection.count_documents({"user_id": user['_id']})
        new_notifications = collection.count_documents({"user_id": user['_id'], "is_new": True})

        response = {
            "success": True,
            "data": {
                "elements": total_notifications,
                "new": new_notifications,
                "request": {
                    "user_id": user_id,
                    "skip": skip,
                    "limit": limit
                },
                "list": notifications
            }
        }
        return jsonify(response), 200
    except PyMongoError as e:
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route('/read', methods=['POST'])
def mark_notification_as_read():
    try:
        user_id = request.args.get('user_id')
        notification_id = request.args.get('notification_id')

        user = get_user(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        notification = collection.find_one({"_id": notification_id, "user_id": user['_id']})
        if not notification:
            return jsonify({"success": False, "message": "Notification not found"}), 404
        collection.update_one({"_id": notification_id}, {"$set": {"is_new": False}})

        return jsonify({"success": True}), 200
    except PyMongoError as e:
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


def get_user(user_id):
    return collection.find_one({"_id": user_id})


def create_user(user_id, email):
    user = {"_id": user_id, "email": email}
    collection.insert_one(user)
    return user


def insert_notification(notification):
    collection.insert_one(notification)


def get_next_notification_id(user):
    max_notification_id = collection.find_one({"user_id": user['_id']}, sort=[("id", -1)])['id']
    if max_notification_id is None:
        return 1
    else:
        return max_notification_id + 1


def get_current_timestamp():
    return int(time.time())


def send_email(user, notification):
    recipient = user['email']
    subject = "Notification"
    message = f"Hello,\n\nYou have a new notification with key: {notification['key']}\n\nRegards,\nYour App"

    msg = MIMEMultipart()
    msg['From'] = smtp_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_login, smtp_password)
        server.send_message(msg)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8080)))
