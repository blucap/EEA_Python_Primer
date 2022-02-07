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
# The libraries allow you to easily formulate you regression models, and conveniently select the results from the regression output. You can select coefficients and *t*-stats, or *p*-values, add them to a data frame (i.e. a table), and export that data frame to LaTeX, markdown, or cvs / Excel format.
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
# ### Part 1: Regression analysis ###
# 
# We use the U.S. Bank Holding Company as described from [Session 7](https://martien.netlify.app/slides/session7/).
# 
# #### Introduction - preparation
# 
# **Price data**
# 
# You will download prices of us Bank Holding Companies using the [**yfinance**](https://pypi.org/project/yfinance/) module. To install this module using Anaconda prompt, run `pip install yfinance`.
# 
# **Accounting data**
# 
# You will also use the bank holding company data used in the [first assignment](https://github.com/blucap/EEA_Python_Primer/blob/master/assignment_1_solutions.ipynb). 
# 
# For this Session you need to:  
# 
# - **Download the BHC data** for [2019](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2019),  [2020](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2020), and  [2021](https://www.ffiec.gov/npw/FinancialReport/FinancialDataDownload?selectedyear=2021). 
# - **Save** the files to a folder on your drive, e.g. `D:/users/my_user_name_here/EAA_python/code/`. The files are zip- compressed (`BHCF20200331.ZIP`, ...,  `BHCF20211231.ZIP`) - **but there is no need to extract the contents of the zip files**. Pandas will do that for you.
# - **Save** the file `ticker_rssd.csv` (see [GitHub](https://github.com/blucap/EEA_Python_Primer)) to the same folder.
# 
# Run the cells below after setting the correct source folder of your files, i.e. replace `my_user_name_here` with something that works on your machine. See this [link](https://www.youtube.com/watch?v=hUW5MEKDtMM) and this [link](https://www.youtube.com/watch?v=7ABkcHLdG_A) for explanations of folders and directories.
# 
# 

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
    os.chdir('/home/EAA_python/data/')  # For Linux or Mac


# ---
# 
# **Step 1a**: Create accounting data

# In[ ]:


def load_bhc_data():
    mdrm = {'RSSD9999': 'ReportingDate',
            'RSSD9001': 'ID',
            'RSSD9010': 'Name',
            'BHCK3210': 'Equity',
            'BHCK2170': 'TotalAssets',
            'BHCK4340': 'NetIncome'}
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
    df.sort_index(inplace = True) # sort along the index
    # read tickers
    dft_r = pd.read_csv('ticker_rssd.csv').set_index(['RSSD9001'])
    # join the tickers
    df = df.reset_index().set_index(['RSSD9001']).join(dft_r).dropna(subset=['ticker'])
    # set the index
    df = df.reset_index().set_index(['RSSD9001', 'datadate'])
    # Do the shift - create and add lagged variables
    df_lag = df.reset_index().set_index(['datadate']).groupby(['RSSD9001'])[['BHCK3210', 'BHCK2170', 'BHCK4340']].shift(3, freq = 'M')
    # Join lagged variables
    dfj = df.join(df_lag, rsuffix='_lag')
    
    # Add date variables to dfj
    dfj.reset_index(inplace=True)
    dfj['year'] = dfj.datadate.dt.year
    dfj['quarter_no'] = dfj.datadate.dt.quarter
    dfj['quarter'] = pd.PeriodIndex(dfj['datadate'], freq='Q') # Let's do this one as well 
    dfj.set_index(['RSSD9001', 'datadate'], inplace = True)
    
    dfo = dfj.groupby(['RSSD9010', 'year'])['BHCK4340'].diff(1).to_frame()
    dfj = dfj.join(dfo, rsuffix='_q')
    
    # For first quarter rows, copy the values from BHCK4340 to BHCK4340_q
    dfj.loc[dfj["quarter_no"]==1,'BHCK4340_q'] = dfj.loc[dfj["quarter_no"]==1,'BHCK4340'] 
    dfj['mu_equity'] = dfj[['BHCK3210', 'BHCK3210_lag']].mean(axis=1, skipna=False)
    dfj['roe'] = dfj['BHCK4340_q'] / dfj['mu_equity']
            
    print(f'\nDone!\n\nTotal rows in data frame: {len(dfj)}')
    print(f'Total variables in data frame: {len(list(dfj))}\n')
    
    return dfj, mdrm

