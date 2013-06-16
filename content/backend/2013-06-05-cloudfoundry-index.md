Title: cloudfoundry 2.0文档小结
Date: 2013-06-05 10:00
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/index
Summary: Hello, World!


不知不觉进入新的new-tech组鼓捣cloudfoundry已经几个月了，项目的起因是youdao之前已经有一个youdao App Engine，主要供内部使用，仅支持php语言，
用来快速实现一些简单需求。但处于无人维护的状态，加入newtech组后，david问我能不能接过来然后改进一下，让它能支持更多语言。

但原有YAE强依赖了PHP的语言特性,所有的YAE的app都是一个apache在serve, 前端nginx将*.domain.com的二级域名前缀转换成path然后由apache来提供服务。
但很多语言的应用部署都是基于独立占用一个端口的方式，新增加语言支持实际上就是要重新设计一套机制，等于做一个PaaS。

> SaaS（Software as a Service）: 软件即服务，极其常见的形式：如gmail，云笔记等

> PaaS（Platform as a Service）: 提供应用运行的平台作为服务。最早的有GAE：Google App Engine 国内发展的比较好的还有SAE, 剩下的基本不知名。

> IaaS（Infrastructure as a Service）: 提供基础架构作为服务。多数开源的云计算项目都位于这一层，例如openstack等等。商业的国外有最著名的amazon。国内有阿里云，盛大云等。

在调研了不同项目之后，我接触到了cloudfoundry：

* 第一个开源的paas，来自vmware。
* 天然分布式，而且可以很方便的添加语言支持
* 已有appfog这种基于它开发的商业项目。自身也已经有公有paas对外提供服务。

最终我选择了基于cloudfoundry搭建一个paas，然后再在其上层实现原有的YAE提供的功能的方案。

## 安装

有可能我是唯一一个采用这种办法安装cloudfoundry的人：使用**各个组件的源代码**在**centOS 6**上搭建cloudfoundry 2.0。之所以这么做，原因见下：

2012年十一月开始的时候，cloudfoundry 1.0和2.0都在同时开发中，1.0已有公有云，文档稍多，且提供了一个部署脚本部署所有的组件到一台机器上；2.0则基本没有任何文档。我选择了1.0作为研究对象，
但cloudfoundry 1.0的脚本只支持部署在ubuntu上，而公司的机器只有centos，在我解决掉一个又一个在centos上特有的bug成功的将cloudfoundry 1.0运行在centos上没多久，
我就在官方的google group上的一个回帖中得知1.0不再进行开发。而很多特性只有2.0才有。这个时候我再转向2.0等于重新开始。

对于最新的2.0，官方仅给出了一种部署方式——基于Iaas和官方开发的用于操作IaaS的一个名为bosh的工具的部署方式。这个需要有openstack，Vsphere 等IaaS作为支持，可公司也没有。

在这种背景下，如果想继续使用cloudfoundry，只有三种方案：

1. 使用cloudfoundry 1.0
2. 先搭一个openstack，用熟了再基于官方提供的部署方式进行安装
3. 自己鼓捣源码，在centOS上自己装

1等于以后都自己玩，2不属于自己的工作范围，等于是一个研发去弄运维的事情。权衡利弊之后选择了方案3，但是在这个过程中同样遇到了很多centOS上特有的问题。

在解决问题的过程中，我们记录了一些文档，放在github上： [链接](https://github.com/youdao-cf/docs/tree/master/install) 上，简单描述如何在centos上安装cloudfoundry并进行配置.

总体来说，如果是ubuntu系统（最好是10.04）基本所有组件都可以正常运行，如果运行不起来就是配置问题，需要特别注意的会在下面各组件细节中提到。

但如果是其他linux发行版，除了配置问题，还会碰到各种因为操作系统引起的bug，有一些需要修改源代码，所有修改的源码地址都在安装文档中给出，在组件细节中也会提出修改的思路。

同时声明一点：**不要指望按照这篇文档能直接毫无问题的搭出cloudfoundry 2.0**

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

CloudFoundry是一个多模块的分布式系统，支持模块自发现，错误自检，且模块间低耦合。其核心原理就是基于消息发布订阅机制。

而NATS则是支持这个机制的最关键的消息系统，它是cloudfoundry中最核心的组件。

[nats链接组件的两个例子](./nats.html)


#### Router
负责处理分发所有的请求到相对应的模块，包括来自外部用户对app的请求和平台内部控制请求。

#### Cloud Controller
Cloud Controller是CloudFoundry的管理模块。对外提供平台全部的api，如：

1. 对apps的增删改读；
2. 启动、停止应用程序；
3. Staging apps（把apps打包成一个droplet）；
4. 修改应用程序运行环境，包括instance、mem等等；
5. 管理service，包括service与app的绑定等；
6. Cloud环境的管理；
7. 修改Cloud的用户信息；
8. 查看Cloud Foundry，以及每一个app的log信息。

#### Warden
warden 在操作系统上层提供轻量级的运行应用的虚拟容器，为平台提供安全支持。

[warden及平台安全](./warden.html)

#### DEA 
接收来自cloud controller的指令，根据指令使用warden提供的虚拟容器对应用进行打包，运行等关键操作。

[dea和buildpack](./dea.html)

#### UAA
全称是User Account and Authentication，负责用户账户和验证

#### Health Manager
负责检查各个组件的状态


#### 其他组件
* Services: cloudfoundry为应用提供的各类服务，如mysql，memcached，由于时间原因，我暂时没有支持。
* Syslog Aggregator：归集log的组件，非必要，也没有支持
* Collector： 监听nats中的各类消息来监控各组件的运行状态，非必要，也没有支持。


#### 自行开发的组件

* console： cloudfoundry的web界面。官方一直到6月10号才有web界面。
* mysql
* monitor

[总结](./review.html)






