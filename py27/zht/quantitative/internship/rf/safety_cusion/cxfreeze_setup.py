#-*-coding: utf-8 -*-
#@author:tyhj

from cx_Freeze import setup, Executable

executables = [
    Executable(
        script='GUI_v3_27.py',  # 目标引用脚本
        base="win32gui",  # GUI程序需要隐藏控制台
        targetName='Test.exe',  # 生成exe的名字
        icon="Test.ico"  # 生成exe的的图标
    )]












