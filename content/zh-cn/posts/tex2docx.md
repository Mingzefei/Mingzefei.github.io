---
title: "Tex2docx"
description: ""
date: "2023-02-13T09:28:02+08:00"
thumbnail: ""
categories:
  - ""
tags:
  - ""
sidebar: true
---

需要从 Latex 文件生成 Word。
主要使用 `pandoc` 和插件`pandoc-crossref`（改善交叉引用）。

## 安装

### `pandoc` 安装

Ubuntu 的 `sudo apt-get install pandoc` 安装的版本太低，这里直接从 Github 的[仓库](https://github.com/jgm/pandoc/releases/)中下载较新的发布版本。

将解压后 `pandoc-$version/bin/` 中的文件添加到 `/usr/bin/`：
```bash
cd pandoc-$version/bin
./pandoc -v # confirm the version of download
sudo mv pandoc /usr/bin
pandoc -v # confirm the version in system
```

### `crossref` 安装

从 Github 的 [仓库](https://github.com/lierdakil/pandoc-crossref/releases) 中下载与 `pandoc` 版本相一致的版本。

添加解压后的相关文件：
```bash
sudo mv pandoc-crossref /usr/bin
sudo chmod a+x /usr/bin/pandoc-crossref
sudo mkdir -p /usr/local/man/man1
sudo mv pandoc-crossref.1 /usr/lcoal/man/man1
man pandoc-crossref # test whether it works
```

## 使用

> 参考
> [使用 Pandoc 将 Latex 转化为 Word](https://zhuanlan.zhihu.com/p/455713759)

综合命令：

```bash
pandoc input.tex  --filter pandoc-crossref --citeproc --csl springer-basic-note.csl  --bibliography=my_ref.bib -M reference-section-title=Reference  -M autoEqnLabels -M tableEqns  -t docx+native_numbering --number-sections -o output.docx

# another way
pandoc main.tex -o output.docx -w docx \
       --reference-doc Hindawi_template.docx \
       --filter pandoc-crossref \
       --bibliography=my_refs.bib \
       --citeproc \
       --csl springer-basic-note.csl
```

- `main.tex`：输入 LaTeX 文件名
- `-o output.docx`：输出 Word 文件名
- `-w docx`：输出文件格式
- `--reference-doc template.docx`：参考模板 Docs 文件
- `--bibliography refs.bib`：参考文献 bib 文件
- `--citeproc`：用于参考文献的引用
- `--csl springer-basic-note.csl`：参考文献样式文件

## 部分问题

- 多子图无法成功转换；
- 公式的 `ref` 无法成功转换。
