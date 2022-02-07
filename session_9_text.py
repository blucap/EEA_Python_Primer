#!/usr/bin/env python
# coding: utf-8

# # Session 9: Analyze data using statistical libraries, text analysis, and web scraping

# ---
# 
# This three-part session starts with data analysis using two stats libraries:
# 
# - [statsmodels](https://www.statsmodels.org/dev/index.html) and 
# - [linearmodels](https://bashtage.github.io/linearmodels/panel/introduction.html)
# 
# The linearmodels library works well with panel data and data frames with multi indexes.
# 
# The libraries allow you to easily formulate you regression models, and conveniently select the results from the regression output. You can select coefficients and *t*-stats, or *p*-values, add them to a data frame (i.e. a table), and exported that data frame to LaTeX, markdown, or cvs / Excel format.
# 
# **The second part** is a brief intro into text analysis using Natural Language Toolkit: [NLTK](https://www.nltk.org/).
# 
# **The last part** is about web-scraping, which features a script that I wrote to collect information from `ssrn.com` for reference management. It uses the [beautifulsoup](https://beautiful-soup-4.readthedocs.io/en/latest/#) library.
# 
# Learning  objectives:
# 
# - How to create tables with descriptives of your data.
# - Perform regression analyses with [statsmodels](https://www.statsmodels.org/dev/index.html) and [linearmodels](https://bashtage.github.io/linearmodels/panel/introduction.html) and extract parameters for presentations in tabular form.
# - Analyze text from financial reports using [nltk](https://www.nltk.org/) and pandas.
# - Scrape a website using [beautifulsoup](https://beautiful-soup-4.readthedocs.io/en/latest/#).
# 
# 
# 
# 
# 
# 

# ---
# ### Part 2: Text analysis ###
# 
# For this part we need to install two libraries: 
# 
# - For extracting text from pdf files we need [**PyMuPDF**](https://pymupdf.readthedocs.io/en/latest/intro.html),  lightweight PDF, XPS, and E-book viewer, renderer, and toolkit. **See this** [**link**](https://pymupdf.readthedocs.io/en/latest/installation.html) for installation.
# 
# - For text analysis we need the Natural Language Toolkit: [NLTK](https://www.nltk.org/). Install this using `pip install nltk`.
# 
# - You may want to learn a bit about regular expressions, or regex. **Regex** allows you to select text using specific patterns. Rexeg is a powerful tool, but it has a steep learning curve. Nevertheless, most of your regex queries can be solved by either using Google or by way of [this excellent website](https://regex101.com/) for testing regex.
# 
# 
# We will analyze a page from an annual report of [BNP-Paribas](https://group.bnpparibas/uploads/file/bnp2019_urd_en_20_03_13.pdf), following the approach taken in [here](https://towardsdatascience.com/getting-started-with-text-analysis-in-python-ca13590eb4f7https://towardsdatascience.com/getting-started-with-text-analysis-in-python-ca13590eb4f7).
# 
# **Note** NLTK may ask you to install additional modules if you run this script for the first time. Please follow the instructions shown in the warnings.

# In[ ]:


# the familiar preamble
import pandas as pd
import numpy as np

# For this session
import re
import fitz  # to connect to the PyMuPDF library
import nltk
import requests


# **Get that very big annual report**

# In[ ]:


response = requests.get('https://group.bnpparibas/uploads/file/bnp2019_urd_en_20_03_13.pdf')
# Write content in pdf file
pdf = open("bnp2019_urd_en_20_03_13_web.pdf", 'wb')
pdf.write(response.content)
pdf.close()


# In[ ]:


doc = fitz.open('bnp2019_urd_en_20_03_13_web.pdf')


# **Find a page with some text**, e.g. the page on with `ethics of the highest standard`.

# In[ ]:


for page in doc:
    s = page.get_text("text")
    found = s.find("ethics of the highest standard")
    if found != -1:
        print(page.number)
        #print(page.get_text('text'))


# **Alas, let's try to ignore the case**

# In[ ]:


#Using regex instead, finding the page with the most text
def find_long_page(search_term):
    words_page_dict = {}
    for page in doc:
        #print(page)
        s = page.get_text("text")
        matches = re.findall(search_term,s, re.IGNORECASE)
        if matches:
            p = page.get_text('words')
            df = pd.DataFrame(p)
            # print(page.number, len(df))
            words_page_dict[page.number] = len(df)
    return(max(words_page_dict, key=words_page_dict.get))

