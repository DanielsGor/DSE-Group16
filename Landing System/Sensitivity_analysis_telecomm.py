import numpy as np

scores = np.array([[8,7,5],[6, 3, 2],[10, 6, 10],[8, 8, 5],[6, 9, 9]])
scores = scores.T

weights =  np.array([10,25,15,20,30]).T

check = scores @ weights / 4
def results (array):
    sorted_array = sorted(list(array),reverse=True) #order list
    position = [] #position of each airfoil
    for value in array:
        position.append(sorted_array.index(value)+1)
    # [sorted(list(array),reverse = True).index(value)+1 for value in array]
    return position

def variation(parameter_index, variation):
    weight = weights[parameter_index]
    newWeight = weight * (1 + variation)

    newWeights = []
    for idx, i in enumerate(weights):
        if idx == parameter_index:
            newWeights.append(newWeight)
        else:
            newWeights.append(i*(100-newWeight)/(100-weight))
    return newWeights

final_result = np.zeros((1,np.shape(scores)[0]))

for var in [0.10,0.20,0.3,-0.1,-0.2,-0.3]:    
    for param_index in range(len(weights)):
        newWeights1 = variation(param_index, var)
        final_result += results(scores @ newWeights1/4)
        
    print(final_result)
    final_result = np.zeros((1,np.shape(scores)[0])) 

#This prints 