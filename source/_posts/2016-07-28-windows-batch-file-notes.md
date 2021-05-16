---
layout: post
title: "Windows Batch File Notes"
date: 2016-07-28 16:34:39 +0800
comments: true
categories: software_development
tags:
- windows
- bat 
---

- 變數
- if
- 導向
- 常用範例
- 參考資料
<!-- more -->

## 變數

### 系統變數
    :: 觀察作業系統環境變數
    set
    :: 將作業系統環境變數輸出至variables.txt
    set > variables.txt


### 設定變數
#### 基本設定

    set LogName=myLog.txt

注意事項如下：

1. 注意空白
2. case insensitive

{% codeblock  lang:bat %}
@ECHO off
SET spaceExam=  beginText
SET aBc=Hello
SET Abc=World
ECHO %spaceExam%
ECHO %aBc% 
PAUSE
{% endcodeblock %}

#### 輸入提示
加上`/p`

{% codeblock  lang:bat %}
@ECHO off 
SET /p LogName=請輸入Log檔案名稱 
ECHO Hello World >%LogName% 
PAUSE
{% endcodeblock %}


#### 運算式
加上`/a`

{% codeblock  lang:bat %}
@ECHO off
SET /p num=Input Number
SET /p price=Input Price
SET /a sum=%num% * %price%
ECHO Sum=%sum%
PAUSE
{% endcodeblock %}

### 取得變數
前後加上%

    ECHO %LogName%

### 常用變數

    %CD% :當前工作目錄
    %DATE% :目前系統日期
    %TIME% :目前系統時間
    %SystemDrive% :系統碟
    %ProgramFiles% :應用程式目錄
    %ProgramFiles(x86)% :應用程式目錄(x86)


## if

直接參考 `if/?`說明

``` bat
在批次檔中執行條件處理。

IF [NOT] ERRORLEVEL number command
IF [NOT] string1==string2 command
IF [NOT] EXIST filename command

  NOT               表示 Windows 應該只有在條件為偽時才執行命令。

  ERRORLEVEL number 當上一個執行的程式傳回的結束代碼大於或等於指定
                    數字時，則條件為真。

  string1==string2  當指定的文字字串相符合時，則條件為真。

  EXIST filename    如果指定的檔名存在時，則條件為真。

  command           指定當條件為真時所要執行的命令。命令之後可以
                    接著 ELSE 命令。當指定條件為偽時，緊接在 ELSE
                    命令之後的命令將會被執行。

ELSE 子句必須出現在 IF 之後的同一行。例如:

    IF EXIST filename. (
        del filename.
    ) ELSE (
        echo filename. missing.
    )

以下命令無法作用，因為 del 命令必須以換行字元來結尾:

    IF EXIST filename. del filename. ELSE echo filename. missing

下面命令也無法作用，因為 ELSE 命令必須在與 IF 命令同一行的結尾:

    IF EXIST filename. del filename.
    ELSE echo filename. missing

下面命令只有在寫成一行時才能作用:

    IF EXIST filename. (del filename.) ELSE echo filename. missing

(more)...
```

範例：

{% codeblock  lang:bat %}
@ECHO off
IF NOT EXIST testFolder ( 
     mkdir testFolder
) ELSE ( 
     ECHO testFolder has been exist 
) 
PAUSE
{% endcodeblock %}


## 導向

```
Standard Output 代號 1
Standard Error  代號 2
Do Nothing      代號 NUL
Console
```

```
> NUL :將Standard Output導向null
2 > NUL :將Standard Error導向null
> NUL 2>&1 :同時將Standard Output和Standard Error導向null
> log.txt 2>&1 :同時將Standard Output和Standard Error導向File(log.txt)
> log_stdout.txt 2>log_stderr.txt :將Standard Output導向至log_stdout.txt以及將Standard Error導向至log_stderr.txt
```


## 常用範例
### 判斷指令是否存在

[Determine if command is recognized in a batch file](http://superuser.com/questions/175466/determine-if-command-is-recognized-in-a-batch-file)

``` bat
@ECHO off
WHERE mycommand 2>NUL
IF %ERRORLEVEL% NEQ 0 (
     ECHO mycommand wasn't found 
)  ELSE ( 
     ECHO mycommand found 
)
PAUSE
```

### 判斷檔案是否存在

檢查7z.exe是否存在

``` bat
@ECHO off
SET filepath=%ProgramFiles%\7-Zip\
SET filename=7z.exe

cd %filepath%
IF EXIST %filename% (
	ECHO %filename%  found
	ECHO %CD%
)  ELSE ( 
    ECHO %filename% wasn't found 
)

:: BAT File所在位置 %~dp0
cd %~dp0
ECHO %CD%
PAUSE
```
### 日期與時間變數

``` bat
::民國年
set /a year=%date:~,4%-1911
::西元年
set year=%date:~,4%
::月
set month=%date:~5,2%
::日
set day=%date:~8,2%
::今天日期
set Today=%year%%month%%day%
::時間
set NowTimeTmp=%time::=%
set NowTime=%NowTimeTmp:~0,6%
```

## 參考資料
- [批次檔的精要學習手冊](https://www.gitbook.com/book/peterju/cmddoc/details)
- [Batch File Basic Tutorial](http://www.tinysoftwares.in/BatchFileTutorial/Index)
- [Display & Redirect Output](http://www.robvanderwoude.com/battech_redirection.php)
- [批次檔BAT中應用Windows的36個環境變數](http://forum.twbts.com/viewthread.php?tid=10152)
- [%CD% 與 %~dp0](http://inpega.blogspot.tw/2012/07/cd-dp0.html)
