Title: Cloud Controller
Date: 2013-05-29 10:20
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/cloudcontroller
Summary: 介绍Cloud Controller

Cloud Controller 是整个cloudfoundry平台的控制中心。它对外提供api，所有的操作都是依赖这些api来进行的。
这里是详细的[api列表](http://docs.cloudfoundry.com/docs/reference/cc-api.html)
同时在项目的根目录的docs目录下有详细的设计文档。
 
Cloud Controller 2.0引入了多个新概念，如Organizations，Spaces，Domains，Routes
这篇[官方文档](http://docs.cloudfoundry.com/docs/using/managing-apps/orgs-and-spaces.html)可以很好的帮助你理解这些概念。

Cloud Controller没有太多可讲，就是哪个API收到请求了就干哪些事情，或通过直接请求CCDB数据库，或通过向NATS发送对应的消息，来实现API所应当提供的功能，包括但不限于

1. 对apps的增删改读；
2. 启动、停止应用程序；
3. Staging apps（把apps打包成一个droplet）；
4. 修改应用程序运行环境，包括instance、mem等等；
5. 管理service，包括service与app的绑定等；
6. Cloud环境的管理；
7. 修改Cloud的用户信息；
8. 查看Cloud Foundry，以及每一个app的log信息。

## Cloud Controller 的用户认证

Cloud Controller 2.0 去除了原有的用户认证相关代码，改为使用与uaa配合验证的方式，即uaa负责认证用户之后生成token，然后用户请求Cloud Controller时，
需要将这个token以request header的形式伴随HTTP请求发送。Cloud Controller对称解密token得到用户信息。

    REQUEST: GET http://api.cf2.youdao.com/v2/spaces/1136694c-1bc2-495e-9aac-1b89894a6dcc/summary
    REQUEST_HEADERS:
      Accept : application/json
      Authorization : bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzZjMyMTNmZS1jODMzLTQ4YmMtYTYwZi00ZmM0NTAzODk0ZjAiLCJzdWIiOiJkNmE2M2Q1OC04ZmQ4LTRhNzUtOGZhOC1mNWI2ZDJjOGQwMDAiLCJzY29wZSI6WyJwYXNzd29yZC53cml0ZSIsImNsb3VkX2NvbnRyb2xsZXIud3JpdGUiLCJvcGVuaWQiLCJjbG91ZF9jb250cm9sbGVyLnJlYWQiXSwiY2xpZW50X2lkIjoiY2YiLCJjaWQiOiJjZiIsInVzZXJfaWQiOiJkNmE2M2Q1OC04ZmQ4LTRhNzUtOGZhOC1mNWI2ZDJjOGQwMDAiLCJ1c2VyX25hbWUiOiJsaW15IiwiZW1haWwiOiJsaW15QHJkLm5ldGVhc2UuY29tIiwiaWF0IjoxMzcxMzcyNjQyLCJleHAiOjEzNzE5Nzc0NDIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC91YWEvb2F1dGgvdG9rZW4iLCJhdWQiOlsib3BlbmlkIiwiY2xvdWRfY29udHJvbGxlciIsInBhc3N3b3JkIl19.cd11MxTrbCCpG_5fU9_DV1_bE9Nz_2lQ_c1kari1WXI
      Content-Length : 0
    RESPONSE: [200]
    RESPONSE_HEADERS:
      connection : keep-alive
      content-length : 88
      content-type : application/json;charset=utf-8
      date : Mon, 17 Jun 2013 10:38:41 GMT
      server : nginx
      x-frame-options : sameorigin
      x-vcap-request-id : a9f046ec-9e1d-423d-ae8e-985495504d08
      x-xss-protection : 1; mode=block

因此，Cloud Controller 配置项中的uaa -> symmetric_secret 要和uaa中的密钥保持一致。


真正直接使用这些API还是比较费劲的，官方和第三方都有不同语言的基于这些api的lib，
比如官方的ruby lib为CFoundry（https://github.com/cloudfoundry/cfoundry）。
基于Cloud Controller api进行更上层开发（比如自己实现一个web界面），可以基于这些lib而不是直接操作api，会省下不少时间。官方的客户端cf也是基于cfoundry进行的开发。

## 安装
TBD

## 配置

    -external_domain: api2.vcap.me
    +external_domain: [api.cf2.youdao.com]
    
gorouter在接收注册的时候是数组格式。将默认配置改为数组，不然router会报错。

##　TIPS
Cloud Controller 需要一个数据库（即CCDB），如果你选择mysql，请使用Innodb或其他支持事务处理的引擎，千万记得不要使用默认的MYisAM引擎，因为它不支持事务。

请看lib/cloud_controller/rest_controller/model_controller.rb

    :::ruby
    # Create operation
    def create
      logger.debug "create: #{request_attrs}"

      json_msg = self.class::CreateMessage.decode(body)
      @request_attrs = json_msg.extract(:stringify_keys => true)
      raise InvalidRequest unless request_attrs

      before_create if respond_to? :before_create
      obj = nil
      model.db.transaction do
        obj = model.create_from_hash(request_attrs)
        validate_access(:create, obj, user, roles)
      end

      [
        HTTP::CREATED,
        { "Location" => "#{self.class.path}/#{obj.guid}" },
        serialization.render_json(self.class, obj, @opts)
      ]
    end

可以看到Cloud Controller 的创建或更新都依赖数据库的事务功能：先创建或更新，再判断是不是有权限执行操作。

如果使用了一个不支持事务的数据库，虽然不会报错，但任何无权限的创建或更新都会被执行，留下隐患。
