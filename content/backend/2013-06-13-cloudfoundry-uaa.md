Title: UAA 和login-server
Date: 2013-06-13 10:00
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/uaa
Keyword: good
Summary: 

## 概述
UAA的设计理念是要实现一个统一的用户认证和权限管理中心，设计思想和全部API见官方的[UAA文档](https://github.com/cloudfoundry/uaa/tree/master/docs)

它提供了几十个API来实现应对不同场景下的用户管理，token分发，client管理。

下图说明了各种组件在UAA中的配合关系

<img src="http://blog.cloudfoundry.com/wp-content/uploads/2013/02/uaa-environ.png"  alt="" width="600" height="350"/>

* UAA可以配置若干Client，每个Client可以有一个权限范围
* 


坦白的说 UAA的所有API我们也没全部弄清楚，而且也完全没有必要修改UAA，所以我们没怎么研究UAA的实现逻辑，只需要知道UAA负责生成token并分发token, CC的验证是通过对称解密token实现的，解密token可以得到用户的信息。我们只需要知道获取token的接口就可以了。

UAA本身的UAADB里面可以存储用户的各种信息，如果不需要使用其他的帐号系统，UAA完全可以独立使用。但如果你需要自定义，比如使用LDAP帐号系统作为验证，只需要自己实现一个login-server，在CC的配置里面配置好login为这个login-server的地址，那么在输入cf login的时就是login-server来处理了。

login-server要做什么事情呢？

* 实现LDAP的登录逻辑
* 











