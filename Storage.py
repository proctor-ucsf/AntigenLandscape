import numpy as np
class Storage:
    def __init__(self, time, data):
        self.time = time
        self.data = data
        
    def get_time(self):
        return self.time
    
    def get_data(self):
        return self.data
        