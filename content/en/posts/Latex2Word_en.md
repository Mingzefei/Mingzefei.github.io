---
title: "Latex2Word Conversion Tool"
description: ""
date: "2023-05-23T18:05:83+08:00"
tags:
  - "latex"
sidebar: true
---

## From LaTeX to Word: An Automated Conversion Tool

LaTeX is commonly used in academic and technical fields for document typesetting, especially for handling equations and cross-references. Since LaTeX files are plain text, they are easy to manage, migrate, and control via versioning systems. However, in day-to-day work, supervisors or colleagues who are unfamiliar with LaTeX often require Word documents for easier collaboration and review. To simplify this process, I developed a tool that automatically converts LaTeX documents into Word format.

Repository: [Mingzefei/latex2word (github.com)](https://github.com/Mingzefei/latex2word)

### Motivation, Challenges, and Solutions

The motivation for this project was simple: I needed a tool to convert LaTeX documents into Word format. While strict formatting was not required, the result needed to be readable, with correctly imported images and cross-references. The Pandoc tool can convert LaTeX (.tex) files to .docx format, but the output is often rough, particularly when handling equation numbering, cross-references, and subfigures. This meant that every conversion required significant manual formatting and reference adjustments, which was inconvenient.

#### Handling Equations and Cross-References

Pandoc-Crossref, a third-party filter for Pandoc, handles cross-references well but does not support equation references ([Equation numbering in MS Word · Issue](https://github.com/lierdakil/pandoc-crossref/issues/221)). The key to solving this was using Lua filters, with inspiration from a script provided by Constantin Ahlmann-Eltze [here](https://gist.githubusercontent.com/const-ae/752ad85c43d92b72865453ea3a77e2dd/raw/28c1815979e5d03cd9ab3638f9befd354797a72b/resolve_equation_labels.lua), which effectively managed equation numbering and cross-referencing.

#### Handling Subfigures

Pandoc struggles with importing subfigures from LaTeX files. To address this, I converted the LaTeX subfigure code into a single large PNG image (by extracting multiple image-only LaTeX files and using LaTeX’s built-in `convert` and `pdftocairo` tools for compilation). I then replaced the original subfigure code with these images, allowing proper import of subfigures into the Word document.

### Case Study

The compiled LaTeX file looks like this:

![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921232609.png)
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921232625.png)

The converted Word document looks like this:

![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921232932.png)
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921233103.png)
![image.png](https://cdn.jsdelivr.net/gh/Mingzefei/myimage@main/img20240921233132.png)

### Appendix

#### Key Pandoc Command

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

Explanation of key parameters:
1. `--lua-filter resolve_equation_labels.lua` processes equation numbering and cross-references, inspired by Constantin Ahlmann-Eltze’s [script](https://gist.githubusercontent.com/const-ae/752ad85c43d92b72865453ea3a77e2dd/raw/28c1815979e5d03cd9ab3638f9befd354797a72b/resolve_equation_labels.lua);
2. `--filter pandoc-crossref` handles non-equation cross-references;
3. `--reference-doc=my_temp.docx` generates a Word document based on the style defined in `my_temp.docx`. The [Mingzefei/latex2word](https://github.com/Mingzefei/latex2word) repository provides two templates: `TIE-temp.docx`, which is the TIE journal's Word submission template (double-column), and `my_temp.docx`, which is a personal single-column template optimized for annotations;
4. `--number-sections` adds numbered headings to sections and subsections;
5. `-M autoEqnLabels` and `-M tableEqns` handle numbering for equations and tables;
6. `-M reference-section-title=Reference` adds a "Reference" title to the bibliography section;
7. `--bibliography=my_ref.bib` generates a bibliography from `ref.bib`;
8. `--citeproc --csl ieee.csl` ensures that the references are formatted according to the IEEE citation style.

#### References
1. [Pandoc Official Documentation](https://github.com/jgm/pandoc/blob/main/INSTALL.md)
2. [Pandoc-Crossref Official Documentation](https://github.com/lierdakil/pandoc-crossref)
3. [Latex to Word Conversion with Pandoc | const-ae](https://const-ae.name/post/2024-08-02-latex-to-word-conversion-with-pandoc/)

## Postscript

There are two types of people in the world: those who use LaTeX and those who don’t. The latter often ask the former for Word documents. Thus, this one-line command was born:

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
```
