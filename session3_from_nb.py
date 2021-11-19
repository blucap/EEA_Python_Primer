#!/usr/bin/env python
# coding: utf-8

# # Session 3: Python commands and variable types.

# ## [EAA - ARC Python Primer for Accounting Research](https://martien.netlify.app/book/example/)

# #### This notebook explains the main Python variable types. It uses a file with Bank Holding Company financial data from the National Information Center. 
# Click [here](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2020) to download the file [BHCF20201231.ZIP](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2020) and save it file to a folder on your PC, e.g. `D:/Users/myusername/EAA_python/code/`. 
# 
# Note, the file is a csv file, but you **do not** have to **unzip** the file!
# 
# ---
# 
# The cells below demonstrate the following data types:
# 
# + Strings
# + Integers
# + Tuples
# + Floats
# + Booleans
# + Date variables
# + Lists
# + Dictionaries
# 
# The cells below also demonstrate:
# 
# + if-then-else statements
# + pretty printing numbers
# + a function that acts like a judge
# 
# The output of this notebook generates a data frame that it exports to Stata, including the variable labels. 
# 
# ---

# Open Spyder or a Jupyter notebook and make a habit of entering these three lines in the editor pane (Spyder) or cell (Jupyter).
# 
# ---

# In[ ]:


import os
import pandas as pd
import numpy as np


# ---
# 
# Using the following commands, I set the working folder, the location on your hard drive where you will store data for this session.

# In[ ]:


if os.name=='nt':  # for Windows users
    os.chdir('D:/users/martien/EAA_python/code/')  # note the forward slashes, change 'martien' to your user name
else:
    os.chdir('/home/martien/EAA_python/code/')  # For Linux or Mac 


# Press \[CTRL-ENTER\] to execute the cell code. 
# 
# ---
# 
# Note that I use cells in the Jupyter to execute bits of code. Spyder has the same functionality if you add 
# 
# `#%%`
# 
# `before and after`
# 
# `#%%`
# 
# your code snippet.
# 
# ---

# Download 'BHCF20201231.ZIP' from [https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2020](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2020) 
# and save it to the folder mentioned in the cell above.

# ---
# #### My first **string**: `fname`.
# 
# I assign the string 'BHCF20201231.ZIP' to the variable `fname`: 

# In[ ]:


fname = 'BHCF20201231.ZIP'
print(fname)


# I use the string to load the Bank Holding Company financial data from the folder `../EAA_python/code/`, see the explanation above.
# 
# Normally you can use the command `df = pd.read_csv(fname)`, but that generates an ugly error message.
# 
# Instead I use: 

# In[ ]:


df = pd.read_csv(fname, sep='^', encoding = "ISO-8859-1", low_memory=False)


# Which aknowledges the funny separator (^) the FED uses as a field separator, the file encoding, and the fact that it is a big file. 
# 
# We do not have to worry about the fact that the file is compressed (zip). 
# 
# ---

# Very basic string manipulations:

# In[ ]:


fname = 'BHCF20201231' + '.ZIP'
print(fname)


# In[ ]:


fname = fname.lower()
print(fname)
fname = fname.upper()
print(fname)


# Trimming

# In[ ]:


fname = "    " + fname + "    "
print(fname,'.')
fname = fname.strip()
print(fname)


# Explore the file using head and tail:

# In[ ]:


df.head()


# In[ ]:


df.tail()


# #### My first **Integer**: `nrows`.
# This shows the number of rows in the data frame.

# In[ ]:


nrows = len(df)
print(nrows)


# ---
# Count the number of valid observations for Total Assets (BHCK2170)

# In[ ]:


n_of_ta = df['BHCK2170'].count()
print(n_of_ta)


# ---
# #### My first **tuple**: `coordinate`.

# In[ ]:


coordinate =  (47.559601, 7.588576)
coordinate[0]


# In[ ]:


coordinate[1]


# #### Another **Tuple**:

# In[ ]:


nrows, ncols = df.shape
print(nrows, ncols)


# In[ ]:


len(df)


# In[ ]:


df.shape[0]


# In[ ]:


df.shape[1]


# ---
# #### My first **float**: `max_ta`.

# In[ ]:


max_ta = df['BHCK2170'].max()
max_ta


# In[ ]:


min_ta = df['BHCK2170'].min()
min_ta


# #### Printing

# In[ ]:


print(max_ta)
print()
print('Maximum value of Total assets: ', max_ta)
print('Maximum value of Total assets: ', int(max_ta)) # convert to integer
print('Maximum value of Total assets: {:,.0f}'.format(max_ta))  # format method version
print(f"Maximum value of Total assets: ${max_ta:,.0f}, minimum value: ${min_ta:,.0f}")  # f-string version
print(f"\nMaximum value of Total assets: ${max_ta:,.0f}, minimum value: ${min_ta:,.0f}\n(in thousands).")


# ---
# #### In 2006, the threshold for filing FR Y-9C forms changed from \\$150 million in total assets to \\$500 million in total assets.

# Before we can check if smaller banks file the form nevertheless, we should divide Total Asset values by 1,000, convert values to millions:

