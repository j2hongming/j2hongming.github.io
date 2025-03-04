---
title: chmod 1777 /tmp發生了什麼事
comments: true
date: 2025-03-04 02:23:53
description:
categories: software_development
tags:
- linux
- sticky_bit
---

稍微記錄一下，以免下次碰到忘記

有三種特殊權限: Sticky Bit,  Set Group ID bit(SGID), Set User ID(SUID)，可單獨設定也可合併在一起使用

## Sticky Bit的影響

> This applies only to directories, and on Linux it prevents users from removing or renaming a file in a directory unless they own that file or directory.

- scope: directories
- operation: removing or renaming a file
- identiry: owner

在啟用Sticky Bit的資料夾內，只能刪除或改名屬於自己的檔案

``` bash
chmod 1777 /tmp
ls -ld /tmp
# drwxrwxrwt. 9 root root 4096 Mar  3 22:34 /tmp
```

## Set Group ID bit(SGID)的影響

> This can be applied to executable files or directories.

> The Set Group ID (SGID) bit on an executable file ensures that the file, when executed, runs with the permissions of the group owner of the file, rather than the group of the user who executed it. 

> When applied to directories, it will make every file or directory created under it inherit the group from the parent directory.

在啟用SGID的的可執行檔案，執行時期的process會取得檔案所屬group的權限。

在啟用SGID的的資料夾內，新增的檔案或資料夾所屬group會繼承該資料夾的group。

## Set User ID(SUID)的影響

> It only applies to files and its behavior is similar to the SGID bit, but the process will run with the privileges of the user who owns the file. 

在啟用SUID的的可執行檔案，執行時期的process會取得檔案所屬owner的權限。

``` bash
ls -la /usr/bin/passwd
-rwsr-xr-x. 1 root root 33424 Feb  7  2022 /usr/bin/passwd
```

## 參考
- [5.3 Lesson 1 - Special Permissions](https://learning.lpi.org/en/learning-materials/010-160/5/5.3/5.3_01/)
- [檔案的特殊屬性](https://dywang.csie.cyut.edu.tw/dywang/linuxSystem/node34.html)
- [permissions - Why does "chmod 1777" and "chmod 3777" both set the sticky bit? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/64126/why-does-chmod-1777-and-chmod-3777-both-set-the-sticky-bit)
- [linux - chmod 1777 or 3777 on /tmp - Server Fault](https://serverfault.com/questions/476737/chmod-1777-or-3777-on-tmp)