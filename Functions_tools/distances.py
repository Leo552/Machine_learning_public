# Made by Leo
import Math

# Can be used if only a relative distance is needed
def get_squared_euclidian_distance(dimensions, example_1, example_2):
    squared_sum = 0
    for dimension in range(dimensions):
        squared_sum += (example_1[dimension] - example_2[dimension]) ** 2
    
    return squared_sum


def get_euclidian_distance(dimensions, example_1, example_2):
    squared_sum = 0
    for dimension in range(dimensions):
        squared_sum += (example_1[dimension] - example_2[dimension]) ** 2
    
    return Math.sqrt(squared_sum)


def get_Manhattan_distance(dimensions, example_1, example_2):
    dist_sum = 0
    for dimension in range(dimensions):
        dist_sum += abs(example_1[dimension] - example_2[dimension])
    
    return dist_sum