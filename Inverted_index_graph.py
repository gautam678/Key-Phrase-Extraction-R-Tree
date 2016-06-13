import matplotlib.pyplot as plt


_STOP_WORDS = open("Facebook.txt").read()

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


f = open("Facebook.txt")
doc = f.read()
f.close()

# Build Inverted-Index for documents
inverted = {}
documents = {'doc':doc}
for doc_id, text in documents.iteritems():
    doc_index = inverted_index(text)
    inverted_index_add(inverted, doc_id, doc_index)


IND = []
f = open("index.txt","w")
# Print Inverted-Index
for word, doc_locations in inverted.iteritems():
    print word, doc_locations
    f.write(word+": ")
    for i in doc_locations.values():
        for j in i:
            IND.append((inverted.keys().index(word),j))
            f.write(("("+str(inverted.keys().index(word)) + ","+ str(j)+")"))
                       
        
##        print inverted.keys().index(word),i 
    f.write("\n")
    
##print IND

x=[]
y=[]
for i in IND:
    x.append(i[0])
    y.append(i[1])

print x
print y
plt.plot(x,y,'ro')
plt.axis([0,30, 0,35600])
plt.xticks(x)
plt.show()
    

input("Press enter to terminate")
