---
title: Latex2Word
description: ''
date: '2023-05-22T23:05:15+08:00'
tags:
  - 文档格式转换
  - 学术工具
  - latex
  - tools
sidebar: false
---

## 从 LaTeX 到 Word：一个自动化转换工具

LaTeX 常用于学术和技术领域的文档排版，尤其适用于公式输入和交叉引用；并且，作为纯文本文件，tex 格式文件容易进行内容迁移和版本控制。然而，日常工作中，不熟悉 LaTeX 的上级或同事常会要求提供 Word 文件，以便共同审阅和修改。为此开发了一个从 LaTeX 转换到 Word 的工具，以自动化这一流程。

仓库地址：[Mingzefei/latex2word (github.com)](https://github.com/Mingzefei/latex2word)

### 初衷、挑战和解决方案

项目的初衷很简单：我需要一个能够将 LaTeX 文档转换为 Word 文件的工具，不需要对 Word 进行严格的格式排版，但是需要排版成易读的格式，以及正确的图片导入和交叉引用。Pandoc 工具可以实现将 tex 格式文件转换为 docx 格式文件，但转换结果十分粗糙，尤其无法正确处理公式编号、交叉引用和多子图等问题。这意味着在每次使用 Pandoc  进行转换后，都需要手动调整 Word 文件的格式和引用，十分不便。

#### 公式和交叉引用的处理

Pandoc-Crossref 作为 Pandoc 的第三方过滤器，可以很好地处理交叉引用，但是无法处理公式的引用（[Equation numbering in MS Word · Issue](https://github.com/lierdakil/pandoc-crossref/issues/221)）。
解决这一问题的关键在于使用 Lua 过滤器，利用 Constantin Ahlmann-Eltze 提供的[脚本](https://gist.githubusercontent.com/const-ae/752ad85c43d92b72865453ea3a77e2dd/raw/28c1815979e5d03cd9ab3638f9befd354797a72b/resolve_equation_labels.lua)，有效处理了公式的编号和交叉引用。

#### 多子图的处理

Pandoc 对 tex 文件中多子图的处理并不理想，一般无法正常导入多子图。为此，我在项目中先将 LaTeX 文件中的多子图代码转换成单个大图的 png 文件（提取成多个只有图片的 tex文件，并利用 LaTeX 自带的 `convert` 和 `pdftocairo` 进行编译），再用这些大图替换原始的多子图。从而实现了多子图的正常导入。

### 案例
待转换的 LaTeX 文件编译结果如下：
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921232609.png)
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921232625.png)

转换生成的 Word 文件如下：
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921232932.png)
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921233103.png)
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921233132.png)


### 附录

#### 核心的 pandoc 命令

```shell
pandoc texfile -o docxfile \
    --lua-filter resolve_equation_labels.lua \
    --filter pandoc-crossref \
    --reference-doc=temp.docx \
    --number-sections \
    -M autoEqnLabels \
    -M tableEqns \
    -M reference-section-title=Reference \
    --bibliography=ref.bib \
    --citeproc --csl ieee.csl
```
其中，
1. `--lua-filter resolve_equation_labels.lua` 处理公式编号及公式交叉引用，受 Constantin Ahlmann-Eltze 的[脚本](https://gist.githubusercontent.com/const-ae/752ad85c43d92b72865453ea3a77e2dd/raw/28c1815979e5d03cd9ab3638f9befd354797a72b/resolve_equation_labels.lua)启发；
2. `--filter pandoc-crossref` 处理除公式以外的交叉引用；
3. `--reference-doc=my_temp.docx` 依照 `my_temp.docx` 中的样式生成 Word 文件。仓库 [Mingzefei/latex2word](https://github.com/Mingzefei/latex2word) 提供了两个模板文件 `TIE-temp.docx` 和 `my_temp.docx`，前者是 TIE 期刊的投稿 Word 模板（双栏），后者是个人调整出的 Word 模板（单栏，且便于批注）；
4. `--number-sections` 在（子）章节标题前添加数字编号；
5. `-M autoEqnLabels`， `-M tableEqns`设置公式、表格等的编号；
6. `-M reference-sction-title=Reference` 在参考文献部分添加章节标题 Reference；
7. `--biblipgraphy=my_ref.bib` 使用 `ref.bib` 生成参考文献；
8. `--citeproc --csl ieee.csl` 生成的参考文献格式为 `ieee` 。
#### 参考资料
1. [Pandoc 官方文档](https://github.com/jgm/pandoc/blob/main/INSTALL.md)
2. [Pandoc-crossref 官方文档](https://github.com/lierdakil/pandoc-crossref)
3. [Latex to Word conversion with pandoc | const-ae](https://const-ae.name/post/2024-08-02-latex-to-word-conversion-with-pandoc/)

## 后记

世界上有两种人，一种人会用 Latex，另一种人不会用 Latex。 后者常常向前者要 Word 版本文件。 因此有了如下一行命令。

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