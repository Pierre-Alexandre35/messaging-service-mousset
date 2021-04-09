import itertools, time

class Campaign():
    newid = itertools.count()
    
    def __init__(self, message):
        self.id = next(Campaign.newid)
        self.timestamp = time
        self.message = message
        
    def dict(self):
        return {
        "id" : self.id,
        "timestamp" : self.timestamp,
        "message" : self.message
        }