# In[ ]:


min_ta = min_ta / 1000
min_ta


# But easier is this, using the division operator followed by the equal sign:

# In[ ]:


min_ta = df['BHCK2170'].min()  # Obain again the minimum value for Total Assets:
print(min_ta)
min_ta /= 1000
print('Minumum valube of Total assets, in millions: ${:,.2f}'.format(min_ta))


# Likewise, using the same method for adding numbers:

# In[ ]:


a = 1
print(a)
a += 1
print(a)


# ---
# #### The **if-statement**:

# In[ ]:


print('Total assets, lowest value in data frame: ${:,.0f} million.'.format(min_ta))
if min_ta > 500:
    print('Above threshold')
else:
    print('Below threshold')


# Note the indents, which is characteristic for Python
# 
# Likewise:

# In[ ]:


if max_ta/1000 > 500:
    print('Above threshold')
else:
    print('Below threshold')


# ---
# Most operators are straightforward: + - * / etc. See for documentation this [site](https://www.w3schools.com/python/python_operators.asp).
# 
# But note these two:

# In[ ]:


min_ta ** 2  # squared


# In[ ]:


min_ta ** 0.5  # square root


# ---
# #### My first **boolean** variable: `low_mem`.

# In[ ]:


low_mem = False
df = pd.read_csv(fname, sep='^', encoding = "ISO-8859-1", low_memory=low_mem)


# Note that the result of `ncols == nrows` in the if-statement below is a boolean:

# In[ ]:


if ncols == nrows:
    print('Square dataframe')
else:
    print('Rectangular dataframe')


# If-statements can take up many lines. 
# 
# The **ternary operator**, however, allows you to write an if-statement in a single line:

# In[ ]:


guilty = True
verdict = "Innocent" if not guilty else "Guilty"
print(verdict)


# Let's write a function and play judge:

# In[ ]:


def judge(guilty_or_not):
    verdict = "innocent" if not guilty_or_not else "guilty"
    return 'The defendant is '+verdict
    
judge(True)


# In[ ]:


judge(False)  


# Likewise:

# In[ ]:


text = "Square " if ncols == nrows else 'Rectangular '
print(text + 'dataframe')


# If-statement with multiple choices:

# In[ ]:


if ncols == nrows:
    print('Square dataframe')
elif ncols > nrows:  # you can add more elifs
    print('Wide dataframe')
else:
    print('Narrow dataframe')


# ---
# #### My first **datetime** variabele: `datadate`
# 
# To work with date variables, please import the datetime library first:

# In[ ]:


from datetime import datetime


# In[ ]:


datadate = df['RSSD9999'].max()
print(datadate)


# In[ ]:


datadate = df['RSSD9999'].min()
print(datadate)
datadate = str(datadate)  # Turn into a string
print(datadate)
datadate = datetime.strptime(datadate, '%Y%m%d')  # Convert to a datetime variable
print(datadate)


# Once a datetime variable, Python can properly work with it:

# In[ ]:


datadate.strftime('%m-%d-%Y')  # String from time


# In[ ]:


datadate.strftime('%d %m %y')  # String from time


# Extract year, month, day, quarter

# In[ ]:


print(f"Year: {datadate.year}")
print(f"Month: {datadate.month}")
print(f"Day: {datadate.day}")
print(f"Quarter: {(datadate.month-1)//3+1}")


# ---
# More flexible is the use of `parser`, which copes with most date formats:

# In[ ]:


from dateutil.parser import parse

print(parse("31;12;2001"))


# In[ ]:


# and for U.S. notation:
print(parse("9/11/2001", dayfirst=False))


# ---
# Calculations with dates: lapsed days.

# In[ ]:


delta = datetime.now() - datadate

print(f"Days from year-end of the data frame: {delta.days}")


# ---
# Calculations with dates: determine a future date.

# In[ ]:


from datetime import timedelta
fdate = datadate + timedelta(90)  # Filing deadline assumed to be 90 days after year-end
print(fdate)
fdate = fdate.strftime('%d/%m/%Y')
print(f"10K filing date: " + fdate)


# ---
# #### My first **list**: `months`

# In[ ]:


months = 'JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC' # String
print(months + '\n')
months = months.split(",")
print(months)


# Likewise:

# In[ ]:


month_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
print(month_num)


# #### Slicing lists
# 
# The syntax for slicing is `list[start:stop:step]`.
# 
# Note that Python counts from zero, not one:

# In[ ]:


months[0:3]


# In[ ]:


months[5:]


# In[ ]:


months[-3:]


# In[ ]:


months[-6:-3]


# In[ ]:


col_names = df.columns
print(list(col_names)[0::100])  # I am not going to list all variables!


# #### Reversing lists

# In[ ]:


months[::-1]


# Adding to list:

# In[ ]:


month_num = month_num + [13]
month_num


# Deleting from list:

# In[ ]:


del month_num[11]  # position
month_num


# Restoring that list:

# In[ ]:


month_num = list(range(1, 13))
month_num


# Removing from list

# In[ ]:


months.remove('DEC')
months


# Restoring that list:

# In[ ]:


months = months + ['DEC']
months


