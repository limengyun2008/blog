Title: Health Manager
Date: 2013-06-13 10:00
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/hm
Keyword: good
Summary: 


Health Manager (简称HM) 主要负责监控app的状态，确保已经启动的app处于running状态，以及这些app的版本和instance数量是正确的。
这些确保机制主要是通过维护应用状态实现的，每个app有一个Actual State 实际运行状态，用来比较它和app的Desired State 期望状态。
当不匹配的情况出现的时候，就要把app的状态调整到期望状态，比如通过start/stop命令来控制missing/extra的instance。

HM也收集和提供app的统计信息，这些统计信息由CC获取和使用。

HM并不是必要的，失去HM的影响仅仅是crash的应用无法自动重启。


## HM对instance的调整策略
调整主要出现在两种情况下：

* 对Nats信息的反应，比如droplet.exited
* 周期性的获取app的状态，寻找异常

## droplet.exited 信号
有三种场景下 droplet.exited会接收到：

* app被显式地stop了，这种情况不需要对app进行调整
* DEA撤离。当有DEA撤离的时候，属于该DEA的instance应该在其他地方重启，HM应该初始化这个重启。
* app崩溃。崩溃的instance应该被重启，除非这个instance短时间内崩溃多次，就会被标识为flapping。

## flapping instance
app的一个instance当在flapping_timeout的秒数内崩溃了flapping_death次就会被标记为flapping。可能的原因有：

* instance已经完全毁坏，最直接的无法启动了
* instance有bug导致每过一会就崩溃
* instance依赖外部世界的服务或者CF提供的服务，当这个依赖不可用的时候导致instance反复崩溃

原理上讲，HM会尽最大努力在避免IO冲突的情况下去重启flapping instance，同时切断彻底崩溃的instance占用的资源。为了实现这些，有下列可以配置的策略：

* 根据min_restart_delay配置的秒数作为delay来初始化instance的重启
* 对于每次崩溃，delay翻番，但是不会超过max_restart_delay配置的秒数
* 每次计算delay都会加入一个随机的噪音，噪音数不会超过delay_time_noise配置的秒数
* 如果flapping instance崩溃的数量超过giveup_crash_number，就放弃该instance的重启。

##　Heartbeat 处理
DEA周期性的会把heartbeat信息发送到Nats总线上。这些heartbeat包括了DEA的识别消息和所有该DEA上的instance的信息。
heartbeat会被用来管理missing和extra 的instance。Missing instance会被要求启动，extra的instance会被要求停止。Droplet对象会跟踪自身每个instance的heartbeat的每个version。
一个当前version的instance如果没有在droplet_lost的秒数内收到heartbeat就被认为是missing。
以下是一个有3个Running的Instance的heartbeat的实例：

    {"timestamp":1371542789.3913922,"message":"Actual: #process_heartbeat: {\"droplets\":[ {\"cc_partition\":\"ng\",\"droplet\":\"26b2ba8b-5143-46c9-9a9c-4d336066bf54\",\"version\":\"2c7d4ccf-825e-4883-aa9fd6d7572df84f\",\"instance\":\"ad250f48ff181f1b97df1233914bb419\",\"index\":0,\"state\":\"RUNNING\",\"state_timestamp\":1371389265.22629},
    {\"cc_partition\":\"ng\",\"droplet\":\"cb58ffe4-4161-4b88-aa89-8c2681695f44\",\"version\":\"e60abbbf-ca23-4e33-97269fc0eeb20cab\",\"instance\":\"a0f8fc83aed024712e0f6cbdfb79df87\",\"index\":0,\"state\":\"RUNNING\",\"state_timestamp\":1371389245.8968444},
    {\"cc_partition\":\"ng\",\"droplet\":\"517dda82-e5bc-4d1d-b7b5-18bdae4257ad\",\"version\":\"08764835-78a1-426c-b17abd7c492b0768\",\"instance\":\"d762b1a691ceb94b09f5a975357e562a\",\"index\":0,\"state\":\"RUNNING\",\"state_timestamp\":1371533092.2616484}],
    \"dea\":\"0-ed133b25d81b3805ac63d1c2d31b90b3\",\"prod\":false}","log_level":"debug","source":"hm","data":{},"thread_id":10743820,"fiber_id":12336320,"process_id":28730,"file":"/home/vcap/health_manager/lib/health_manager/actual_state.rb","lineno":86,"method":"process_heartbeat"}

## HM的配置

HM是为数不多的在centos上能修改几个配置就能无脑正常运行的cloudfoundry组件之一（还有一个就是gorouter）

但有几点要注意：
HM在源文件constants.rb里提供了一套缺省的配置，值得注意的是HM缺省配置中cc_partition是default，
而CF 2.0组件cloud_controller 启动时缺省的配置是cc_partition=ng，这种情况下HM不会跟CC有任何交互，
我们猜测可能的原因是有一段时间1.0和2.0的CC共存，
所以需要用这个东西告诉HM将这两个不同的版本区分开

新增一行 cc_partition=ng (或者您为cc启动时配置的值)

bulk_api下host 要填写CC的域名或者IP








