#!/usr/bin/env python
# coding: utf-8

# # Session 5: Data munging with Pandas

# ## [EAA - ARC Python Primer for Accounting Research](https://martien.netlify.app/book/example/)

# #### Use Pandas to explore, manage, clean data, deal with missing observations.
# ---
# 
# The cells below demonstrate how use Pandas to explore, manage, clean data, deal with missing observations.
# 
# The focus of this session is on the use of [Pandas](https://pandas.pydata.org/), your friend for analyzing **Pa**nel **Da**ta.
# 
# We will download and munge Google mobility data. 
# 
# An assignment, separately published, then will apply the techniques learned in this lesson to accounting data from U.S. bank holding companies (free, high-quality accounting data).
# 
# Learning objectives:
# 
#  - Download  and explore data from the cloud
#  - Make column names look pretty
#  - Use the index of a data frame
#  - Use the index to select rows
#  - Select rows based on date(s)
#  - Dealing with missing observations
#  - Appending, replacing, and joining data
#  - Make a pretty graph
#  - Write functions

# ### Google mobility data
# 
# This data shows how your community is moving around differently due to [COVID-19](https://www.google.com/covid19/mobility/). The data is available via this [link](https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv).
# 
# Downloading takes some time, as it is big. We save the data to disk, compressed, to save space.

# **Let's start!**

# In[ ]:


import pandas as pd 
import numpy as np


# Normally you need not set the low_memory option to False, but hey, this is big data!

# In[ ]:


df = pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv', low_memory=False)


# Let's save the data, compressed, and ignore the index for now. I will come back to indexes shortly.

# In[ ]:


df.to_csv('Global_Mobility_Report.csv.zip', compression='zip', index=False)


# We can read the data using the follwing command. No need to unzip the zip file.

# In[ ]:


df = pd.read_csv('Global_Mobility_Report.csv.zip', low_memory=False)


# 
# 
# **Let's explore the data frame:**

# In[ ]:


df.head()


# **Question**: How to show the last row(s) of the data frame?

# In[ ]:





# More information on our data frame:

# In[ ]:


df.info()


# In[ ]:


df.count()


# In[ ]:


df['country_region'].value_counts()


# In[ ]:


print(f'Shape {df.shape}, rows: {df.shape[0]}, columns: {df.shape[1]}')


# **Question**: can we use a shorter command to show the number of rows in the data frame?

# In[ ]:





# **Question**: How can we quickly list the column variables?

# In[ ]:





# ---
# 
# **Note the following in the data frame:**
# 
# - The column names look awful, we will change that.
# - The leftmost column is the index. The index here is not meaningful. But we will make a habit of using the index. It is an extremely powerful feature of Pandas! 
# - The number of observations is large: > 8 million. To make our life easy, we will keep only a few countries. 
# - The date column is a float, we should turn that in a date variable.
# - There are observations called NaN, these are empty cells, and we will learn how to manage them. 

# In[ ]:


df.head(3)


# ---
# 
# ### Changing column names ###
# 
# The column names are very long. Let's make the shorter by eliminating this part:`_percent_change_from_baseline` from each column name.
# 
# We use list comprehension to accomplish that. While walking over each column name, we eliminate the unwanted parts from each of them. 

# In[ ]:


df.columns = [x.replace('_percent_change_from_baseline', '') for x in list(df)]
df.columns = [x.replace('_', ' ') for x in df]  # get rid of underscores
df.columns = [x.strip() for x in df]  # get rid of leading and lagging space (like Excel's 'trim')
df.columns = [x.capitalize() for x in df]  # Even nicer!
df.head(3)


# In[ ]:


list(df)


# **Question**: We use use four lines to change the column names. That is too much. Can we make the code in the cell above more efficient?

# In[ ]:





# ---
# 
# **Setting the index**
# 
# Let's start with setting an index, as that will make it easier to manage the data. 
# 
# You can change the index whenever you want, so don't worry too much about setting them right or wrong.
# 
# In this case I will set `country_region_code` as the index, because we want to select country observations.
# 

# In[ ]:


df = df.set_index('Country region code')
df.index


# In[ ]:


df.head(3)


# Note the index is now in **boldface**.
# 

