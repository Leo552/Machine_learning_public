# Made by Leo
import random

def get_difference(N, list_1, list_2): # Takes two lists and returns the proportion that the are simular
    sum_correct = 0
    for example in range(N):
        if list_1[example] == list_2[example]:
            sum_correct += 1
    
    return (sum_correct/N)


def get_random_points(X, num_req):
    points = []
    counter = 0
    while counter < num_req:
        random_index = random.randint(-1,(num_req - 1)) 
        if not random_index in points:
            points.append(X[random_index])
            counter += 1
            
    return points 


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


def build_sublists(X, y, pivot, label): # Build two list with the pivot and label provided
    list_1_X = []
    list_1_y = []
    list_2_X = []
    list_2_y = []
    for example in range(len(X)):
        if X[example][label] <= pivot:
            list_1_X.append(X[example])
            list_1_y.append(y[example])
        else:
            list_2_X.append(X[example])
            list_2_y.append(y[example])
    
    return list_1_X, list_1_y, list_2_X, list_2_y

def shuffle(X, y):
    c = list(zip(X, y))
    random.shuffle(c)
    X, y = zip(*c)
    
    return X, y