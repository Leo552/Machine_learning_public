# Made by Leo
import random

class K_Means:
    # Needs doing:
    # Shared information/variance
    # Between cluster sum of squares BSS
    
    # Constructor
    def __init__(self, k, N, dimensions, max_iterations = 20, min_difference = 0.01):
        self.name = 'K means clustering model'
        self.k = k
        self.N = N
        self.dimensions = dimensions
        self.max_iterations = max_iterations # Max number of changes to the centroids 
        self.min_difference = min_difference # Min change in the clusters each point is allocated to 
    
    
    def fit(self, X, repeats = 10):
        X = K_Means.min_max_transformation(self, X)
        start_centroids = K_Means.get_best_start_points(self, X, repeats) # These are the best ones 
        start_closest_centroids = K_Means.get_closest_centroids(self, X, start_centroids)
        self.scaled_centroids, closest_centroids = K_Means.get_new_centroids(self, X, start_centroids, start_closest_centroids, 0)
        self.centroids = K_Means.inverse_min_max_transformation(self, self.scaled_centroids)
        
        
    def get_new_centroids(self, X, old_centroids, old_closest_centroids, it_count):
        if it_count >= self.max_iterations:
            new_centroids = K_Means.new_centroid_mean(self, X, old_closest_centroids)
            closest_centroids = K_Means.get_closest_centroids(self, X, new_centroids) # This contains the indexes to which each point is closest to in data space
              
            if self.min_difference >  K_Means.get_difference(self, closest_centroids, old_closest_centroids):
                return old_centroids, old_closest_centroids
            
            new_centroids = K_Means.get_new_centroids(self, X, new_centroids, closest_centroids, (it_count + 1)) # Recursive function - two different end conditions - max iterations and min difference
        else:
            return old_centroids, old_closest_centroids
        
    
    def new_centroid_mean(self, X, closest_centroids):
        new_centroids = []
        for cluster in range(self.k):
            new_centroid_point = [0] * self.dimensions # Quick way of making the a list full of zeros
            for example in range(self.N):
                if cluster == closest_centroids[example]: # Ignore all the other cluster centroids
                    for dimension in range(self.dimensions):
                        new_centroid_point[dimension] += X[example, dimension]
            new_centroids.append([x / self.N for x in new_centroid_point])
        
        return new_centroids
    
    
    def get_WSS(self, X, centroids, closest_centroids):
        WSS_sum = 0
        for cluster in range(self.k):
            for example in range(self.N):
                if cluster == closest_centroids[example]: # Ignore all the other cluster centroids
                    for dimension in range(self.dimensions):
                        WSS_sum += (centroids[cluster][dimension] - X[example][dimension]) ** 2
        
        return WSS_sum
    
    
    def get_best_start_points(self, X, repeats):
        best_WSS = -1
        best_start_centroid = [[]]
        for repeat in range(repeats):
            # This process does the k means from scratch
            old_centroids = K_Means.get_random_points(self, X)
            old_closest_centroids = K_Means.get_closest_centroids(self, X, old_centroids)
            scaled_centroids, closest_centroids = K_Means.get_new_centroids(self, X, old_centroids, old_closest_centroids, 0)
                   
            if (K_Means.get_WSS(self, X, scaled_centroids, closest_centroids)) < best_WSS or best_WSS == -1:
                best_start_centroid = scaled_centroids
                best_WSS = K_Means.get_WSS(self, X, scaled_centroids, closest_centroids)
                print(best_WSS, K_Means.inverse_min_max_transformation(self, best_start_centroid))
        
        return best_start_centroid 
    
    
    def min_max_transformation(self, X): # Doesn't work for negatives
        reshuffled_X = K_Means.reshuffle(X)
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
            
        return K_Means.reshuffle(new_X)
    
    
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
    
    
    def get_closest_centroids(self, X, centroids):
        closest_centroid = []
        for example in range(self.N):
            closest_centroid.append(-1) # As opposed to doing it in one go
            current_best_distance = -1 # Needs to be bigger than any possible distance 
            
            for centroid in range(self.k):
                
                squared_sum = K_Means.get_squared_euclidian_distance(self.dimensions, X[example], centroids[centroid])
                
                if squared_sum < current_best_distance or current_best_distance == -1:
                    current_best_distance = squared_sum
                    closest_centroid[example] = centroid
        
        return closest_centroid


    def get_difference(self, list_1, list_2): # Takes two lists and returns the proportion that the are simular
        sum_correct = 0
        for example in range(self.N):
            if list_1[example] == list_2[example]:
                sum_correct += 1
        
        return (sum_correct/self.N)
    
    
    def get_random_points(self, X):
        points = []
        counter = 0
        while counter < self.k:
            random_index = random.randint(-1,(self.N - 1)) 
            if not random_index in points:
                points.append(X[random_index])
                counter += 1
                
        return points 
    
    
    def get_squared_euclidian_distance(dimensions, example_1, example_2):
        squared_sum = 0
        for dimension in range(dimensions):
            squared_sum += (example_1[dimension] - example_2[dimension]) ** 2
        
        return squared_sum