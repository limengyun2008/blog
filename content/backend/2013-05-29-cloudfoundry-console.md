Title: Console
Date: 2013-05-29 10:20
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/console
Summary: 

在写这篇文章的前两天，cloudfoundry 2.0 的官方云出品了。伴随着一个web console：[地址](http://run.pivotal.io/)

我们自己也开发了一个console……

## 咱的console有哪些不同？

可以先用用官方的，然后再看视频……


在cloudfoundry api的框架范围内，我们赋予了更多的功能适应内部使用的需要。

首先，登录使用LDAP，不提供注册功能。当然这是属于login-server的修改范畴。

第二，屏蔽了space的概念，首次登录默认创建与LDAP账号相同的organization，在这个organization下创建一个名为default的space，
space对用户不可见，但用户所有的app都被放置在default space中，所以感觉上是应用都是直接归属于organization。 这样设计是感觉两层的权限对内部使用还是太繁琐了

第三，用户可以在web上直接一键创建应用，而不用跟官方console一样，还需要使用cf命令行。
且应用一旦创建便绑定一个svn代码地址，修改svn之后，在web上输入版本号便可以更新应用。

第四，个人觉得长得漂亮，更直观……

当然，时间原因，先做demo，代码基本没进行边界和错误处理，请勿吐槽。
