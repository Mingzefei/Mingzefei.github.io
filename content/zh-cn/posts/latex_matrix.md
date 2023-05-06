---
title: "Latex 中的复杂矩阵"
description: ""
date: "2023-03-24T17:23:33+08:00"
thumbnail: ""
categories:
  - ""
tags:
  - ""
sidebar: true
---

写 paper 时遇到一个矩阵，需要对块、行和列进行标记。

## 方法一

```latex
\begin{equation}
\bordermatrix{
    & e_\text{o} & & e_\text{b}  & & & & & &e_\text{s}  & & & & &\cr
v_1    &-1  &0 &0 &0   &1 &0 &0 &0 &0 &0 &0 &0 &0 &0 \cr
v_2    &0   &0 &0 &0   &-1&1 &1 &1 &0 &0 &0 &0 &0 &0 \cr
v_3    &0   &1 &0 &0   &0 &-1&0 &0 &1 &0 &0 &0 &0 &0 \cr
v_4    &0   &0 &1 &0   &0 &0 &-1&0 &0 &1 &0 &0 &0 &0 \cr
v_5    &0   &0 &0 &1   &0 &0 &0 &-1&0 &0 &0 &0 &0 &0 \cr
v_6    &0   &-1&0 &0   &0 &0 &0 &0 &0 &0 &1 &0 &0 &0 \cr
v_7    &0   &0 &-1&0   &0 &0 &0 &0 &-1&0 &0 &1 &0 &0 \cr
v_8    &0   &0 &0 &-1  &0 &0 &0 &0 &0 &-1&0 &0 &1 &0 \cr
v_9    &0   &0 &0 &0   &0 &0 &0 &0 &0 &0 &-1&-1&-1&1 \cr
},
\end{equation}
```

![](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img/latex-1.jpg)

最简单，但暂未找到划分块的方法。

## 方法二

```latex
\begin{equation}
    \begin{array}{cc}
        &  \begin{array}{c ccc ccccccccccc} e_o &\quad  &e_{b} & \quad & \quad & \quad & \quad & \quad & \quad & e_s & \quad & \quad & \quad & \quad & \quad \end{array}\\
    \begin{array}{c} v_1\\v_2\\v_3\\v_4\\v_5\\v_6\\v_7\\v_8\\v_9\end{array}&
    \left(
    \begin{array}{c|ccc|cccccccccc}
        -1  &0 &0 &0   &1 &0 &0 &0 &0 &0 &0 &0 &0 &0\\
        0   &0 &0 &0   &-1&1 &1 &1 &0 &0 &0 &0 &0 &0\\
        0   &1 &0 &0   &0 &-1&0 &0 &1 &0 &0 &0 &0 &0\\
        0   &0 &1 &0   &0 &0 &-1&0 &0 &1 &0 &0 &0 &0\\
        0   &0 &0 &1   &0 &0 &0 &-1&0 &0 &0 &0 &0 &0\\
        0   &-1&0 &0   &0 &0 &0 &0 &0 &0 &1 &0 &0 &0\\
        0   &0 &-1&0   &0 &0 &0 &0 &-1&0 &0 &1 &0 &0\\
        0   &0 &0 &-1  &0 &0 &0 &0 &0 &-1&0 &0 &1 &0\\
        0   &0 &0 &0   &0 &0 &0 &0 &0 &0 &-1&-1&-1&1\\
    \end{array}
    \right)
        \end{array},
\end{equation}
```

![](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img/latex-2.jpg)

此处手动调整 第一行`array` 的列间距。

## 方法三

```latex
\begin{equation}
    \begin{array}{cc}
        &  \begin{array}{c c ccc cccccccccc} & e_o &e_{b1}  &e_{b2} & e_{b3} & e_{s1} & e_{s2} & e_{s3} & e_{s4} & e_{s5} & e_{s6} & e_{s7} & e_{s8} & e_{s9} & e_{s10} \end{array}\\
    \begin{array}{c} v_1\\v_2\\v_3\\v_4\\v_5\\v_6\\v_7\\v_8\\v_9\end{array}&
        \left(
    \begin{array}{c|ccc|cccccccccc}
        -1  &0 &0 &0   &1 &0 &0 &0 &0 &0 &0 &0 &0 &0\\
        0   &0 &0 &0   &-1&1 &1 &1 &0 &0 &0 &0 &0 &0\\
        0   &1 &0 &0   &0 &-1&0 &0 &1 &0 &0 &0 &0 &0\\
        0   &0 &1 &0   &0 &0 &-1&0 &0 &1 &0 &0 &0 &0\\
        0   &0 &0 &1   &0 &0 &0 &-1&0 &0 &0 &0 &0 &0\\
        0   &-1&0 &0   &0 &0 &0 &0 &0 &0 &1 &0 &0 &0\\
        0   &0 &-1&0   &0 &0 &0 &0 &-1&0 &0 &1 &0 &0\\
        0   &0 &0 &-1  &0 &0 &0 &0 &0 &-1&0 &0 &1 &0\\
        0   &0 &0 &0   &0 &0 &0 &0 &0 &0 &-1&-1&-1&1\\
    \end{array}
        \right)
        \end{array},
\end{equation}
```

![](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img/latex-3.jpg)

## 其他复杂矩阵

可参考：[如何用latex编写矩阵（包括各类复杂、大型矩阵）？|知乎](https://zhuanlan.zhihu.com/p/266267223)
