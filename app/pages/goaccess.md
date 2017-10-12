title: GoAccess —— 实时日志分析工具
date: 2017-09-05 15:43:36
tags: Tools


无聊中决定分析一下 nginx 的日志玩玩。操起 awk 就开干，但很快就被 awk 的神奇语法打败了( ´◔ ‸◔') 还是用现成的工具吧。

#### GoAccess 简介

简单来说呢 [GoAccess](https://github.com/allinurl/goaccess) 是一个专门用来分析日志的工具，既可以在终端中展示结果，也可以生成 HTML 报表在浏览器中查看。GoAccess 最吸引人的一点就是它生成的 HTML 足够炫酷(ÒωÓױ)。
![炫酷不](/images/goaccess.webp)

<!-- more -->

其他方面的特性包括
1. 数据近乎是实时的——浏览器通过 WebSocket 从服务器上的 GoAccess 实时获取数据；

2. 配置简单；

3. 支持的日志格式多（反正只要支持 nginx 就行(ÒωÓױ)）。

#### 安装
遵循着能用包管理器安装的软件绝不编译的原则，用 Ubuntu 上的 apt 安装后发现版本太旧了，不支持 WebSocket 实时刷新数据，只好从头编译了。

1. 安装依赖库

```bash
$ apt install libncursesw5-dev libssl-dev
```


由于我是通过 https 来访问到 GoAccess 生成的 HTML 的，GoAccess 使用的 WebSocket 也必须使用加密的`wss://` 协议，需要安装 `libssl-dev`，你如果走 http 的话就不用安装这个包了。

2. 下载源码

```bash
$ wget http://tar.goaccess.io/goaccess-1.2.tar.gz
```

为什么不从 GitHub 上克隆呢？因为这个是稳定版，要遵循少踩坑的原则└(￣^￣ )┐

3. 编译

```bash
$ tar -xf goaccess-1.2.tar.gz
$ cd goaccess-1.2/
$ ./configure --enable-utf8 --with-openssl
$ make -j2
$ make install
```

参数 `-j2` 让 `make` 可以同时编译两个文件，这样稍微快一些，我的 VPS 是单核的所以没有开太大(ノДＴ)，还有 不需要走 https 的话可以去掉 `--with-openssl` 选项。


#### 配置
GoAccess 的配置文件在 `/etc/goaccess.conf`，不过我喜欢把配置文件放在 $HOME。

`~/.goaccessrc`
```
time-format %H:%M:%S
date-format %d/%b/%Y
log-format %h %^[%d:%t %^] "%r" %s %b "%R" "%u"

real-time-html true
daemonize true
ssl-cert <cert.crt>
ssl-key <priv.key>
ws-url wss://<your-domain>
port <port>
output /var/www/<xxx>/stat/index.html
```
需要注意的几点
1. 三个 `format` 的设置要与 nginx 的设置一致，当然如果你像我这样根本没改过 nginx 的日志格式的话就用这个就行了；
2. `real-time-html` 用来使用实时刷新特性，结合 `daemonize` 让 GoAccess 启动一个守护进程，就不需要 Tmux 或者 nohup 了；
3. `port` 是用来和浏览器通信的，选一个没被占用的就行（别忘了在防火墙里开启端口！血的教训〒△〒 哭）；
4. 如果你不走 https 的话，`ssl-cert`，`ssl-key`，`ws-url`都不是必需的；
5. 把 `output` 放到你的站点目录下面。

另外说一下 `ws-url`，我之前没有设置这个选项的时候 HTML 里 WebSocket 用的协议是 `ws://`， 浏览器是不允许在 https 网页里使用非加密协议的，找了一圈发现 `ws-url` 这个选项，其实我觉得应该叫 `ws-scheme` 才贴切呢（・∀・）

#### 运行
```bash
$ goaccess --config-file=.goaccessrc /var/log/nginx/access.log
```
现在用浏览器打开 `http://<your-domain>/stat/` 应该就可以看见分析结果了，每秒钟刷新一次数据。
如果想每次开机启动的话可以把这行加到 `/etc/rc.local`
```bash
/usr/local/bingoaccess --config-file=/root/.goaccessrc /var/log/nginx/access.log
```

可以来看看我的[统计](https://udoubi.top/stat/)噢 ٩̋(๑˃́ꇴ˂̀๑)
