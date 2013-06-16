Title: NATS
Date: 2013-05-29 10:20
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/nats
Summary: an article for cloudfoundry architecture

NATS是一个轻量级的基于pub-sub机制的分布式消息队列系统，它负责衔接各组件。官方文档在这里：(http://docs.cloudfoundry.com/docs/running/architecture/messaging-nats.html)。

但看完官方文档仍然有点不太直观，举几个典型的例子来说明：


## 向router注册
不管是外部用户对平台上的应用发起的请求，还是内部组件提供对外的api（uaa和cloud controller），都是通过router转发的request，要能让router转发则首先需要向router注册。
以下是实现逻辑：

* router启动时，会订阅 **router.register** 这个channel，同时也会定时的向 **router.start** 这个channel发送消息，
* 其他需要向router注册的组件，启动时会订阅**router.start**这个channel。一旦接收到消息，会立刻收集需要注册的信息（如ip，port等）然后向router.register频道发送消息。
* router接收到**router.register**消息后立即更新路由信息。
* 以上过程不停循环，使router的状态时刻保持最新。


## cloud controller指挥dea进行打包和运行。

* 所有组件，包括dea启动时，会生成一个唯一的UUID，来标识组件。dea会定时的将自身情况和ID发送到**stager.advertise** 和 **dea.advertise**这两个channel，同时会订阅
**staging.<uuid\>.start** 和**dea.<uuid\>.start**这两个channel
* cloud controller 订阅这两个channel 并根据channel的信息构造并时刻更新dea_pool和stager_pool,
* 当有打包或者运行应用的请求时，cloud controller会去查询这两个pool，如果有合适的dea，就会向对应的**[dea|stager].<uuid\>.start**发送消息
* 对应uuid的dea收到消息，根据消息执行打包或运行任务。

还有很多类似的衔接各组件的逻辑，都可以在源码中发现。

这里有一个非官方且不完整的cloudfoundry 1.0的消息说明文档，http://apidocs.cloudfoundry.com/ ，仅供参考。
