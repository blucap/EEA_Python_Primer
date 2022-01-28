#!/usr/bin/env python
# coding: utf-8

# # Session 6: Use Pandas to index, split, apply, and combine data.

# ## [EAA - ARC Python Primer for Accounting Research](https://martien.netlify.app/book/example/)

# ### Preparation ###
# 
# **Complete the cells below so that by the start of the Tuesday session you have a data frame that we can use to split, apply and combine.**
# 
# At the session we will complete our analysis of the EBA Risk Dashboard data.
# 
# ---
# 
# #### Introduction
# ---
# 
# The cells below demonstrate how use Use Pandas to index, split, apply, and combine data.
# 
# We will download and munge data from the EBA Risk Dashboard, which is part of the regular risk assessment conducted by the EBA and complements the Risk Assessment Report. The EBA Risk Dashboard summarizes the main risks and vulnerabilities in the banking sector in the European Union (EU) by looking at the evolution of Risk Indicators (RI) among a sample of banks across the EU.
# 
# The [EBA Risk Dashboard pdf](https://www.eba.europa.eu/sites/default/documents/files/document_library/Risk%20Analysis%20and%20Data/Risk%20dashboard/Q3%202021/1025829/EBA%20Dashboard%20-%20Q3%202021%20v2.pdf?retry=1) has lots of tables, but for research purposes it is better to get the data in machine readable form.
# 
# Luckily the EBA thought about us. Under the name [the intractive tool](https://www.eba.europa.eu/sites/default/documents/files/document_library/Risk%20Analysis%20and%20Data/Risk%20dashboard/Q3%202021/1025834/EBA%20Interactive%20Dashboard%20-%20Q3%202021%20-%20Protected.xlsm) they offer an Excel file with a treasure trove of data.
# 
# The challenge we face in this Session is that the data is not as well-structured as the BHC data. It requires more work to get it into shape.
# 
# Learning objectives:
# 
# - Splitting the data into groups based on some criteria
# - Applying a function to each group independently
# - Combining the results into a data structure, using merge and join
# - Reshaping data, using `melt`
# - Reshaping data, using pivot
# - Presenting data in graph and table

# **Required**:
# 
# From the EBA website, **download the interactive Dashboard data**, i.e. this spreadsheet: `EBA Interactive Dashboard - Q3 2021 - Protected.xlsm` for [2021Q3](https://www.eba.europa.eu/sites/default/documents/files/document_library/Risk%20Analysis%20and%20Data/Risk%20dashboard/Q3%202021/1025834/EBA%20Interactive%20Dashboard%20-%20Q3%202021%20-%20Protected.xlsm). 
# 
# The file is an Excel file.  **Save** it to a folder on your drive, e.g. `D:/users/my_user_name_here/EAA_python/code/`. 
# 
# **Note:** python may throw an error if you want to import an Excel file for the first time. See solutions [here](https://stackoverflow.com/questions/64432641/pandas-and-xlrd-error-while-reading-excel-files) and [here](https://techoverflow.net/2021/08/01/how-to-fix-pandas-pd-read_excel-error-xlrderror-excel-xlsx-file-not-supported/).
# 
# Run the cells below after setting the correct source folder of your files, i.e. replace `my_user_name_here` with something that works on your machine. See this [link](https://www.youtube.com/watch?v=hUW5MEKDtMM) and this [link](https://www.youtube.com/watch?v=7ABkcHLdG_A) for explanations of folders and directories.

# **Let's start!**

# In[ ]:


# the familiar preamble
import pandas as pd
import numpy as np
import os # To set our working folder

if os.name=='nt':  # for Windows users
    os.chdir('D:/users/my_user_name_here/EAA_python/data/')  # note the forward slashes, change 'martien' to your user name
else:
    os.chdir('/home/my_user_name_here/EAA_python/data/')  # For Linux or Mac


# ---
# The Excel file has many sheets, but we will focus on 
# 
# - 'RI database' and 'Data' for *Risk Indicator data*
# - 'Data Annex' 'Mapping' for data from the *Statistical Annex*
# 
# Open the Excel file, from the *Data* sheet, columns `'AF:DA'`. The first row in the sheet is empty, so we skip it.

# In[ ]:


