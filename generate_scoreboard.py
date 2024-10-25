import json
from jinja2 import Template

MATCH_JSON = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\match_data.json"
SCOREBOARD_OUTPUT = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\scoreboard.html"

def generate_scoreboard():
    with open(MATCH_JSON, 'r', encoding='utf-8') as f:
        match_data = json.load(f)
    
    template = Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ElevenVR Scoreboard</title>
        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                margin: 0;
                padding: 5px;
            }
            .scoreboard {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #222;
                border-radius: 5px;
                padding: 5px 10px;
                max-width: 500px;
                margin: 0 auto;
            }
            .player {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                width: 45%;
            }
            .player-right {
                align-items: flex-end;
            }
            .player-name {
                font-size: 18px;
                font-weight: bold;
                display: flex;
                align-items: center;
            }
            .flag {
                width: 24px;
                height: 16px;
                margin-right: 5px;
                vertical-align: middle;
            }
            .player-right .flag {
                margin-right: 0;
                margin-left: 5px;
            }
            .score {
                font-size: 28px;
                font-weight: bold;
                margin-top: 2px;
            }
            .elo {
                font-size: 14px;
                color: #aaa;
            }
            .match-score {
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                width: 10%;
                color: #2ecc71;  /* 绿色 */
            }
            .blue {
                color: #3498db;
            }
            .red {
                color: #e74c3c;
            }
            .player-stats {
                font-size: 12px;
                color: #aaa;
            }
        </style>
    </head>
    <body>
        <div class="scoreboard">
            <div class="player">
                <div class="player-name blue">
                    <img class="flag" src="https://flagcdn.com/w40/{{ match_data['playerCountryCodes'][0].lower() }}.png" alt="{{ match_data['playerCountryCodes'][0] }} flag">
                    {{ match_data['playerNames'][0] }}
                </div>
                <div class="score blue">{{ match_data['currentScores'][-1][0] if match_data['currentScores'] else '0' }}</div>
                <div class="elo">ELO {{ match_data['playerELOs'][0] }}</div>
                <div class="player-stats">WR#{{ match_data['playerRanks'][0] }} | W/L: {{ match_data['playerWins'][0] }}/{{ match_data['playerLosses'][0] }}</div>
            </div>
            <div class="match-score">
                {{ match_data['matchScore'][0] }} - {{ match_data['matchScore'][1] }}
            </div>
            <div class="player player-right">
                <div class="player-name red">
                    {{ match_data['playerNames'][1] }}
                    <img class="flag" src="https://flagcdn.com/w40/{{ match_data['playerCountryCodes'][1].lower() }}.png" alt="{{ match_data['playerCountryCodes'][1] }} flag">
                </div>
                <div class="score red">{{ match_data['currentScores'][-1][1] if match_data['currentScores'] else '0' }}</div>
                <div class="elo">ELO {{ match_data['playerELOs'][1] }}</div>
                <div class="player-stats">WR#{{ match_data['playerRanks'][1] }} | W/L: {{ match_data['playerWins'][1] }}/{{ match_data['playerLosses'][1] }}</div>
            </div>
        </div>
    </body>
    </html>
    ''')
    
    html_output = template.render(match_data=match_data)
    
    with open(SCOREBOARD_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html_output)

if __name__ == "__main__":
    generate_scoreboard()
