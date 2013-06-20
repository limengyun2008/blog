Title: warden及平台安全
Date: 2013-06-13 00:00
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/warden
Summary: 


warden 是整个cloudfoundry平台的基石。它负责最关键的资源控制——包括cpu，mem，disk等。
资源控制直接关系到如何让多个应用之间直接互不干扰，以及阻止恶意代码的执行，从而保证平台的安全性。
虚拟机可以很好的隔离，但这个解决方案对于隔离一个应用就显得太重量级了。

有一种基于linux系统内核的资源隔离技术
> Resource control is done by using [Control Groups](http://kernel.org/doc/Documentation/cgroups/cgroups.txt). Every container is placed in its own control group, 
where it is configured to use an equal slice of CPU compared to other containers, and the maximum amount of memory it may use.

著名的开源资源控制项目Linux Containers(LXC)基于cgroups开发的。 
Linux Container容器是一种内核虚拟化技术，可以提供轻量级的虚拟化，以便隔离进程和资源，而且不需要提供指令解释机制以及全虚拟化的其他复杂性。
容器有效地将由单个操作系统管理的资源划分到孤立的组中，以更好地在孤立的组之间平衡有冲突的资源使用需求
简单的讲就是创建一个容器之后可以让一个进程运行在一个容器中，使用单独的文件系统，限制的网络和内存资源。
而不是像虚拟机那样相当于在一个容器中运行了一整套操作系统。

早期的warden就是使用的LXC，但后来发现不太能提供外层完整的控制接口，而且LXC的很多功能也并不需要，warden的开发人员就自己实现了一个更满足需求的“container”，仅用了1千行C代码。

我并没有深入研究warden的源代码逻辑，只是局限在它提供给上层的功能上。一般说warden实际上指的是warden server，上层DEA通过warden client来调用warden server提供的api创建并控制container
container可以添加诸多限制，且container之间互相隔离。应用的实例最终在container中运行。

## 安装

[链接](https://github.com/youdao-cf/docs/blob/master/install/warden.html.md)


## 配置

默认的配置大部分都不用修改，除了一个隐藏的配置可能会有问题：

    port:
      pool_start_port: 10000
      pool_size: 10000

在warden/lib/warden/config.rb中对这个配置是这么处理的

    :::ruby
    def self.ip_local_port_range
      File.read("/proc/sys/net/ipv4/ip_local_port_range").split.map(&:to_i)
    end

    def self.port_defaults
      _, ephemeral_stop = self.ip_local_port_range
      start = ephemeral_stop + 1
      stop = 65000 + 1
      count = stop - start

      {
        "pool_start_port" => start,
        "pool_size"       => count,
      }
    end

如果没有在配置文件中定义，则使用/proc/sys/net/ipv4/ip_local_port_range文件中的数值，但是这文件的值是受linux
系统设置影响的，在我的centos VPS上被设置成了65000，那么pool_size就会为0，会报错。

为了保险起见，最好还是在配置文件里面按照上面的示范加上关于port的配置。


## 功能示例

安装完成后，在warden/bin 目录下有一个脚本。它可以用来测试warden所提供的所有功能，也可以用来调试已有的warden container。

    [vcap@yae warden]$ ./bin/warden 

列出正在运行的所有container，一个container可以理解为一个简易的操作系统。

    warden> list
    handles[0] : 16ucmjgeeil
    handles[1] : 16ucmjgeeik
    handles[2] : 16ucket2otf
    handles[3] : 16uci088oas
    handles[4] : 16ucuupdlgb
    handles[5] : 16ucuupdlgt
    handles[6] : 16ucuupdlh3
    handles[7] : 16ucuupdlh5

查看或设置一个container的内存限制

    warden> limit_memory --handle 16ucuupdlh5 
    limit_in_bytes : 603979776

查看在某一个container下运行的程序

    warden> run --handle 16ucuupdlh5 --script "ps xf"
      PID TTY      STAT   TIME COMMAND
      100 ?        Ss     0:00 /bin/bash
      101 ?        R      0:00  \_ ps xf
       22 ?        Ss     0:00 /bin/bash
       23 ?        S      0:00  \_ /bin/bash ./startup -p 10446
       25 ?        S      0:00      \_ /bin/bash ./startup -p 10446
       28 ?        Sl     1:17          \_ /home/vcap/app/.jdk/bin/java -Xss1m -Dresin.home=/home/vcap/app/resin-3.0.21 -Dserver.root=/home/vcap/app/resin-3.0.21 -Djava.util.logging.manager=com.caucho.log.LogManagerImpl -Djavax.management.builder.initial=com.caucho.jmx.MBeanServerBuilderImpl com.caucho.server.resin.Resin -conf /home/vcap/app/resin.conf

上面显示的结果就是一个java应用的进程。

在命令行输入help可以得到warden的全部功能

    warden> help

        copy_in       Copy files/directories into the container.
        copy_out      Copy files/directories out of the container.
        create        Create a container, optionally pass options.
        destroy       Shutdown a container.
        echo          Echo a message.
        info          Show metadata for a container.
        limit_disk    set or get the disk limit for the container.
        limit_memory  Set or get the memory limit for the container.
        link          Do blocking read on results from a job.
        list          List containers.
        net_in        Forward port on external interface to container.
        net_out       Allow traffic from the container to address.
        ping          Ping warden.
        run           Short hand for spawn(stream(cmd)) i.e. spawns a command, streams the result.
        spawn         Spawns a command inside a container and returns the job id.
        stop          Stop all processes inside a container.
        stream        Do blocking stream on results from a job.
        help          Show help.

    Use --help with each command for more information.

详细的功能列表参见warden server源代码下的README文件：[地址](https://github.com/cloudfoundry/warden/tree/master/warden)


## centos TIPS

warden源代码的readme里阐述了container的文件系统的实现方式

> Every container gets a private root filesystem. 
This filesystem is created by stacking a read-only filesytem and a read-write filesystem. 
This is implemented by using aufs on Ubuntu versions from 10.04 up to 11.10, and overlayfs on Ubuntu 12.04.

在centos上没有这两个文件系统，但warden专门为centos做了个适配，使用了默认文件系统做替代，
在创建container的时候把 container文件系统的/目录设置为ro，把 /dev /etc /home /sbin /tmp 等几个目录设置为rw ，（代码如下）

    :::shell
    function setup_fs_other() {
      mkdir -p tmp/rootfs mnt
      mkdir -p $rootfs_path/proc

      mount -n --bind $rootfs_path mnt
      mount -n --bind -o remount,ro $rootfs_path mnt

      overlay_directory_in_rootfs /dev rw
      overlay_directory_in_rootfs /etc rw
      overlay_directory_in_rootfs /home rw
      overlay_directory_in_rootfs /sbin rw

      mkdir -p tmp/rootfs/tmp
      chmod 777 tmp/rootfs/tmp
      overlay_directory_in_rootfs /tmp rw
    }

正常情况下在这几个目录读写文件不会有问题，但是DEA在container中操作的时候会在根目录创建一个目录/app,放置内容
问题就在这: /目录是readonly的  不可能创建得了文件夹。

有人会觉得直接把/设置为rw不就可以了么。warden在centos上是根据一个文件夹（默认为/tmp/warden/rootfs/）作为文件系统模板来创建文件系统的，
设置/为rw会导致文件系统模板收到污染，即任何在container中进行的操作 会直接反映到这个文件夹上。

最后才用了一个笨办法：加上一行代码

    overlay_directory_in_rootfs /app rw

即创建container时新添加一个/app目录为rw。

后来又发现centos 上的container里无法创建软连接。但上层组件dea和buildpack部分代码使用了软链接，导致必须修改这些使用到了软链接的与warden相关的代码。
那既然这样，上面的做法就没有必要了，因为如果使用centos上的warden，不论如何都要修改上层dea代码，
还不如彻底一点，把dea所有在warden container中的操作都在/home/vcap/app目录下进行，不再创建根目录下的/app，
同时也不要使用任何软链接。这样warden就可以完全不用修改，保持跟官方的一致。
但目前为止，我们仍然采用的是修改后的warden代码以保证上层代码不出错。

dea强依赖warden，但在非ubuntu系统上warden和dea无法正常协同运行，这应该是阻碍大部分人在其他平台上成功运行cloudfoundry的原因。


