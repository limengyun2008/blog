Title: 一些有用的css代码片段
Date: 2013-06-04 11:00
Category: frontend
Tags: css
Slug: frontend/css-templates
Summary: A few useful css templates.
status: draft

收集了一些有用的css模板，以备不时之需。

## css reset
基本每个项目都要用到的……[cssreset](http://www.cssreset.com/) 上有几个模板，有大而全的也有小而精的。我选的 html5 doctor

    :::css
    /** 
     * html5doctor.com Reset Stylesheet
     * v1.6.1
     * Last Updated: 2010-09-17
     * Author: Richard Clark - http://richclarkdesign.com 
     * Twitter: @rich_clark
     */

    html, body, div, span, object, iframe,
    h1, h2, h3, h4, h5, h6, p, blockquote, pre,
    abbr, address, cite, code,
    del, dfn, em, img, ins, kbd, q, samp,
    small, strong, sub, sup, var,
    b, i,
    dl, dt, dd, ol, ul, li,
    fieldset, form, label, legend,
    table, caption, tbody, tfoot, thead, tr, th, td,
    article, aside, canvas, details, figcaption, figure, 
    footer, header, hgroup, menu, nav, section, summary,
    time, mark, audio, video {
        margin:0;
        padding:0;
        border:0;
        outline:0;
        font-size:100%;
        vertical-align:baseline;
        background:transparent;
    }

    body {
        line-height:1;
    }

    article,aside,details,figcaption,figure,
    footer,header,hgroup,menu,nav,section { 
        display:block;
    }

    nav ul {
        list-style:none;
    }

    blockquote, q {
        quotes:none;
    }

    blockquote:before, blockquote:after,
    q:before, q:after {
        content:'';
        content:none;
    }

    a {
        margin:0;
        padding:0;
        font-size:100%;
        vertical-align:baseline;
        background:transparent;
    }

    /* change colours to suit your needs */
    ins {
        background-color:#ff9;
        color:#000;
        text-decoration:none;
    }

    /* change colours to suit your needs */
    mark {
        background-color:#ff9;
        color:#000; 
        font-style:italic;
        font-weight:bold;
    }

    del {
        text-decoration: line-through;
    }

    abbr[title], dfn[title] {
        border-bottom:1px dotted;
        cursor:help;
    }

    table {
        border-collapse:collapse;
        border-spacing:0;
    }

    /* change border colour to suit your needs */
    hr {
        display:block;
        height:1px;
        border:0;   
        border-top:1px solid #cccccc;
        margin:1em 0;
        padding:0;
    }

    input, select {
        vertical-align:middle;
    }

## clear-fix 
一个container内 有若干个元素浮动时，如果不清除浮动会导致后续元素显示样式出错，常规的办法是在需要清除浮动的地方加上一个冗余元素，类似这样：

    :::html
    <div class="container">
        <div class="section">Float</div>
        <div class="section">Float</div>
        <div style="clear:both;"></div>
    </div>



但是现在有个更简单的办法：在container里加上一个class就可以了。

    :::css
    /**
     * For modern browsers
     * 1. The space content is one way to avoid an Opera bug when the
     *    contenteditable attribute is included anywhere else in the document.
     *    Otherwise it causes space to appear at the top and bottom of elements
     *    that are clearfixed.
     * 2. The use of `table` rather than `block` is only necessary if using
     *    `:before` to contain the top-margins of child elements.
     */
    .clear-fix:before,
    .clear-fix:after {
        content: " "; /* 1 */
        display: table; /* 2 */
    }

    .clear-fix:after {
        clear: both;
    }

    /**
     * For IE 6/7 only
     * Include this rule to trigger hasLayout and contain floats.
     */
    .clear-fix {
        *zoom: 1;
    }

html 代码

    :::html
    <div class="container clear-fix">
        <div class="section">Float</div>
        <div class="section">Float</div>
    </div>

原文和DEMO请戳这里：[http://nicolasgallagher.com/micro-clearfix-hack/](http://nicolasgallagher.com/micro-clearfix-hack/)
