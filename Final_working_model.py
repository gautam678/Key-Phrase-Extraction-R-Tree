import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use("Agg")
import glob
import re
import rtree_imp as rt

"""
FUNCTIONS LIST
"""
def word_split(text):
    """
    Split a text in words. Returns a list of tuple that contains
    (word, location) location is the starting byte position of the word.
    """
    word_list = []
    wcurrent = []
    windex = None

    for i, c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
            windex = i
        elif wcurrent:
            word = u''.join(wcurrent)
            word_list.append((windex - len(word) + 1, word))
            wcurrent = []

    if wcurrent:
        word = u''.join(wcurrent)
        word_list.append((windex - len(word) + 1, word))

    return word_list

def words_cleanup(words):
    """
    Remove words with length less then a minimum and stopwords.
    """
    cleaned_words = []
    for index, word in words:
        if word  in _STOP_WORDS and len(word)>3:
            cleaned_words.append((index, word))
        else:
            continue
    return cleaned_words

def words_normalize(words):
    """
    Do a normalization precess on words. In this case is just a tolower(),
    but you can add accents stripping, convert to singular and so on...
    """
    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
        normalized_words.append((index, wnormalized))
    return normalized_words

def word_index(text):
    """
    Just a helper method to process a text.
    It calls word split, normalize and cleanup.
    """
    words = word_split(text)
    words = words_normalize(words)
    words = words_cleanup(words)
    return words

def inverted_index(text):
    """
    Create an Inverted-Index of the specified text document.
        {word:[locations]}
    """
    inverted = {}

    for index, word in word_index(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)

    return inverted

def inverted_index_add(inverted, doc_id, doc_index):
    """
    Add Invertd-Index doc_index of the document doc_id to the
    Multi-Document Inverted-Index (inverted),
    using doc_id as document identifier.
        {word:{doc_id:[locations]}}
    """
    for word, locations in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted

def search(inverted, query):
    """
    Returns a set of documents id that contains all the words in your query.
    """
    words = [word for _, word in word_index(query) if word in inverted]
    results = [set(inverted[word].keys()) for word in words]
    return reduce(lambda x, y: x & y, results) if results else []

#######################################################

user = "windows"
#user = "windows"
if user is "windows":
    keys = glob.glob("keys\*")
    trans = glob.glob("transcript\*")
if user in ["ubuntu","linux"]:
    keys = glob.glob("keys/*")
    trans = glob.glob("transcript/*")
data={}
data1={}
points=[]

#print keys
print "********************",len(keys)
for n in range(len(keys)):
    f = open(keys[n])
    print keys[n]
    key =  f.read()
    g = open(trans[n])
    tran = g.read()
    f.close()
    g.close()

    _STOP_WORDS = key

    doc = tran


    # Build Inverted-Index for documents
    inverted = {}
    documents = {'doc':doc}
    for doc_id, text in documents.iteritems():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

    _1gdict={}
    IND = []

    for word, doc_locations in inverted.iteritems():

        _1gdict[word]=[]
        for i in doc_locations.values():
            for j in i:
                IND.append((inverted.keys().index(word),j))
                _1gdict[word].append(j)


    print "1G::"
##    print IND
    print _1gdict
    data.update(_1gdict)
    print "$$"*59

    x=[]
    y=[]
    s=[]
    for i in inverted.keys():
        s.append(str(i))
    for i in IND:
        x.append(i[0])
        y.append(i[1])
        points.append(i[1])

    xtic=[]
    for i in range(min(x),max(x)):
        xtic.append(i)
    xtic.append(max(x))
    temp=[]
    for i in range(0,len(y)):
        temp.append((x[i],y[i]))
##    print temp
    output = sorted(temp, key=lambda x: x[-1])
    #print key
    print " 2 - Grams"
    print "************************************************************************************************************"
    Two_gram_dict={}
    for j in range((len(y)-1)):
        store=output[j+1][1]-output[j][1]-len(s[output[j][0]])-1
        if(store==0):
            ### FOLLOWING CODE TO ARRANGE THE OCCURENCE OF 2G IN A DICTIONARY. WILL LATER APPEND TO IND TO FACILITATE THE PLOTTING ###
            keey = s[output[j][0]],s[output[j+1][0]]
            occ = output[j][1]
            if keey not in Two_gram_dict.keys():
                Two_gram_dict[keey]=[occ]
            else:
                Two_gram_dict[keey].append(occ)

        else:
            pass

    ### NEW LIST OF IND FOR PLOTTING THE 2G WORDS ###
    New_IND2 = []
    ### TWO GET THE PREVIOUSLY ACCESSED KEY WHILE PLOTTING ###
    L = IND[-1][0] + 1
    L_temp = 0
    ### TWO CONSTRUCT THE NEWIND BY ADDING THE 2G VALUES ###
    keeys = Two_gram_dict.keys()
    for k in keeys:
        for i in Two_gram_dict[k]:
            New_IND2.append((L_temp,i))
        L_temp+=1
    print "2G::::"
