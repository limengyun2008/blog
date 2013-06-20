Title: DEA 和 buildpack
Date: 2013-06-13 10:00
Category: backend
Tags: cloudfoundry
Slug: cloudfoundry/dea
Keyword: good
Summary: 

## 术语
dea组件的全称是 droplet execution agency， droplet是cloudfoundry自创的一个概念，它是一个app的可运行实例配合实例启停脚本的压缩包。

举例来说，如果我们要让一个php app程序运行，我们将代码下载之后需要做什么呢？

* 首先需要需要下载一个apache，
* 然后配置apache
* 最后将启动命令写入一个脚本。

那如果我们将代码+apache+脚本一起打成一个压缩包，在其他服务器上启动这个应用的多个实例的时候只需要下载这个压缩包之后解压，启动脚本即可。
这个机制也是整个cloudfoundry实现应用分布式的关键。

* 这个压缩包即为 droplet
* 将用户代码和服务器打包压缩生成droplet的过程叫 staging
* 针对不同类型应用专门编写staging程序叫 buildpack
* 解压运行droplet的组件叫dea。

TODO: 这是整个CLOUDFUNDRY 设计最出彩的地方，想想别的PAas 开发新加一门语言是多么费劲？ 而且类似GAE这种开发者还需要去熟悉GAE的SDK，而cloudfoudry就不用。

这也是cloudfoundry比SAE GAE先进的地方。有着极强的扩展性。预留了接口给第三方做扩展。


## dea职责

### staging和running droplet

在1.0中，staging 是由专门的组件stager来完成的，在2.0中去掉了stager改为直接在dea中进行staging。

这是dea最重要的两个职责。

官方专门针对staging和running的流程撰写了文档： <a href="http://docs.cloudfoundry.com/docs/running/architecture/how-applications-are-staged.html">文章链接</a>

如何在众多dea中选择合适的dea来完成任务，是通过消息机制来实现的，参见在[NATS细节](/cloudfoundry/nats.html)中的例子“cloud controller指挥dea进行打包和运行”

### 向router注册使应用实例可以对外提供服务

dea上的应用流量无论有多大，对dea的影响都微乎其微。
因为dea不对外提供服务，dea控制的container才对外提供服务。
router和dea会定时通过NATS通信，dea将dea下的container的ip，host，port等消息报告给router，参见在[NATS细节](/cloudfoundry/nats.html)中的例子“向router注册”


### 查看应用文件

dea启动时会附带启动一个file api server，而dea directory server的启动则是单独进行的，代码在dea/go目录下。
这两个server的区别在于：

dea directory server 启动后会向router注册，即外部可以访问到dea directory server。
所有跟dea相关的上传（上传droplet）和下载（获取各种文件内容，如log文件）都是直接通过dea directory server来进行的。
file api server起一个验证并返回请求真实路径的作用

比如执行cf logs XXX -t命令，表面上看起来是客户端cf向cloud controller发起请求，但实际上是cloud controller 重定向到dea directory server来提供服务的

    Getting logs for 23423 #0>>>
    REQUEST: GET http://api.cf2.youdao.com/v2/apps/de48824b-8243-4218-8b52-d92c974453f8/instances/0/files/logs
    REQUEST_HEADERS:
      Authorization : bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzZjMyMTNmZS1jODMzLTQ4YmMtYTYwZi00ZmM0NTAzODk0ZjAiLCJzdWIiOiJkNmE2M2Q1OC04ZmQ4LTRhNzUtOGZhOC1mNWI2ZDJjOGQwMDAiLCJzY29wZSI6WyJwYXNzd29yZC53cml0ZSIsImNsb3VkX2NvbnRyb2xsZXIud3JpdGUiLCJvcGVuaWQiLCJjbG91ZF9jb250cm9sbGVyLnJlYWQiXSwiY2xpZW50X2lkIjoiY2YiLCJjaWQiOiJjZiIsInVzZXJfaWQiOiJkNmE2M2Q1OC04ZmQ4LTRhNzUtOGZhOC1mNWI2ZDJjOGQwMDAiLCJ1c2VyX25hbWUiOiJsaW15IiwiZW1haWwiOiJsaW15QHJkLm5ldGVhc2UuY29tIiwiaWF0IjoxMzcxMzcyNjQyLCJleHAiOjEzNzE5Nzc0NDIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC91YWEvb2F1dGgvdG9rZW4iLCJhdWQiOlsib3BlbmlkIiwiY2xvdWRfY29udHJvbGxlciIsInBhc3N3b3JkIl19.cd11MxTrbCCpG_5fU9_DV1_bE9Nz_2lQ_c1kari1WXI
      Content-Length : 0
    .  RESPONSE: [302]
    RESPONSE_HEADERS:
      connection : keep-alive
      content-length : 0
      content-type : application/json;charset=utf-8
      date : Sun, 16 Jun 2013 08:51:37 GMT
      location : http://882aa9de3cfa35c4e06a6f5613f0df2d.cf2.youdao.com/instance_paths/b6d11bf2865189aafe0a4be4133688b7?hmac=cc48aa1aa305154ea4e49e8ee33c1ee4a3bbb9ddccd626b73f0a6ed9fe7d6d191a79ecf78b680e5e252ba8948e7ee444029e38ce216a9b828b3898e49dc49a06&path=logs&timestamp=1371372696
      server : nginx
      x-frame-options : sameorigin
      x-vcap-request-id : 76e95020-cd2c-4ba8-b41b-d99e8638e7aa
      x-xss-protection : 1; mode=block


