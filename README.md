# BaWangCan
大众点评一键报名所有霸王餐 生成excel表格反馈
## 运行环境
需要Python3.x的环境，没有的可以看[廖雪峰的Python安装教程](https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624)。
另外可能还需要几个三方库，可以直接用pip install安装。
## 使用指南
使用前首先需要自行在浏览器中获取cookie中的dper值，然后写入config.ini并保存。比如在chrome中随便找到一个霸王餐的报名链接，然后按下F12打开开发者工具，按下“报名”按钮之后再Network标签中找到一个cookies带有dper的请求就可以了。
![chrome中的cookies获取](https://raw.githubusercontent.com/cnbeiyu/MarkdownPhotos/master/projectPhoto/BaWangCan/chrome%20cookie.png)
config.ini中的cityId是指所需要获取霸王餐活动的所在城市，也是需要再浏览器中切换所在城市然后找到一个名为ajaxList的Post请求，请求中的cityId就是所需要城市的cityId,将cityId写入config.ini中即可。
这里给出几个常见的大众点评cityId
- 上海 1
- 北京 2
- 杭州 3
- 广州 4
- 南京 5
- 苏州 6
- 深圳 7
- 成都 8
- 重庆 9
- 天津 10

配置好config中的dper和cityId后就可以直接运行了，等待一段时间后会在当前目录生成名为霸王餐+当前时间的excel表格，表格中记录的霸王餐的报名情况。
![运行结果](https://raw.githubusercontent.com/cnbeiyu/MarkdownPhotos/master/projectPhoto/BaWangCan/excel.png)
