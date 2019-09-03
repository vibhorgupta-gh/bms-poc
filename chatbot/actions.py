from rasa_sdk.forms import FormAction
from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
import random
import os
import pickle
import pathlib


class ComplaintForm(FormAction):
    def name(self) -> Text:
        return 'complaint_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["category", "complaint_text"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "category": self.from_entity(entity="category"),
            "complaint_text": self.from_text()
        }

    def submit(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        a = {}
        filename = 'complains.pickle'
        abspath = pathlib.Path(filename).absolute()
        # load dictionary

        if os.path.exists(str(abspath)):
            with open(str(abspath), 'rb') as handle:
                a = pickle.load(handle)
        # Generate random tracking id
        complaint_id = int(random.random() * 1000)
        while complaint_id in a:
            complaint_id = int(random.random() * 1000)
        # save complaint
        category = tracker.get_slot('category')
        complaint_text = tracker.get_slot('complaint_text')
        # category,complaint,status
        a[complaint_id] = [category, complaint_text, "successfully submitted"]
        # save dictionary
        with open(str(abspath), 'wb') as handle:
            pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

        dispatcher.utter_message(
            f"Tracking ID: {complaint_id} \nCategory: {category} \nComplaint : {complaint_text}")
        return []


class TrackingForm(FormAction):
    def name(self) -> Text:
        return 'tracking_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["tracking_id"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "tracking_id": self.from_entity(entity="tracking_id")
        }

    def submit(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        tracking_id = int(tracker.get_slot('tracking_id'))
        filename = 'complains.pickle'
        abspath = pathlib.Path(filename).absolute()
        with open(str(abspath), 'rb') as handle:
            a = pickle.load(handle)
        if tracking_id not in a:
            dispatcher.utter_message(f"Please enter a valid Tracking ID : f{a}")
        else:
            dispatcher.utter_message(
                f"Category: {a[tracking_id][0]} \nComplaint : {a[tracking_id][1]} \nStatus: {a[tracking_id][2]}")
        return []
