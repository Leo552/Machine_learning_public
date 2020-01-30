# Made by Leo

# Stores the inverse values in self
def min_max_transformation(self, X): # Doesn't work for negatives
    reshuffled_X = reshuffle(X)
    new_X = []
    self.min_range_list = [] # Used to inverse the min max transformation
    for feature in range(self.dimensions): # Runs through the features
        max_val = max(reshuffled_X[feature])
        min_val = min(reshuffled_X[feature])
        feature_range = max_val - min_val
        self.min_range_list.append({'min':min_val, 'range': feature_range})
        inter_X = [] # Stores the one dimension intermediate values
        for example in range(self.N):
            inter_X.append((X[example][feature] - min_val) / feature_range) # The min example not removed although the book said it usually is
        new_X.append(inter_X)
        
    return reshuffle(new_X)


def inverse_min_max_transformation(self, scaled_data):
    non_scaled_data = []
    for example in range(len(scaled_data)):
        inter_data = []
        for feature in range(self.dimensions):
            inter_data.append(scaled_data[example][feature] * self.min_range_list[feature]['range'] + self.min_range_list[feature]['min'])
        non_scaled_data.append(inter_data)
        
    return non_scaled_data


def reshuffle(two_d_list): # Make x to y and y to x
    new_list = []
    max_x = len(two_d_list)
    max_y = len(two_d_list[0])
    for y in range(max_y):
        one_d_list = []
        for x in range(max_x):
            one_d_list.append(two_d_list[x][y])
        new_list.append(one_d_list)
    
    return new_list