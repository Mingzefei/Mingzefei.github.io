---
title: "Latex2Word"
description: ""
date: "2023-05-22T23:05:15+08:00"
thumbnail: ""
categories:
  - ""
tags:
  - "latex"
sidebar: true
---

世界上有两种人，一种人会用 Latex，另一种人不会用 Latex。
后者常常向前者要 Word 版本文件。
因此有了如下一行命令。

```bash
pandoc input.tex -o output.docx\
  --filter pandoc-crossref \
  --reference-doc=my_temp.docx \
  --number-sections \
  -M autoEqnLabels -M tableEqns \
  -M reference-section-title=Reference \
  --bibliography=my_ref.bib \
  --citeproc --csl ieee.csl
```

该命令用到的文件可以在仓库 [Mingzefei/latex2word](https://github.com/Mingzefei/latex2word)中找到。

## 软件安装

1. pandoc ：介绍及安装参考[官方文档](https://github.com/jgm/pandoc/blob/main/INSTALL.md)。建议在[Releases · jgm/pandoc (github.com)](https://github.com/jgm/pandoc/releases)上下载最新 deb 安装包，用`sudo dpkg -i /path/to/the/deb/file`。
2. pandoc-crossref : 介绍及安装参考[官方文档](https://github.com/lierdakil/pandoc-crossref)。下载与 pandoc 相**匹配**的版本，并将其中的可执行文件 `pandoc-crossref` 移入 `/usr/bin` ，或在转换时指定具体文件。

## 使用说明

1. `--filter pandoc-crossref` 处理交叉引用；
2. `--reference-doc=my_temp.docx` 依照 `my_temp.docx` 中的样式处理转换后的 `output.docx`。在仓库 [Mingzefei/latex2word](https://github.com/Mingzefei/latex2word) 中有两个模板文件 `TIE-temp.docx` 和 `my_temp.docx`，前者是 TIE 期刊的投稿 Word 模板（双栏），后者是个人调整出的 Word 模板（单栏，字大，便于批注）；
3. `--number-sections` 在（子）章节标题前添加数字编号；
4. `-M autoEqnLabels`， `-M tableEqns`设置公式、表格等的编号；
5. `-M reference-sction-title=Reference` 在参考文献部分添加章节标题 Reference；
6. `--biblipgraphy=my_ref.bib` 使用 `my_ref.bib` 生成参考文献；
7. `--citeproc --csl ieee.csl` 生成的参考文献格式为 `ieee` 。

## 遗留问题

1. 可能出现转换后的 docx 文档无法打开。大概率是待转换的 tex 文件过于复杂导致，尝试避免使用 tikz 、减少图片数量等。
2. 对 subfigure 支持一般，特别是编号容易出错。如果 tex 文件没有涉及子图，可以使用 `-t docx+native_numbering` 对图片和表格的编号进行优化。
3. 公式的引用会以 `[<label>]` 的形式出现。参考[Equation numbering in MS Word · Issue](https://github.com/lierdakil/pandoc-crossref/issues/221)，尚未找到解决方法；可以在 Word 中用全局替换命令进行替换。
4. 在 tex 中设置的图片大小不对转换后的 docx 起作用；图片的 caption 样式尚未找到设置方法。
