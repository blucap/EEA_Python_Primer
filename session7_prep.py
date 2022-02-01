#!/usr/bin/env python
# coding: utf-8

# # Session 7: Analyze financial data, handle data with different year-ends.

# ## [EAA - ARC Python Primer for Accounting Research](https://martien.netlify.app/book/example/)

# ### Preparation ###
# 
# 
# **Complete the cells below so that by the start of the Thursday session you have an understanding of munging data for accounting research**
# 
# ---
# 
# #### Introduction - preparation
# ---
# 
# The cells below demonstrate how use Use Pandas to analyze financial data, handle data with different year-ends, etc.
# 
# By the end of this session you are able to craft your own panel data set for accounting research.
# 
# #### Price data 
# 
# You will download prices of us Bank Holding Companies using the [**yfinance**](https://pypi.org/project/yfinance/) module. To install this module using Anacondo prompt, run `pip install yfinance`.
# 
# #### Accounting data 
# 
# You will also use the bank holding company data used in the [first assignment](https://github.com/blucap/EEA_Python_Primer/blob/master/assignment_1_solutions.ipynb). 
# 
# For this Session you need to:  
# 
# - **Download the BHC data** for [2019](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2019),  [2020](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2020), and  [2021](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2021). 
# - **Save** the files to a folder on your drive, e.g. `D:/users/my_user_name_here/EAA_python/code/`. The files are zip- compressed (`BHCF20200331.ZIP`, ...,  `BHCF20211231.ZIP`) - **but there is no need to extract the contents of the zip files**. Pandas will do that for you.
# - Save the file `ticker_rssd.csv` (see [GitHub](https://github.com/blucap/EEA_Python_Primer)) to the same folder.
# 
# Run the cells below after setting the correct source folder of your files, i.e. replace `my_user_name_here` with something that works on your machine. See this [link](https://www.youtube.com/watch?v=hUW5MEKDtMM) and this [link](https://www.youtube.com/watch?v=7ABkcHLdG_A) for explanations of folders and directories.
# 
# Learning objectives:
# 
# - Obtaining price data from Yahoo, 
# - Determining cumulative returns for a sample of Bank Holding Companies,
# - Learning about time series for different year-ends, quarter-ends,
# - Creating a data frame of cumulative returns that we will merge with accounting data of Bank Holding Companies,
# - Preparing data from Bank Holding Companies for analysis
# - Creating lagged data
# - Creating row-differences
# - Merging accouting and price data
# 

# ---
# 
# **Let's start!**

# In[ ]:


# the familiar preamble
import pandas as pd
import numpy as np

# For this session
import glob # for iterating through a folder
import os # To set our working folder
from pandas.tseries.offsets import MonthEnd # To set dates to the end of the month
import yfinance as yf  # This gets us prices from Yahoo finance. See https://pypi.org/project/yfinance/

if os.name=='nt':  # for Windows users
    os.chdir('D:/users/my_user_name_here/EAA_python/data/')  # note the forward slashes, change 'martien' to your user name
else:
    os.chdir('/home/martien/EAA_python/data/')  # For Linux or Mac


# ---
# ### Loading price data for U.S. banks using yfinance ###
# 
# For this course, I decided to rely on publicly available data only. So, for price data I rely on [yfinance](https://pypi.org/project/yfinance/) instead of WRDS-CRSP. 
# 
# The price data allows me to show some powerful pandas functions, such as determining cumulative returns and finding prices at the end of quarter. 
# 
# The [yfinance](https://pypi.org/project/yfinance/) module returns a data frame with financials for a single firm, or for a list of firms. With the bank holding company data available for the years 2019-2021, we will only load price data for these years.
# 
# The cells below retrieve that data for a long list of bank tickers (`bank_list`) that I compiled for you. 

# In[ ]:


