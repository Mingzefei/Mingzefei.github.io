---
title: IOP Latex 模板的部分报错问题
description: ''
date: '2022-11-21T09:51:05+08:00'
tags:
  - 宏包冲突
  - 模板报错解决
  - LaTeX模板问题
  - 学术写作
sidebar: false
---

要在英国物理学会（Institute of Physics, IOP）上发文章，使用[官方提供的 Latex 模板](https://publishingsupport.iopscience.iop.org/questions/latex-template/)编写，期间遇到如下问题，记录如下。

## `amsmath` 和 `iopart` 不兼容

同时使用两个宏包会出现如下报错：

```
! LaTeX Error: Command \equation* already defined. 
Or name \end... illegal, see p.192 of the manual.
```

[Ji-Huan Guan 提到过](https://www.guanjihuan.com/archives/3598)是不兼容问题，官网上也有类似说明。

妙脆角 提供了[一种解决方法](https://zhuanlan.zhihu.com/p/41469740)：

```
\expandafter\let\csname equation*\endcsname\relax
\expandafter\let\csname endequation*\endcsname\relax
\usepackage{amsmath}
```

不再产生报错。

