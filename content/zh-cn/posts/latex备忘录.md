---
title: "Latex 备忘录"
description: ""
date: "2023-12-01T14:12:83+08:00"
thumbnail: ""
categories:
  - ""
tags: 
  - "latex"
sidebar: true
---

一些关于 Latex 的琐碎笔记，可以获得更好的编辑体验。

## vscode 中查看正文字数

1. 借助插件 LaTeX Workshop
2. 在 `COMMANDS` 栏中的 `Miscellaneous` 下，点击 `Count words in LaTeX project`

## 形成 change marked 版本

1. 需要 `latexdiff`
2. `latexdiff old.tex new.tex > changed.tex`

## 跨文件交叉引用

1. 使用 `xr` 宏包： `\usepackage{xr}`
2. 导入待引用标签的文件：`\externaldocument{texfile}`

## 安装 standalone 宏包

1. 使用 `sudo apt-get install texlive-latex-extra` 命令安装
2. 使用 `sudo apt-file search standalone.sty` 命令查看是否存在

## 公式环境

1. `gather*` 环境在设置全局左对齐后，适合写公式推导
2. `align` 环境每行一个编号
3. `gather` 居中对齐

## 公式引用

使用 `\eqref` 自带括号

## 与 visio 配合使用

1. visio 绘图时
	1. 统一页面大小：A4 paper
	2. 统一缩放比例：100% 实际尺寸
	3. 统一字体大小：小四号 12pt
2. visio 导出时
	1. `设计->大小->适应绘图` ：用于去掉白边
	2. 导出 pdf：在 `选项` 栏，勾选 `当前页`，取消 `辅助功能文档结构标记`：用于去掉外边框
3. latex 导入时
	1. 使用默认大小导入图片

## 图表占一页且空白较多

```tex
\renewcommand{\floatpagefraction}{.9}
```

允许页面90%为图片，10%为文字。
默认是50%是图片，50%是文字，因此占比超过50%的图片会单独一页。