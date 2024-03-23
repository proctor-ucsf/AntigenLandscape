from Antigen import Antigen
from Storage import Storage
import math
import numpy as np
import matplotlib.pyplot as plt


class Landscape:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clock = 0
        self.landscape = []
        self.new_antigens = []
        self.previous_landscape_count = -1
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Antigen(position=(i, j)))
            self.landscape.append(row)
        
    def __str__(self):
        result = ""
        for row in self.landscape:
            for antigen in row:
                if antigen.timestamp == -1:
                    result += "_"
                else:
                    result += "A"
                result += " "
            result += "\n"
        return result
    
    def graph(self, show_clock=False):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = np.linspace(0, self.width, 100)
        y = np.linspace(0, self.height, 100)
        X, Y = np.meshgrid(x, y)
        
        for i in range(self.height):
            for j in range(self.width):
                curr_ant = self.landscape[i][j]
                if curr_ant.timestamp >= 0:
                    mean_x, mean_y = curr_ant.position
                    variance = curr_ant.spread
                    # calculating Z values for the gaussian
                    Z = np.exp(-((X - mean_x)**2 + (Y - mean_y)**2) / (2 * variance))
                    ax.plot_surface(X, Y, Z * curr_ant.get_response(), rstride=1, cstride=1, alpha=0.5, cmap='viridis')
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Antigen Response')
        if show_clock:
            ax.set_title(f'Clock: {self.clock}', fontsize=8)
        plt.show()

    def clear_new_ants_arr(self):
        self.new_antigens = []
        
    def get_new_ants(self):
        return self.new_antigens
        
    def add_antigen(self, x, y, antigen):
        # first check if the position is available
        if self.landscape[x][y].position is not None:
            antigen.set_timestamp(self.clock)
            antigen.set_position((x, y))
            self.landscape[x][y] = antigen
            self.new_antigens.append(antigen)
        # if it is, then add the position otherwise error
        else:
             print('Error: space already taken')
    
    
    # Purpose for this is to compare the current count with previous count
    # so we can see how the landscape has evolved compared to the past
    def get_landscape_count(self):
        result = 0 
        for row in self.landscape:
            for antigen in row:
                if antigen.timestamp != -1:
                    result += 1
        return result
    
    # Returns a list of which antigens a certain antigen lies
    # in the spread of, returns an empty is list if it doesn't live in the
    # spread of any other antigens

    # Note there is a slight inconsistency here because in the
    # graphing code, we treat the spread as the variance of a
    # gaussian rather than a hard cut off, so theoretically the
    # spread of these are infinite, but just small at certain places
    # thus instead we will simply use the ±2 * spread^2 as a cutoff
    # because this would be ± 2 SD
    def find_intersections(self, antigen):
        # First find area to search through, since the
        # cross section of a 3D gaussian is a cirlce
        # the radius will be 2 SD
        center_x, center_y = antigen.get_position()
        radius = 2 * (antigen.get_spread() ** 2)
        points = []
        result = []

        for x in range(max(0, center_x - radius), min(center_x + radius + 1, self.width)):
            for y in range(max(0, center_y - radius), min(center_y + radius + 1, self.height)):
                if math.sqrt((x - center_x)**2 + (y - center_y)**2) <= radius:
                    points.append((x, y))

        for point in points:
            curr_ant = self.landscape[point[0]][point[1]]
            if curr_ant.timestamp != -1:
                result.append(curr_ant)

            return result


    # Also outputs a Storage object
    # essentially saving the previous
    # landscape if we want to go back and look at it again
    # for analytics purposes
    def increment_time(self): #month
        result = Storage(self.clock, self.landscape)
        self.clock += 1
        # Here we will also update the variance of each antigen
        # based on severity and novelty 
        # so if it is very severe we will only decrease spread by
        # a little but
        # and if it is new then the rate of varaince decreasing is slow
    
        
        # We think that spread should remain constant because 
        # it's unlikely that the property of the immune cells
        # change overtime, rather just the quantity which would only
        # reflect a change in the response rather than the spread 
        def update_antigen_spread(antigen):
            return antigen.get_spread()
        
        # calculates new response value
        def update_antigen_response(antigen):
            reduce_const = 0.93 # make this global maybe
            def no_antigen_presence_update(reduce_const):
                curr = antigen.get_response()
                result = max(curr * reduce_const, antigen.get_baseline())
                return result
            
            if len(self.new_antigens) > 0:
                # then we need to check if the new antigen(s) 
                # lies within the spread of the current antigen
                for ant in self.new_antigens:
                    curr_intersections = self.find_intersections(ant)
                    if len(curr_intersections) == 0:
                        return no_antigen_presence_update(reduce_const)
                    else:
                        # if the memory of our antigen is high
                        # and it was imprinted when individual was
                        # young then we increase by a lot
                        if self.clock - antigen.get_timestamp() <= 6 * 12:
                            # aka if got it when less than 6 yrs old (young)
                            multiplier = 0.5
                        else:
                            multiplier = 0.25
                        return antigen.get_response() * (1 + multiplier * antigen.get_memory())
                        # lowest possible increase occurs when antigen appears after 6 yrs
                        # and has a low memory in which case we would have 
                        # an increase of 25%
                        # in the highest possible increase occurs when antigen appears
                        # before 6 yrs and has a high memory in which case we have an incrase
                        # of 0.5 * 4 of 200%    
            else:
                # if no new antigen then response just goes down exponetially
                return no_antigen_presence_update(reduce_const)
            
    
        # loop through the antigens and update their spread:
        for i in range(self.height):
            for j in range(self.width):
                curr_antigen = self.landscape[i][j]
                if curr_antigen.get_timestamp() != -1:
                    new_response_val = update_antigen_response(curr_antigen)
                    curr_antigen.set_response(new_response_val)    
                    
                    
        self.clear_new_ants_arr()
        return result