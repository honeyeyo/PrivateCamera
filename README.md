# PrivateCamera
PrivateCamera for ETT match recording and streaming
这是一个用于《Eleven Table Tennis VR》游戏的自动观战和比赛数据分析工具,主要用于直播和数据统计。

## Main Features / 主要功能

### 1. Automatic Spectating System / 自动观战系统
- Automatically monitors specified player's game status / 自动监控指定玩家的游戏状态
- Auto-enters spectator mode when player joins a room / 当玩家进入房间时自动进入观战
- Auto-exits when player leaves the room / 当玩家退出房间时自动退出观战
- Detects inactivity and exits room automatically / 检测长时间无击球自动退出房间

### 2. Match Data Analysis / 比赛数据分析
- Real-time game log parsing / 实时解析游戏日志文件
- Score and match progress tracking / 记录比分变化和比赛进程
- Ball hit analysis (speed, spin direction, etc.) / 分析击球数据(球速、旋转方向等)
- Player stats tracking (ELO, rank, etc.) / 追踪房间内选手数据(ELO分、排名等)

### 3. Real-time Scoreboard Display / 实时记分牌显示
- HTML+CSS scoreboard interface / 使用HTML+CSS制作美观的记分牌界面
- Current score and match score display / 显示当前比分和大局比分
- Player information display (flags, ELO, win rate) / 显示选手信息(国旗、ELO分、胜率等)
- Round win indicators / 显示每局获胜方
- Auto-updates every second / 自动每秒更新数据

### 4. Data Persistence / 数据持久化
- Match data saved in JSON format / 将比赛数据保存为JSON格式
- Match logs recorded in CSV format / 记录比赛日志到CSV文件
- Automatic backup of historical data / 备份历史数据文件

### 5. Desktop Automation Control / 桌面自动化控制
- Keyboard and mouse simulation using pyautogui / 使用pyautogui模拟键鼠操作
- Automatic game interface operation / 自动进行游戏界面操作
- Exception handling for various exceptions / 处理各种异常情况

### 6. Live Streaming Support / 直播支持
- OBS integration for match information display / 支持OBS直播显示比赛信息
- Real-time match status updates / 实时更新最新比赛状态
- Streaming-friendly UI design / 美观的UI设计适合直播使用

2024-11-07 
Yesterday, I found that the official PC client version 350.4 has fixed the 10s delay bug, this script can now output real-time ball hit data and score updates. / 昨晚打ETT的时候发现官方PC客户端的最新版本350.4已经修复了10s延迟的bug, 此脚本终于可以正常实时输出击球数据和比分更新了

2024-10-26
New feature: Added a local scoreboard that automatically refreshes based on the log file / 新特性: 增加了根据日志自动刷新的local scoreboard

![image](https://github.com/user-attachments/assets/6fd5367e-fc5d-4810-b4e1-e4a5e23c8576)


The usage instructions are in the link below / 使用说明在下面链接
https://unmsviwi6a.feishu.cn/docx/CMhtdbFPOo4Qrhxg1FecnFEbnwd

If you encounter any problems during use, please leave a message in the github repository. / 使用中遇到任何问题, 请在github仓库留言.