# Prepare the main data
# Load the data
df, mdrm = load_bhc_data()


# In[ ]:


df.head(3)


# ---
# 
# **Step 1b**: Get returns data from Yahoo

# In[ ]:


import yfinance as yf
bank_list = ['AAIC', 'ABCB', 'ABTX', 'ACBI', 'ACNB', 'AI', 'AIG', 'AMNB', 'AMP', 'ANCX', 'AROW', 'ASB', 'ASRV', 'ATLO', 'AUB', 'AUBN', 'AX', 'BAC', 'BANC', 'BANF', 'BANR', 'BCBP', 'BEN', 'BFIN', 'BFST', 'BHB', 'BHLB', 'BK', 'BKSC', 'BKU', 'BMRC', 'BMTC', 'BOH', 'BOKF', 'BPOP', 'BRKL', 'BSRR', 'BSVN', 'BUSE', 'BWB', 'BWFG', 'BY', 'C', 'CAC', 'CADE', 'CARV', 'CASH', 'CASS', 'CATC', 'CATY', 'CBAN', 'CBFV', 'CBNK', 'CBSH', 'CBTX', 'CBU', 'CCBG', 'CCNE', 'CFB', 'CFFI', 'CFFN', 'CFG', 'CFNB', 'CFR', 'CHCO', 'CHMG', 'CIT', 'CIVB', 'CIZN', 'CLBK', 'CMA', 'CNOB', 'COF', 'COLB', 'CPF', 'CSTR', 'CTBI', 'CUBI', 'CVBF', 'CVCY', 'CVLY', 'CWBC', 'CZNC', 'CZWI', 'DCOM', 'DFS', 'EBMT', 'EBTC', 'EFSC', 'EGBN', 'EMCF', 'EQBK', 'ESSA', 'EVBN', 'EVER', 'EWBC', 'FAF', 'FBC', 'FBIZ', 'FBK', 'FBMS', 'FBNC', 'FBP', 'FCB', 'FCBC', 'FCCO', 'FCCY', 'FCF', 'FCNCA', 'FFBC', 'FFIC', 'FFIN', 'FFNW', 'FFWM', 'FGBI', 'FHN', 'FIBK', 'FISI', 'FITB', 'FLIC', 'FMAO', 'FMBH', 'FMBI', 'FMNB', 'FNB', 'FNCB', 'FNLC', 'FNWB', 'FRBK', 'FRME', 'FSFG', 'FULT', 'FUNC', 'FUSB', 'GABC', 'GBCI', 'GBNK', 'GFED', 'GLBZ', 'GNBC', 'GNTY', 'GSBC', 'GWB', 'HAFC', 'HBAN', 'HBCP', 'HBMD', 'HBNC', 'HBT', 'HFWA', 'HMNF', 'HMST', 'HOMB', 'HONE', 'HOPE', 'HTBI', 'HTBK', 'HTH', 'HTLF', 'HWBK', 'HWC', 'IBCP', 'IBOC', 'IBTX', 'INBK', 'INDB', 'IROQ', 'ISBC', 'ISTR', 'JPM', 'KEY', 'KRNY', 'LARK', 'LBAI', 'LCNB', 'LEVL', 'LION', 'LKFN', 'LMST', 'LOB', 'MBCN', 'MBIN', 'MBWM', 'MCBC', 'MGYR', 'MLVF', 'MOFG', 'MPB', 'MRLN', 'MSBI', 'MTB', 'MVBF', 'MYFW', 'NBHC', 'NBN', 'NBTB', 'NCBS', 'NFBK', 'NKSH', 'NRIM', 'NTRS', 'NWBI', 'NWFL', 'NYCB', 'OBNK', 'OCFC', 'OFG', 'ONB', 'OPHC', 'OPOF', 'ORRF', 'OSBC', 'OVBC', 'OVLY', 'OZK', 'PACW', 'PB', 'PBCT', 'PBHC', 'PBIP', 'PBNC', 'PCSB', 'PEBK', 'PEBO', 'PFBX', 'PFC', 'PFG', 'PFIS', 'PFS', 'PGC', 'PKBK', 'PLBC', 'PNBK', 'PNC', 'PNFP', 'PPBI', 'PRK', 'PROV', 'PVBC', 'PWOD', 'QCRH', 'RBB', 'RBCAA', 'RBNC', 'RF', 'RJF', 'RNST', 'RRBI', 'RVSB', 'SAL', 'SASR', 'SBCF', 'SBFG', 'SBSI', 'SBT', 'SCHW', 'SEIC', 'SF', 'SFBS', 'SFNC', 'SFST', 'SHBI', 'SIFI', 'SIVB', 'SMBC', 'SMBK', 'SMMF', 'SNV', 'SPFI', 'SRCE', 'SSB', 'STBA', 'STBZ', 'STL', 'STT', 'SYBT', 'SYF', 'TBBK', 'TBK', 'TBNK', 'TCBI', 'TCBK', 'TCFC', 'TFC', 'THFF', 'TMP', 'TRMK', 'TROW', 'TRST', 'TSBK', 'TSC', 'UBCP', 'UBFO', 'UBOH', 'UBSI', 'UCBI', 'UMBF', 'UMPQ', 'UNB', 'UNTY', 'USB', 'UVSP', 'VBFC', 'VBTX', 'VLY', 'WABC', 'WAFD', 'WAL', 'WASH', 'WBS', 'WFC', 'WNEB', 'WSBC', 'WSBF', 'WSFS', 'WTBA', 'WTFC', 'WVFC', 'ZION']
dfy = yf.download(bank_list, start='2019-01-01', end='2021-12-31', progress=True)
dfy.dropna(axis = 1, inplace=True, how= 'all')
df_close = dfy['Adj Close']

