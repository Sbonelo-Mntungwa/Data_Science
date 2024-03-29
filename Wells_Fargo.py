#Sbonelo Mntungwa
#2 September 2019
#NLP Program - Pricing Text Prediction

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split as tts
from collections import Counter
from nltk.corpus import stopwords
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid


#hardcode
punctuations = '''!()-[]{};:'"\,<>.?$%^&*_~'''
filename = "skills_test.csv"


#removing punctuation marks
def rm_punctuation_marks(dictionary):
    counter = 0
    for word in dictionary:
        no_punct = ""
        for char in word:
            if char not in punctuations:
                no_punct = no_punct + char
        dictionary[counter] = no_punct
        counter +=1
    return dictionary

#removing a # from a hashtag to have an english word
def rm_hashtag(dictionary):
    counter = 0
    for word in dictionary:
        if len(word) >1 and word[0] == '#':
            dictionary[counter] = word[1:]
        counter +=1
    return dictionary

#removing symbols identifying a user
def rm_user(dictionary):
    counter = 0
    for word in dictionary:
        if len(word) > 1 and word[0] == '@':
            dictionary[counter] = word[1:]
        if len(word)> 3 and word[0:3] == '/u/':
            dictionary[counter] = word[3:]
        counter +=1
    return dictionary

#removing the common english terminologies
def rm_stop_words(dictionary):
    stop_words = set(stopwords.words('english'))
    new_dictionary = []
    for word in dictionary:
        if not word.lower() in stop_words:
            new_dictionary.append(word)
    return new_dictionary

#creating the top most common words in the input csv file
#input :csv file
#output:3000 most common words
def import_data(filename):
    print('dictionary begin....\n')
    text_dict = []
    csvfile = pd.read_csv(filename)
    unfiltered_dict = csvfile['Text']
    for text in unfiltered_dict:
        words = text.split(' ')
        #preprocessing data
        words= rm_punctuation_marks(words)
        words = rm_hashtag(words)
        words = rm_user(words)
        words = rm_stop_words(words)
        for word in words:
            text_dict.append(word)
    dictionary = Counter(text_dict)
    print('....dictionary complete\n')
    return dictionary.most_common(3000)

#creating a dataset for the dictionary
#input :dictionary of words + filepath
#output:features + labels
def make_dataset(dictionary, filename):
    print('dataset begin....\n')
    csvfile = pd.read_csv(filename)
    text_entry = csvfile['Text']
    label_set = csvfile['label']
    feature_set = []
    for text in text_entry:
        words = text.split(' ')
        words= rm_punctuation_marks(words)
        words = rm_hashtag(words)
        words = rm_user(words)
        words = rm_stop_words(words)
        data = []
        for entry in dictionary:
            data.append(words.count(entry[0]))
        feature_set.append(data) 
    print('....dataset complete\n')
    return feature_set, label_set


def run_naive_bayes(feature, label):
    print ('naive bayes begin...\n')
    x_train, x_test, y_train, y_test = tts(feature, label, test_size=0.2)
    clf = MultinomialNB()
    print(clf.fit(x_train, y_train))
    preds = clf.predict(x_test)
    run_result(y_test, preds)
    print('....naive bayes complete\n')
        
def run_support_vector_machine(feature, label):
    print ('support vector machine begin...\n')
    x_train, x_test, y_train, y_test = tts(feature, label, test_size=0.2)
    clf = svm.SVC(kernel='linear')
    clf.fit(x_train, y_train)
    preds = clf.predict(x_test)
    run_result(y_test, preds)
    print ('...support vector machine complete\n')
    
def run_random_forest(feature, label):
    print ('random forest begin...\n')
    x_train, x_test, y_train, y_test = tts(feature, label, test_size=0.2)
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(x_train, y_train)
    preds = clf.predict(x_test)
    run_result(y_test, preds)
    print ('...random forest complete\n')
    
def run_nearest_neighbour(feature, label):
    print ('nearest neighbour begin...\n')
    x_train, x_test, y_train, y_test = tts(feature, label, test_size=0.2)
    clf = NearestCentroid()
    clf.fit(x_train, y_train)
    preds = clf.predict(x_test)
    run_result(y_test, preds)
    print ('...nearest neighbour complete\n')
    
def run_neural_network(feature, label):
    print ('neural network begin...\n')
    x_train, x_test, y_train, y_test = tts(feature, label, test_size=0.3)
    clf = MLPClassifier(alpha=1e-5,hidden_layer_sizes=(5, 4),activation='logistic')
    clf.fit(x_train, y_train)
    preds = clf.predict(x_test)
    run_result(y_test, preds)
    print ('...neural network complete\n')
    
def run_result(y_test, preds):
    print ('accuracy:', accuracy_score(y_test, preds))
    print ('tp:',sum((y_test == 1) & (preds == 1)))
    print ('tn:', sum((y_test == 0) & (preds == 0)))
    print ('fn:', sum((y_test == 1) & (preds == 0)))
    print ('fp:', sum((y_test == 0) & (preds == 1)))


dictionary = import_data(filename)
feature, label = make_dataset(dictionary, filename)


while True:
    print ('.....choose your classification algorithm.....')
    print('(a) Naive Bayes...')
    print('(b) Support Vector Machine...')
    print('(c) Random Forest...')
    print('(d) Nearest Neighbour...')
    print('(e) Neural Network...')
    print('(q) quit program...')
    algorithm = input("")
    if algorithm == 'q':
        print("...end of program")
        break
    if algorithm == 'a':
        print("...Naive Bayes selected\n")
        run_naive_bayes(feature, label)
    elif algorithm == 'b':
        print("...Support Vector Machine selected\n")
        run_support_vector_machine(feature, label)
    elif algorithm == 'c':
        print("...Random Forest selected\n")
        run_random_forest(feature, label)
    elif algorithm == 'd':
        print("...Nearest Nighbour selected\n")
        run_nearest_neighbour(feature, label)
    elif algorithm == 'e':
        print("...Neural Network selected\n")
        run_neural_network(feature, label)
