# Made by Leo
import K_Nearest_Neighbours_threading
import matplotlib.pyplot as plt
import time

'''
   Input variables (based on physicochemical tests):
   1 - fixed acidity
   2 - volatile acidity
   3 - citric acid
   4 - residual sugar
   5 - chlorides
   6 - free sulfur dioxide
   7 - total sulfur dioxide
   8 - density
   9 - pH
   10 - sulphates
   11 - alcohol
   Output variable (based on sensory data): 
   12 - quality (score between 0 and 10)
'''

X = []; y = []

with open('white_wine_dataset.txt', 'r') as file:
    line = file.readline()
    cnt = 1
    while line:
        X.append([float(value) for value in line.strip().split(',')[:11]])
        y.append(int(line.strip().split(',')[11]))
        line = file.readline()
        cnt += 1
            
# X, y, = K_Nearest_Neighbors.K_Nearest_Neighbors_Regression.shuffle(X, y)

# Split the data
split = 3000
training_X = X[split:]
training_y = y[split:]
test_X = X[:split]
test_y = y[:split]

# Run the model
start = time.time()
KNN = K_Nearest_Neighbours_threading.K_Nearest_Neighbours_Regression(20, 'manhattan')
KNN.fit(training_X, training_y)
predict_y, MeanError = KNN.test(test_X, test_y, True)
#print(predict_y)
print('Mean error of: ' + str(MeanError))
print('Time taken: ' + str(time.time() - start))

# Plot a graph
fig=plt.figure()
ax=fig.add_axes([0,0,1,1])
ax.scatter(test_y, predict_y, color='r')
ax.set_xlabel('True y')
ax.set_ylabel('Predict y')
ax.set_title('White wine quality prediction')
plt.show()