# ---
# 
# **Keeping the data manageable**
# 
# - For now, we want only New Zealand data.
# - We also don't want all identifying variables: we keep  the last 7 columns (from `date` to `residential_percent_change_from_baseline`.)
# 
# To accomplish this we can use `loc` or, alternatively, the index. 

# In[ ]:


# using loc, but for now not specifying columns
dfnz = df.loc[df['Country region']=="New Zealand"]
dfnz.head(3)


# In[ ]:


# using loc, specifying two columns. Note that the columns we need are in a list, between brackets.
dfnz = df.loc[df['Country region']=="New Zealand", ['Date', 'Residential']]
dfnz.head(3)


# In[ ]:


# using loc, specifying columns the columns we need, with sliced column names:
dfnz = df.loc[df['Country region']=="New Zealand",'Date':'Residential']
dfnz.head(3)


# ---
# 
# **Data selection using the index** 
# 
# The loc. syntax is not always practical, especially if you select rows using multiple criteria. 
# 
# In many cases you can select rows using the index. 
# 
# Let's, for now, select data from the Netherlands using the index (NL). Remember, we set the index to `country_region_code` a while ago.

# In[ ]:


dfnl = df.loc["NL"]
dfnl.head(3)


# ---
# 
# **Combining selections**
# 
# **Question**: using the index, can combine selections, e.g. from a list of countries, say `["NL","NZ"]`?

# In[ ]:



# Show the head of the newly created data frame dfnlnz:


# In[ ]:


# Show the tail of dfnlnz:


# ---
# 
# **Specify columns when we select rows using the index**
# 
# We specify the the columns in a bracketed list:

# In[ ]:


dfnl = df[['Date','Residential']].loc["NL"]
dfnl.head(3)


# ---
# Finally selecting the last 7 columns of the data frame for the New Zealand.

# In[ ]:


dfnz = df.loc["NZ", 'Date':'Residential']
dfnz.head(3)


# In[ ]:


dfnz.shape


# ---
# 
# **Saving the data**
# 
# We now have a much more easy to manage data frame. Let's save it. 
# 
# We want to keep the index, so we save the csv file without using the `index=False` parameter.

# In[ ]:


dfnz.to_csv('New_Zealand_Mobility_Report.csv')
dfnz.head(3)


# If you retrieve the csv data, you will need to set the index again, but don't worry about that for now.

# In[ ]:


dfnz = pd.read_csv('New_Zealand_Mobility_Report.csv')
dfnz.head(3)


# ---
# 
# ### Changing the date column in a proper date-time format ###
# 
# 
# We should change the date column in a proper date format. This allows us select rows on the basis of dates. 
# 
# We set the date column as index:

# In[ ]:


dfnz['Date']= pd.to_datetime(dfnz['Date'])

dfnz.set_index('Date', inplace=True) # This is equivalent to dfnz = dfnz.set_index('date'). 
                                     # The `inplace` parameter allows for shorter writing.


# Given that our data is only from New Zealand we do not need the `Country region code` column. 

# In[ ]:


dfnz.drop("Country region code", inplace=True, axis ='columns')  # To drop labels from columns set axis 1 or ‘columns’.


# In[ ]:


dfnz.tail(3)


# ---
# 
# **Date selection using the index** 
# 
# With Date as index, it is easy to select rows based on dates. Again, the index shows how powerful indexing is.

# In[ ]:


# All observations from 2020:
dfnz.loc['2020'].tail(2)


# **Question**: Using the index, show only observations from this month:

# In[ ]:





# In[ ]:


# All observations from the second half of 2021:
dfnz.loc['2021-06':'2021-12']


# ---
# 
# ### Dealing with missing data (NaNs) ###
# 
# Thus far we ignored the NaN's, which in many cases is fine. For example, when we want to calculate basic statistics:

# In[ ]:


dfnz_june = dfnz.loc['2021-06']
dfnz_june.describe()


# ---
# 
# We may want to use only complete cases, or exclude rows with missing data on some variables.
# 
# - In that case we use `dropna()`

# In[ ]:


dfnz_dropna_demo = dfnz_june.copy()  # First make a copy* from an original dataframe. 
dfnz_dropna_demo = dfnz_dropna_demo.dropna() 
dfnz_dropna_demo.describe()