dfm = pd.melt(df_close.reset_index(), id_vars=['Date'], var_name='ticker', value_name='prc')
dfm.dropna(inplace=True)
dfm.rename(columns = {'Date': 'datadate'} , inplace=True)

dfm['year']       = dfm.datadate.dt.year
dfm['quarter_no'] = dfm.datadate.dt.quarter
dfm['quarter']    = pd.PeriodIndex(dfm.datadate, freq='Q')  # See https://stackoverflow.com/questions/50459301/how-to-convert-dates-to-quarters-in-python

dfm.set_index(['ticker', 'datadate'], inplace=True)

dfm['dprc'] = dfm['prc'].groupby('ticker').pct_change() + 1
dfm.dropna(subset = ['dprc'], inplace=True)  # Get rid of the row witout valied value change

dfm_qtr_qp = dfm.groupby(['ticker', 'quarter'])

df_all_bks = dfm_qtr_qp['dprc'].prod() - 1
df_all_bks.head(3)


# ---
# 
# **Step 1c**: Merge the accounting and price data, rename some columns:

# In[ ]:


df = df.reset_index().set_index(['ticker', 'quarter'])
df = df.join(df_all_bks)
mdrm['dprc'] = 'Returns'
mdrm['roe'] = 'ROE'
mdrm['BHCK4340_q'] = 'NetIncomeQ'
df.rename(columns = mdrm, inplace=True)


# In[ ]:


df.head(3)


# ---
# 
# **Step 2: Descriptive statistics**
# 
# In this step we create tables that describe the data. The tables are data frames that can be exported to Excel, csv, LaTeX, markdown format. 
# 
# For the descriptives we first select the non-ratio columns:

# In[ ]:


varlist = ['NetIncomeQ','TotalAssets','Equity']


# In[ ]:


df[varlist].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T


# **Turning the line above in a pretty table**:

# In[ ]:


def table1(df, varlist, k, fmt):
    table = df[varlist].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T
    table = table * k
    table = table[['mean', 'min', '5%', '25%', '50%', '75%', '95%', 'max', 'std', 'count']]
    if fmt:
        table = table.applymap("{0:,.2f}".format)
    return(table)
Tabel1a = table1(df, varlist, 0.001, True)
Tabel1a


# **Likewise, for the ratios**:

# In[ ]:


Tabel1b = table1(df, ['ROE', 'Returns'], 100, True)
Tabel1b


# In[ ]:


Tabel1a.append(Tabel1a)


# In[ ]:


def table2(df, varlist, fmt=False, freq = "year"):
    years = df.groupby(freq)
    table = years[varlist].mean() * 0.001
    if fmt:
        table = table.applymap("{0:,.2f}".format)
    table = table.join(years['TotalAssets'].count().to_frame(name='nobs'))
    table = table[varlist + ['nobs']]
    return(table)

