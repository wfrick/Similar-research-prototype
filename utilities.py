import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer 
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import feedparser

def remove_stop_words(tokens):
    #Takes a list of words, remove common ones
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in tokens if w.lower() not in stopwords]
    return content

def pair_similarity(doc1,doc2):
    #Takes two strings, returns cosine similarity
    vect = TfidfVectorizer()
    docs = [doc1,doc2]
    tfidf = vect.fit_transform(docs)
    similarity = (tfidf * tfidf.T).A
    return similarity[1][0]

def similarity(doc, docs):
    #Takes a string and a list of strings.
    #Calculates tdidf scores
    #Returns the highest similarity score
    vect = TfidfVectorizer()
    all_docs = docs + [doc]
    tfidf = vect.fit_transform(all_docs)
    similarity_matrix = (tfidf * tfidf.T).A
    similarity_scores = similarity_matrix[len(similarity_matrix)-1]
    max_similarity = max(similarity_scores[0:len(similarity_scores)-1])
    index = list(similarity_scores).index(max(similarity_scores[0:len(similarity_scores)-1]))
    return max_similarity, index

def stem_and_stop(doc):
    #Tokenize, stem words, remove stop words
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(doc)
    tokens = remove_stop_words(tokens)
    ps = PorterStemmer()
    tokens = [ps.stem(t) for t in tokens]

    #Recombine into a string
    content = ' '.join(tokens).lower()
    return content

def parse_similarity(feed,topics,beats):
    #Takes an RSS feed, and a list of strings
    #Returns headlines based on maximum similarity to one of the strings
    feed = feedparser.parse(feed)
    for a in feed.entries:
        title = a.title.split(' --')[0] #Remove authors from NBER feed titles
        title = stem_and_stop(title)
        results = similarity(title,beats)
        top_score = results[0]
        beat_index = results[1]
        study_topic = topics[beat_index]
        if top_score > .2:
            print top_score
            print beat_index
            print study_topic
            print a.title

def heds_to_topics(df):
    #Reads dataframe of heds, topics

    #Read data, lowercase, combine headline and topic 
    #Remove "- HBR" and "- Harvard Business Review" from headlines
    df['Page Title'] = df['Page Title'].str.lower()
    df['Page Title'] = df['Page Title'].str.split(' - h').str[0]
    df['Topic'] = df['Topic'].str.lower()

    #Combine headlines into single string for each topic
    beats = []
    topics = []
    for t in df['Topic'].unique():
        articles = df.loc[df['Topic'] == t]
        if len(articles.index) > 5:
            beat = articles['Page Title'].str.cat(sep=' ')
            beat = stem_and_stop(beat)
            beats.append(beat)
            topics.append(t)

    print len(beats)
    print len(topics)
    
    return topics, beats