# The documentation of [dropna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html) shows that it is a powerful and versatile command.
# 
# The default dropna() is aggressive: it deletes all rows with a NaN. 
# 
# **Questions**: 
# 
# - which parameter setting for dropna do you need to delete only the rows that are empty?
# - which parameter setting for dropna do you need to delete rows for which a specific column has missing values?
# - which parameter setting for dropna do you need to delete columns with missing values?
# 

# We may also want to fill missing variables with, say, zeros.  
# 
# - In that case we use `fillna()`

# In[ ]:


dfnz_fillna_demo = dfnz_june.copy()    # First make a copy from an original dataframe.
dfnz_fillna_demo.fillna(0, inplace = True)  # Now using inplace = True
dfnz_fillna_demo


# ---
# 
# ### Appending dataframes ###
# 
# Suppose we want a data frame where we append data from, say, June to data from September.
# 
# We can achieve this with the `append` method:

# In[ ]:


dfnz_september = dfnz.loc['2021-09']
dfnz_combined = dfnz_june.append(dfnz_september)
dfnz_combined


# **Question**: can we create `dfnz_combined` in a singly line, without creating `dfnz_september`?

# In[ ]:





# ---
# 
# ### Replacing values ###
# 
# Suppose we want to replace values in our data frame.
# 
# We can achieve this with the `replace` method. (But there are more ways of achieving this). 
# See this [link](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html) ands this [link](https://stackoverflow.com/questions/61996932/replacing-values-greater-1-in-a-large-pandas-dataframe) for more info on `replace`.

# In[ ]:


dfr = dfnz_september.copy()  # First make a copy from an original dataframe.
dfr = dfr.replace(0, 1)     # Replace all zero values by one 

dfr.loc[dfr['Grocery and pharmacy'] == 0] # Should return no valid rows.


# ---
# 
# The following command allows us to replace all negative values by zero.
# 
# Note, this applies to the entire frame, which is fine, because non-numerical data (in this case Date) are safely tucked away in the index, and won't be affected.

# In[ ]:


dfpos = dfnz_september.copy()  # First make a copy from an original dataframe.
dfpos[dfpos < 0] = 0
dfpos.min()


# Applying this logic to a single column:

# In[ ]:


dfpos = dfnz_september.copy()  # First make a copy from an original dataframe.
dfpos['Workplaces'][dfpos['Workplaces']<0] = 0
dfpos


# Using .loc

# In[ ]:


dfpos = dfnz_september.copy()  # First make a copy from an original dataframe.
dfpos.loc[dfpos.Workplaces < 0, ['Parks', 'Workplaces']] = 0
dfpos


# ---
# 
# We can also use `clip` to achieve similar results, though in practice, I hardly use the clip command. 
# 
# You can use it to control the results per row, see this [link](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.clip.html). 

# In[ ]:


dfclip = dfnz_september.copy()  # First make a copy from an original dataframe.
dfclip = dfclip.clip(lower=-50, upper=10)


# **Question**: Can we apply a single command to the `dfclip` data frame to display only the minimum and maximum values - this  to verify the outcome of the cell above? Hint: use [`agg`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.agg.html?highlight=agg).

# In[ ]:





# ---
# 
# ### Pandas Series ###
# 
# Until now, we worked with Pandas Data Frames. However, in some cases we use Series. Pandas Series have only a single column. Otherwise they are pretty much the same as a Data Frame. 
# 
# The Series is the data structure for a single column of a DataFrame, not only conceptually, but literally, i.e. the data in a DataFrame is actually stored in memory as a collection of Series. 
# 
# When you select a single column from a data frame, you will get a series:

# In[ ]:


s = dfnz['Parks']
s.hist(bins=50)


# In[ ]:


#s.info() # Will give an error message
s.shape


# In[ ]:


# Converting a series into a DataFrame:
s.to_frame().head(3)