bank_list = ['AAIC', 'ABCB', 'ABCW', 'ABTX', 'ACBI', 'ACFC', 'ACNB', 'AF', 'AI', 'AIG', 'ALTA', 'AMNB', 'AMP', 'AMRB', 'AMTBB', 'ANCB', 'ANCX', 'AROW', 'ASB', 'ASBB', 'ASBI', 'ASRV', 'ATLO', 'AUB', 'AUBN', 'AVNU', 'AX', 'BAC', 'BANC', 'BANF', 'BANR', 'BBCN', 'BBT', 'BCBP', 'BDGE', 'BEN', 'BFIN', 'BFST', 'BHB', 'BHBK', 'BHLB', 'BK', 'BKJ', 'BKMU', 'BKSC', 'BKU', 'BLMT', 'BMRC', 'BMTC', 'BNCL', 'BNCN', 'BNK', 'BOCH', 'BOFI', 'BOH', 'BOKF', 'BPFH', 'BPOP', 'BRKL', 'BSRR', 'BSVN', 'BUSE', 'BWB', 'BWFG', 'BXS', 'BY', 'BYBK', 'BYLK', 'C', 'CAC', 'CACB', 'CADE', 'CARO', 'CARV', 'CASH', 'CASS', 'CATC', 'CATY', 'CBAN', 'CBF', 'CBFV', 'CBNJ', 'CBNK', 'CBSH', 'CBTX', 'CBU', 'CCBG', 'CCNE', 'CFB', 'CFCB', 'CFFI', 'CFFN', 'CFG', 'CFNB', 'CFNL', 'CFR', 'CHCO', 'CHEV', 'CHFC', 'CHFN', 'CHMG', 'CIT', 'CIVB', 'CIZN', 'CLBH', 'CLBK', 'CMA', 'CNBKA', 'CNOB', 'COB', 'COBZ', 'COF', 'COLB', 'CPF', 'CSBK', 'CSFL', 'CSTR', 'CTBI', 'CUBI', 'CUBN', 'CUNB', 'CVBF', 'CVCY', 'CVLY', 'CWBC', 'CZNC', 'CZWI', 'DCOM', 'DFS', 'DNBF', 'EBMT', 'EBSB', 'EBTC', 'EFSC', 'EGBN', 'EMCF', 'ENFC', 'EQBK', 'ESSA', 'ESXB', 'ETFC', 'EVBN', 'EVBS', 'EVER', 'EWBC', 'FAF', 'FBC', 'FBIZ', 'FBK', 'FBMS', 'FBNC', 'FBNK', 'FBP', 'FBSS', 'FCB', 'FCBC', 'FCCO', 'FCCY', 'FCF', 'FCFP', 'FCLF', 'FCNCA', 'FCVA', 'FDEF', 'FFBC', 'FFIC', 'FFIN', 'FFKT', 'FFNW', 'FFWM', 'FGBI', 'FHN', 'FIBK', 'FISI', 'FITB', 'FLIC', 'FMAO', 'FMBH', 'FMBI', 'FMD', 'FMER', 'FMNB', 'FNB', 'FNBC', 'FNBG', 'FNCB', 'FNFG', 'FNLC', 'FNWB', 'FRBK', 'FRME', 'FSB', 'FSBK', 'FSFG', 'FULT', 'FUNC', 'FUSB', 'FXCB', 'GABC', 'GBCI', 'GBNK', 'GFED', 'GLBZ', 'GNBC', 'GNTY', 'GSBC', 'GWB', 'HAFC', 'HBAN', 'HBCP', 'HBHC', 'HBMD', 'HBNC', 'HBT', 'HEOP', 'HFBC', 'HFFC', 'HFWA', 'HMNF', 'HMPR', 'HMST', 'HOMB', 'HONE', 'HOPE', 'HTBI', 'HTBK', 'HTH', 'HTLF', 'HWBK', 'HWC', 'IBCP', 'IBKC', 'IBOC', 'IBTX', 'ICBK', 'INBK', 'INDB', 'IROQ', 'ISBC', 'ISTR', 'JAXB', 'JPM', 'JXSB', 'KEY', 'KRNY', 'LARK', 'LBAI', 'LCNB', 'LEVL', 'LION', 'LKFN', 'LMST', 'LOB', 'LSBG', 'LTXB', 'MBCN', 'MBFI', 'MBIN', 'MBNAB', 'MBRG', 'MBTF', 'MBVT', 'MBWM', 'MCBC', 'METR', 'MFNC', 'MFSF', 'MGYR', 'MLVF', 'MNRK', 'MOFG', 'MPB', 'MRLN', 'MSBI', 'MSFG', 'MSL', 'MTB', 'MVBF', 'MYFW', 'NBBC', 'NBHC', 'NBN', 'NBTB', 'NCBS', 'NCOM', 'NFBK', 'NKSH', 'NPBC', 'NRIM', 'NTRS', 'NVSL', 'NWBI', 'NWFL', 'NYCB', 'OBNK', 'OCFC', 'OFG', 'OKSB', 'OLBK', 'ONB', 'OPHC', 'OPOF', 'ORIT', 'ORRF', 'OSBC', 'OSHC', 'OVBC', 'OVLY', 'OZK', 'OZRK', 'PACW', 'PB', 'PBCT', 'PBHC', 'PBIB', 'PBIP', 'PBNC', 'PCBK', 'PCSB', 'PEBK', 'PEBO', 'PFBI', 'PFBX', 'PFC', 'PFG', 'PFIS', 'PFS', 'PGC', 'PKBK', 'PLBC', 'PMBC', 'PNBK', 'PNC', 'PNFP', 'PPBI', 'PRK', 'PROV', 'PSTB', 'PUB', 'PULB', 'PVBC', 'PVTB', 'PWOD', 'QCRH', 'RBB', 'RBCAA', 'RBNC', 'RBPAA', 'RF', 'RJF', 'RNST', 'RRBI', 'RVSB', 'SAL', 'SASR', 'SBBX', 'SBCF', 'SBFG', 'SBSI', 'SBT', 'SCHW', 'SCNB', 'SEIC', 'SF', 'SFBS', 'SFNC', 'SFST', 'SGB', 'SHBI', 'SIFI', 'SIVB', 'SLCT', 'SMBC', 'SMBK', 'SMMF', 'SNBC', 'SNV', 'SOCB', 'SONA', 'SPFI', 'SRCE', 'SSB', 'SSFN', 'STBA', 'STBZ', 'STI', 'STL', 'STT', 'SVBI', 'SYBT', 'SYF', 'TBBK', 'TBK', 'TBNK', 'TCB', 'TCBI', 'TCBK', 'TCF', 'TCFC', 'TFC', 'THFF', 'TLMR', 'TMP', 'TRCB', 'TRMK', 'TROW', 'TRST', 'TSBK', 'TSC', 'UBCP', 'UBFO', 'UBNK', 'UBOH', 'UBSH', 'UBSI', 'UCBA', 'UCBI', 'UCFC', 'UMBF', 'UMPQ', 'UNB', 'UNTY', 'USB', 'USBI', 'UVSP', 'VBFC', 'VBTX', 'VLY', 'WABC', 'WAFD', 'WAL', 'WASH', 'WBB', 'WBS', 'WFBI', 'WFC', 'WFD', 'WIBC', 'WNEB', 'WSBC', 'WSBF', 'WSFS', 'WTBA', 'WTFC', 'WVFC', 'XBKS', 'YCB', 'YDKN', 'ZION']
print('Banks :', len(bank_list))