dea directory server 收到类似http://882aa9de3cfa35c4e06a6f5613f0df2d.cf2.youdao.com/instance_paths/b6d11bf2865189aafe0a4be4133688b7?hmac=cc48aa1aa305154ea4e49e8ee33c1ee4a3bbb9ddccd626b73f0a6ed9fe7d6d191a79ecf78b680e5e252ba8948e7ee444029e38ce216a9b828b3898e49dc49a06&path=logs&timestamp=1371372696
这样的请求后会向file api server 发起请求，file api server根据hmac 判断请求是否合法，如果合法就返回log文件在操作系统上的真实地址，最后由dea directory server 返回log的内容。


## 配置

    domain: 你的平台域名。
    
这个配置项在默认配置中没有，但上面提到dea directory server会向router注册对外提供服务，
在lib/dea/directory_server_v2.rb提供给外部访问路径的时候如果domain值为nil，会导致directory server无法被访问。

    def external_hostname
      "#{uuid}.#{domain}"
    end
    
此外，还需要特别注意你的ruby安装路径，配置项中与ruby相关的路径要填对。
 
## 自定义buildpack支持

如果想要cloudfoundry支持一门新的语言或框架，自定义一个buildpack就可以了，
比如我们就将官方的java buildpack修改为支持ant+ivy编译，且从tomcat改为使用resin。
（J2EE架构下一个war包能在resin下跑不一定能在tomcat下跑）
这样就可以直接上传源代码而不用上传war包，且与公司的习惯保持一致。。

每一种语言只有一个buildpack，不同类别的应用打包在buildpack代码里面单独进行区分。
在buildpacks/vendor目录下，官方提供了三种语言（java，nodejs，ruby）的若干种应用类型的支持，同时也提供了一种方便添加自定义buildpack支持的机制。

新增添一个语言的buildpack需要实现以下三个脚本：

* ./bin/detect 检查同一种语言下应用的类型，例如是一个sinatra应用还是一个rails应用，以供compile脚本使用
* ./bin/compile  打包的主脚本，根据detect的结果选择打包的方式。
* ./bin/release  输出自定义的启动命令等相关信息，以便写入到最终的启动脚本。

dea会遍历所有的detect脚本，如果你编写的detect脚本满足条件，就会选择对应的compile脚本执行。

在执行你编写的compile脚本之前，dea已经给创建好了container，然后下载并解压好了代码，compile的内容就是根据这个代码要怎么打包。
按照这个方式，怎么编写compile脚本就取决于你的实际情况，可以使用shell 也可以使用ruby脚本。写之前参考一下已有的buildpack就能了解思路。


####  注意1：

官方或开源第三方的buildpack在staging的时候基本都通过http下载一些东西，比如apache等等，关键在于这些地址都是在amazon s3上。
在天朝的网络下，采用这种方式就要看GFW的心情了，要正常使用最好把那些下载地址全部换成内网地址。

#### 注意2：

有些buildpack 会将/home/vcap/app  软连接到/app/app   然后再在/app/app中进行操作。
但之前在warden中提到过，在centos 6上使用默认文件系统实现的warden container 不具备完整的软连接功能（无法cd进入软连接后的目录，详情见warden的cent OS tip），
所以想要在centos上正常使用仍然需要修改这部分代码。

#### 提示：

http://www.appfog.com 是一个基于cloudfoundry的paas，他自定义了许多语言的buildpack支持并在github上开源出来（github： https://github.com/appfog/ ）。
