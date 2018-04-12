#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import nltk
import numpy as np

#Performing sentiment analysis on positive and negative words from the reviews to evaluate sentiment of the review.
def sentiment_analysis(text, positive_words, negative_words):
    
    sentiment=None
    negations=['not', 'too', 'n\'t', 'no', 'cannot', 'neither','nor']
    positive_tokens = []
    negative_tokens=[]
    tokens = nltk.word_tokenize(text)  

    for idx, token in enumerate(tokens):
        if token in positive_words or token in negative_words:
            if idx>0 and token in positive_words:
                if tokens[idx-1] not in negations:
                    positive_tokens.append(token)
                else:
                    negative_tokens.append(token)
            elif idx>0 and token in negative_words:
                if tokens[idx-1] in negations:
                    positive_tokens.append(token)
                else:
                    negative_tokens.append(token)
    #sentiment is 2 for a positive review and sentiment is 1 for a negative review
    if len(positive_tokens)>len(negative_tokens):
        sentiment = 2
        
    elif len(positive_tokens)<=len(negative_tokens):
        sentiment = 1
    return sentiment

#Evaluating sentiment calculated, to illustrate percentage of positive and negative reviews for a product.
def sentiment_evaluate(input_file, positive_words, negative_words):
    
    sentiments=None
    positive_review =0
    negative_review =0
    review_list=pd.read_csv(input_file, header=0).values.tolist()
    review_data=pd.DataFrame(review_list, columns=['rating','review'])
    reviews= review_data[['rating','review']].values
    for review in reviews:
        sentiment=sentiment_analysis(review[1], positive_words, negative_words)
        if sentiment == 2:
            positive_review +=1
        elif sentiment == 1:
            negative_review +=1
    print ("\n Number of Positive Reviews:", positive_review)
    print ("\n Number of Negative Reviews:", negative_review) 
    percentage_of_positive_reviews = np.around(np.divide(positive_review, (positive_review+negative_review))*100, 2)
    percentage_of_negative_reviews = np.around(np.divide(negative_review, (positive_review+negative_review))*100, 2)
    print ("\n Percentage of Positive Reviews:", percentage_of_positive_reviews, "%")         
    print ("\n Percentage of Negative Reviews:", percentage_of_negative_reviews, "%")     
    if percentage_of_positive_reviews > percentage_of_negative_reviews:
        sentiments = "Positive"
    elif percentage_of_positive_reviews < percentage_of_negative_reviews:
        sentiments = "Positive"
    elif percentage_of_positive_reviews == percentage_of_negative_reviews:
        sentiments = "Mixed"
    return sentiments

if __name__ == "__main__":  
      
    
    with open("positive-words.txt",'r') as f:
        positive_words=[line.strip() for line in f]
        
    with open("negative-words.txt",'r') as f:
        negative_words=[line.strip() for line in f]

    #Prints the overall positive or negative percentage of the sentiment for a given product.
    sentiments=sentiment_evaluate("Clean_New_Apple-ipad-latest-model-with-wifi-cellular-32gb.csv", positive_words, negative_words)
    print ("\n Our sentiment evaluation predicts reviews as: ", sentiments)