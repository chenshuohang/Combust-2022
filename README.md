# 北京大学物理化学实验 - 燃烧热和溶解热测定小助手

> 从理论到了实验，哥们耗费好多体力，都什么年代，还在做传统实验？ 
> 
> —— *Zood*, **114**,(5), *14*, 191-9810.

本程序参考了https://github.com/Benzoin96485/Combust 的代码并在此基础上搭建了GUI界面，使得程序变得好用。

## 我该如何操作？

首先你需要安装一些必要的包。在确保你有安装Python的情况下，打开命令行（Win+R之后输入cmd或者开始菜单搜索），输入：

```
pip install pyserial matplotlib pandas
```

然后用Python运行`serdata.py`，此时你会得到界面。

当然，作者已经用`pyinstaller`将`serdata.py`打包成`exe`文件，可惜只能上传25MB以下的文件，因此实在比较懒需要一步到位的话，请自行联系作者。

## 界面介绍

左下的五个文字框依次表示实验序号，采样间隔（作者测试时设置为0.4秒，但依旧实际采样间隔为1秒。），还有加入的物质，加入的质量（可以多个一起写，例如加入物质可以填`棉线 - 棉线+苯甲酸 - 镍丝`，质量填的是`0.0114, 0.5141, 0.0091`，仅作为`info.txt`的填写材料。）

点击“开始采集”，系统会自动搜索有没有对应的USB接口。如果提示无可用串口，可能原因在于没有安装`ch341a`驱动。驱动文件老师在蒸气压数据采集的链接里一并给出，注意安装。

如果没有出现异常，会出现文字“已经找到仪器”，并且在右下角开始记录，对应作图于右上角显示。

点击“开始加热”，系统会自动记录你开始加热的时间，点击“停止加热”后，系统会记录你的通电时间，并显示于左下角。

（**注意：由于作者没有电源的接口，你必须手动摁下电源开始加热后（或者同时）摁下开始加热按钮**）

点击“停止采集”，系统会将图片和数据点保存为`figure{x}.jpg`和`data{x}.csv`。同时左下角的数据也会被记录于`info{x}.txt`，其中`{x}`表示你的实验序号。

## 温馨提示

1. 请一定要安装驱动！
2. 本测定小助手的数据文件只有在停止采集后才生成。因此请勿测定过程中退出小助手。
3. 出现问题可能原因是线没插牢固，多试试几次，或者试试看万能的重启电脑。
4. 本作者由于疏忽且懒惰，忘记了溶解热的时候还需要填写电流和电阻，有能力的同学可以自己改代码。
5. 欢迎随时交流。
