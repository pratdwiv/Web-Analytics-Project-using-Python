# -*- coding: utf-8 -*-
import csv
import nltk, string
stop_words = ['a', 'an', 'the', 'and', 'or']

def get_review_tokens(review):
    pattern = r'\w+[\-]*\w+'                          
    # get unigrams
    tokens=[token.strip() \
            for token in nltk.regexp_tokenize(review.lower(), pattern) \
            if token.strip() not in string.punctuation and \
            token.strip() not in stop_words and \
            token.strip() if not token.isdigit() and \
            token.strip() if not token.startswith('\'')
            ]    
    return tokens

def clean_review(tokens):
    review = " ".join(get_review_tokens(tokens))
    return review   

def save(reviews):
    file_name = "ipad_pro_clean.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f, dialect = 'excel')
        writer.writerows(reviews)
    f.close()

if __name__ == "__main__":
    f = open("ipadpro_raw.csv", "r")
    reader = csv.reader(f)
    row = list(reader)
    reviews = []
    for utf8_row in row:
        if utf8_row:
            unicode_row = [utf8_row[1].encode().decode('utf8') for row in utf8_row]
            review = [utf8_row[0], clean_review(unicode_row[1])]
            reviews.append(review)
    f.close()
    save(reviews)
