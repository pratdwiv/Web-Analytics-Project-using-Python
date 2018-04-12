#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import pandas as pd
import nltk
import numpy as np

#Performing sentiment analysis on positive and negative words from the reviews to evaluate sentiment of the review.
def sentiment_analysis(text, positive_words, negative_words):
   
    sentiment = None
    positive_word = 0
    negative_word = 0
    tokens = nltk.word_tokenize(text) 
    negative = ['not', "n't", 'no', 'cannot', 'neither', 'nor', 'too']
   
    for index, token in enumerate(tokens):
        if token in positive_words:
            if tokens[index-1] not in negative:
                positive_word += 1
            if tokens[index-1] in negative:
                negative_word += 1
       
        if token in negative_words:
            if tokens[index-1] in negative:
                positive_word += 1
               
            if tokens[index-1] not in negative:
                negative_word += 1
   
    if positive_word > negative_word:
        sentiment = '2'
    elif positive_word <= negative_word:
        sentiment = '1'
   
    return sentiment

#Generating a temporary file, with updated sentiment_value column, based on customer ratings.
def sentiment_evaluate(input_file, positive_words, negative_words):
 
    result=[]
    sentiment_value=None
    review_list=pd.read_csv(input_file, header=0).values.tolist()
    review_data=pd.DataFrame(review_list, columns=['rating','review'])
    ratings=review_data[['rating']].values
    df = pd.DataFrame(review_data)

    #If the customer rating is greater than equal to 3, it is assigned as positive(2) sentiment, 
    #otherwise negative(1) sentiment.
    for rating in ratings:
        if int(rating)>= 3:
            sentiment_value=2
        elif int(rating)< 3:
            sentiment_value=1
            
        result.append(sentiment_value)
    df['sentiment_value']=result
    df.to_csv('temp_sentiment_output_file.csv',mode='w+')   
    #For individual review sentiment, please check the newly generated temp_sentiment_output_file.csv
    return None

#Evaluating performance of our sentiment analysis, by comparing the sentiments based on the customer
#ratings and the sentiments calculated from the customer reviews.
def performance_evaluate(input_file, positive_words, negative_words):

    with open(input_file, 'r') as input_file:
        sentiment_file = csv.reader(input_file)
        total_rows = 0
        sentiment_predictions = 0
       
        for sentiment in sentiment_file:
            total_rows += 1
           
            if sentiment[3] == sentiment_analysis(sentiment[2], positive_words, negative_words):
                sentiment_predictions += 1
           
           
    return sentiment_predictions/total_rows

if __name__ == "__main__":
    
    sentiments= None
    with open("positive-words.txt",'r') as f:
        positive_words=[line.strip() for line in f]
      
    with open("negative-words.txt",'r') as f:
        negative_words=[line.strip() for line in f]

  
    sentiments=sentiment_evaluate("Clean_New_Apple-ipad-latest-model-with-wifi-cellular-32gb.csv", positive_words, negative_words)
    
    
    accuracy=performance_evaluate("temp_sentiment_output_file.csv", positive_words, negative_words)
    print("\nEvaluated performance of our sentiment analysis, by comparing the sentiments based on the customer\
 ratings and the sentiments calculated from the customer reviews.")
    print("\nHence, the accuracy of our Sentiment Analysis is:", np.around(accuracy,5))