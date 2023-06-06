# PrivateCamera
PrivateCamera for ETT match recording and streaming

演示效果可以看我的直播间 【暴力能喵樊帝东的个人空间-哔哩哔哩】 https://b23.tv/mTYmC59 目前已经录制了与超过500个对手的比赛.

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
10. 头显进入游戏, 上线后通过输入房间号的方式随便进入一个房间. 如果PC客户端账号会立刻跟着头显进入同一个房间, 则验证了PrivateCamera脚本已经正常运行. 请开始你的表演!

Instructions for use [English version]: Refer to the following steps to operate. All the extra files used are uploaded in the repository .Please download all by yourself.

1. Install Microsoft Power Automate Desktop (PAD for short), for detailed steps refer to  安装 Power Automate - Power Automate 
  1. Download Power Automate installer Save the file to your desktop or downloads folder.
  2. Run the Setup.Microsoft.PowerAutomate.exe file.
2. After installation, start PAD, create a new Flow, and set the name to "**PrivateCamera**"
  1. Select all, copy the text content of Main.txt and paste it to **Main** flow
  2. Select Subflows, click +New subflow at the bottom, create 3 new subflows, named **location_loop**, **joinroom**, **exitroom**
  3. Copy the text content of location_loop.txt and paste it to **location_loop**
  4. Copy the text content of joinroom.txt and paste it into **joinroom**
  5. Copy the text content of exitroom.txt and paste it to **exitroom**
3. Make sure the ETT PC client is installed normally. Use the 2d.bat file in the ETT installation directory to start the Eleven PC client, login with the guest account and add your headset user account as a friend. When this is done . Exit first.
4. Prepare the live streaming/recording software on the PC by yourself (obs is recommended) . 
5. Create a new **ettpath.txt** file on the desktop, copy and paste the ELEVEN PC client installation path to ettpath.txt . For example, my ETT is installed on the D: drive, and the path is D:\Oculus\Software\Software\for-fun-labs- eleven-table-tennis-vr\, so I pasted this path into ettpath.txt. If your Windows login user name is not **Administrator**, you need to modify C:\Users\Administrator\Desktop in lines 1 and 2 of the Main flow  ettpath.txt path is the actual path where you store the ettpath.txt file.
6. Copy and paste **Eleven.exe**, **HookTest64.dll**, and **dllconfig.ini** files to the ETT installation directory. Eleven.exe will overwrite the original official version, so it is recommended to back up in advance. Modify the **dllconfig.ini** file : **ETTUser** set to be the nickname of the user you want to follow and watch.(Make sure you have added it to your friend list in step 3)
7. Copy and paste the **roomSetting-eleven.json** file to the settings directory under the ETT installation directory. The original file will be overwritten, you can back it up first.
8. Use the 2d.bat file in the ETT installation directory to start Eleven's PC client
9. Click the **▷Run** button of the PrivateCamera script to start the script.
10. Then start ETT in your headset, and enter a room randomly by entering the room number after being online. If the PC client account immediately enters the same room that the headset is in, it is verified that the PrivateCamera script has been running normally. Start your show!
