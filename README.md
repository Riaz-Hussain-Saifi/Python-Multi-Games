# Python Multi-Games Platform

A multiplayer game platform built with Streamlit that allows multiple users to compete against each other in different games.

## 🎮 Features

- **Multi-player Support**: Play games with friends on different devices
- **Unique User IDs**: Each player gets a unique ID starting from 01
- **Real-time Matching**: Automatically pairs players who want to play the same game
- **Multiple Games**: Three distinct games to choose from
- **Leaderboard**: Track scores across all games
- **Responsive Design**: Works on desktop and mobile devices

## 🎲 Available Games

### 1. Programming Quiz Battle 🧠
Test your knowledge of programming languages (NextJS, TypeScript, Python) with different difficulty levels. The player with the most correct answers wins!

### 2. Cricket Showdown 🏏
A turn-based cricket simulation game where players choose actions (Bowl, Bat, Field) and get results based on chance.

### 3. Pattern Matching Duel 🧩
Identify patterns in sequences of numbers, colors, or shapes. The player who identifies the most patterns correctly wins!

## 🚀 Setup and Installation

### Prerequisites
- Python 3.7 or higher
- Streamlit
- Pandas

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Riaz-Hussain-Saifi/Python-Multi-Games.git
cd Python-Multi-Games
```

2. Install the required packages:
```bash
pip install streamlit pandas
```

3. Run the application:
```bash
streamlit run main.py
```

4. Open the provided URL in your browser (typically http://localhost:8501).

## 📝 How to Play

1. **Register**: Enter your name to join the platform. You'll receive a unique user ID.
2. **Select a Game**: Choose from Programming Quiz, Cricket Game, or Pattern Matching.
3. **Wait for Opponent**: The system will keep you in a waiting room until another player selects the same game.
4. **Play the Game**: Once matched, play against your opponent according to the specific game rules.
5. **Check Scores**: View your scores on the leaderboard.

## 📱 Multi-device Usage

For the best experience, access the application from multiple devices using the network URL provided when you run the application. If you're running on your local network, other devices can join by accessing the IP address shown in the Streamlit output.

## 🔧 Technical Details

- Built with Streamlit for the UI
- Uses session state to manage user data and game state
- Implements a waiting room system for player matching
- Dynamically generates quiz questions and puzzles
- Tracks user scores across games

## 🧑‍💻 Developer

Created by Riaz Hussain Saifi

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.