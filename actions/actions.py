from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Expanded rate data
rates_data = [
    {"country": "India", "category": "CC", "profile": "IVR", "rate": "0.05", "status": "Active"},
    {"country": "India", "category": "CLI", "profile": "Outbound", "rate": "0.12", "status": "Active"},
    {"country": "India", "category": "CC", "profile": "Outbound", "rate": "0.08", "status": "Inactive"},
    {"country": "India", "category": "CLI", "profile": "IVR", "rate": "0.10", "status": "Active"},
    {"country": "USA", "category": "CC", "profile": "IVR", "rate": "0.15", "status": "Active"},
    {"country": "USA", "category": "CLI", "profile": "Outbound", "rate": "0.20", "status": "Inactive"},
    {"country": "UK", "category": "CC", "profile": "IVR", "rate": "0.18", "status": "Active"},
    {"country": "UK", "category": "CLI", "profile": "Outbound", "rate": "0.25", "status": "Active"},
    {"country": "Canada", "category": "CC", "profile": "IVR", "rate": "0.22", "status": "Active"},
    {"country": "Canada", "category": "CLI", "profile": "Outbound", "rate": "0.30", "status": "Inactive"},
    {"country": "UAE", "category": "CLI", "profile": "Outbound", "rate": "0.35", "status": "Active"},
    {"country": "Australia", "category": "CC", "profile": "IVR", "rate": "0.28", "status": "Active"}
]

class ActionShowRate(Action):
    def name(self):
        return "action_show_rate"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Get the destination from the user's message
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Please tell me the country you want rates for.")
            return []

        # Filter rates for the requested country
        country_rates = [r for r in rates_data if r["country"].lower() == destination.lower()]
        if not country_rates:
            dispatcher.utter_message(text=f"Sorry, no rates found for {destination}.")
            return []

        # Build response message
        msg = f"Rates for {destination}:\n"
        for r in country_rates:
            msg += f"{r['category']} | {r['profile']} | Rate: {r['rate']} | Status: {r['status']}\n"

        dispatcher.utter_message(text=msg)
        return []