# Set the file name as `fn`, we will use the file a couple of times
fn = 'EBA Interactive Dashboard - Q3 2021 - Protected.xlsm' 

def read_risk_indicators(fn, sn):
    df = pd.read_excel(fn, sheet_name=sn, usecols='AF:BI', skiprows=[0])
    return df

df = read_risk_indicators(fn, 'Data')
df.tail(5)


# **Observations**
# 
# - Some column names have a dot (.), which is not helping us. 
# - Some cells have a dot (.), which should be changed in a NaN.
# - The Name column combines country codes `SK` with a variable code `SVC_3`. These are separated by a dash `_`. We need to split that column.
# - Some observations are from the `EU`, which is not a separate country. I suggest to remove these rows.
# - The variable codes are hard to interpret. 
# - The columns are years.
# - Ideally we want the data frame to feature the variable names in columns, and the country and date as an index. This requires reshaping.

# ---
# **Renaming the column names**
# 
# Before we rename the relevant columns, we set `Name` as the index, which protects it from being renamed.

# In[ ]:


df.set_index('Name', inplace=True)


# **Some column names have a dot (.), which is not helping us**
# 
# To solve this, we should rename the columns. The challenge is that the column names with the dots are strings while the others are integers. 
# 
# We can use list comprehension to solve this for all columns except for `Name`. 

# In[ ]:


# Before
print([x for x in df])


# In[ ]:


# This is how the names should look like:
print([str(x) if isinstance(x, int) else x.split('.')[0] for x in df]) # Take the first item from the split string [0]


# Use the contents of the previous cell  and `df.columns = ` to change the column names into strings.

# In[ ]:


df.columns = [str(x) if isinstance(x, int) else x.split('.')[0] for x in df]
print(list(df))


# In[ ]:


df.head(8).tail(4)


# **Some cells have a dot (.), which should be changed in a NaN**
# 
# The next challenge is to deal with missing observations, which also are marked as a dot. As a consequence, Python marks these columns as object, which is not ideal for analysis.

# In[ ]:


df.dtypes[1:5]


# The solution is to coercing these observations into becoming numbers using `apply()` to the data frame:

# In[ ]:


df = df.apply(pd.to_numeric, errors='coerce')


# Now all cells are numbers, which you can check with `df.dtypes`:

# In[ ]:


df.dtypes[1:5]


# In[ ]:


df.dtypes[-5:]


# In[ ]:


df.head(8).tail(4)


# ---
# 
# **The Name column combines country codes with variable codes. They are separated by a dash `_`.**
# 
# The next challenge is to split the `Name` column into a country label and a variable name.
# 
# This can be done by the following method, which splits a string as follows:

# In[ ]:


s = 'EU_LIQ_17'
print(s)
s = s.split('_', 1)
print(s)


# We now **apply** this approach to the `Name` column of the data frame, which requires us to reset the index. 
# 
# Once we reset the data frame, we split the Name column into 'Country' and 'Variable'.
# 
# This method is documented [here](https://datascienceparichay.com/article/pandas-split-column-by-delimiter/).

# In[ ]:


df.reset_index(inplace=True)
df[['Country', 'Variable']] = df['Name'].str.split('_', 1, expand=True).rename(columns={0: 'Country', 1: 'Variable'})


# In[ ]:


# Check the outcome
df[['Name', 'Country', 'Variable']].head(2)


# We don't need the name column any longer:

# In[ ]:


df = df.drop('Name', axis=1)


# ---
# 
# **Some observations are from the `EU`, which is not a separate country**
# 
# I suggest to remove these rows using `.loc`.

# In[ ]:


print(f'Before: {len(df)}')
df = df.loc[df['Country']!='EU']
print(f'After: {len(df)}')


# Setting the index to `['Country', 'Variable']` renders a data frame with only numbers and NaNs.

# In[ ]:


df.set_index(['Country', 'Variable'], inplace=True)


# In[ ]:


df


# ---
# 
# **The variable names are hard to interpret**
# 
# The next functions create a frame which we can use to lookup the data definition from the `RI database` sheet in the Excel file. I use a helper function that cleans the text of the labels. 
# 
# Note the use of `df['Dashboard name'].apply(clean_text)`. It **applies** a function to a column on the data frame. This can also be used to apply complex numerical calculations to a column of a data frame. 

