---
title: "ssh2win10"
description: ""
date: "2023-06-13T23:06:70+08:00"
tags:
  - "tool"
sidebar: true
---

实验室的一台计算机是 Win10 系统，通过 ssh 连接并使用 git bash 的终端。

## Win10服务启动

1. 在`开始-设置-应用-可选功能`中安装 OpenSSH 客户端和服务端，cmd中输入`ssh`正常响应则成功。
2. cmd中输入`net start sshd`启动服务。如权限不够则以管理员身份运行cmd命令。
3. 获取用户名和IP：
	1. cmd中输入 `echo %username%` 显示用户名；
	2. cmd中输入 `ipconfig` 显示 IPv4 地址等信息。

## SSH连接

 `ssh <username>@<IPv4>`
 密码为账户密码

## 终端设置

两种方法，一种在 ssh 时指定，另一种在 Win10 上设为默认。

### 方法一

`ssh <username>@<IPv4> -t "pwsh"`  使用新版的 Powershell

`ssh <username>@<IPv4> -t "bash"`  使用 Git Bash 或 WSL

### 方法二

管理员权限运行

````powershell
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "<git 的 bash.exe 文件位置>" -PropertyType String -Force
````