# ---
# 
# ### Joining data using the index ###
# 
# Join data frames using the index is very easy, but it requires setting up the data. Both data frames need the same index.
# 
# The next example shows how to add the country names in Spanish to the main data frame (df). 
# 
# We need a list of Spanish country names that we can merge on the `Country region code`, which is the current index of the main data frame.
# 
# Luckily there is such a list: see this Github [link](https://github.com/stefangabos/world_countries/).
# 
# The next code prepares the data from Github, and the returns a list properly prepared for joining. 
# 
# I decided to write a function that allows us to make country name lists for various languages. 

# In[ ]:


def intl_country_names(ctry, new_column_name):
    # read from the cloud:
    dfj = pd.read_csv('https://cdn.jsdelivr.net/npm/world_countries_lists@latest/data/'+ctry.lower()+'/countries.csv')
    # convert the country codes to upper case:
    dfj['alpha2'] = dfj['alpha2'].str.upper()  
    # We need meaningful column names: 
    dfj.rename(columns = {'alpha2': 'Country region code', 'name': new_column_name}, inplace=True)
    # We need the index name to be the same as the one of the main data frame
    dfj = dfj.set_index('Country region code')
    # We don' t need the following colums
    dfj.drop(['id','alpha3'], inplace=True, axis ='columns')
    return dfj

dfj = intl_country_names('es', 'Nombre del país')
dfj


# The next step is to perform the merge, which is dead easy, because we rely on `Country region code` as the key column for joining.

# In[ ]:


df = df.join(dfj)  


# In[ ]:


df['Nombre del país'].value_counts(normalize=True)


# ---
# 
# **Question**: can we add a column with French names to our main data frame **without referring to a data frame directly**, but using the `intl_country_names` function instead? The relevant country code and column name are `fr` and  'Nom du pays'.

# In[ ]:





# ---
# 
# ### Performing operations on all but a few columns of a  data frame ###
# 
# Suppose we want to divide all values of the NZ data frame by 100 (without affecting the index values). This is relatively easy:

# In[ ]:


dfnz /= 100


# In[ ]:


dfnz.head(3)


# Again, this shows the power of indexing: You can 'hide' columns that you do not want to be affected by an operation in the index. Once you are done, you reset the index (by way of `df.reset_index(inplace=True)`) and continue working on your data frame. 
# 
# Of course, you can apply an operation to a single column (or a set of columns) by selecting them as shown before:
# `dfnz['Date'] = pd.to_datetime(dfnz['Date'])`. 
# But, if all except for a few columns should undergo the same treatment, then the approach shown above is the way to go.

# ---
# ### Consolidating our knowledge:  a graph ###
# 
# What we learned today can be used to make a nice graph.

# In[ ]:


dfnz.plot()


# Well, maybe we should tweak the graph.
# 
# We can resample the data to weekly data, not daily, using the `resample` command:

# In[ ]:


dfnz.resample('W').mean().plot(figsize=(10,8), title= 'Mobility data: Percentage Change from Base line (NZ).')


# ---
# ### Consolidating our knowledge: a function that shows the graph and returns a proper data set  ###
# 
# What we learned today can be combined into a single function, for which we can use the country code as an input. 
# 
# The start of the function checks if the data is already on disk. If not, it loads the data from the cloud.

# In[ ]:


import pandas as pd 
import numpy as np
import os

def arc_mobility(country_code):
    if os.path.isfile('Global_Mobility_Report.csv.zip'):
        fn = 'Global_Mobility_Report.csv.zip'
        file_location = 'Disk'
    else:
        fn = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv'
        file_location = 'Cloud'
        
    print(f'\nThe mobility data location: {file_location}.\n')
    df = pd.read_csv(fn, low_memory=False)

    df.columns = [x.replace('_percent_change_from_baseline', '').replace('_', ' ').strip().capitalize() for x in df]

    df = df.set_index('Country region code')

    df = df.loc[country_code, 'Date':'Residential']
    df['Date']= pd.to_datetime(df['Date'])
  
    df = df.reset_index().set_index('Date')

    df.drop("Country region code", inplace=True, axis ='columns')

    df /= 100

    df.resample('W').mean().plot(figsize=(10,8), title= 'Mobility data: Change from Base line ('+ country_code + ').')
    return df
    
dfnz = arc_mobility('NZ')


# In[ ]:


dfnz


# \* See documentation on copy [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.copy.html).
