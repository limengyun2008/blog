Title: 解决ssh broken pipe的问题
Date: 2013-05-30 10:20
Category: backend
Tags: linux
Slug: backend/ssh-broken-pipe
Summary: 解决在ssh连接在长时间不输入命令会自动断开出现broken pipe的问题

ssh连接在长时间不输入命令之后会出现连接中断的情况，即broken pipe的错误。

解决办法有两个

## 在服务器端修改ssh server的配置

    vi /etc/ssh/sshd_config
    
增加一行

    ClientAliveInterval 60

表示每60s发送一次心跳包。如果还想要在100次心跳包之后断开（即6000秒之后断开），可以再增加一行

    ClientAliveInterval 100
    
这两个配置的详细含义，摘抄自<b>man sshd_config</b>

    ClientAliveCountMax
             Sets the number of client alive messages (see below) which may be sent without
             sshd(8) receiving any messages back from the client.  If this threshold is reached
             while client alive messages are being sent, sshd will disconnect the client, termi‐
             nating the session.  It is important to note that the use of client alive messages
             is very different from TCPKeepAlive (below).  The client alive messages are sent
             through the encrypted channel and therefore will not be spoofable.  The TCP
             keepalive option enabled by TCPKeepAlive is spoofable.  The client alive mechanism
             is valuable when the client or server depend on knowing when a connection has become
             inactive.

             The default value is 3.  If ClientAliveInterval (see below) is set to 15, and
             ClientAliveCountMax is left at the default, unresponsive SSH clients will be discon‐
             nected after approximately 45 seconds.  This option applies to protocol version 2
             only.

    ClientAliveInterval
             Sets a timeout interval in seconds after which if no data has been received from the
             client, sshd(8) will send a message through the encrypted channel to request a
             response from the client.  The default is 0, indicating that these messages will not
             be sent to the client.  This option applies to protocol version 2 only.

    
    
    
## 如果没有服务器端的权限，可以修改ssh client的配置    

    vi /etc/ssh/ssh_config  #  对全部用户生效
    
或者

    vi ~/.ssh/config #  对当前用户生效
    
增加一行

    ServerAliveInterval 60
    
同样也可以增加ServerAliveCountMax来实现多少秒之后断开连接

    ServerAliveCountMax 10

表示600秒之后断开

这两个配置的详细含义，摘抄自<b>man ssh_config</b>

    ServerAliveCountMax
             Sets the number of server alive messages (see below) which may be sent without
             ssh(1) receiving any messages back from the server.  If this threshold is reached
             while server alive messages are being sent, ssh will disconnect from the server,
             terminating the session.  It is important to note that the use of server alive mes‐
             sages is very different from TCPKeepAlive (below).  The server alive messages are
             sent through the encrypted channel and therefore will not be spoofable.  The TCP
             keepalive option enabled by TCPKeepAlive is spoofable.  The server alive mechanism
             is valuable when the client or server depend on knowing when a connection has become
             inactive.

             The default value is 3.  If, for example, ServerAliveInterval (see below) is set to
             15 and ServerAliveCountMax is left at the default, if the server becomes unrespon‐
             sive, ssh will disconnect after approximately 45 seconds.  This option applies to
             protocol version 2 only; in protocol version 1 there is no mechanism to request a
             response from the server to the server alive messages, so disconnection is the
             responsibility of the TCP stack.

    ServerAliveInterval
             Sets a timeout interval in seconds after which if no data has been received from the
             server, ssh(1) will send a message through the encrypted channel to request a
             response from the server.  The default is 0, indicating that these messages will not
             be sent to the server, or 300 if the BatchMode option is set.  This option applies
             to protocol version 2 only.  ProtocolKeepAlives and SetupTimeOut are Debian-specific
             compatibility aliases for this option.
