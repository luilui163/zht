#-*-coding: utf-8 -*-
#author:tyhj
#params.py 2017/9/18 17:17
import os


#======================project parameters=================================

#the port are updated yearly
updateFreq='Y'

#the update month is at the end of June,that is,the new port
#are rebuild in July of every year.
updateMonth='06'

#the report data has a time lag of 6 months,that is,we can only
#get the financial data of 6 months ago.For example,the data in
#balance sheet of 2012-12-31 are available at 2013-06.But,for trading
#data (open,close,high,low,volume and so on),there is no time lag.
rdtl=6



#project directory
directory=r'D:\quantDb\researchTopics\factorModel'

#source data path
sp=r'D:\quantDb\sourceData\gta\data\csv'




#paths
bdp=os.path.join(directory,'baseData')#base data
#notice that the time in indicator of idp are available time,that is,
#it has been adjusted by using time lag,if needed.And their frequency
#is once a year,so,there should be only one tick for every year.Taking
#these constraints into consideration,the index of df in idp are like
#'2013-06'.
idp=os.path.join(directory,'indicator')#indicator repository
fdp=os.path.join(directory,'factor')#factor return time series
tmpp=os.path.join(directory,'tmp')#tmp data


#indicator id

#the frequency is monthly in idip
idip=os.path.join(directory,'indicatorId')
id2p=os.path.join(idip,'2')
id3p=os.path.join(idip,'3')
id10p=os.path.join(idip,'10')


bmp=os.path.join(directory,'benchmarkModels')
ff5p=os.path.join(directory,'ff5')
liq4p=os.path.join(directory,'liq4')


#constructPlayingField
cpfp=os.path.join(directory,'constructPlayingField')
spfp=os.path.join(cpfp,'spreadFig')
regp=os.path.join(cpfp,'regress')
mdp=os.path.join(cpfp,'models')


idrp=os.path.join(directory,'indicatorRet')

estimateAlphaPath=os.path.join(cpfp,'estimateAlpha')
eap=os.path.join(estimateAlphaPath,'alpha')
eatp=os.path.join(estimateAlphaPath,'alphat')


rvmp=os.path.join(cpfp,'regValidModels')
eaoatmp=os.path.join(cpfp,'estimateAlphaOnAllTestModels')
alphap=os.path.join(eaoatmp,'alpha')
alphatp=os.path.join(eaoatmp,'alphat')


#reformFF3
rff3p=os.path.join(cpfp,'reformFF3')
myfp=os.path.join(rff3p,'myFactors')
mymp=os.path.join(rff3p,'myModels')




