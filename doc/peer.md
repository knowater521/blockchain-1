# 网络中的节点

## 一个全节点包括4个功能：

W - 钱包	M - 矿工	B - 完整的区块链数据库	N - 网络路由

![node](.img/node.jpg)



## 各功能之间的依赖关系

![dependency](.img/dependency.jpg)



> 4个功能设计为4个服务，采用消息队列的方式以避免线程同步问题。



## N功能

![peer](.img/peer.png)



