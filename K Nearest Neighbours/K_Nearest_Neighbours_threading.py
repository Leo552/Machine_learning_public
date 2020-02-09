# Made by Leo
import random
import threading
from queue import Queue
import psutil # For getting the number of CPUs

class K_Nearest_Neighbours_Regression:
    # Need to do:
    # - Confidence level of each prediction
    # - Implement a lot of speed efficiency improvements

    def __init__(self, k, distance_measure='euclidean'):
        self.k = k
        if distance_measure == 'euclidean':
            self.distance_measure = self.get_squared_euclidean_distance
        elif distance_measure == 'manhattan':
            self.distance_measure = self.get_squared_euclidean_distance
        else:
            print('Enter a valid distance')
        
    def fit(self, X, y):
        self.X = X
        self.y = y
        self.dimensions = len(X[0])

    def test(self, test_X, true_y, discrete_y):
        predict_y = K_Nearest_Neighbours_Regression.get_predictions(self, test_X, discrete_y)
        return predict_y, K_Nearest_Neighbours_Regression.get_mean_squared_error(self, true_y, predict_y)
    
    def get_predictions(self, test_X, discrete_y):  # Run the threads in parallel
        # Set up the job queue
        self.job_q = Queue()
        # Set up the return bus queue
        self.r_bus = Queue()

        # Set up the threads
        for worker in range(psutil.cpu_count()): # Number of cores = number of workers
            t = threading.Thread(target = self.threader)
            t.daemon = True # Die when the main thread dies
            t.start()
                        
        # Add the jobs to the queue
        for job in range(len(test_X)):
            self.job_q.put([job, test_X[job], discrete_y])
        
        # Wait till all the jobs are complete
        self.job_q.join()
        
        predictions = [0 for i in range(len(test_X))]
        for i in range(len(test_X)):
            [job_num, predicted] = self.r_bus.get()
            predictions[job_num] = predicted
            self.r_bus.task_done()
        return predictions
    
    def predict(self, test_example, discrete_y, job_num):        
        default_val = 123456789
        neighbours_X = [default_val]
        neighbours_y = [default_val] # Ensure this is well above the max distance
        items_added = 0
        items_added_dist = [default_val]
        for i in range(len(self.X)):  # Run through all the examples to find the neighbors
            distance = self.distance_measure(self.dimensions, test_example, self.X[i])
            if  distance < max(items_added_dist) or items_added < self.k:
                
                if not items_added < self.k - 1:
                    index = items_added_dist.index(max(items_added_dist))
                    neighbours_X.pop(index)
                    neighbours_y.pop(index)
                    items_added_dist.pop(index)
                else:
                    items_added += 1
                
                items_added_dist.append(distance)
                neighbours_X.append(self.X[i])
                neighbours_y.append(self.y[i])
        
        # Return the data back along the return bus 
        self.r_bus.put([job_num, self.get_mean_y(neighbours_y, discrete_y)])
        # Keep the job number to maintain the order
        
    def threader(self):
        while True:
            job_num, test_example, discrete_y = self.job_q.get()
            self.predict(test_example, discrete_y, job_num)
            self.job_q.task_done()

    def get_mean_squared_error(self, true_y, test_y):
        MSE = 0
        for i in range(len(true_y)):
            MSE += (true_y[i] - test_y[i]) ** 2
        return round(MSE/len(true_y), 4)
    
    def get_mean_y(self, neighbours_y, discrete_y):
        sum_of_variable = 0
        for example in neighbours_y:
            sum_of_variable += example;
        if discrete_y:
            return int(round(sum_of_variable/self.k, 0))
        else:
            return round(sum_of_variable/self.k, 4)
    
    def get_mean(self, neighbours):
        average = []
        for feature in range(self.dimensions):
            sum_of_feature = 0
            for example in neighbours:
                sum_of_feature += example[feature]
            average.append(round(sum_of_feature/self.k, 5))
        return average

    def get_squared_euclidean_distance(self, dimensions, example_1, example_2): # All relative
        squared_sum = 0
        for dimension in range(dimensions):
            squared_sum += (example_1[dimension] - example_2[dimension]) ** 2
        return squared_sum

    def get_manhattan_distance(self, dimensions, example_1, example_2):
        dist_sum = 0
        for dimension in range(dimensions):
            dist_sum += abs(example_1[dimension] - example_2[dimension])
        return dist_sum
    
    def shuffle(X, y):
        c = list(zip(X, y))
        random.shuffle(c)
        X, y = zip(*c)
        return X, y
