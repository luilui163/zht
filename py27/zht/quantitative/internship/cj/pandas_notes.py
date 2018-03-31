import pandas as pd
import numpy as np

s3=pd.Series(['red','green','blue'],index=[0,3,5])
s4=s3.reindex(np.arange(0,7),method='ffill')
print s3
print s4
msft_cum_ret=pd.DataFrame({'a':range(100)},index=pd.date_range('2010-01-01','2015-01-01'))
msft_cum_ret['2012-01'].mean()

'''
as with frequency conversion,the new index labels can be forward filled
or back filled_method and specifying bfill or ffill.Another option  is
to interpolate the missing data,which can be done using the time-series
object's .interpolate() method,which will perform a linear interpolation.
'''
aapl=pd.DataFrame()
aapl.describe(percentiles=[0.025,0.5,0.975])
