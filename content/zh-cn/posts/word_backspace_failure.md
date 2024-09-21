---
title: "Word中选中文本后按Backspace键不能删除问题"
description: ""
date: 2024-06-03T11:06:18+08:00
thumbnail: ""
categories:
  - ""
tags: 
  - "tools"
sidebar: true
---


在使用Word过程中，选中文本后按Backspace键无法删除，而DEL键可以正常删除。

## 解决方法

1. 打开Word文件。
2. 点击左上角的“文件”菜单。
3. 选择左下角的“选项”。
4. 在弹出的“Word选项”窗口中，选择“高级”选项。
5. 在“编辑选项”部分，勾选“键入内容替换所选文字”。
6. 点击“确定”保存设置。

## 原理
Word的编辑设置中，“键入内容替换所选文字”选项控制着Backspace键的行为。当该选项未被选中时，Backspace键不会删除选中文本，只会插入新内容。勾选此选项后，Backspace键将正常删除选中的文本内容。

