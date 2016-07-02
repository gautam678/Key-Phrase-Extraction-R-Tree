from rtree import index
#from Output import biochem2 as dataDict
idx=index.Index()
import numpy as np
import matplotlib.pyplot as plt
def indexWordOccurence():
    data=[]
    keyMap = {}
    for keyIndex, keyPoints in enumerate(dataDict.items()):
        key,points = keyPoints
        keyMap[key] = keyIndex+1
        for point in points:
            data.append((keyIndex+1,point))
    return data,keyMap


def createRTree(data):
    for i in data:
        left,bottom,right,top=(i[0],i[1],i[0],i[1])
        idx.insert(i[0],(left,bottom,right,top))
    return idx


def query_for_nearest_terms(idx,data,keyMap,queryKey,numOfNearest = 5, notincludeQuery = True):
    x = keyMap[queryKey]
    Y = dataDict[queryKey]
    histogram={}
    for y in Y:
        print queryKey
        for i in idx.nearest((x,y,x,y),numOfNearest):
            try:
                #print i,
                for key,xValue in keyMap.iteritems():
                    if xValue == i:
                        nearTerm = key
                        break
                if nearTerm == queryKey and notincludeQuery:
                    continue
                if histogram.has_key(keyMap[nearTerm]):
                    histogram[keyMap[nearTerm]]+=1
                else:
                    histogram[keyMap[nearTerm]]=1
            except Exception as e:
                print e
                continue
    nearestTermsHistogram = sorted(histogram.iteritems(), key=lambda x:x[::-1], reverse=True)
    X=[]
    Y=[]
    ann=[]
    for x,y in nearestTermsHistogram:
        X.append(x)
        ann.append(keyMap.keys()[x-1])
        Y.append(y)
    fig, ax = plt.subplots()
    ax.scatter(X, Y)
    for i, txt in enumerate(ann):
        ax.annotate(txt, (X[i],Y[i]))
    #print data
    plt.show()
    #print "NH:",nearestTermsHistogram
    print "="*27

def __init__(self, name):
    self.name = []

def main():
    print "Entring main.."
    data,keyMap = indexWordOccurence()
    idx = createRTree(data)
    print dataDict
    for keys in dataDict:
        nearestTermsHistogram = query_for_nearest_terms(idx,data,keyMap,keys,numOfNearest=5)