# In[ ]:


dfy = yf.download(bank_list, start='2019-01-01', end='2021-12-31', progress=True)


# **Note that `dfy` has a multi-index set of columns**
# 
# This is a great feature of Pandas: it allows us to select a set of columns in one go.

# In[ ]:


dfy.head()


# We only need `Adj Close`:

# In[ ]:


df_close = dfy['Adj Close'].copy()
df_close.head(5)


# **Note that there are many empty columns**
# 
# Let's delete columns without any price value using `dropna` and `axis=1` for columns, instead of the default `axis=0`.

# In[ ]:


df_close.shape


# In[ ]:


df_close.dropna(axis=1, inplace=True, how='all')
df_close.shape


# In[ ]:


df_close.head(5)


# In[ ]:


df_close.tail(5)


# **Observations**
# 
# - The data looks fine, but the shape of the data should change: tickers and dates should be the index
# - Using the date variable we can create variables that are based on the date, one for the year, one for the quarter number [1,2,3,4], and one for the quarter '2021Q1'. These variables facilitate grouping.
# - The main date variable should be named `datadate`.
# - The price variable should be renamed to `prc`.
# 
# To reshape the data frame we use `melt`, see [Session 6](https://martien.netlify.app/slides/session6/). 

# In[ ]:


# Melt
dfm = pd.melt(df_close.reset_index(), id_vars=['Date'], var_name='ticker', value_name='prc')
dfm.dropna(inplace=True)
dfm.rename(columns = {'Date': 'datadate'} , inplace=True)
dfm.head()


