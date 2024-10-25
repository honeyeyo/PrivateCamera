import csv
import json
from datetime import datetime
import os
import time
import pyautogui 
import shutil
import re
import math
from generate_scoreboard import generate_scoreboard

# 配置
LOG_DIR = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\logs\\"
CSV_OUTPUT = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\log_analysis.csv"
OBS_OUTPUT = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\obs.log"
MATCH_JSON = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\match_data.json"
SCOREBOARD_OUTPUT = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\scoreboard.html"
LAST_POSITION_FILE = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\.last_position" # 保存本次处理的日志中处理到的行
# PERFORMANCE_LOG = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\performance.log" # 性能日志
PLAYER_ID = "1418464"  # VIOLENTPANDA 的 ID
CAMERA_ID = "1461990"  # CHN_CAMERA 的 ID
PLAYER_NAME = "VIOLENTPANDA"
CAMERA_NAME = "CHN_CAMERA"
# CSV_COLUMNS = ["Timestamp", "Analysis Time", "Event", "Details", "Delay (seconds)"]
CSV_COLUMNS = ["Event", "Details"]

# 全局变量
in_room = False
camera_in_room = False

# 屏幕坐标（根据您的屏幕分辨率调整）
PLAYER_NAME_POS = (-520, 320)
JOIN_ROOM_POS = (-620, 530)
EXIT_ROOM_POS = (-1120, 600)
EXIT_ROOM_OK_POS = (-1060, 520)
REJOIN_NO_POS = (-920, 520)
SCREEN_CORNER_POSE = (-1,1)

# def force_flush_file(file_path):
#     try:
#         with open(file_path, 'a') as f:
#             os.fsync(f.fileno())
#         # print(f"Successfully flushed file: {file_path}")
#     except Exception as e:
#         print(f"Error flushing file {file_path}: {e}")

def simulate_mouse_move(x, y):
    pyautogui.moveTo(x, y, duration=0.05)
    time.sleep(0.5)

def simulate_keypress(key):
    pyautogui.keyDown(key)
    time.sleep(0.01)
    pyautogui.keyUp(key)
    time.sleep(0.01)

def simulate_click(x, y):
    # 移动鼠标
    pyautogui.moveTo(x, y, duration=0.05)
    time.sleep(0.02)
    # 模拟鼠标按下
    pyautogui.mouseDown(x, y)
    time.sleep(0.02)
    # 模拟鼠标松开
    pyautogui.mouseUp(x, y)
    time.sleep(0.02)

def enter_room():
    # 切换到侧面视角
    simulate_keypress('0')

    # 呼出菜单
    simulate_keypress('m')

    # 点击被观战者名称位置
    simulate_click(*PLAYER_NAME_POS)

    # 点击JOIN ROOM按钮
    simulate_click(*JOIN_ROOM_POS)

    # 切换到观战视角
    simulate_keypress('6')

    simulate_mouse_move(*SCREEN_CORNER_POSE)

def exit_room():
    # 切换到侧面视角
    simulate_keypress('0')

    # 点击退出房间按钮
    simulate_click(*EXIT_ROOM_POS)

    # 点击弹窗OK按钮
    simulate_click(*EXIT_ROOM_OK_POS)

    # 关闭菜单
    simulate_keypress('m')

    # 点击弹窗NO按钮
    simulate_click(*REJOIN_NO_POS)

    simulate_mouse_move(*SCREEN_CORNER_POSE)

    # 等待退出完成
    time.sleep(0.1)

def get_latest_log_file():
    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.log')]
    if not log_files:
        return None
    return os.path.join(LOG_DIR, max(log_files, key=lambda f: os.path.getctime(os.path.join(LOG_DIR, f))))

# 保存本次处理的日志中处理到的行
def get_last_position(file_path):
    if os.path.exists(LAST_POSITION_FILE):
        with open(LAST_POSITION_FILE, 'r') as f:
            last_file, position = f.read().split(',')
        if last_file == file_path:
            return int(position)
    return 0

def save_last_position(file_path, position):
    with open(LAST_POSITION_FILE, 'w') as f:
        f.write(f"{file_path},{position}")

