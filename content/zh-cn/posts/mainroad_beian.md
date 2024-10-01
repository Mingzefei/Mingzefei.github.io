---
title: "Mainroad 主题的 Hugo 相关修改"
description: ""
date: "2023-02-27T22:35:46+08:00"
tags:
  - "tool"
sidebar: true
---

当前的个人网站使用 [Hogo](https://gohugo.io/) 生成，主题为 [Mainroad](https://github.com/Vimux/Mainroad/)，在客制化时遇到一些问题，解决过程记录如下。

## 备案号添加

1. 在配置文件中添加备案信息。

```config
# in config.toml
# below [Params]
BeianURL = "http://beian.miit.gov.cn"
BeianTXT = "Your Bei An Hao"
```

2. 创建样式文件 `themes/mainroad/layouts/partials/beian.html`。

```html
<a href="{{ .Site.Params.BeianURL }}" target="_blank" >{{ .Site.Params.BeianTXT }}</a>
```

3. 在`themes/mainroad/layouts/partials/footer.html` 中添加样式引用。

```html
# below this line with same indentation : <span class="footer__copyright-credits">{{ T "footer_credits" | safeHTML }}</span>
</div>
<div style="font-size: 10px">{{ partial "beian.html" $ }}</div>   
```

4. 更新，检查。

## 评论区搭建

已搭建完成，待记录。

## 访问统计

待处理。