##    print New_IND2
    data.update(Two_gram_dict)
    #print Two_gram_dict
    print "%%%"*29
    x2=[]
    y2=[]
    s2=[]
    for i in Two_gram_dict.keys():
        g=str(i[0])+" "+str(i[1])
        s2.append(g)
        s.append(g)
    for i in New_IND2:
        x2.append(i[0])
        x.append(i[0])
        points.append(i[1])
##
##    print x

##    IND = [i for i in New_IND]

    ### VOILA! YOU HAVE YOUR IND BACK WITH YOU ###



    ### WORKING WITH 3G DICT NOW AND CHOOSING A BETTER DICT NAME ###
    _3gdict = {}

    print "3 - Grams"
    print "*************************************************************************************************************"
    for j in range((len(y)-2)):
        store=output[j+2][1]-output[j][1]-len(s[output[j+1][0]])-len(s[output[j][0]])-2
        #print store
        if(store==0):
            keey = s[output[j][0]],s[output[j+1][0]],s[output[j+2][0]]
            occ = output[j][1]

            if keey not in Two_gram_dict.keys():
                _3gdict[keey]=[occ]
            else:
                _3gdict[keey].append(occ)

        else:
            pass
    print "3G::"
    data.update(_3gdict)
    #print _3gdict
    print "##"*29

    ### NEW LIST OF IND FOR PLOTTING THE 3G WORDS ###

    New_IND3 = []
    L_temp = 0

    ### TWO CONSTRUCT THE NEWIND BY ADDING THE 3G VALUES ###
    keeys = _3gdict.keys()
    for k in keeys:
        for i in _3gdict[k]:
            New_IND3.append((L_temp,i))
        L_temp+=1
    #print New_IND3


    x3=[]
    y3=[]
    s3=[]
    for i in _3gdict.keys():
        g=str(i[0])+" "+str(i[1])+" "+str(i[2])
        s3.append(g)
        s.append(g)
        #print s3
    for i in New_IND3:
        x3.append(i[0])
        x.append(i[0])
        points.append(i[1])


    ### VOILA! YOU HAVE YOUR IND BACK WITH YOU ###


    ### TO APPEND 4G KEYS ###
    print "4 - Grams"
    print "*************************************************************************************************************"
    _4gdict = {}
    for j in range((len(y)-3)):
        store=output[j+3][1]-output[j][1]-len(s[output[j+2][0]])-len(s[output[j+1][0]])-len(s[output[j][0]])-3
        if(store==0):
            keey = s[output[j][0]],s[output[j+1][0]],s[output[j+2][0]],s[output[j+3][0]]
            occ = output[j][1]

            if keey not in Two_gram_dict.keys():
                _4gdict[keey]=[occ]
            else:
                _4gdict[keey].append(occ)

        else:
            pass

    #print _4gdict
    ### NEW LIST OF IND FOR PLOTTING THE 4G WORDS ###
    New_IND4 = []
    ### TWO GET THE PREVIOUSLY ACCESSED KEY WHILE PLOTTING ###
##    L = IND[-1][0] + 1
    L_temp = 0
    ### TWO CONSTRUCT THE NEWIND BY ADDING THE 4G VALUES ###
    keeys = _4gdict.keys()
    for k in keeys:
        for i in _4gdict[k]:
            New_IND4.append((L_temp,i))
        L_temp+=1


##    IND = [i for i in New_IND]
    print "4G"
    data.update(_3gdict)
    print _4gdict
    print "***"*29
    ### VOILA! YOU HAVE YOUR IND BACK WITH YOU ###
    x4=[]
    y4=[]
    s4=[]
    for i in _4gdict.keys():
        g=str(i[0])+" "+str(i[1])+" "+str(i[2])+" "+str(i[3])
        s4.append(g)
        s.append(g)
        #print s
    for i in New_IND4:
        x4.append(i[0])
        x.append(i[0])
        points.append(i[1])

    xtic=[]
    for i,y in data.items():
        data1[str(i)]=y

    name=str(keys[n])
    name=name.replace('keys\\','')
    name = re.sub('\.key$', '', name)
    print name
    print "***"*29
    rt.dataDict=data1
    rt.main()

    k = raw_input("Press enter to terminate")
