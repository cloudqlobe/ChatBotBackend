from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector
import logging
import os

# DB connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot",
        port="3307"
    )


class ActionShowRate(Action):
    def name(self):
        return "action_show_rate"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_msg = tracker.latest_message.get("text", "").lower()
        
        # Keywords to filter qualityDescription
        keywords = ['cc rate', 'cli rate', 'mob', 'mobile', 'ivr', 'local', 'international', 'correct', 'random']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Fetch all countries and country codes from DB
            cursor.execute("SELECT DISTINCT country, countryCode FROM ccrate")
            countries = cursor.fetchall()  # List of dicts: {"country":..., "countryCode":...}

            destination = None
            dest_code = None

            # Match country name or country code (with/without +)
            for row in countries:
                country_name = row['country'].lower()
                country_code = str(row['countryCode']).lower().lstrip('+')  # remove + if exists

                if country_name in user_msg or country_code in user_msg or f"+{country_code}" in user_msg:
                    destination = row['country']
                    dest_code = row['countryCode']
                    break

            if not destination:
                dispatcher.utter_message(text="Please specify the country or country code you want rates for.")
                return []

            # Build dynamic SQL for qualityDescription keywords
            like_conditions = " OR ".join(["LOWER(qualityDescription) LIKE %s" for _ in keywords])
            query = f"""
                SELECT category, profile, billingCycle, rate, status, qualityDescription
                FROM ccrate
                WHERE (LOWER(country) = %s OR countryCode = %s)
                AND ({like_conditions})
            """
            params = [destination.lower(), dest_code] + [f"%{kw}%" for kw in keywords]
            cursor.execute(query, params)
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            if not results:
                dispatcher.utter_message(text=f"No rates found for {destination} ({dest_code}).")
                return []

            # Build response message
            msg = f"📊 Rates for {destination} ({dest_code}):\n"
            for r in results:
                msg += (
                    f"{r['category']} | {r['profile']} | "
                    f"Billing: {r['billingCycle']} | Rate: {r['rate']} | Status: {r['status']}"
                )
                if r['qualityDescription']:
                    msg += f" | Quality: {r['qualityDescription']}"
                msg += "\n"

            dispatcher.utter_message(text=msg)

        except mysql.connector.Error as e:
            logging.error(f"MySQL Error: {e}")
            dispatcher.utter_message(text="⚠️ Sorry, I cannot fetch rates right now. Please try later.")

        return []

class ActionShowSupport(Action):
    def name(self):
        return "action_show_support"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(
            text="You can contact support at:\n📧 support@cloudqlobe.com\n📞 +91-9876543210\n24/7 Helpdesk"
        )
        return []

class ActionTradeSignup(Action):
    def name(self):
        return "action_trade_signup"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(
            text="To open a trade account, visit: https://cloudqlobe.com/signup"
        )
        return []

class ActionTestRoute(Action):
    def name(self):
        return "action_test_route"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(
            text="To test a route:\n1️⃣ Open a trade account\n2️⃣ Request trial route testing\n3️⃣ Configure SIP/VoIP\n4️⃣ Test sample calls"
        )
        return []