# 添加新函数用于解析击球数据
def parse_ball_hit_data(content):
    match = re.search(r'pos:\((.*?)\) vel:\((.*?)\) rrate:\((.*?)\)', content)
    if match:
        pos = [float(x) for x in match.group(1).split(',') if x]
        vel = [float(x) for x in match.group(2).split(',') if x]
        rrate = [float(x) for x in match.group(3).split(',') if x]
        
        speed = math.sqrt(sum(v**2 for v in vel))
        rotation = math.sqrt(sum((r/360)**2 for r in rrate))
        # 确保vel是3维的
        while len(vel) < 3:
            vel.append(0.0)
        
        # 如果vel超过3维，只保留前3个值
        vel = vel[:3]

        # 确保rrate是3维的
        while len(rrate) < 3:
            rrate.append(0.0)
        
        # 如果rrate超过3维，只保留前3个值
        rrate = rrate[:3]
        
        x_rotation, y_rotation, z_rotation = rrate
        
        # 设定阈值
        threshold = 3600  # 这个阈值可能需要根据实际情况调整
        
        # 判断球的运动方向
        direction = "Forward" if vel[2] > 0 else "Backward"
        
        # 判断旋转方向
        horizontal_spin = ""
        vertical_spin = ""

        if abs(x_rotation) > threshold:
            # 根据运动方向和x轴旋转方向判断上下旋
            if (direction == "Forward" and x_rotation < 0) or (direction == "Backward" and x_rotation > 0):
                vertical_spin = "Back"
            else:
                vertical_spin = "Top"
        
        if abs(y_rotation) > threshold:
            # 根据运动方向和y轴旋转方向判断左右旋
            if (direction == "Forward" and y_rotation > 0) or (direction == "Backward" and y_rotation < 0):
                horizontal_spin = "Left"
            else:
                horizontal_spin = "Right"     
        
        # 组合旋转描述，根据旋转强度决定顺序
        if horizontal_spin and vertical_spin:
            if abs(x_rotation) > abs(y_rotation):
                spin_direction = f"{vertical_spin} {horizontal_spin} spin"
            else:
                spin_direction = f"{horizontal_spin} {vertical_spin} spin"
        elif vertical_spin:
            spin_direction = f"{vertical_spin} spin"
        elif horizontal_spin:
            spin_direction = f"{horizontal_spin} spin"
        else:
            spin_direction = "No significant spin"
        
        return {
            'position': pos,
            'velocity': vel,
            'rotation_rate': rrate,
            'speed': speed,
            'rotation': rotation,
            'spin_direction': spin_direction,
            'direction': direction
        }
    return None

last_score = []
match_info = None

