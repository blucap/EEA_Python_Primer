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
# **The last part** is about web-scraping, which features a script that I wrote to collect information from `ssrn.com` for reference management. It uses the [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#) library.
# 
# Learning  objectives:
# 
# - How to create tables with descriptives of your data.
# - Perform regression analyses with [statsmodels](https://www.statsmodels.org/dev/index.html) and [linearmodels](https://bashtage.github.io/linearmodels/panel/introduction.html) and extract parameters for presentations in tabular form.
# - Analyze text from financial reports using [nltk](https://www.nltk.org/) and pandas.
# - Scrape a website using [beautifulsoup](https://beautiful-soup-4.readthedocs.io/en/latest/#).
# 

# ---
# ### Part 3: Web scraping ###
# 
# For this part we need to install the [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#) library. 
# 
# BeautifulSoup is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. It commonly saves programmers hours or days of work.
# 
# - Use Anaconda to install [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#). See [**this link**.](https://anaconda.org/anaconda/beautifulsoup4)
# - You may want to learn a bit about regular expressions, or regex. **Regex** allows you to select text using specific patterns. Rexeg is a powerful tool, but it has a steep learning curve. Nevertheless, most of your regex queries can be solved by either using Google or by way of [this excellent website](https://regex101.com/) for testing regex.
# 
# 
# **We will extract data from SSRN.com for reference management**, specifically the following items: authors, title, pages, journal, title, publisher, year. In this case I prepare for BibTex, but it should be easy to prepare for a different format.
# 
# The reason I wrote this script is that most publisher site include far too much fields. For most paper you only need a handful of fields.

# ---
# 
# **What output does the script generate?**
# 
# For example, for this [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3197365), the script generates: 
# 
#     Regulation and Risk Shuffling in Bank Securities Portfolios
#     
#     Author's names:
#     
#     Andreas Fuster (1093471)
#     James I. Vickery (497725)
#     
#     Bibtex:
#     
#     @article{FusterVickery2018,
#     author = {Fuster, Andreas and Vickery, James I.},
#     title = {{Regulation and Risk Shuffling in Bank Securities Portfolios}},
#     pages = {1--44},
#     journal = {SSRN Electronic Journal},
#     publisher = {Elsevier BV},
#     note = "\url{https://ssrn.com/abstract=3197365}",
#     month = jun,
#     year = 2018
#     }
#     
#     
#     https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3197365

# **... after which you can import the `@article{ ... }` part into your reference manager.**
# 
# ---
# 
# **Notes** 
# 
# - you may need to install additional libraries; see the first block of lines in the preamble below. 
# - you should be able to run the script from the `cmd` prompt. In that case you can just enter: `ipython ssrn.py 3197365` to get the paper from Andreas Fuster and James Vickery. 
# - The stand-alone version of the python script is on this GitHub [page](https://github.com/blucap/SSRN_to_BibTex).
# 

# In[ ]:


# New preamble

import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen as uReq
import urllib.error as uErr
import re
from collections import OrderedDict
from dateutil.parser import parse
import calendar
import tenacity

# The code below tries the SSRN site until is loads the page you need.

