---
title: 就決定是你了! Apache
description: 架設Apache的注意事項
categories: software_development
tags:
  - apache
  - http
  - web
comments: true
date: 2021-01-29 00:42:16
---


## 從可以動的Apache開始吧

OS環境: Ubuntu 20.04, 安裝apache

``` bash
sudo apt update
sudo apt install apache2
```

設定j2hongming.dev

``` bash
sudo mkdir -p /var/www/j2hongming.dev/public_html
sudo chown -R $USER:$USER /var/www/j2hongming.dev/public_html
sudo vim /etc/apache2/sites-available/j2hongming.dev.conf
```

j2hongming.dev.conf的內容
``` xml
<VirtualHost *:80>
        ServerAdmin admin@j2hongming.dev
        ServerName j2hongming.dev
        DocumentRoot /var/www/j2hongming.dev/public_html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

啟用j2hongming.dev.conf設定檔, 關閉預設設定檔000-default.conf, 原因是設定檔順序為字母排序, 若同時開啟且使用ip存取的話, 會載入000-default.conf的設定
重新載入設定
``` bash
sudo a2ensite j2hongming.dev
# optional, stop default
sudo a2dissite 000-default.conf
systemctl reload apache2
```

編輯首頁
``` bash
sudo vim /var/www/j2hongming.dev/public_html/index.html
```

index.html的內容
``` html
<!doctype html>
<html>
  <head>  
      <title>Hi, I'm j2hongming</title>
  </head>
  <body>  
      Welcome! This is j2hongming.dev
      <p>This is an example paragraph. Anything in the <strong>body</strong> tag will appear on the page, just like this <strong>p</strong> tag and its contents.</p>
  </body>
</html>

```
![](index_ip.png)

因為還沒申請網域, 本機先修改host試試看吧, windows系統的位置`%SystemRoot%\System32\drivers\etc\hosts`, linux系統的位置`/etc/hosts`

![](host.png)

改好了, 但好像沒反應, 使用`curl http://j2hongming.dev`可以但使用瀏覽器不行QQ

查了一下似乎是因為HSTS, 目前還沒仔細研究這個東西, 等我們幫HTTP加上s再來試試

### 參考
- [一台主機但需要架設兩個以上的網站 - Amazon EC2 Ubuntu 設定 Apache Virtual Hosts](https://diary.taskinghouse.com/posts/664386-amazon-ec2-ubuntu-setup-apache-virtual-hosts/)
- [How To Set Up Apache Virtual Hosts on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-18-04)
- [通用頂級域](https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E9%A0%82%E7%B4%9A%E5%9F%9F)
- [How to set the default virtual host on Apache 2?](https://www.digitalocean.com/community/questions/how-to-set-the-default-virtual-host-on-apache-2)
- [Hosts檔案](https://zh.wikipedia.org/wiki/Hosts%E6%96%87%E4%BB%B6)
- [Google Chrome redirecting localhost to https](https://stackoverflow.com/questions/25277457/google-chrome-redirecting-localhost-to-https/28586593#28586593)
