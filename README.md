# personal blog

Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/#summary)

## blog building tool

- hexo: 7.3.0
    - nodejs: 20.18.1
    - [nvm](https://github.com/nvm-sh/nvm):
    - theme: [cactus](https://github.com/probberechts/hexo-theme-cactus)
- comments system
    - [utterances](https://utteranc.es/)
- analytics
    - [umami](https://eu.umami.is)
- seo
    - Google Search Console
    - [試著學 Hexo - SEO 篇 - Google Search Console](https://ithelp.ithome.com.tw/articles/10249885)
    - [試著學 Hexo - SEO 篇 - SEO 觀念補充](https://ithelp.ithome.com.tw/articles/10250681)
    - [Hexo搜尋引擎優化 | 是 Ray 不是 Array](https://israynotarray.com/hexo/20190514/2072033203/)
    - [輕鬆地提交 Hexo 部落格的 Sitemap.xml 到 Google Search Console - Askie's Coding Life](https://askie.today/upload-sitemap-google-search-console-seo-hexo-blog/)
    - errors
        - [Hexo Sitemap 建立索引 無法擷取 | KentDoIt](https://kentdoit.github.io/hexo/2629412870/)
        - wrong url: [Hexo 添加Keywords和提交Sitemap到Google的心得 | nereuseng](https://nereuseng.github.io/2017/10/05/Hexo-sitemap-and-Keywords/)
        - sitemap format for Google Search Console: [Hexo 搭建系列 - SEO優化篇 | 雲沐居](https://zenreal.github.io/posts/7993/#google%E7%84%A1%E6%B3%95%E8%AE%80%E5%8F%96sitemap-%E4%B8%80%E8%88%AC%E7%9A%84http%E9%8C%AF%E8%AA%A4-%E8%A7%A3%E6%B1%BA%E6%96%B9%E5%BC%8F)

### nvm
``` bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
nvm ls-remote
nvm install 20.18.1
nvm use 20.18.1
node -v
```

### hexo

for new environment
``` bash
npm install -g hexo-cli
cd j2hongming.github.io
npm install
```

if rss feed is required
``` bash
# https://github.com/hexojs/hexo-generator-feed
npm install hexo-generator-feed --save
```

if local search is required
``` bash
# https://github.com/Wzpan/hexo-generator-search
npm install hexo-generator-search --save
```

if seo is required
``` bash
# https://github.com/hexojs/hexo-generator-sitemap
npm install hexo-generator-sitemap --save
```

post, test and verify on local
``` bash
hexo new post "update blog flow"
hexo generate
hexo server
```

## build the github page
- [GitHub Pages | Hexo](https://hexo.io/docs/github-pages.html)
