#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : ob2hugo.py
@Time : 2023/05/07 19:53:49
@Auth : Ming(<3057761608@qq.com>)
@Vers : 1.0
@Desc : build hugo content from obsidian
@Usag : python ob2hugo.py
"""
# here put the import lib
from obsidian_to_hugo import ObsidianToHugo
import os

def custom_filter(content: str, path: str) -> bool: 
    return "include" in path 

def main():

    obsidian_to_hugo = ObsidianToHugo(
        obsidian_vault_dir="/mnt/c/Users/Hua/win_workbench/my_note/5_Blog",
        hugo_content_dir="./content/",
        # filters=[custom_filter],
    )

    obsidian_to_hugo.run()
    
    os.system("chmod -R 744 ./content")
    os.system("find content/ -type f -exec chmod 644 {} +")

    os.system("hugo server")

if __name__ == '__main__':
    main()
