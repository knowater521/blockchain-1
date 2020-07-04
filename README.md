# 简易区块链
自己用python写的一个区块链程序  
大部分的底层细节参照了比特币  

# 安装
1、使用 pipenv 生成虚环境，Pipfile 本项目中已给定。
```sh
pip install pipenv -U
pipenv install --skip-lock
```
2、进入虚环境，运行 app.pyw 文件。
```sh
pipenv shell
python app.pyw
```
3、如果要编译的话。
```sh
pyinstaller -w -i files/img/main.ico app.pyw
.\install.sh
```
生成的可执行文件在 dist/app 目录下，为app.exe，这个app目录就是完整的可执行程序目录。
