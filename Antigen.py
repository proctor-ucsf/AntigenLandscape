from numpy import exp

class Antigen:
    def __init__(self, spread=0, memory=0, response=0,
                 name=None, position=None, timestamp=-1):
        self.spread = spread
        self.memory = memory
        
        # here memory will range between the following values
        # 1 - mild
        # 2 - intense
        # 3 - extreme
        # 4 - permanent (e.g. chicken pox)
        
        self.response = response
        self.init_response = response
        self.name = name
        self.position = position
        self.timestamp = timestamp # (in months)

        self.imprinting_age = 6 * 12
    # 6 years old      
    
    def get_timestamp(self):
        return self.timestamp
    
    def get_position(self):
        return self.position
    
    def get_response(self):
        return self.response
    
    def get_spread(self):
        return self.spread
    
    def get_baseline(self):
        # Here all the math and visualization is here
        # https://www.desmos.com/calculator/vvaez1jd1v
        # We can adjust parameters as needed
        a = self.timestamp
        m = self.memory
        c = self.init_response
        return c / (1 + exp((a - m*c) / (m*c/4)))
    
    def get_memory(self):
        return self.memory
    
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
        
    def set_position(self, position):
        self.position = position
        
    def set_response(self, response):
        self.response = response
        
    def set_spread(self, spread):
        self.spread = spread
    
    