from rasa_sdk.events import SlotSet, UserUtteranceReverted 
import mysql.connector
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

class SaveChatToMySQL(Action):
    def name(self):
        return "action_save_chat_to_mysql"

    def run(self, dispatcher, tracker, domain):
        # Initialize variables
        user_id = tracker.sender_id
        message = ""
        bot_response = ""
        message_time = None  # Variable to store message time

        # Iterate through tracker events to capture user messages and the last bot response
        for event in reversed(tracker.events):
            if event.get("event") == "user":
                message = event.get("text", "")
                message_time = datetime.datetime.fromtimestamp(event.get("timestamp")).strftime('%Y-%m-%d %H:%M:%S')  # Convert timestamp to datetime
                break  # Stop when the last user message is found
            elif event.get("event") == "bot":
                bot_response = event.get("text", "")

        # Insert the data into the MySQL database
        conn = mysql.connector.connect(
            host="192.168.19.160",
            user="usher",
            password="Um@ir65048420",
            database="lastdemandrasa"
        )
        cursor = conn.cursor()

        insert_query = "INSERT INTO ld_chat_history (user_id, message, bot_response, message_time) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (user_id, message, bot_response, message_time))
        conn.commit()

        cursor.close()
        conn.close()

        return []
