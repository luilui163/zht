#-*-coding: utf-8 -*-
#author:tyhj
#params.py 2017/8/15 17:40
import os
'''
weight:tradable market value

capm:rp
ff3:rp,smb,hml
ff5:rp,smb,hml,rmw,cma

'''



#project directory
directory=r'D:\quantDb\researchTopics\assetPricing'

#source data path
sp=r'D:\quantDb\sourceData\gta\data\csv'

#paths
bdp=os.path.join(directory,'baseData')#base data
idp=os.path.join(directory,'indicator')#indicator repository
fdp=os.path.join(directory,'factor')#factor return time series
tmpp=os.path.join(directory,'tmp')#tmp data
indicatorIdPath=os.path.join(directory,'indicatorId')#used to store the port Id
portIdPath=os.path.join(directory,'portId')#used to store the Id of the intersection ports
portRetPath=os.path.join(directory,'portRet')#store the return of ports
portEretPath=os.path.join(directory,'portEret')#store the excess return
portEretFigPath=os.path.join(directory,'portEretFig')#fig of the excess return
factorRetPath=os.path.join(directory,'factorRet')#store the return of the factors
validatePath=os.path.join(directory,'validate')#store the validation results
regressPath=os.path.join(directory,'regress')#store the regression results
grsPath=os.path.join(directory,'GRS')
bmmp=os.path.join(directory,'benchmarkModel')

#myFactor
myFactorPath=os.path.join(directory,'myFactor')
myIndicatorPath=os.path.join(myFactorPath,'indicator')#store the indicators from source data
myIndicatorIdPath=os.path.join(myFactorPath,'indicatorId')
prp=os.path.join(myFactorPath,'portRet')
perp=os.path.join(myFactorPath,'portEret')
spreadPath=os.path.join(myFactorPath,'spreadFig')
regressResultPath=os.path.join(myFactorPath,'regress')
estimateAlphaPath=os.path.join(myFactorPath,'estimateAlpha')
eap=os.path.join(estimateAlphaPath,'alpha')
eatp=os.path.join(estimateAlphaPath,'alphat')
fip=os.path.join(myFactorPath,'financialIndicator')
fiip=os.path.join(myFactorPath,'financialIndicatorId')

#ff3
ff3P=os.path.join(directory,'ff3')
ff3FactorP=os.path.join(ff3P,'factor')

#HXZ 4-factor
hxz4P=os.path.join(directory,'hxz4')
hxz4FactorP=os.path.join(hxz4P,'factor')

#build myModel
cfp=os.path.join(myFactorPath,'constructFactor')
chunk2p=os.path.join(cfp,'2')
chunk3p=os.path.join(cfp,'3')
rmp=os.path.join(myFactorPath,'randomModel')
testmodelp=os.path.join(myFactorPath,'testmodel')
pfp=os.path.join(myFactorPath,'playingField')
pfip=os.path.join(pfp,'indicators')
indidp=os.path.join(pfp,'id')
indid2p=os.path.join(indidp,'2')
indid3p=os.path.join(indidp,'3')
indid10p=os.path.join(indidp,'10')
mdp=os.path.join(pfp,'model')
iprp=os.path.join(pfp,'indicatorPortRet')
regp=os.path.join(pfp,'regress')
alphap=os.path.join(pfp,'alpha')
alphatp=os.path.join(pfp,'alphat')














def initialize():
    #create neccessary directorys to store data
    for d in [directory,bdp,idp,fdp,tmpp,
              indicatorIdPath,portIdPath,portRetPath,
              portEretPath,portEretFigPath,
              factorRetPath,validatePath,
              regressPath,grsPath]:
        if not os.path.exists(d):
            os.makedirs(d)








