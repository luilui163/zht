#-*-coding: utf-8 -*-
#author:tyhj
#main.py 2017/9/19 11:56
import os


def run():
    scripts=['initialize.py',
             'getData.py',
             'multi_getIndicatorId.py',
             'classicalModels.py',
             'multi_getIndicatorPortRet.py',
             'constructPlayingField.py',
             'multi_getIndicatorPortRet.py',
             'multi_builTestModels',
             'multi_estimateAlphaOnAllTestModels.py',
             'reformFF3.py',
             'spreadFig.py']

#TODO:multi_estimateGRSOnAllTestModels.py

    cwd=os.getcwd()
    for script in scripts:
        cmd='python %s'%(os.path.join(cwd,script))

        os.system(cmd)
        print '%s finished'%script










if __name__=='__main__':
    run()