# In[ ]:


# Adding additional date variables using datadate 

dfm['year']       = dfm.datadate.dt.year
dfm['quarter_no'] = dfm.datadate.dt.quarter
dfm['quarter']    = pd.PeriodIndex(dfm.datadate, freq='Q')  # See https://stackoverflow.com/questions/50459301/how-to-convert-dates-to-quarters-in-python

dfm.set_index(['ticker', 'datadate'], inplace=True)


# **Presto** we now have a properly designed *long* data frame that we can use for various analyses.

# In[ ]:


dfm.head(5)


# ---
# 
# **Cumulative returns**
# 
# In the absence of readily available dividend data we rely on price changes for determining returns. 
# 
# To determine price changes, use Pandas `pct_change` function.
# 
# Let's do that for Bank of America, with ticker `BAC`.

# In[ ]:


df_boa = dfm['prc'].loc['BAC'].pct_change()
df_boa.head()


# For the calculation of cumulative returns we should add one (1) to the price changes:

# In[ ]:


df_boa += 1
df_boa


# Use Pandas `cumprod` to determine the cumulative product of the price changes per day, then take away 1.

# In[ ]:


df_boa_cumret_all = df_boa.cumprod()-1


# In[ ]:


df_boa_cumret_all.plot(figsize=(10,6))


# Apparently BoA performed well!

# ---
# 
# **Resampling the data frequency to quarterly**
# 
# What if we are not interested in daily observations, but only in end-of quarter data?
# 
# Here again Pandas shows its strength, you can resample the data to a different frequency and tell pandas to `take` the last observation of each quarter.

# In[ ]:


df_boa_cumret_qtr = df_boa_cumret_all.resample('Q').last().fillna(0)
df_boa_cumret_qtr


# In[ ]:


df_boa_cumret_qtr.plot()


# **Note that the series above starts at a zero**, and then continues using that zero value as the base reference.
# 
# Alternatively, if you want the cumulative returns per quarter, use the **product** (not cumulative product) of the values:

# In[ ]:


df_boa_ret_qtr = df_boa.resample('Q').prod()-1  
df_boa_ret_qtr.plot(kind='bar')


# **Year-ends not December**
# 
# Pandas takes the approach shown above a step further by allowing you to set your own quarter/year-end. 
# 
# For example, if you want annual observations, you can specify the relevant year-end, be it December or April. See this Pandas [help-file](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)
# for a wealth of time-series features. 

# In[ ]:


# Annual - generic
df_boa_ret_ann = df_boa.resample('A').prod()-1  
df_boa_ret_ann.plot(kind='bar')


# In[ ]:


# Annual - December
df_boa_ret_ann = df_boa.resample('A-DEC').prod()-1  
df_boa_ret_ann.plot(kind='bar')


# In[ ]:


# Annual - April
df_boa_ret_ann = df_boa.resample('A-APR').prod()-1  
df_boa_ret_ann.plot(kind='bar')


