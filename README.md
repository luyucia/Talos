Talos
=====

Talos is a monitoring system


全部依赖
jdk
logstash
redis
python
tornado

部署说明:

1、有python环境后安装tronado框架。
2、部署一台redis
3、在talos的config中配置下redis地址，并启动talos
4、将要监控的文件配置到logstash中，logstash输出到redis中，访问8888端口即可在web界面中查看

