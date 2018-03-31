Title:cite2c-A jupyter extension for zotero  
Date:2017-10-10  
Tags:Zotero,Academic  
Category:IT  

Steps:  
1. install the cite2c:  
    1. `pip install cite2c`
    2. `python -m cite2c.install`
2. set zotero  
    1. open the zotero webpage
    2. check `Setting>Privacy` to make sure that `Publish entire library` is ticked.(If not,it will always tell you there are no matches when you want to insert citations.    
3. You will see two new toolbar buttons ![inline](https://raw.githubusercontent.com/takluyver/cite2c/master/toolbar_buttons.png).If this two toolbar buttons do not show,the possible reason is that there are some other jupyter extension may have covered the toolbar buttons (such as "Table of Contents (2)").In this way,you have to disable this kind of extensions in jupyter to use cite2c.(You can use Nbextensions to manage your extensions)  
4. For your first time to use,click the left button in ![inline](https://raw.githubusercontent.com/takluyver/cite2c/master/toolbar_buttons.png),and input your userID (not your Key).If you do not have any matches when you try to insert citations,make sure you have set the zotero as the steps (2.A).If there is still no matches,it may be due to wrong userID.To change the userID,open 'cite2c.json' in '.jupyter\nbconfig' and change it.Usually,it will be OK.  

Here is the example of how the citation is like:
This is the first citation (Barillas and Shanken 2017)  
This is another citation (Fama and French 1996)    

And this is the bibliography:  

Barillas, Francisco, and Jay Shanken. 2017. “Which Alpha?” *The Review of Financial Studies* 30 (4): 1316–38. doi:10.1093/rfs/hhw101.  

Fama, Eugene F., and Kenneth R. French. 1996. “Multifactor Explanations of Asset Pricing Anomalies.” *The Journal of Finance* 51 (1): 55–84. doi:10.1111/j.1540-6261.1996.tb05202.x.  