# ---
# 
# **Applying the same logic for all banks**
# 
# We generally work with panel data. So, instead of lifting the data from a single firm, we should be able to apply the same approach to all banks in our data frame `dfm`. This involves the use of `groupby`, see also [Session 6](https://github.com/blucap/EEA_Python_Primer/blob/master/assignment_1_solutions.ipynb).
# 
# - Let's add a variable `dprc` to our main data frame `dfm`
# - Then get rid of rows without valid value change observations

# In[ ]:


dfm['dprc'] = dfm['prc'].groupby('ticker').pct_change() + 1
dfm['dprc'].head()


# In[ ]:


dfm.dropna(subset = ['dprc'], inplace=True)  
dfm['dprc'].head()


# **Presto!**
# 
# The next cells show how this approach works for three banks (Bank of America, Well Fargo, Citi). This instead of testing this for all banks.

# In[ ]:


# Obtain the price-change data (with 1 added) for Bank of America, Well Fargo, Citi:
df_3_bks = dfm['dprc'].loc[['BAC', 'WFC', 'C']]
df_3_bks


# In[ ]:


# Reshaping the melted data using unstack
df_3_bks = dfm['dprc'].loc[['BAC', 'WFC', 'C']].unstack()
df_3_bks


# In[ ]:


# Better to transpose (T) the frame and eliminate empty rows
df_3_bks = dfm['dprc'].loc[['BAC', 'WFC', 'C']].unstack().T.dropna(how = 'all')
df_3_bks


# In[ ]:


df_3_bks.cumprod().plot()


# ---
# 
# Likewise, if you want the cumulative returns per quarter:
# 
# - Create a group object which groups on `['ticker', 'quarter']`.
# - Calculate the cumulative returns per quarter using Pandas product function, then deduct 1.
# - If we want to: reshape the resulting frame and plot.

# In[ ]:


dfm_qtr_qp = dfm.groupby(['ticker', 'quarter'])
dfm_qtr_qp.head()


# In[ ]:


df_all_bks = dfm_qtr_qp['dprc'].prod() - 1
df_all_bks.head(5)


# In[ ]:


#Check for Bank of America
df_all_bks.loc['BAC']


# In[ ]:


df_all_bks[['BAC', 'WFC', 'C']].unstack()


# In[ ]:


df_all_bks[['BAC', 'WFC', 'C']].unstack().T.plot(kind = 'bar', figsize = (10,6))


# In[ ]:


# Note, `df_all_bks`is a Pandas **Series**. Best to convert it to a frame.

df_all_bks = df_all_bks.to_frame()


# In[ ]:


df_all_bks.tail(3)


# We now have a data frame with quarterly returns data that we can merge with the Bank Holding Company data.

# 
# ---
# ### Accounting data - Loading the Bank Holding Company Data  ###
# 
# We now will use the downloaded BHC data, see the top of this notebook, to prepare the accounting data.
# 
# The function below relies on [Assignment 1](https://github.com/blucap/EEA_Python_Primer/blob/master/assignment_1_solutions.ipynb). It sorts out the accounting data in one go.

# In[ ]:


def load_bhc_data():
    mdrm = {'RSSD9999': 'REPORTING DATE',
            'RSSD9001': 'Borrower RSSD ID',
            'RSSD9010': 'Entity Short Name',
            'BHCK3210': 'Total Equity Capital',
            'BHCK2170': 'Total Assets',
            'BHCK4340': 'Net Income'}
    var_list = [key for key, value in mdrm.items()]
    df = pd.DataFrame()
    for fname in glob.glob('BHCF*.ZIP'):
        print(fname)
        df = df.append(pd.read_csv(fname, sep='^', encoding="ISO-8859-1", low_memory=False))
    df = df[var_list]
    # Create a date variable that matches the price data panel.
    df['datadate'] = pd.to_datetime(df['RSSD9999'], format = '%Y%m%d')
    df.set_index(['RSSD9001' , 'datadate'], inplace=True)
    # Get rid of rows without the relevant accounting data:
    df.dropna(subset = [x for x in df if x.startswith('BHCK')], inplace=True)
    print(f'\nDone!\n\nTotal rows in data frame: {len(df)}')
    print(f'Total variables in data frame: {len(list(df))}\n')
    df.sort_index(inplace = True) # sort along the index
    return df, mdrm

