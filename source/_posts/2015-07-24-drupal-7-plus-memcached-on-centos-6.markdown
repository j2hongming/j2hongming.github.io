---
layout: post
title: "Drupal 7 + Memcached on CentOS 6"
date: 2015-07-24 17:24:34 +0800
comments: true
categories:
- Linux
- Drupal7
- Memcache 
---

- 安裝Memcached
- 設定Memcached
- 安裝Memcached PHP extension(PECL Memcache)
- 設定Memcached PHP extension
- 安裝Drupal 7 memcache 模組
- 設定Drupal 7 setting.php
- 注意事項
<!-- more -->
##  Memcached  ##
### 安裝Memcached ###

{%codeblock%}
yum install memcached
{% endcodeblock %}

### 設定Memcached ###

設定 /etc/sysconfig/memcached
注意OPTIONS="-l 127.0.0.1"

## Memcached PHP extension ##
### 安裝Memcached PHP extension ###
指定版本
{%codeblock%}
sudo pecl install channel://pecl.php.net/memcache-3.0.6
{%endcodeblock%}

### 設定Memcached PHP extension ###
設定/etc/php.d/memcache.ini

開啟hash相關設定
{%codeblock%}
memcache.hash\_strategy=consistent
{%endcodeblock%}

## Drupal 7 ##
### 安裝Drupal 7 memcache 模組 ###
[Memcache API and Integration](https://www.drupal.org/project/memcache)

### 設定Drupal 7 setting.php ###
{%codeblock%}
$conf['cache_backends'][] = 'sites/all/modules/memcache/memcache.inc';
// The 'cache_form' bin must be assigned no non-volatile storage.
$conf['cache_class_cache_form'] = 'DrupalDatabaseCache';
$conf['cache_default_class'] = 'MemCacheDrupal';
$conf['memcache_key_prefix'] = 'something_unique';
// Don't bootstrap the database when serving pages from the cache.
$conf['page_cache_without_database'] = TRUE;
$conf['page_cache_invoke_hooks'] = FALSE;

$conf['memcache_stampede_protection'] = TRUE;
$conf['lock_inc'] = 'sites/all/modules/memcache/memcache-lock.inc';

{%endcodeblock%}


## 注意事項 ##
1. 若memcache service有起來，Druapl卻沒連到，注意防火牆設定

## Ref ##
- [Drupal 7 Memcache Tutorial](https://www.drupal.org/node/1131468)
大致流程說明
- [Memcached and PECL memcache on CentOS and Fedora](http://tag1consulting.com/blog/memcache-centos-fedora)
CentOS安裝注意事項
- [Install Memcached (Caching Server) on RHEL/CentOS 6.3/5.8 and Fedora 17-12](http://www.tecmint.com/install-memcached-caching-server-on-rhel-centos-fedora/)
安裝流程與指令(推薦)
- [Chapter 16. Alternative Storage and Cache Backends](http://chimera.labs.oreilly.com/books/1230000000845/ch16.html)
觀念
- [Drupal Memcached中文教學](http://www.hellosanta.com.tw/Drupal%E7%B6%B2%E7%AB%99%E8%A8%AD%E8%A8%88/drupal-memcached)
