---
layout: post
title: "Inno Setup with Wine in Linux"
date: 2016-07-20 17:16:45 +0800
comments: true
categories:
- inno setup
- linux
- wine
- ubuntu
- centos
---
- 安裝紅酒(wine)
- 測試紅酒(wine)
- 安裝Inno Setup
- 執行exe, cmd
- 參考資源
<!-- more -->

## 安裝紅酒(wine)
### Ubuntu 14.04
    sudo apt-get install wine

### Cent OS 6.5
    yum install epel-release
    yum install wine

目前CentOS使用手動make尚未成功

## 測試紅酒(wine)
    wine --version
    # 下載putty.exe測試
    wine putty.exe

## 安裝Inno Setup
下載[Inno Setup QuickStart Pack](http://www.jrsoftware.org/isdl.php)
    
    wget http://www.jrsoftware.org/download.php/ispack.exe
    wine ispack.exe

安裝完成後Inno Setup會出現在~/.wine/drive_c/Program Files (x86)/Inno Setup 5
[cd到Program Files (x86)的方式](http://unix.stackexchange.com/questions/40492/change-directory-with-space-followed-by)

## 執行exe, cmd
下載大神做好的[iscc](https://gist.githubusercontent.com/derekstavis/8288379/raw/f8f1f7ef290d4116cc30ec341e6b8e996cf8e602/iscc)放在可執行的目錄或是自己加到$PATH
    
    echo $PATH
    # 自己加到$PATH,關掉Terminal後就會失效，下一次需要重新加入
    export PATH=$PATH:~/bin/my
    # 測試iscc
    iscc myScript.iss

## 參考資源
- [How To Install Wine 1.9.9 (Development Release) on CentOS, RHEL & Fedora](http://tecadmin.net/steps-install-wine-centos-rhel-fedora-systems/)
- [How to Install & Configure Wine 1.7.34 on RHEL/CentOS 6/7 and Fedora 23/22/21 - Desktop](https://www.youtube.com/watch?v=Ds3Y9thewNQ)
- [CREATING A INSTALLER USING INNO SETUP ON LINUX AND MAC OS X](http://derek.nodeconf.org/posts/creating-a-installer-using-inno-setup-on-linux-and-mac-os-x/)
