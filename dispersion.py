from data import Google as testDict
import numpy as np

def calc_dispersion(key, occurences):

    if len(occurences)<2:
        return 0,0
    return np.mean(occurences),np.std(occurences)

def main():

    keyPropertiesList = []
    means, stdDevs = [], []
    for key in testDict:
        mean, stdDev = calc_dispersion(key,testDict[key])
        if mean+stdDev is not 0:
            keyPropertiesList.append({"key":key,"mean":mean,"stdDev":stdDev,"numberOfOccurences":len(testDict[key])})
    print keyPropertiesList

main()
