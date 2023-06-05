# PrivateCamera
PrivateCamera for ETT match recording and streaming

使用说明[中文版本]:
参考以下步骤操作. 所有用到的额外文件在仓库文件里上传了,可自取.
1. 安装微软Power Automate Desktop (简称PAD) , 详细步骤参考 [安装 Power Automate - Power Automate ](https://learn.microsoft.com/zh-cn/power-automate/desktop-flows/install)
  1. 下载 Power Automate 安装程序。 将文件保存到您的桌面或下载文件夹。
  2. 运行 Setup.Microsoft.PowerAutomate.exe 文件。
2. 安装完后 启动PAD, 新建一个Flow , 名称设置为PrivateCamera
  1. 全选复制Main.txt的文本内容粘贴到Main flow
  2. 选择Subflows,点击最下方的+New subflow, 新建3个subflow, 命名为location_loop, joinroom, exitroom
  3. 复制location_loop.txt的文本内容, 粘贴到location_loop
  4. 复制joinroom.txt的文本内容, 粘贴到joinroom
  5. 复制exitroom.txt的文本内容, 粘贴到exitroom
3. ETT PC客户端正常安装, PC客户端登陆后, 用ETT安装目录下的2d.bat文件启动Eleven的PC客户端, 加上你头显用户为好友. 先退出.
4. 自行准备好PC上的直播推流/录播软件(推荐obs)
5. 在桌面上新建ettpath.txt文件, 把ELEVEN的PC客户端安装路径复制粘贴到ettpath.txt, 比如我的ETT安装在D盘,路径为D:\Oculus\Software\Software\for-fun-labs-eleven-table-tennis-vr\ ,那就把这个路径贴到ettpath.txt里面. 如果你登陆Windows的用户名不是Administrator, 需要修改Main flow第1,2行里的C:\Users\Administrator\Desktop\ettpath.txt路径为你自己存放ettpath.txt文件的实际路径.
6. 把 Eleven.exe, HookTest64.dll, dllconfig.ini这几个文件复制粘贴到ETT的安装目录下. Eleven.exe会覆盖掉原来的官方版本,以防万一建议提前备份. 修改dllconfig.ini文件里的ETTUser对应的用户名为你要观战用户的昵称.
7. 把roomSetting-eleven.json文件复制粘贴到ETT安装目录下的settings目录下. 会覆盖原来的文件,可以先备份.
8. 用ETT安装目录下的2d.bat文件启动Eleven的PC客户端
9. 点击PrivateCamera脚本的▷Run按钮启动脚本.
10. 头显进入游戏, 上线后通过输入房间号的方式随便进入一个房间. 如果PC客户端账号会立刻跟着头显进入同一个房间, 则验证了PrivateCamera脚本已经正常运行.
