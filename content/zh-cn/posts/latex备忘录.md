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

额外：配合 git 使用
参考 [CTAN: Package git-latexdiff](https://www.ctan.org/pkg/git-latexdiff) 

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

## biber 和 bibtex

biber 更为强大，使用 `biber` 命令进行编译。
```tex
\documentclass{article}
% \usepackage[backend=biber]{biblatex}  % 使用biber作为后端处理引用，可进行更精细的参考文献设置
\usepackage[backend=biber,style=mystyle]{biblatex}  % 使用biber作为后端处理引用，并使用mystyle.sty作为样式文件
\addbibresource{sample.bib}  % 引用的数据库

\begin{document}
Hello world \cite{ref1}.

\printbibliography  % 打印参考文献列表
\end{document}
```

bibtex 适配更好，使用 `bibtex` 命令进行编译。
```tex
\documentclass{article}

\begin{document}
Hello world \cite{ref1}.

\bibliography{sample}  % 引用的BibTeX数据库文件名
\bibliographystyle{mystyle}  % mystyle是你的.sty文件名
\end{document}
```

![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20231201151516.png)
(图片来源：[bibliographies - bibtex vs. biber and biblatex vs. natbib - TeX - LaTeX Stack Exchange](https://tex.stackexchange.com/questions/25701/bibtex-vs-biber-and-biblatex-vs-natbib))

## tikz、pgf 和 pdf 导入 matplotlib 绘图的比较

- 使用 [nschloe/tikzplotlib](https://github.com/nschloe/tikzplotlib?tab=readme-ov-file) 中的 `tikzplotlib.save("mytikz.tex")` 命令将 matplotlib 绘图转成 tikz 命令
	- 写这段文字时，该项目已经一年多没有更新
	- tex 中绘图结果 python 脚本绘图结果有差异
	- 可以完全保证图片字体与正文字体一致
- 使用 matplotlib 直接导出 pgf 
	- 生成的 pgf 文件为命令行
	- tex 中绘图结果与 python 脚本绘图结果一致
- 使用 matplotlib 直接导出 pdf
	- 生成的 pdf 文件常见，可用常用浏览器打开
	- tex 中直接导入该文件，不涉及再次渲染

在 pgf 和 pdf 中，我更倾向后者。两者最终结果相同，而 pdf 更易查阅。

matplotlib 中使用如下命令控制字体大小和图片尺寸：
```python
matplotlib.rcParams.update({'font.size': 8})
matplotlib.rcParams.update({'figure.figsize': [4., 2.5]})
```

## 删除 bib 中未引用文献

```bash
bibexport -o clean_ref.bib main.aux
```
该命令将从 `main.aux` 中生成仅在文中引用的 bib 文件。

## 使用 cleveref 宏包自动确定交叉引用格式

官方文档：[cleveref.pdf](https://mirror.its.dal.ca/ctan/macros/latex/contrib/cleveref/cleveref.pdf)

### 加载宏包

```tex
\usepackage{cleveref}
```

### 基本用法

```tex
1. \label{eq:1}, ..., \cref{eq:1} % 自动添加前缀 eq.
2. \Cref{fig1} % 自动添加大写的前缀 Fig. , 适用于句首
3. \cref{eq1,eq2,eq3,,eq4} % 多重引用, eqs. (1) to (3) and (4)
4. \crefrange{eq1}{eq3} % 范围引用, eqs. (1) to (3)
5. \cpageref{sec2} % 页码引用, page 2
```

### 自定义格式

```tex
\crefformat{equation}{Eq.~(#2#1#3)} % 自定义公式引用格式
```
