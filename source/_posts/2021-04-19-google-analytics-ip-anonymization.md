---
title: Google Analytics IP 去識別化功能
comments: true
date: 2021-04-19 23:34:15
description:
categories: software_development
tags:
- google_analytics
---

IP 去識別化功能的效果
> 會在 IP 位址傳送到 Google Analytics (分析) 後，立即在記憶體中將 IPv4 使用者 IP 位址的最後八位元及 IPv6 位址的最後 80 個位元皆設為零。在此情況下，完整 IP 位址絕對不會寫入磁碟


啟用的方式

```
gtag('config', '<GA_MEASUREMENT_ID>', { 'anonymize_ip': true });
```

## 參考
- [Google Analytics (分析) 中的 IP 去識別化 (或 IP 遮蓋)](https://support.google.com/analytics/answer/2763052?hl=zh-Hant)
- [IP anonymization with gtag.js](https://developers.google.com/analytics/devguides/collection/gtagjs/ip-anonymization)
