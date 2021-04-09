import itertools
from datetime import datetime

class Campaign():
    newid = itertools.count()

    def __init__(self, message, selected_list, cost, successes, failures):
        self.id = next(Campaign.newid)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.message = message
        self.selected_list = selected_list
        self.cost = cost
        self.successes = successes
        self.failures = failures
        

    def dict(self):
        return {
        "id" : self.id,
        "timestamp" : self.timestamp,
        "message" : self.message,
        "selected_list" : self.selected_list,
        "cost" : self.cost,
        "successes" : self.successes,
        "failures" : self.failures
        }