find_long_page(r'ethics of the highest standard')


# **Show the text after removing line breaks `\n`**

# In[ ]:


text = doc.load_page(find_long_page(r'ethics of the highest standard')).get_text()
text =  re.sub("\n", " ",text)  # get rid of line breaks
text[0:1000]


# ---
# Let's **tokenize** the text and add all separate items to a data frame

# In[ ]:


from nltk.tokenize import sent_tokenize, word_tokenize
tokenized_text = sent_tokenize(text)

df = pd.DataFrame(tokenized_text, columns=['full_text'])
df['len_text'] = df['full_text'].apply(len)
df.head(10)


# **Okay, now we are going to prepare the text for sentiment analysis, which requires cleaning, removing stopwords, stemming or lemmatizing words.**
# 
# However, it makes sense to apply this approach to the separate items of the data frame. 
# 
# So, I will first show these steps applied to one cell of the data frame. Then I show a function for that does all these steps in one go.

# In[ ]:


# Find the longest string in df:
text_max = df['len_text'].idxmax()
text_max = df.iloc[text_max]['full_text']
print(text_max)


# In[ ]:


# Cleaning the text
def clean_text(text):
    text =  re.sub("[^a-zA-Z]+", " ", text ) # get rid everything except words
    return text

letters_only_text = clean_text(text_max)
print(letters_only_text)


# In[ ]:


# Split text in a list of words
words = letters_only_text.lower().split()
print(words)


# In[ ]:


# Get rid of stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words

def words_cleanup(words, stop_words):
    cleaned_words = []
    # remove stopwords
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)
    return cleaned_words

cleaned_words = words_cleanup(words, stop_words)
print(cleaned_words)


# In[ ]:


from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
lemmatizer = PorterStemmer() #plug in here any other stemmer or lemmatiser you want to try out


# In[ ]:


# stemm or lemmatise words
def words_lemmatizer(words):
    stemmed_words = []
    for word in words:
        word = lemmatizer.stem(word)   #dont forget to change stem to lemmatize if you are using a lemmatizer
        stemmed_words.append(word)   
    return stemmed_words
    
stemmed_words = words_lemmatizer(cleaned_words)
print(stemmed_words)


# In[ ]:


# converting list back to string
pre_senti_text = " ".join(stemmed_words)
pre_senti_text


# ---
# 
# #### Analyze sentiment ####

# In[ ]:


from nltk.sentiment import SentimentIntensityAnalyzer


# In[ ]:


sia = SentimentIntensityAnalyzer()
polarity_score =  sia.polarity_scores(pre_senti_text)
polarity_score


# Following this [page](https://realpython.com/python-nltk-sentiment-analysis/), I use only the positivity of the compound score to assess sentiment. 

# In[ ]:


polarity_score['compound']


# ---
# 
# #### Bringing it all together ####
# 
# The function below determines the polarity score of a text:

# In[ ]:


from nltk.sentiment import SentimentIntensityAnalyzer

def preprocess(raw_text):
    letters_only_text =  re.sub("[^a-zA-Z]+", " ", raw_text ) # get rid everything except words, numbers, spaces
    #text =  re.sub("\s\.\s+", ". ",text ) # get rid of space dot space
    #text =  re.sub("\s+", " ",text )  # get rid of multiple spaces
    # convert to lower case and split into words -> convert string into list ( 'hello world' -> ['hello', 'world'])
    words = letters_only_text.lower().split()
    
    cleaned_words = []
    # remove stopwords
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)

    lemmatizer = PorterStemmer() # plug in here any other stemmer or lemmatiser you want to try out

    # stemm or lemmatise words
    stemmed_words = []
    for word in cleaned_words:
        word = lemmatizer.stem(word)   #don't forget to change stem to lemmatize if you are using a lemmatizer
        stemmed_words.append(word)

    # converting list back to string
    pre_senti_text = " ".join(stemmed_words)
    sia = SentimentIntensityAnalyzer()
    polarity_score =  sia.polarity_scores(pre_senti_text)
    return polarity_score['compound']

preprocess(text_max)


# In[ ]:


# Find the original text of the first entry  
df.loc[0]['full_text']


# In[ ]:


# Apply the function to that text 
preprocess(df.loc[0]['full_text'])


# In[ ]:


# Apply the function to all entries in the data frame
df['compound_senti_score'] = df['full_text'].apply(preprocess)
df.sort_values('compound_senti_score')

