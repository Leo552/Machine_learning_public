import math
import operator
from collections import Counter

class DecisionTree:
    # Needs doing:
    # Pruning
    # Numerisation of the qualitative data
    
    # Constructor
    def __init__(self, criterion = 'entropy', max_depth = 5, min_split = 10): # Instantiate the class
        self.name = 'Decision tree classifier model'
        self.criterion = criterion
        self.max_depth = max_depth  
        self.min_split = min_split
    
    
    def fit(self, X, y): # Make the tree
        no_classes = len(Counter(y).keys())
        self.tree_X, self.tree_y, self.nodes = DecisionTree.get_sublists(self, X, y,no_classes, 0)
            
    
    def test(self, test_X, test_y):
        predictions = DecisionTree.predict(self, test_X) # Need to fit the tree first
        return DecisionTree.accuracy(predictions, test_y)
    
        
    def predict(self, test_data): # Classifies all the test data according to the nodes of the decision tree
        predicted_classes = []
        for test_data_example in test_data: # Run through the data set
            predicted_classes.append(DecisionTree.find_the_leaf(test_data_example, self.nodes))
        return predicted_classes

    
    def numerise_data(X, y):
        numbers_to_class = []
        for label in range(len(X[0])): # Assumes the first entry completely represents the data e.g. type and number of labels
            if not type(X[label]) == int or not type(X[label]) == float:
                if not X[label] in numbers_to_class:
                    numbers_to_class
                    
                    #### Continue here
                    
                    
    def find_the_leaf(test_data_example, current_node): # Recursive function
        if test_data_example[current_node['label']] > current_node['pivot']: # Above the pivot
            if type(current_node['branch_2']) is str:
                return current_node['branch_2']
            else:
                return DecisionTree.find_the_leaf(test_data_example, current_node['branch_2'])
        else: # Below the pivots
            if type(current_node['branch_1']) is str: 
                return current_node['branch_1']
            else:
                return DecisionTree.find_the_leaf(test_data_example, current_node['branch_1'])
       
         
    def get_sublists(self, X, y, no_classes, depth_counter):
        best_information_gain = 0 # This will contain the current best total information gain
        best_pivot = 0 # Index of the current best
        best_label = 0

        for example in range(len(X)): # Assumes a complete dataset
            # Runs through each example choosing it as the pivot point - may repeat

            for label in range(len(X[example])): # Runs through each label
                # This dictionary is used to find the start entropy
                dict_0 = dict.fromkeys(range(no_classes)); dict_0['total'] = 0
                dict_1 = dict_2 = dict_0
                # Creates two dictionaries that contain the actual class distribution above and below the pivot
                # The total will make it easier to calculate the probablilities of each class later
                for data_point in range(len(X)):
                    dict_0[y[data_point]] += 1
                    dict_0['total'] += 1
                    if X[data_point][label] <= X[example][label]: # Get the distribution of the data either side of the pivot
                        dict_1[y[data_point]] += 1
                        dict_1['total'] += 1
                    else:
                        dict_2[y[data_point]] += 1
                        dict_2['total'] += 1
                
                # To stop a class containing all of one type from splitting                    
                for class_index in range(no_classes):
                    if dict_0[class_index] == dict_0['total']:
                        return X, y, str(max({x:dict_0[x] for x in range(no_classes)}.items(), key=operator.itemgetter(1))[0])
                # Leaf class stored as a string
                
                total_information_gain = 2*DecisionTree.get_weighted_entropy(dict_0) - DecisionTree.get_weighted_entropy(dict_1) - DecisionTree.get_weighted_entropy(dict_2)

                if total_information_gain > best_information_gain:
                    best_information_gain = total_information_gain
                    best_label = label # Best label - a coordinate
                    best_pivot = X[example][label] # An actual value
                    prominant_class_1 = str(max({x:dict_1[x] for x in range(3)}.items(), key=operator.itemgetter(1))[0]) # Used to classify the leaf in it reaches max depth or minimum split size
                    prominant_class_2 = str(max({x:dict_2[x] for x in range(3)}.items(), key=operator.itemgetter(1))[0]) # Used to remove the total part

        list_1_X, list_1_y, list_2_X, list_2_y = DecisionTree.build_sublists(X, y , best_pivot, best_label)
        depth_counter += 1

        if depth_counter < self.max_depth:
            if len(list_1_X) >= self.min_split:
                list_1_X, list_1_y, node_1 = DecisionTree.get_sublists(self, list_1_X, list_1_y, no_classes, depth_counter)
            else:
                node_1 = prominant_class_1
            if len(list_2_X) >= self.min_split:
                list_2_X, list_2_y, node_2 = DecisionTree.get_sublists(self, list_2_X, list_2_y, no_classes, depth_counter)
            else:
                node_2 = prominant_class_2
        else:
            node_1 = prominant_class_1; node_2 = prominant_class_2

        return [list_1_X, list_2_X], [list_1_y, list_2_y], {'pivot':best_pivot, 'label':best_label, 'branch_1':node_1, 'branch_2':node_2}


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
    
    
    def get_weighted_entropy(distribution_of_classes): # recieves a dictionary of the distribution of the classes
        entropy = 0
        for class_ in range(len(distribution_of_classes) - 1): # Minus 1 to disclude the total part
            try:
                probability_of_class = distribution_of_classes[class_]/distribution_of_classes['total']
                if probability_of_class != 0:
                    # Weighted by the probability
                    entropy -= probability_of_class * (probability_of_class * math.log2(probability_of_class)) # See equation for entropy
            except: # Zero error
                continue
        
        if distribution_of_classes['total'] == 0: # To stop 0 length classes
            entropy += 10

        return entropy
    
    
    def accuracy(list_1, list_2): # Assumes they are the same length
        predictions_correct = 0
        for i in range(len(list_1)):
            if str(list_1[i]) == str(list_2[i]):
                predictions_correct += 1
        return (predictions_correct/len(list_1))
