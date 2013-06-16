Title: 用pelican搭建自己的博客
Date: 2013-05-29 09:20
Category: misc
Tags: pelican
Slug: backend/blogging-with-pelican
Summary: 使用pelican搭建一个纯静态博客

## 什么是pelican

pelican是一个用python写的开源的博客系统，类似ruby的jekyll/otcopress。这一类博客都属于static site generator，工作原理就是直接使用markdown等结构化文本语言撰写博客内容之后再使用脚本配合定制的CSS/JS及templates文件生成一个静态站点,很对我的胃口。最早接触的static site generator就是otcpress，但个人用python习惯之后实在是不习惯ruby的语法，在一番折腾之后终于找到了一个python版的otcopress——pelican。

<b>这个博客就是使用的pelican</b>

## requirements
* linux
* python 2.7.3
* python pip
* git

## 安装
    pip install pelican # 3.2.1
    pip install ghp-import # 为了使用github pages

## 写博客

    pelican-quickstart

会生成一个文件夹，在contents 目录下创建后缀名为.md的文件，就可以使用markdown写博客了，当然,文件里面还是需要有一些必要的metadata的。给一个示例的文件
    
    :::Markdown
    Title: Hello, World!
    Date: 2013-01-01 00:00
    Category: misc
    Tags: pelican
    Slug: helloworld
    Summary: Hello, World!
    
    ## Hello, World!
    
    this is a template for article.

## 部署
文件保存之后执行

    make html

会生成一个output 文件夹，里面是一个完整的静态页面站点，你可以用讲output上传到自己的服务器即可提供服务了。

如果想要使用github pages服务，则需要将使用站点的源代码创建一个github代码库。
在pelicanconf.py所在目录执行以下命令

    make github

比otcopress方便不少。

###还有很多高级用法请参见<a href="http://getpelican.com/">Pelican官方文档</a>
