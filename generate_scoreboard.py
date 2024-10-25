import json
from jinja2 import Template

MATCH_JSON = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\match_data.json"
SCOREBOARD_OUTPUT = "D:\\Oculus\\Software\\Software\\for-fun-labs-eleven-table-tennis-vr\\RPA\\scoreboard.html"

def generate_scoreboard():
    template = Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ElevenVR Scoreboard</title>
        <style>
            body {
                font-family: 'Roboto', Arial, sans-serif;
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
                border-radius: 10px;
                padding: 10px 20px;
                max-width: 600px;
                margin: 0 auto;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .player {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                width: 40%;
            }
            .player-right {
                align-items: flex-end;
            }
            .player-name {
                font-size: 24px;
                font-weight: bold;
                display: flex;
                align-items: center;
                margin-bottom: 5px;
            }
            .flag {
                width: 32px;
                height: 24px;
                margin-right: 10px;
                vertical-align: middle;
                border-radius: 4px;
            }
            .player-right .flag {
                margin-right: 0;
                margin-left: 10px;
            }
            .score {
                font-size: 48px;
                font-weight: bold;
                margin-top: 5px;
            }
            .elo {
                font-size: 16px;
                color: #aaa;
                margin-top: 5px;
            }
            .match-score {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                width: 20%;
                color: #2ecc71;
            }
            .blue {
                color: #3498db;
            }
            .red {
                color: #e74c3c;
            }
            .player-stats {
                font-size: 14px;
                color: #aaa;
                margin-top: 5px;
            }
            .set-indicator {
                font-size: 18px;
                font-weight: bold;
                color: #f1c40f;
                margin-left: 5px;
            }
        </style>
        <script>
            let lastSuccessfulData = null;

            function updateScoreboard() {
                fetch('match_data.json')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        lastSuccessfulData = data;
                        updateScoreboardDisplay(data);
                    })
                    .catch(error => {
                        console.error('Error fetching scoreboard data:', error);
                        if (lastSuccessfulData) {
                            updateScoreboardDisplay(lastSuccessfulData);
                        }
                    });
            }

            function updateScoreboardDisplay(data) {
                document.querySelector('.player-name.blue').innerHTML = `
                    <img class="flag" src="https://flagcdn.com/w40/${data.playerCountryCodes[0].toLowerCase()}.png" alt="${data.playerCountryCodes[0]} flag">
                    ${data.playerNames[0]}
                    ${Array(data.currentSetStatus[0]).fill('<span class="set-indicator">●</span>').join('')}
                `;
                document.querySelector('.player-name.red').innerHTML = `
                    ${Array(data.currentSetStatus[1]).fill('<span class="set-indicator">●</span>').join('')}
                    ${data.playerNames[1]}
                    <img class="flag" src="https://flagcdn.com/w40/${data.playerCountryCodes[1].toLowerCase()}.png" alt="${data.playerCountryCodes[1]} flag">
                `;
                document.querySelector('.score.blue').textContent = data.currentScores.length > 0 ? data.currentScores[data.currentScores.length - 1][0] : '0';
                document.querySelector('.score.red').textContent = data.currentScores.length > 0 ? data.currentScores[data.currentScores.length - 1][1] : '0';
                document.querySelector('.match-score').textContent = `${data.matchScore[0]} - ${data.matchScore[1]}`;
                document.querySelectorAll('.elo')[0].textContent = `ELO ${data.playerELOs[0]}`;
                document.querySelectorAll('.elo')[1].textContent = `ELO ${data.playerELOs[1]}`;
                document.querySelectorAll('.player-stats')[0].textContent = `WR#${data.playerRanks[0]} | W/L: ${data.playerWins[0]}/${data.playerLosses[0]}`;
                document.querySelectorAll('.player-stats')[1].textContent = `WR#${data.playerRanks[1]} | W/L: ${data.playerWins[1]}/${data.playerLosses[1]}`;
            }

            // 页面加载完成后立即更新一次
            document.addEventListener('DOMContentLoaded', updateScoreboard);

            // 每3秒更新一次计分板
            setInterval(updateScoreboard, 3000);  
        </script>
    </head>
    <body>
        <div class="scoreboard">
            <div class="player">
                <div class="player-name blue">Loading...</div>
                <div class="score blue">0</div>
                <div class="elo">ELO -</div>
                <div class="player-stats">-</div>
            </div>
            <div class="match-score">0 - 0</div>
            <div class="player player-right">
                <div class="player-name red">Loading...</div>
                <div class="score red">0</div>
                <div class="elo">ELO -</div>
                <div class="player-stats">-</div>
            </div>
        </div>
    </body>
    </html>
    ''')
    
    html_output = template.render(match_json='match_data.json')
    
    with open(SCOREBOARD_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html_output)

if __name__ == "__main__":
    generate_scoreboard()