# ---
# Sorting lists

# In[ ]:


month_num.sort()
month_num


# In[ ]:


month_num.sort(reverse = True)
month_num


# Restoring order:

# In[ ]:


month_num.sort()
print(month_num)


# ---
# ### List comprehension
# 
# List comprehension allows one to quickly iterate over a list. This is often much more efficient than using a traditional for-next loop:
# 
# ---
# 
# The hard way:

# In[ ]:


for x in range(0, 12):
    print(x, months[x])


# ---
# It is better to use this instead:

# In[ ]:


for x in months:
    print(x)


# The approaches above create a variable (`x`), which we probably won't use going forward.

# In[ ]:


print(x) 


# Let's try list comprehension, which creates a new list:

# In[ ]:


[y for y in months]


# In[ ]:


'y' in locals()  # No y-variable to be seen!


# I can also edit the items in the list, for example by adding a characters (`Q-`) before the month: 

# In[ ]:


["Q-"+x for x in months]


# Or select months starting with a `J` and convert them to lower case:

# In[ ]:


[x.lower() for x in months if x.startswith('J')]


# ---
# Select from the data frame the variables that contain text:

# In[ ]:


text_cols = [x for x in df if x.startswith('TEXT')]
print(len(text_cols))
print()
print(text_cols[::10])


# Selecting column names starting with `RSSD`:

# In[ ]:


rssd_cols = [x for x in df if x.startswith('RSSD')]
print(len(rssd_cols))
print()
print(rssd_cols[::5])


# Selecting all other column names:

# In[ ]:


bhc_cols = [x for x in df if not x.startswith('RSSD') and not x.startswith('TEXT')]
print(len(bhc_cols))
print()
print(bhc_cols[::100])


# Extracting the numbers from the RSSD variable codes ending with '9', then convert them in to integers:

# In[ ]:


[int(x[-4:]) for x in rssd_cols if x.endswith('9')]


# ---
# #### My first **dictionary**: `weekday`
# 
# Dictionaries are the Python equivalent of `=vlookup()` in Excel, but much more versatile of course!

# In[ ]:


weekday = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

weekday["Thu"]


# Deleting a key-value pair, I don't like Mondays:

# In[ ]:


del weekday['Mon']
weekday


# Adding a key-value pair:

# In[ ]:


weekday['Mon'] = 0
weekday


# Check before adding

# In[ ]:


if "Sun" in weekday:
    print("Sunday is definitively there!")
else:
    print("Sunday is missing.")


# Alternatively, using `.keys()`

# In[ ]:


someday = 'Sun'
if someday in weekday.keys():
    print(f"{someday}day is definitively there!")
else:
    print(f"{someday}day is missing :-(")


# Likewise, using `.values()`

# Check if a value is present in the dictionary:

# In[ ]:


somedaynum = 1
if somedaynum in weekday.values():
    print(f"{str(somedaynum)} is definitively there!")  # convert somedaynum to a string first, using str()
else:
    print(f"{str(somedaynum)} is missing :-(")  # convert somedaynum to a string first, using str()


# ---
# Iterating over a dictionary:

# In[ ]:


for key, value in weekday.items():
    print('Key:', key, '- Value:', value)


# More efficient is this:

# In[ ]:


[key for key, value in weekday.items()]  # keys


# In[ ]:


[value for key, value in weekday.items()]  # values


# In[ ]:


[key for key, value in weekday.items() if value == 3]  # select a key-value pair


# Dictionary comprehension - create a new dictionary from an existing one:

# In[ ]:


{key:value+1 for (key, value) in weekday.items()}


# Flipping keys and values of a dictionary:

# In[ ]:


dayweek = {value: key for key, value in weekday.items()}
dayweek


# In[ ]:


dayweek[0]


# Obtain values using `.get()`. This does not give an error if a key is missing. Instead it returns 'None' or a variable of choice:

# In[ ]:


print(weekday.get('Sun'))
print(weekday.get('Sin'))
print(weekday.get('Sin', "The key doesn't exist"))


# ---
# Create a dictionary from two lists:

# In[ ]:


print(month_num)
print(months)


# In[ ]:


monts_dict = dict(zip(month_num, months))
monts_dict


# ---
# We can apply this to our dataframe to generate lables for the variable columns.
# 
# The labels are from the  Micro Data Reference Manual [MDRM](https://www.federalreserve.gov/apps/mdrm/).

# In[ ]:


list(df)[::200] # these are the variable names in the data frame, way too many, so I list every 200-th item:


# We want the names of some of the items in the data frame:

# In[ ]:


var =    ['RSSD9001', 'RSSD9999',       'BHCK2170',     'BHCK3210']
labels = ['ID RSSD',  'Reporting date', 'Total Assets', "Total Equity Capital"]


# In[ ]:


df[var].head(10)


# The dictionary:

# In[ ]:


bhc_dict = dict(zip(var, labels))
bhc_dict


# ---
# We can now export these four variables to Stata, including the lables.

# In[ ]:


df[var].to_stata('my_first_stata_output.dta', write_index=False, version=114, variable_labels=bhc_dict)

