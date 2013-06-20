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

## 实践LDAP登录

虽然UAA能够实现用户认证，但如果需要自定义登录比如使用LDAP登录，其实并不需要修改UAA的代码。

由于使用了oauth协议，UAA可以仅仅起一个token分发者的作用，然后将用户认证的部分委托出去。cloudfoundry已经替我们考虑到了这一点。

我们的做法：fork官方的[login-server](https://github.com/cloudfoundry/login-server/) ，然后:

1. 给login-server加上ldap的登录逻辑
2. 当用户第一次登录时，login-server使用admin权限调用CC提供的api，给用户创建一个默认的space和org,分配一个domain。然后把用户的权限

在CC的配置中配置好login的相关项之后，使用客户端或者cfoundry访问cloudfoundry时都会使用login-server作为验证。


## 看看默认的uaa.none能不能创建org??
## login-server配置的权限？？


这一部分实现的并不完美，官方的文档里面有专门给login-server使用的api，而我们也没有用到。