df, mdrm = load_bhc_data()


# In[ ]:


df.head(3)


# In[ ]:


df.tail(3)


# ---
# #### Adding the ticker codes from file ####
# 
# The next cells 
# 
# - load a file from disk that allows you to link the bank ids `RSSD9001` to the `ticker` data,
# - join that data with data frame `df`. To perform this join, we should reset the index and set it to match on ticker and date,
# - eliminate rows without ticker,
# - and finally resets the index to its previous state, with index `['RSSD9001', 'datadate']`.

# In[ ]:


dft_r = pd.read_csv('ticker_rssd.csv').set_index(['RSSD9001'])


# In[ ]:


dft_r.head()


# In[ ]:


df = df.reset_index().set_index(['RSSD9001']).join(dft_r).dropna(subset=['ticker'])
df.head()


# In[ ]:


df = df.reset_index().set_index(['RSSD9001', 'datadate'])
df.head(3)


# We now have a neat data frame which we can use for panel data analysis.
# 
# However, sometimes we may want to use lagged data.
# 
# Unlike with Stata, which creates lagged data with ease, Pandas requires a bit more work. However, this is really doable.
# 
# ---
# 
# ### Lagging, leading, ... shifting  ###
# 
# The Pandas way of creating lagged data is by way of `shift`. This commands plays tricks with the index, which ideally should be a Datetime Index.
# 
# Let's try it for Bank of America (you guessed it right, I am an account holder of that bank).
# 

# In[ ]:


boa = df.loc[1073757] # Which leaves datadate as the index - clever!
boa.head(3)


# In[ ]:


# Check if the index is indeed a DatetimeIndex 
boa.info()


# Now do the shift:

# In[ ]:


boa.shift(3)


# The result is not entirely compelling. Yes, the data is shifted by three rows, but we end up with some empty cells. Moreover, this approach may lead to problems if we apply this to the entire frame, it may lead to data being shifted to rows that 'belong' to the wrong dates or banks.   
# 
# It is better to tell Pandas the proper offset, e.g. in months.

# In[ ]:


# Do the shift for three months 
boa.shift(3, freq = 'M')


# You can see that data from 20190930 (September) now has a timestamp of 2019-12-31 (December). 
# 
# This is great! We can use the shifted data and join it with the main data frame. The resulting data frame will have a set of lagged variables.
# 
# **Now let's apply this for the entire dataframe:**

# **Step 1**: make sure we set the proper (Datetime) Index

# In[ ]:


df = df.reset_index().set_index(['datadate'])
df.head(3)


# **Step 2**: group by bank (`RSSD9001`) and apply `shift` to the accounting variables only: Equity, Total Assets, Net Income (`BHCK3210`, `BHCK2170`, `BHCK4340`). 
# 
# Assign the result to a data frame `df_lag`.

# In[ ]:


df_lag = df.groupby(['RSSD9001'])[['BHCK3210', 'BHCK2170', 'BHCK4340']].shift(3, freq = 'M')
df_lag.head()


# In[ ]:


# Compare to
df[['BHCK3210', 'BHCK2170', 'BHCK4340']].head()


# **Step 3**: join both frames, and use `_lag` as a suffix, to properly name the variables.
# 
# But first reset the index of the main data frame to `['RSSD9001', 'datadate']`. Else we cannot join on the two dimensions.
#     

# In[ ]:


df = df.reset_index().set_index(['RSSD9001', 'datadate'])
dfj = df.join(df_lag, rsuffix='_lag')
dfj.head()


# ---
# #### Consolidating the process of shifting in a few rows:
# 
# The cell below summarizes the process of loading that, adding the tickers, and shifting in a few lines:

