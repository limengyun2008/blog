Title: Cloud Controller
Date: 2013-05-29 10:20
Category: backend
Tags: cloudfoundry
Slug: backend/cloudfoundry-cloud_controller
Summary: 介绍Cloud Controller

Cloud Controller 是整个cloudfoundry平台的控制中心。它对外提供api，所有的操作都是依赖这些api来进行的。
这里是详细的api列表：http://docs.cloudfoundry.com/docs/reference/cc-api.html
同时在项目的根目录的docs目录下有详细的设计文档。

Cloud Controller 2.0引入了多个新概念，如Organizations，Spaces，Domains，Routes
这篇官方文档http://docs.cloudfoundry.com/docs/using/managing-apps/orgs-and-spaces.html可以很好的帮助你理解这些概念。

直接使用这些API还是比较费劲的，官方和第三方都有不同语言的基于这些api的lib，比如官方的ruby lib为CFoundry（https://github.com/cloudfoundry/cfoundry）。
进行更上层开发的时候可以基于这些lib而不是直接操作api，会省下不少时间。官方的客户端cf也是基于cfoundry进行的开发。

## 安装
TBD

## 配置
TBD

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
