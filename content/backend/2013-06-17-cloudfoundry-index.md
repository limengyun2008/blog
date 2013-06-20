Title: cloudfoundry 2.0 on CentOS 6 小结
Date: 2013-06-17 10:00
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/index
Summary: Hello, World!



## 安装

这不是官方安装说明的中文版：这里讲的是使用**各个组件的源代码**在**centOS 6**上搭建cloudfoundry 2.0并进行适当的自定义开发。不论cloudfoundry 1.0还是2.0都有相当一部分源代码基于ubuntu 发行版开发，其他系统上根本运行不起来，但之所以这么做，原因见下：

且对于最新的2.0，官方仅给出了一种基于Iaas的部署方式，大批量的创建ubuntu 虚拟机，然后使用cloudfoundry的发行包（cf-release）批量部署cloudfoundry。

这个需要有openstack，Vsphere 等底层IaaS作为支持，如果没有IaaS, 而且物理机的操作系统也不是ubuntu发行版，但又想继续使用cloudfoundry，只有三种方案：

1. 使用cloudfoundry 1.0 [vcap](https://github.com/cloudfoundry/vcap), 1.0提供了一个脚本来将所有组件安装到一台机器上(实体机和虚拟机都可以)。
2. 先搭一个openstack，用熟了再基于官方提供的部署方式进行安装
3. 自己鼓捣源码，在centOS上自己装

* 方案1：虽然笔者曾经成功将1.0适配到centOS上，但这意味着以后都得不到官方的任何改进，
* 方案2不属于自己的工作范围，等于一个研发去弄运维的事情。

权衡利弊之后选择了方案3，在这个过程中遇到了很多centOS上特有的问题，同时在解决问题的过程中，我们记录了一些文档，放在github上： [链接](https://github.com/youdao-cf/docs/tree/master/install) 上，简单描述如何在centos上安装cloudfoundry并进行配置。
有些做法的理由会在组件细节中说明

总体来说，如果你是ubuntu系统（官方声明最好是10.04）基本所有组件安装后经过合理的配置，都可以正常运行。如何合理的配置在这个系列中博客会提到。

但如果是其他linux发行版，以本文中的centOS为例，除了配置问题，还会碰到各种因为操作系统引起的bug需要修改源代码，在组件细节中也会提出修改的思路。


## cloudfoundry 组件简介

Cloudfoudnry 1.0已于在2013年1月底停止开发与维护。现在网上许多cloudfoundry的文章将的都是跟1.0有关的内容，在此指出一些主要的区别。

* 1.0中router使用的是nginx+lua+ruby server的方式，2.0使用了go语言gorouter，据称支持了websocket且极大提升了性能。
* 2.0中cloud contoller新增了quota，org，space等新的概念，更方便的进行权限和资源管理。
* 1.0中为应用打包使用的是stager组件，2.0中移除了该组件，将打包功能加入到dea中，并将所有语言的打包程序以submodule的形式放在buildpacks/vendors 目录下。
* 完全重写了health manager
* 1.0里 dea可以独立运行，一个dea负责的所有app都以子进程的形式挂在dea主进程下。但2.0之后dea强依赖于warden提供的安全容器来运行app了

下面是cloudfoundry 2.0的架构示意图，

<img src="http://docs.cloudfoundry.com/images/cf_architecture.png" style="width:785px;" alt="cloudfoundry 架构图" />

#### NATS

CloudFoundry是一个多模块的分布式系统，支持模块自发现，错误自检，且模块间低耦合。其核心原理就是基于消息发布-订阅机制。

而NATS则是支持这个机制的最关键的消息系统，它是cloudfoundry中最核心的组件。

整个cloudfoundry的消息channel有上百个，无法在此一一列举，请参考[nats链接组件的两个例子](/cloudfoundry/nats.html)获得对这个组件最直观的印象
 
#### Router
负责处理分发所有的请求到相对应的模块，包括来自外部用户对app的请求和平台内部控制请求。

整个模块的主要逻辑就是处理来自这些请求的处理者的注册请求，注册逻辑已经在NATS中讲过了，不再赘述。router的安装和配置都非常轻松，仅需要修改下NATS的相关配置就可以启动了，参考 [gorouter 的安装和配置](https://github.com/youdao-cf/docs/blob/master/install/gorouter.html.md)

值得一提的是2.0用了go重写了1.0用nginx+lua嵌入脚本的router 改称[gorouter](https://github.com/cloudfoundry/gorouter) 号称比1.0有4X的性能提升，如果属实，go前途无量。


#### Warden
warden 在操作系统上层提供轻量级的运行应用的虚拟容器，为平台提供安全支持。

[warden及平台安全](/cloudfoundry/warden.html)

#### DEA 
接收来自cloud controller的指令，根据指令使用warden提供的虚拟容器对应用进行打包，运行等关键操作。

[dea和buildpack](/cloudfoundry/dea.html)

#### Cloud Controller
Cloud Controller是CloudFoundry的管理模块。对外提供平台全部的api

[Cloud Controller](/cloudfoundry/cloudcontroller.html)


#### UAA
全称是User Account and Authentication，负责用户账户和验证

[UAA](/cloudfoundry/uaa.html)

#### Health Manager
负责检查各个组件的状态

[Health Manager](/cloudfoundry/hm.html)


#### 其他组件
* Services: cloudfoundry为应用提供的各类服务，如mysql，memcached，由于时间原因，我暂时没有支持。
* Syslog Aggregator：归集log的组件，非必要，也没有支持
* Collector： 监听nats中的各类消息来监控各组件的运行状态，非必要，也没有支持。


#### 自行开发的组件

* console： 自行开发的cloudfoundry的web界面，详情：[console](/cloudfoundry/console.html)


总结：给cloudfoundry做centos的适配是个吃力不讨好的事情，费劲千辛万苦DEBUG却并没有添加什么新功能，
但在这个过程中不可避免的需要深入了解cloudfoundry的架构和细节，也算是不小的收获。
纵使以后用BOSH+IaaS安装cloudfoundry遇到bug也会轻松一点，不至于惊慌失措。

另外，我的实习生赵大超主要负责研究UAA和login-server与ldap的集成以及研究HM的机制，相关章节由他贡献。