# In[ ]:


# Prepare the main data
# Load the data
df, mdrm = load_bhc_data()
# Load the tickers
dft_r = pd.read_csv('ticker_rssd.csv').set_index(['RSSD9001'])
# join the tickers
df = df.reset_index().set_index(['RSSD9001']).join(dft_r).dropna(subset=['ticker'])
# set the index
df = df.reset_index().set_index(['RSSD9001', 'datadate'])

# Do the shift - create and add lagged variables
df_lag = df.reset_index().set_index(['datadate']).groupby(['RSSD9001'])[['BHCK3210', 'BHCK2170', 'BHCK4340']].shift(3, freq = 'M')

dfj = df.join(df_lag, rsuffix='_lag')


# In[ ]:


len(dfj)


# In[ ]:


dfj.head(8)


# ---
# #### Create a Return on Equity variable ####
# 
# With the data frame in good shape we can calculate a column for Return on Equity, which uses the average equity value as denominator (`mu_equity`):
# 

# In[ ]:


dfj['mu_equity'] = dfj[['BHCK3210', 'BHCK3210_lag']].mean(axis=1, skipna=False)

dfj['roe']  = dfj['BHCK4340'] / dfj['mu_equity']

roe = dfj['roe'].groupby('datadate').mean()
roe


# In[ ]:


roe.plot(kind= 'bar')


# In[ ]:


roe.resample('A-DEC').last().plot(kind = 'bar')


# In[ ]:


roe.resample('A-MAR').last().plot(kind = 'bar')


# ---
# 
# Note that the ROE data cumulates over the year, thus not showing the true quarterly data.
# 
# We can solve this by 
# 
# - taking the difference in net income `BHCK4340` per year, bank. Then store the differences in a separate data frame (`dfo`), in a separate column `BHCK4340_q`;
# - join that data frame with the main frame (`dfj`);
# - then add the first quarter values of `BHCK4340` to `BHCK4340_q`
# - then create a new `roe` column.
# 
# To make this work we first need some new columns in `dfj`: `year`, and `quarter_no`.
# 
# 

# In[ ]:


# Add `year`, and `quarter_no` to dfj
dfj.reset_index(inplace=True)
dfj['year'] = dfj.datadate.dt.year
dfj['quarter_no'] = dfj.datadate.dt.quarter
dfj['quarter'] = pd.PeriodIndex(dfj['datadate'], freq='Q') # Let's do this one as well 
dfj.set_index(['RSSD9001', 'datadate'], inplace = True)


# In[ ]:


dfj.tail(8)


# In[ ]:


# using diff to create first differences by bank and year
dfo = dfj.groupby(['RSSD9010', 'year'])['BHCK4340'].diff(1).to_frame()
dfo


# In[ ]:


# Join dfo with dfj
dfj = dfj.join(dfo, rsuffix='_q')


# In[ ]:


dfj.head(8)


# In[ ]:


# For first quarter rows, copy the values from BHCK4340 to BHCK4340_q
dfj.loc[dfj["quarter_no"]==1,'BHCK4340_q'] = dfj.loc[dfj["quarter_no"]==1,'BHCK4340'] 
dfj


# In[ ]:


dfj['roe_improved'] = dfj['BHCK4340_q'] / dfj['mu_equity']
dfj['roe_improved']


# In[ ]:


roe_mark2 = dfj['roe_improved']
roe_mark2.groupby('datadate').mean().dropna().plot(kind='bar')


# ---
# ### Merging price and accounting data 
# 
# In the last step of this Session merges the `dfj` frame with accounting data with the price data file `df_all_bks`.
# 
# To make this work, we need to reset  the index of `dfj` to `['ticker', 'quarter']`.

# In[ ]:


dfj = dfj.reset_index().set_index(['ticker', 'quarter'])


# In[ ]:


df_all_bks.head(3)


# In[ ]:


dfj.head(3)


# In[ ]:


dfj = dfj.join(df_all_bks)


# In[ ]:


dfj