# In[ ]:


def clean_text(s):
    return s.replace('\n', ' ').strip() # Get rid of line breaks and trim leading and lagging spaces. 

def ri_data_definitions(fn):
    df = pd.read_excel(fn, sheet_name='RI database', usecols='D:E', skiprows=[0]).dropna()
    df['Dashboard name'] = df['Dashboard name'].apply(clean_text)    
    df.set_index('Risk Indicator code', inplace=True)
    print(df)  #print(df.to_markdown())
    return df

df_ri_defs =  ri_data_definitions(fn)


# In[ ]:


# Check
df_ri_defs.loc['SVC_13']


# --- 
# 
# ### Reshaping the data, Part 1: melting ###
# 
# 
# The data frame currently is useful for analysis of indicators of different countries. 
# 
# For example, suppose we want to track the evolution of the Liquidity coverage ratio (`LIQ_17`) for Austria.

# In[ ]:


df.loc[('AT','LIQ_17')].dropna().plot(kind = 'bar')


# However, the shape of the data frame is such that we can not easily analyze variables grouped by country.
# 
# One way to sort out that problem is to reshape the frame into  one with only one value column and a triple-index column with Variable name, Country code, and Date.
# 
# Let's do that using the [melt](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.melt.html) command.
# 
# To make this work, we need the values from the data frame, and `Variable`, `Country` as `id` variables. To get 'Variable' and 'Country', we extract them from the current index, hence the use of `df.reset_index()` in the command below:

# In[ ]:


dfm = pd.melt(df.reset_index(), id_vars=['Variable', 'Country'], value_vars=list(df), var_name='Date', value_name='value')
dfm.set_index(['Variable', 'Country', 'Date'], inplace=True)
dfm


# In[ ]:


print(df_ri_defs.loc['LIQ_17'])
print(df_ri_defs.loc['SVC_3'])


# In[ ]:


df_lr = dfm.loc['LIQ_17']
dfcet = dfm.loc['SVC_3']


# It is now easier to analyze variables in groups, more on that later.

# ---
# 
# ### Bringing it all together ###
# 
# Consolidate all of the above in one function to create a workable data. The function also returns a list of EU countries, which we can use when we want to select data from individual countries. 
# 
# The function outputs three frames, one that is close to the original EBA spreadsheet (`df`), a melted version (`dfm`), and the list of EU country codes. 

# In[ ]:


def read_risk_indicators(fn, sn):
    df = pd.read_excel(fn, sheet_name=sn, usecols='AF:BI', skiprows=[0])
    df.set_index('Name', inplace=True)
    df.columns = [str(x) if isinstance(x, int) else x.split('.')[0] for x in df]
    df = df.apply(pd.to_numeric,  errors='coerce')
    df.reset_index(inplace=True)
    df[['Country', 'Variable']] = df['Name'].str.split('_', 1, expand=True).rename(columns={0: 'Country', 1: 'Variable'})
    df = df.drop('Name', axis=1)
    df = df.loc[df['Country']!='EU']
    eu_ctrys = sorted(list(set(df['Country'].tolist())))  # let's get a list of EU countries
    dfm = pd.melt(df, id_vars=['Variable', 'Country'], value_vars=list(df), var_name='Date', value_name='value')
    dfm.set_index(['Variable', 'Country', 'Date'], inplace=True)
    df.set_index(['Country', 'Variable'], inplace=True)
    return df, dfm, eu_ctrys

fn = 'EBA Interactive Dashboard - Q3 2021 - Protected.xlsm'
df, dfm, eu_ctrys = read_risk_indicators(fn, 'Data')


# In[ ]:


print(eu_ctrys)


# In[ ]:


df.head()


# In[ ]:


dfm


# In[ ]:


# checking CET 1 capital ratio, grouped by Date
dfm.loc['SVC_3'].groupby('Date').mean().plot(kind='bar')


# In[ ]:


# checking CET 1 capital ratio, grouped by Country
dfm.loc['SVC_3'].groupby('Country').mean().plot(kind='bar')


# --- 
# 
# ### Reshaping the data, Part 2: pivoting the data ###
# This section will be completed by by end of Sunday CET.