def parse_snapshot(content):
    print(content)
    try:
        data = json.loads(content.replace("Snapshot reads: ", ""))
        current_scores = data["RoundScores"]
        
        match_data = {
            "playerNames": data["PlayerNames"],
            "playerELOs": data["PlayerELOs"],
            "currentScores": current_scores,
            "matchId": data["MatchId"],
            "bestOf": data["BestOf"],
            "ranked": data["Ranked"],
            "matchWinner": data["MatchWinner"]
        }
        
        update_match_data(match_data)
        
        global last_score, match_info
        
        # 如果是新的比赛或者新的对手，重置 match_info、last_score 和 currentSetStatus
        if not match_info or match_info["MatchId"] != data["MatchId"]:
            match_info = {
                "PlayerNames": data["PlayerNames"],
                "PlayerELOs": data["PlayerELOs"],
                "MatchId": data["MatchId"],
                "BestOf": data["BestOf"],
                "Ranked": data["Ranked"]
            }
            last_score = []
            event = "Match Start"
            details = f"New match started: {match_info}"
            
            # 重置 currentSetStatus 和 matchScore
            try:
                with open(MATCH_JSON, 'r', encoding='utf-8') as f:
                    match_data = json.load(f)
                match_data['currentSetStatus'] = [0, 0]
                match_data['matchScore'] = [0, 0]
                
                # 更新玩家信息
                match_data['playerNames'] = data["PlayerNames"]
                match_data['playerELOs'] = data["PlayerELOs"]
                
                # 如果有其他需要重置或更新的字段，也在这里处理
                
                with open(MATCH_JSON, 'w', encoding='utf-8') as f:
                    json.dump(match_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Error resetting match data: {e}")
            
            # 生成新的记分牌
            generate_scoreboard()
            
            return event, details
        
        if last_score != current_scores:
            current_round = len(current_scores)
            
            if current_scores:
                current_round_score = current_scores[-1]
                scoring_side = data["LastPointReasonSide"]
                scoring_player = data["PlayerNames"][0] if scoring_side == "SideA" else data["PlayerNames"][1]
                losing_player = data["PlayerNames"][1] if scoring_side == "SideA" else data["PlayerNames"][0]
                
                server_id = int(data["CurrentServer"])
                server_name = data["PlayerNames"][0] if server_id == data["PlayerIds"][0] else data["PlayerNames"][1]
                
                reason = data["LastPointReason"]
                
                # 检查是否是新的Round开始
                if len(current_scores) > len(last_score or []):
                    event = "New Round"
                    details = f"Round {current_round} started. "
                    if len(current_scores) == 1:
                        details += f"First round of the match, "
                    else:
                        previous_score = current_scores[-2]
                        details += f"Previous round score: {previous_score[0]}-{previous_score[1]}, New round of the match, "
                        
                        # 更新 currentSetStatus
                        try:
                            with open(MATCH_JSON, 'r', encoding='utf-8') as f:
                                match_data = json.load(f)
                            current_set_status = match_data.get('currentSetStatus', [0, 0])
                            
                            # 确定上一轮的获胜者
                            winner_index = 0 if previous_score[0] > previous_score[1] else 1
                            current_set_status[winner_index] += 1
                            
                            update_match_data({'currentSetStatus': current_set_status})
                        except Exception as e:
                            print(f"Error updating currentSetStatus: {e}")
                    
                    # 生成新的记分牌
                    generate_scoreboard()
                else:
                    event = "Score Update"
                    details = ""

                # 更新 last_score
                last_score = current_scores
                
                details += f"Current round score: {current_round_score[0]}-{current_round_score[1]}. "
            else:
                event = "Match Reset"
                details = "Scores have been reset."
            
            if data["MatchWinner"] != "0":
                event = "Match End"
                winner_index = 0 if int(data["MatchWinner"]) == data["PlayerIds"][0] else 1
                winner_name = data["PlayerNames"][winner_index]
                details += f", Match Winner: {winner_name}"
                
                # 更新大比分
                try:
                    with open(MATCH_JSON, 'r', encoding='utf-8') as f:
                        match_data = json.load(f)
                    match_score = match_data.get('matchScore', [0, 0])
                    match_score[winner_index] += 1
                    update_match_data({'matchScore': match_score})
                    # 这里也要更新 currentSetStatus
                    current_set_status = match_data.get('currentSetStatus', [0, 0])
                    current_set_status[winner_index] += 1
                    update_match_data({'currentSetStatus': current_set_status})
                except Exception as e:
                    print(f"Error updating match score and currentSetStatus: {e}")
            
        else:
            if data["MatchWinner"] != "0":
                event = "Match End"
                winner_index = 0 if int(data["MatchWinner"]) == data["PlayerIds"][0] else 1
                winner_name = data["PlayerNames"][winner_index]
                details = f"Match ended. Winner: {winner_name}, Final score: {' '.join([f'{s[0]}-{s[1]}' for s in current_scores])}"
                
                # 更新大比分
                try:
                    with open(MATCH_JSON, 'r', encoding='utf-8') as f:
                        match_data = json.load(f)
                    match_score = match_data.get('matchScore', [0, 0])
                    match_score[winner_index] += 1
                    update_match_data({'matchScore': match_score})
                    # 这里也要更新 currentSetStatus
                    current_set_status = match_data.get('currentSetStatus', [0, 0])
                    current_set_status[winner_index] += 1
                    update_match_data({'currentSetStatus': current_set_status})
                except Exception as e:
                    print(f"Error updating match score and currentSetStatus: {e}")
            else:
                return "Unknown", None  # 如果比分没有变化且比赛未结束，不记录

        # 生成新的记分牌
        generate_scoreboard()

        return event, details
    except json.JSONDecodeError:
        print(f"Failed to parse snapshot data: {content}")
        return "Unknown", None

def parse_log_line(line):
    if '"msgType":"Message"' in line or '"msgType":"Response"' in line:
        try:
            timestamp, content = line.split("]", 1)
            timestamp = timestamp.strip("[")
            content = content.strip()
            if "TCPSERVERCOMMUNICATIONS]Received message from server:" in content:
                _, json_content = content.split("server:", 1)
                return timestamp, json.loads(json_content)
        except (ValueError, json.JSONDecodeError):
            pass
    elif "[MPMatch]Received ball hit from opponent:" in line:
        match = re.match(r'\[(.*?)\].*?\[MPMatch\](.*)', line)
        if match:
            timestamp, content = match.groups()
            # print(f"Timestamp: {timestamp}")
            # print(f"Content: {content}")
            return timestamp, content.strip()
    elif line.strip().startswith("Snapshot reads:"):
        # match = re.search(r'Snapshot reads: (.*)', line)
        # if match:
            # content = match.group(1)
            # # 使用当前时间作为时间戳，因为日志中没有提供
            # timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            # return timestamp, content.strip()
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        return timestamp, line.strip()
    return None, None

def backup_and_reset_files():
    # 备份 CSV_OUTPUT 文件
    if os.path.exists(CSV_OUTPUT):
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{CSV_OUTPUT[:-4]}_{backup_time}.csv"
        shutil.copy2(CSV_OUTPUT, backup_file)
        print(f"已备份 CSV 输出文件到: {backup_file}")

        # 清空原 CSV 文件
        open(CSV_OUTPUT, 'w').close()
        print(f"已清空 CSV 输出文件: {CSV_OUTPUT}")

    # 删除 LAST_POSITION_FILE
    if os.path.exists(LAST_POSITION_FILE):
        os.remove(LAST_POSITION_FILE)
        print(f"已删除上次位置文件: {LAST_POSITION_FILE}")

def analyze_log():
    global in_room, camera_in_room

    start_time = datetime.now()
    # print(f"开始分析日志: {start_time}")

    log_file_path = get_latest_log_file()
    if not log_file_path:
        print("No log file found.")
        return
    
    # print(f"正在分析最新日志: {log_file_path}")

    # 强制刷新日志文件
    # force_flush_file(log_file_path)

    last_position = get_last_position(log_file_path)

    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_file.seek(last_position)
        new_lines = log_file.readlines()
        lines_processed = len(new_lines)

        if new_lines:
            with open(CSV_OUTPUT, 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                if os.path.getsize(CSV_OUTPUT) == 0:
                    csv_writer.writerow(CSV_COLUMNS)

                for line in new_lines:
                    analysis_time = datetime.now()
                    timestamp, data = parse_log_line(line)
                    event = "Unknown"
                    details = "Unknown"

                    if timestamp and data:
                        log_timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
                        delay = (analysis_time - log_timestamp).total_seconds()

                        if isinstance(data, dict) and data["msgType"] == "Message":
                            # 处理 StateChange (摄像头状态变化)
                            if data["key"] == "StateChange" and any(user["UserId"] == CAMERA_ID for user in data["data"]):
                                old_state = data["data"][0]["Location"]["locationType"]
                                new_state = data["data"][1]["Location"]["locationType"]
                                if new_state == "room" and old_state != "room":
                                    camera_in_room = True
                                    event = "Camera Enter Room"
                                elif old_state == "room" and new_state != "room":
                                    camera_in_room = False
                                    event = "Camera Exit Room"
                                details = f"From {old_state} to {new_state}"

                            # 处理 FriendStateChange (被跟踪玩家状态变化)
                            elif data["key"] == "FriendStateChange" and any(user["UserId"] == PLAYER_ID for user in data["data"]):
                                old_state = data["data"][0]["Location"]["locationType"]
                                new_state = data["data"][1]["Location"]["locationType"]
                                if new_state == "room" and old_state != "room":
                                    in_room = True
                                    event = "Player Enter Room"
                                    enter_room()  # 执行进���房间操作
                                elif old_state == "room" and new_state != "room":
                                    in_room = False
                                    event = "Player Exit Room"
                                    exit_room()  # 执行退出房间操作
                                else:
                                    continue
                                details = f"From {old_state} to {new_state}"

                            elif data["key"] == "RoomJoined":
                                roomId = data["data"][0]["Id"]
                                hostId = data["data"][0]["HostId"]
                                matchId = data["data"][0]["MatchId"]
                                viewCount = data["data"][0]["ViewCount"]
                                players = data["data"][0]["Players"]
                                playerIds = data["data"][0]["PlayerIds"]
                                print(f"Room Joined: {roomId}, Host: {hostId}, Match: {matchId}, Viewers: {viewCount}, Players: {playerIds}")
                                
                                # 提取玩家信息，排除摄像机
                                player_data = {
                                    'playerNames': [],
                                    'playerELOs': [],
                                    'playerCountryCodes': [],
                                    'playerRanks': [],
                                    'playerWins': [],
                                    'playerLosses': []
                                }

                                valid_players = [p for p in players if p['Id'] != CAMERA_ID and p['UserName'] != CAMERA_NAME]
                                
                                if len(valid_players) == 2:
                                    # 根据玩家在数组中的位置确定主客顺序
                                    home_player = valid_players[0]
                                    away_player = valid_players[1]
                                    
                                    # 读取现有的 match_data（如果存在）
                                    try:
                                        with open(MATCH_JSON, 'r', encoding='utf-8') as f:
                                            old_match_data = json.load(f)
                                    except FileNotFoundError:
                                        old_match_data = {}
                                    
                                    # 检查玩家是否相同，并调整顺序和分数
                                    old_players = old_match_data.get('playerNames', [])
                                    new_players = [home_player['UserName'], away_player['UserName']]
                                    
                                    if set(old_players) == set(new_players):
                                        # 玩家相同，但可能顺序改变
                                        if old_players != new_players:
                                            # 顺序改变，调整大局分
                                            old_match_score = old_match_data.get('matchScore', [0, 0])
                                            match_score = old_match_score[::-1]  # 反转大局分
                                        else:
                                            # 顺序相同，保持原有大局分
                                            match_score = old_match_data.get('matchScore', [0, 0])
                                    else:
                                        # 新的玩家组合，重置大局分
                                        match_score = [0, 0]
                                    
                                    # 第一局的局分初始化0:0
                                    current_set_status = [0, 0]

                                    
                                    # 更新玩家数据
                                    for player in [home_player, away_player]:
                                        player_data['playerNames'].append(player['UserName'])
                                        player_data['playerELOs'].append(player['ELO'])
                                        player_data['playerCountryCodes'].append(player['CountryCode'])
                                        player_data['playerRanks'].append(player['Rank'])
                                        player_data['playerWins'].append(player['Wins'])
                                        player_data['playerLosses'].append(player['Losses'])
                                    
                                    player_data['matchScore'] = match_score
                                    player_data['currentSetStatus'] = current_set_status
                                    
                                    # 更新 match_data
                                    update_match_data(player_data)
                                    generate_scoreboard()
                                else:
                                    print("Warning: Unexpected number of players detected. Scoreboard not updated.")

                            # 处理 RoomExitUser
                            # elif data["key"] == "RoomExitUser":
                            #     if data["data"][0]["Id"] == PLAYER_ID:
                            #         event = "Player Left Room"
                            #     else:
                            #         event = "Other Player Left Room"
                            #     details = f"Player ID: {data['data'][0]['Id']}, Player Name: {data['data'][0]['UserName']}"
                        
                        elif isinstance(data, str) and "Received ball hit from opponent:" in data:
                            ball_data = parse_ball_hit_data(data)
                            if ball_data and ball_data['speed'] >= 1:  # 只处理速度大于等于1的数据
                                event = "Ball Hit"
                                details = (f"{ball_data['speed']:.2f} m/s, "
                                        f"{ball_data['rotation']:.2f} rev/s, "
                                        f"{ball_data['spin_direction']}, "
                                        f"{ball_data['direction']}")
                                print(f"Ball hit detected at {timestamp}")
                                print(f"Speed: {ball_data['speed']:.2f} m/s")
                                print(f"Rotation: {ball_data['rotation']:.2f} rev/s")
                                print(f"Spin direction: {ball_data['spin_direction']}")
                                print(f"Ball direction: {ball_data['direction']}")
                                print(f"Velocity vector: {ball_data['velocity']}")
                                print(f"Rotation rate vector: {ball_data['rotation_rate']}")
                                print(f"Delay: {delay:.3f} seconds")
                                print("---")
                            else:
                                # print(f"Failed to parse ball hit data : {data}")
                                continue
                        elif isinstance(data, str) and data.startswith("Snapshot reads:"):
                            content = data.replace("Snapshot reads:", "").strip()
                            event, details = parse_snapshot(content)

                            print(f"Event: {event}")
                            print(f"Details: {details}")
                            print(f"Log Timestamp: {timestamp}")
                            print(f"Analysis Time: {analysis_time}")
                            print(f"Delay: {delay:.3f} seconds")
                            if event == "New Round":
                                print("=" * 50)  # 添加一个分隔线���突出显示新的Round开始
                            elif event == "Match End":
                                print("#" * 50)  # 比赛结束添加特殊的分隔线
                            else:
                                print("-" * 30)
                        else:
                            continue

                        
                        if (event != "Unknown"):
                            log_timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
                            delay = (analysis_time - log_timestamp).total_seconds()
                            csv_writer.writerow([
                                        # timestamp,
                                        # analysis_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                        event,
                                        details
                                        # details,
                                        # f"{delay:.3f}"
                                    ])
                            print(f"Event: {event}")
                            print(f"Log Timestamp: {timestamp}")
                            print(f"Analysis Time: {analysis_time}")
                            print(f"Delay: {delay:.3f} seconds")
                            print("---")
        else:
            return # 没有新行，直接返回

        # 保存最后处理的位置
        save_last_position(log_file_path, log_file.tell())

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # 记录性能信息
    # with open(PERFORMANCE_LOG, 'a', encoding='utf-8') as perf_log:
    #     perf_log.write(f"开始时间: {start_time}, 结束时间: {end_time}, 持续时间: {duration:.2f}秒, 处理行数: {lines_processed}\n")

    print(f"结束分析日志: {end_time} 本次分析处理了 {lines_processed} 行日志，耗时 {duration:.2f} 秒")

def read_last_lines(file_path, num_lines=5):
    with open(file_path, 'r') as file:
        lines = file.readlines()[-num_lines:]
    return ''.join(lines)

def set_text_source(text):
    # 把text写入OBS_OUTPUT文件,如果已有则直接覆盖
    with open(OBS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(text)

def update_match_data(new_data):
    try:
        with open(MATCH_JSON, 'r', encoding='utf-8') as f:
            match_data = json.load(f)
    except FileNotFoundError:
        match_data = {}
    
    # 更新所有新数据，包括玩家信息
    for key, value in new_data.items():
        match_data[key] = value
    
    # 保留其他可能存在的字段
    for key in match_data.keys():
        if key not in new_data:
            match_data[key] = match_data[key]
    
    with open(MATCH_JSON, 'w', encoding='utf-8') as f:
        json.dump(match_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 在脚本启动时执行上次运行输出文件的备份和重置
    backup_and_reset_files()

    simulate_mouse_move(*SCREEN_CORNER_POSE)
    time.sleep(0.1)
    simulate_click(*SCREEN_CORNER_POSE)

    time.sleep(0.1)

    # 一开始先呼出 -> 关闭菜单一下 确保好友列表中我名字加载出来了。
    # 呼出菜单
    simulate_keypress('m')

    time.sleep(3)

    # 关闭菜单
    simulate_keypress('m')

    while True:
        analyze_log()
        text_to_display = read_last_lines(CSV_OUTPUT,20)
        # 设置到obs的文本源
        set_text_source(text_to_display)
        generate_scoreboard()  # 生成新的 scoreboard.html
        time.sleep(1)  # 每1秒运行一次



