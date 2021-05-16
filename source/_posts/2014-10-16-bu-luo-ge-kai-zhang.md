---
layout: post
title: "部落格開張Markdown Demo"
date: 2014-10-16 16:22:49 +0800
comments: true
categories: lab
tags:
- markDown
- blog
---
- Sharing Code Snippets
- Quote
- List
- Email
- Atx Format Header
- Setext Format Header
- Break Line
- Link
<!-- more -->
[Markdown Syntax](http://markdown.tw/)
[Markdown Syntax 2](http://genius.com/Genius-formatting-and-markdown-guide-annotated)

## Sharing Code Snippets ##
### Example  1 ###
{% codeblock PHP echo-hello.php lang:php http://php.net/manual/en/function.echo.php %}
echo '部落格開張';
{% endcodeblock %}

### Example  2###
[Octopress: Sharing Code Snippets](http://octopress.org/docs/blogging/code/)
{% codeblock  lang:html %}
<!DOCTYPE html>
<html>
<body>

<h1>My First Heading</h1>

<p>My first paragraph.</p>

</body>
</html>
{% endcodeblock %}

### Example 3
[Octopress: Sharing Code Snippets](http://octopress.org/docs/blogging/code/)
>\`\`\` [language] [title] [url] [link text]
>code snippet
>\`\`\`


``` ruby Discover if a number is prime http://www.noulakaz.net/weblog/2007/03/18/a-regular-expression-to-check-for-prime-numbers/ Source Article
class Fixnum
  def prime?
    ('1' * self) !~ /^1?$|^(11+?)\1+$/
  end
end
```

### Example 4: gist embed
\{ % gist 89c858fdf4fd510fd910787a64eb9f04 % \}

{% gist 89c858fdf4fd510fd910787a64eb9f04 %}

## Quote ##
### Example 1 ###
[Octopress: Blockquote](http://octopress.org/docs/plugins/blockquote/)
>Stay hungry, Stay foolish. -Steve Jobs

>A apple a day, keep the doctor away
>>May I help U?

>1. First
>    Line
>2. Two
>    Line

### Example 2 ###
{% blockquote Douglas Adams, The Hichhikers Guide to the Galaxy %}
Flying is learning how to throw yourself at the ground and miss.
{% endblockquote %}

## List ##
### Example ###
#### TODO List ####
- open
- *hadle em*
- **\*strong\***
  1. s1
  2. s2
  3. s3

## Email ##
### Example ###
<address@example.com>

# Atx format Header L1#
## Example
## Header L2
### Header L3
#### Header L4
##### Header L5
###### Header L6

This is an Setext Format  H1
=============
### Example
This is an  Setext Format  H2
-------------

Break Line
============
Example
-------------
BreakLine
- - -
* * *
--------------

Link
============
### Example 1: Inline
This is [an example](http://example.com/ "Title") inline link.

### Example 2: Ref
This is [an example] [id] reference-style link.

[id]: http://example.com/  "Optional Title Here"
