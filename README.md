# personal blog

Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/#summary)

## blog building tool

- hexo: 7.3.0
    - nodejs: 20.18.1
    - [nvm](https://github.com/nvm-sh/nvm):
    - theme: [cactus](https://github.com/probberechts/hexo-theme-cactus)
- comments system
    - [utterances](https://utteranc.es/)

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

post, test and verify on local
``` bash
hexo new post "update blog flow"
hexo generate
hexo server
```

## build the github page
- [GitHub Pages | Hexo](https://hexo.io/docs/github-pages.html)