Tabel2 = table2(df, varlist, True)
print('\nMarkdown:\n')
print(Tabel2.to_markdown())  
print('\nLatex:\n')
print(Tabel2.to_latex())  


# ---
# 
# **Step 3a: Regressions using statsmodels**
# 
# Basic regressions can be done with [statsmodels](https://www.statsmodels.org/stable/install.html).
# 
# If not installed yet, install via:
# 
# - `conda install -c conda-forge statsmodels` or 
# - `pip install statsmodels`
# 
# The cells below show the results of a regression of `Returns` on `ROE`. I add a constant using `sm.add_constant` and  year dummies using [`pd.get_dummies`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html).

# In[ ]:


import statsmodels.api as sm

data = df[['Returns', 'ROE']].join(pd.get_dummies(df['year'], prefix='year', drop_first=True)).dropna()

data = sm.add_constant(data)

x = data.loc[:,[x for x in data if x!='Returns']]

y = data['Returns']

res = sm.OLS(y, x).fit()
print(res.summary())


# In[ ]:


# The coefficients:
res.params


# The function below creates a table from the regression results:

# In[ ]:


def reg_result(res, fmt):
    result = pd.DataFrame(res.params).transpose()
    result['rsq'] = res.rsquared_adj
    result['nobs'] = res.nobs
    trow = pd.DataFrame(res.tvalues).transpose()
    result = result.append(trow, sort=False)
    prow = pd.DataFrame(res.pvalues).transpose()
    result = result.append(prow, sort=False)
    result.index = ['b', 't', 'p']
    if fmt:
        result = result.applymap("{0:,.2f}".format)
    return result.T
Table3 = reg_result(res, True)
Table3


# ---
# 
# **Using R-style formulas**
# 
# For convenience there is a library (`statsmodels.formula.api `) that allows you to use R-style model specifications:

# In[ ]:


import statsmodels.formula.api as smf


# In[ ]:


data = df[['Returns', 'ROE']].join(pd.get_dummies(df['year'], prefix='Y', drop_first=True)).dropna()

mod = smf.ols(formula='Returns ~ ROE + Y_2020 + Y_2021', data=data)

res = mod.fit() 

# res = mod.fit(cov_type="hc1") # https://cran.r-project.org/web/packages/sandwich/vignettes/sandwich.pdf

print(res.summary())


# ---
# 
# **Step 3b: Regressions using linearmodels**
# 
# Linearmodels complements statsmodels regarding the estimation and inference in some common linear models that are missing from said library. 
# 
# - See the  linearmodels web-page [here](https://bashtage.github.io/linearmodels/#).
# - Install using `pip install linearmodels`, see [this page](https://pypi.org/project/linearmodels/).

# In[ ]:


from linearmodels.panel import PanelOLS
from linearmodels.panel import PooledOLS
from linearmodels.panel import RandomEffects
from linearmodels.panel import compare


# Note that linearmodels will use the index, but the time-index needs to be a DateTime column. Currently it is a Period column, so we should make some adjustments.

# In[ ]:


data = df[['Returns', 'ROE', 'datadate', 'ID']].reset_index().set_index(['ID', 'datadate']).dropna()


# We can now run panel data regressions:

# In[ ]:


# Pooled OLS
mod = PooledOLS.from_formula("Returns ~ 1 + ROE", data=data)
pooled_res = mod.fit(cov_type="clustered")
print(pooled_res)


# In[ ]:


# Random Effects
mod = RandomEffects.from_formula("Returns ~ 1 + ROE", data=data)
re_res = mod.fit(cov_type="clustered")
print(re_res)


# In[ ]:


# Fixed Effects
mod = PanelOLS.from_formula("Returns ~ 1 + ROE + EntityEffects + TimeEffects", data=data)
fe_res = mod.fit(cov_type="clustered")
print(fe_res)


# In[ ]:


# Fixed Effects
mod = PanelOLS.from_formula("Returns ~ 1 + ROE + EntityEffects + TimeEffects", data=data)
fe_res_robust = mod.fit(cov_type="robust")
print(fe_res)


# ---
# Compare the results:

# In[ ]:


#import warnings
#warnings.filterwarnings('ignore')
#warnings.simplefilter('ignore')


# In[ ]:


print(compare({"RE": re_res, "Pooled": pooled_res, "Fixed Effects": fe_res, "Fixed Effects Robust": fe_res_robust}))

