import csv
import json
from datetime import datetime
import os
import time
import pyautogui 
import shutil
import re
import math

# 配置
LOG_DIR = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\logs\\"
CSV_OUTPUT = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\log_analysis.csv"
LAST_POSITION_FILE = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\.last_position" # 保存本次处理的日志中处理到的行
# PERFORMANCE_LOG = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\performance.log" # 性能日志
PLAYER_ID = "1418464"  # VIOLENTPANDA 的 ID
CAMERA_ID = "1461990"  # CHN_CAMERA 的 ID
PLAYER_NAME = "VIOLENTPANDA"
CAMERA_NAME = "CHN_CAMERA"
CSV_COLUMNS = ["Timestamp", "Analysis Time", "Event", "Details", "Delay (seconds)"]

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
    time.sleep(0.05)
    # 模拟鼠标按下
    pyautogui.mouseDown(x, y)
    time.sleep(0.02)
    # 模拟鼠标松开
    pyautogui.mouseUp(x, y)
    time.sleep(1)

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
    time.sleep(2)

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
        pos = [float(x) for x in match.group(1).split(',')]
        vel = [float(x) for x in match.group(2).split(',')]
        rrate = [float(x) for x in match.group(3).split(',')]
        
        speed = math.sqrt(sum(v**2 for v in vel))
        rotation = math.sqrt(sum((r/360)**2 for r in rrate))
        
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
        
        global last_score, match_info
        
        # 如果是新的比赛或者新的对手，重置 match_info 和 last_score
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
            return event, details
        
        if last_score != current_scores:
            current_round = len(current_scores)
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
                    details += f", First round of the match, "
                else:
                    details += f"Previous round score: {current_scores[-2][0]}-{current_scores[-2][1]}, New round of the match, "
            else:
                event = "Score Update"
                details = ""
            
            details += (f"Current round score: {current_round_score[0]}-{current_round_score[1]}, "
                        f"Match score: {sum(1 for s in current_scores if s[0] > s[1])}-{sum(1 for s in current_scores if s[1] > s[0])}, "
                        f"Point won by: {scoring_player}, "
                        f"Point lost by: {losing_player}, "
                        f"Server: {server_name}, "
                        f"Reason: {reason}")
            
            if data["MatchWinner"] != "0":
                event = "Match End"
                winner_name = data["PlayerNames"][0] if int(data["MatchWinner"]) == data["PlayerIds"][0] else data["PlayerNames"][1]
                details += f", Match Winner: {winner_name}"
            
            last_score = current_scores
        else:
            if data["MatchWinner"] != "0":
                event = "Match End"
                winner_name = data["PlayerNames"][0] if int(data["MatchWinner"]) == data["PlayerIds"][0] else data["PlayerNames"][1]
                details = f"Match ended. Winner: {winner_name}, Final score: {' '.join([f'{s[0]}-{s[1]}' for s in current_scores])}"
            else:
                return "Unknown", None  # 如果比分没有变化且比赛未结束，不记录

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
    elif "Snapshot reads:" in line:
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
                                    enter_room()  # 执行进入房间操作
                                elif old_state == "room" and new_state != "room":
                                    in_room = False
                                    event = "Player Exit Room"
                                    exit_room()  # 执行退出房间操作
                                else:
                                    continue
                                details = f"From {old_state} to {new_state}"

                            # 处理 RoomJoined
                            elif data["key"] == "RoomJoined":
                                for player in data["data"][0]["Players"]:
                                    if player["Id"] == PLAYER_ID:
                                        event = "Player Join Room"
                                    elif player["Id"] == CAMERA_ID:
                                        event = "Camera Join Room"
                                    else:
                                        event = "Other Player Join Room"
                                    details = f"Room ID: {data['data'][0]['Id']}, Player ID: {player['Id']}, Player Name: {player['UserName']}"

                            # 处理 RoomExitUser
                            elif data["key"] == "RoomExitUser":
                                if data["data"][0]["Id"] == PLAYER_ID:
                                    event = "Player Left Room"
                                else:
                                    event = "Other Player Left Room"
                                details = f"Player ID: {data['data'][0]['Id']}, Player Name: {data['data'][0]['UserName']}"
                        
                        elif isinstance(data, str) and "Received ball hit from opponent:" in data:
                            ball_data = parse_ball_hit_data(data)
                            if ball_data and ball_data['speed'] >= 1:  # 只处理速度大于等于1的数据
                                event = "Ball Hit"
                                details = (f"Speed: {ball_data['speed']:.2f} m/s, "
                                        f"Rotation: {ball_data['rotation']:.2f} rev/s, "
                                        f"Spin: {ball_data['spin_direction']}, "
                                        f"Direction: {ball_data['direction']}")
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
                                print(f"Failed to parse ball hit data : {data}")
                                continue
                        elif isinstance(data, str) and "Snapshot reads:" in data:
                            match = re.search(r'Snapshot reads: (.*)', line)
                            if match:
                                content = match.group(1)
                            event, details = parse_snapshot(content)

                            print(f"Event: {event}")
                            print(f"Details: {details}")
                            print(f"Log Timestamp: {timestamp}")
                            print(f"Analysis Time: {analysis_time}")
                            print(f"Delay: {delay:.3f} seconds")
                            if event == "New Round":
                                print("=" * 50)  # 添加一个分隔线以突出显示新的Round开始
                            elif event == "Match End":
                                print("#" * 50)  # 为比赛结束添加特殊的分隔线
                            else:
                                print("-" * 30)
                        else:
                            continue

                        
                        if (event != "Unknown"):
                            log_timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
                            delay = (analysis_time - log_timestamp).total_seconds()
                            csv_writer.writerow([
                                        timestamp,
                                        analysis_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                        event,
                                        details,
                                        f"{delay:.3f}"
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


if __name__ == "__main__":
    # 在脚本启动时执行上次运行输出文件的备份和重置
    backup_and_reset_files()

    simulate_mouse_move(*SCREEN_CORNER_POSE)
    time.sleep(1)
    simulate_click(*SCREEN_CORNER_POSE)

    time.sleep(1)

    # 一开始先呼出 -> 关闭菜单一下 确保好友列表中我名字加载出来了。
    # 呼出菜单
    simulate_keypress('m')

    time.sleep(3)

    # 关闭菜单
    simulate_keypress('m')

    while True:
        analyze_log()
        time.sleep(1)  # 每1秒运行一次