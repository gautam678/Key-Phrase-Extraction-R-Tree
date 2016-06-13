from rtree import index
from data import Google as dataDict
idx=index.Index()
import matplotlib
#following line added because shiva is working on a server machine with no GUI
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
'''
dataDict = {'website': [384, 568, 646, 1209, 15849, 15937, 16293, 16502, 18826, 22352, 22567]
,'google': [1024, 2961, 3093, 5067, 6009, 6083, 6375, 14246, 22940]
,'providers': [493, 8844, 9370]
,'communication': [8121]
,'site': [1284, 6175, 9230, 11684, 13849, 14441, 15086, 18980, 23072]
,'tumblr': [4850, 5276, 5435, 25740]
,'street': [5233, 13728, 22603]
,'technology': [4998, 13112, 16039]
,'information': [6779, 9156, 9269, 9691, 10752, 13439, 15256, 15879, 16329, 19642, 22450]
,'system': [8796, 9838, 11769, 11908]
,'messenger': [6918, 8158, 10594, 17175]
,'internet': [5091, 11740, 13925, 15332, 21693, 26433]
,'company': [70, 1077, 3167, 3427, 3685, 3767, 4321, 4424, 4866, 5301, 5398, 5462, 6455, 6512, 8677, 17329, 20012, 20128, 21084, 22122, 22797, 22962, 23200, 24041, 24683]
,'yahoo': [0, 22, 219, 236, 248, 260, 275, 289, 526, 751, 787, 898, 1469, 1490, 1554, 1724, 1983, 2133, 2373, 2411, 2466, 2553, 2588, 2749, 2943, 3109, 3318, 3345, 3503, 3672, 3979, 4279, 4350, 4533, 4628, 4731, 4786, 5046, 5558, 5756, 5959, 6064, 6156, 6225, 6301, 6408, 6569, 6666, 6698, 6836, 6856, 6868, 6880, 6895, 6981, 7125, 7244, 7346, 7461, 7650, 7783, 8097, 8172, 8253, 8358, 8375, 8410, 8422, 8435, 8508, 8596, 8638, 8772, 8807, 8874, 8888, 8903, 8916, 8930, 8945, 8957, 8975, 9024, 9069, 9122, 9206, 9326, 9525, 9801, 10431, 10525, 10608, 10647, 10664, 10677, 10699, 10819, 10881, 11003, 11044, 11062, 11081, 11107, 11132, 11240, 11467, 11546, 11717, 12012, 12153, 12178, 12222, 12426, 12678, 12726, 12790, 12836, 12908, 12982, 13097, 13361, 13455, 13649, 13757, 13858, 13973, 14001, 14107, 14217, 14340, 14398, 14648, 14828, 15118, 15397, 15461, 15512, 15595, 15634, 15745, 15918, 15977, 16031, 16175, 16250, 16413, 16630, 16753, 16820, 16908, 16998, 17117, 17130, 17148, 17160, 17229, 17306, 17584, 17710, 17822, 17900, 17940, 17957, 18049, 18063, 18145, 18327, 18358, 18491, 18618, 18954, 19063, 19342, 19396, 19479, 19525, 19602, 19901, 19989, 20103, 20289, 20445, 20570, 20625, 20672, 20756, 21037, 21133, 21207, 21435, 21488, 21590, 21757, 21843, 21958, 22249, 22476, 22642, 22994, 23028, 23150, 23185, 23250, 23305, 23344, 23423, 23487, 23544, 23587, 23752, 23831, 23920, 23938, 24106, 24194, 24309, 24511, 24535, 24585, 24779, 25029, 25079, 25232, 26062, 26211, 26251, 26414]
,'phone': [6190, 9758, 15420, 17193]
,'search': [159, 179, 2517, 2972, 3027, 6323, 7258, 9831, 10308, 10344, 11277, 11330, 11845, 11882, 12048, 12659, 13011, 13068, 14377, 14490, 14698, 16129, 18076, 20551, 20780, 20848, 21857]
,'mobile': [9606, 9663, 9868, 10452, 10570, 14051]}
'''
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


def query_for_nearest_terms(idx,keyMap,queryKey,numOfNearest = 5, notincludeQuery = True):
    x = keyMap[queryKey]
    print x
    Y = dataDict[queryKey]
    print Y
    histogram = {}
    for y in Y:
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
    return sorted(histogram.iteritems(), key=lambda x:x[::-1], reverse=True)


def main():
    data,keyMap = indexWordOccurence()
    idx = createRTree(data)
    for keys in dataDict:
        print keys
        X=[]
        Y=[]
        annotations=[]
        nearestTermsHistogram = query_for_nearest_terms(idx,keyMap,keys,numOfNearest=10)
        print nearestTermsHistogram
        for x,y in nearestTermsHistogram:
            X.append(x)
            annotations.append(keyMap.keys()[x-1])
            Y.append(y)
        print annotations
        fig, ax = plt.subplots()
        ax.scatter(X, Y)
        for i, txt in enumerate(annotations):
            ax.annotate(txt, (X[i],Y[i]))
        print keyMap
        plt.show()
        print nearestTermsHistogram
        plt.savefig("test.png")
        print "="*27

main()
#print dataDict.keys()