@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=64), stop=tenacity.stop_after_attempt(5))
def get_that_page(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        uClient = uReq(req)
        print('Success')
    except Exception:
        print('Trying again.')
    return uClient

# The code below is a helper function to get the correct month data
def get_month(m):
    dic = dict(enumerate(calendar.month_abbr))
    m = dic[m]
    return m.lower()


# **Main code to get that reference**

# In[ ]:


def get_ssrn_entry(url):
    if isinstance(url, int): # if url is a number such as 3197365, then convert that to a string and add it to the ssrn url
        url = str(url)
        url = 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=' + url
        ssrn_id_int = True

    # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # uClient = uReq(req)
    uClient = get_that_page(url)

    # Let BeautifulSoup do its work on the downloaded page
    
    soup = BeautifulSoup(uClient, 'lxml')
    
    # Create a dictionary for the fields that we want
    
    authorsstring = ""
    authorscount = 0
    articledict = OrderedDict({"bib_entry": "",
                               'authors': "",
                                "title": "",
                                "pages": "",
                                'journal': "",
                                'title': "",
                                'publisher': "",
                                "note": "",
                                'year': ""})

    
    # Pre-populate the dictionary
    
    second_author = ""
    first_author = ""

    articledict['journal'] = "{SSRN Electronic Journal}"
    articledict['publisher'] = "{Elsevier BV}"
    
    
    # Pre-populate, get the SSRN id from the url
    
    articledict['ssrn_no'] = re.search('abstract(_id)?=(\d+)', url, re.IGNORECASE).group(2)
    articledict['note'] = '"\\url{https://ssrn.com/abstract=' + articledict['ssrn_no'] + '}"'

    
    # Here is where all the action takes place!
    # Best to open the page source of the page and search for the 'meta'-tags. These have most of the information we need
    
    for tag in soup.find_all('meta'):
        if tag.get("name", None) == 'citation_title':
            # print(tag.get("content", None))
            articledict['title'] = "{{" + tag.get("content", None) + "}}"
            raw_title = tag.get("content", None)

        if tag.get("name", None) == 'citation_online_date':
            # print(tag.get("content", None))
            cite_date_str = tag.get("content", None)
            try:
                cite_date = parse(cite_date_str)
            except:
                cite_date = parse("01/01/2099")

        if tag.get("name", None) == 'citation_publication_date':
            # print(tag.get("content", None))
            try_date_str = tag.get("content", None)
            try:
                try_date = parse(try_date_str)
            except:
                try_date = cite_date


            articledict['date_str'] = try_date_str  # tag.get("content", None)
            articledict['date'] = try_date  # parse(articledict['date_str'])

            articledict['month'] = get_month(articledict['date'].month)
            articledict['year'] = str(articledict['date'].year)

        if tag.get("name", None) == 'citation_author':
            author = tag.get("content", None)
            # print(author)
            if len(author) > 0:
                authorscount += 1
                if authorscount == 1:
                    first_author = author.split(',')[0]
                if authorscount == 2:
                    second_author = author.split(',')[0]
                authorsstring += author + ' and '
    
    # Create an unique ID for the article: FusterVickery2018

    if authorscount == 1:
        bib_entry = first_author + articledict['year']
    elif authorscount == 2:
        bib_entry = first_author + second_author + articledict['year']
    else:
        bib_entry = first_author + 'EtAl' + articledict['year']
        
    articledict['bib_entry'] = "@article{" + bib_entry
    authorsstring = re.sub(r' and $', r"", authorsstring)  # get rid of unwanted `and`
    articledict['authors'] = "{" + authorsstring + "}"

    pp = "0"
    # print('\n', pp)
    pages = re.search('Number of pages:\s+(\d+)', soup.get_text(strip=True), re.IGNORECASE)
    if pages != None and pp == "0":
        pp = pages.group(1)
        articledict['pages'] = "pages = {1--" + str(pp) + "}"
        articledict['pagescount'] = int(pp)

    pages = re.search('pp.\s+(\d+-\d+)', soup.get_text(strip=True), re.IGNORECASE)
    if pages != None and pp == "0":
        pp = pages.group(1)
        articledict['pagescount'] = int(pp.split('-')[1]) - int(pp.split('-')[0])
        articledict['pages'] = "pages = {" + str(pp) + "}"

    pages = re.search('(\d+) Pages', soup.get_text(strip=False), re.IGNORECASE)
    if pages != None and pp == "0":
        pp = pages.group(1)
        articledict['pages'] = "pages = {1--" + str(pp) + "}"
        articledict['pagescount'] = int(pp)
    
    # Find (other) authours on page
    dic = {}
    print('\n')
    print(f'{raw_title}')
    print('\n')
    authors_prefix = 'Author\'s names:\n' if authorscount > 1  else 'Author\'s name:'
    print(authors_prefix)
    for link in soup.find_all('a', href=True):
        dlink = link.get('title')
        #print(dlink)
        if dlink == "View other papers by this author":
            #print(link.get('href'))
            ssrn_id = re.search('per_id=(\d+)', link.get('href'), re.IGNORECASE)
            if (ssrn_id) and (not link.get_text().startswith("See all articles")):
                ssrn_id = int(ssrn_id.group(1))
                if ssrn_id not in dic:
                    dic[ssrn_id] = link.get_text()
                    print(f'{dic[ssrn_id]} ({ssrn_id})')

    print('\nBibtex:\n')
    print(f'{articledict["bib_entry"]},')
    print(f'author = {articledict["authors"]},')
    print(f'title = {articledict["title"]},')
    if pp != "0":
        print(f'{articledict["pages"]},')
    print(f'journal = {articledict["journal"]},')
    print(f'publisher = {articledict["publisher"]},')
    print(f'note = {articledict["note"]},')
    print(f'month = {articledict["month"]},')
    print(f'year = {articledict["year"]}')
    print('}')
    print('\n')
    print(url)
    print('\n')

    return articledict, soup.prettify(), dic, bib_entry


# ---
# #### Running the script ####

# In[ ]:


test, soup, dic, bib_entry = get_ssrn_entry(3197365)


# ----
# #### For standalone execution ####
# The cell below makes the scrip accessible from the command prompt.

# In[ ]:


def main(argv):
    if len(argv) > 1:
        if isinstance(argv, str):
            if argv.startswith('https://'):
                get_ssrn_entry(argv)
            elif argv.startswith('--help'):
                print("\nUsage:\nssrn 3846655\nssrn https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3846655\n")
            else:
                print(f":{argv}.")
                try:
                    argv = int(argv.strip())
                    print(f"+{str(argv)}.")
                    get_ssrn_entry(argv)
                except:
                    print("Check your inputs, give it some time, or use the URL instead.")


if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        print("Please add the SSRN # or url string")


# ---
# #### Adding the entry to a data frame ####

# In[ ]:


import pandas as pd
pd.DataFrame.from_dict(test, orient ='index', columns = [bib_entry])

