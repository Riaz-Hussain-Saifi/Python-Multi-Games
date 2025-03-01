import streamlit as st
import random
import time
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional
import uuid

# === Data Models ===
@dataclass
class User:
    id: int
    name: str
    score: int = 0
    current_game: Optional[str] = None
    
@dataclass
class Question:
    id: int
    text: str
    options: List[str]
    correct_answer: int
    difficulty: str
    category: str

# === Database Simulation ===
if 'users' not in st.session_state:
    st.session_state.users = {}
    
if 'next_user_id' not in st.session_state:
    st.session_state.next_user_id = 1
    
if 'waiting_users' not in st.session_state:
    st.session_state.waiting_users = []
    
if 'active_games' not in st.session_state:
    st.session_state.active_games = {}
    
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# === Question Database ===
# NextJS 15 Questions
nextjs_easy = [
    Question(1, "What is NextJS?", ["A JavaScript library", "A React framework", "A database system", "A CSS framework"], 1, "easy", "NextJS 15"),
    Question(2, "Which company develops NextJS?", ["Facebook", "Google", "Vercel", "Amazon"], 2, "easy", "NextJS 15"),
    Question(3, "What is the latest version of NextJS as of 2024?", ["NextJS 13", "NextJS 14", "NextJS 15", "NextJS 16"], 2, "easy", "NextJS 15"),
    Question(4, "What does SSR stand for in NextJS?", ["Server Side Rendering", "Single Source Routing", "Static Site Rendering", "System State Reducer"], 0, "easy", "NextJS 15"),
]

nextjs_medium = [
    Question(5, "What is the App Router in NextJS 15?", ["A navigation component", "A new routing system", "A state management tool", "A form handling library"], 1, "medium", "NextJS 15"),
    Question(6, "Which function is used for server-side data fetching in NextJS?", ["useEffect", "getServerSideProps", "useState", "fetchData"], 1, "medium", "NextJS 15"),
    Question(7, "What is the purpose of 'next.config.js'?", ["To configure database", "To configure the application", "To define components", "To set up routing"], 1, "medium", "NextJS 15"),
    Question(8, "Which of these is NOT a data fetching method in NextJS?", ["getStaticProps", "getServerSideProps", "getInitialProps", "getFetchProps"], 3, "medium", "NextJS 15"),
]

nextjs_hard = [
    Question(9, "What is the purpose of Incremental Static Regeneration in NextJS?", ["To update cached pages incrementally", "To add new components gradually", "To load JavaScript incrementally", "To scale servers incrementally"], 0, "hard", "NextJS 15"),
    Question(10, "Which API is used for API routes in NextJS App Router?", ["API Routes", "Route Handlers", "Server Actions", "Edge Functions"], 1, "hard", "NextJS 15"),
    Question(11, "What is the purpose of the 'use client' directive in NextJS?", ["To specify client components", "To enforce client-side validation", "To enable WebSockets", "To optimize bundle size"], 0, "hard", "NextJS 15"),
    Question(12, "How can you handle middleware in NextJS 15?", ["Using the middleware.js file", "Using getMiddleware function", "Using the middleware prop", "Using a plugin system"], 0, "hard", "NextJS 15"),
]

# TypeScript Questions
typescript_easy = [
    Question(13, "What is TypeScript?", ["A JavaScript framework", "A superset of JavaScript", "A database language", "A markup language"], 1, "easy", "TypeScript"),
    Question(14, "Which company developed TypeScript?", ["Google", "Facebook", "Microsoft", "Amazon"], 2, "easy", "TypeScript"),
    Question(15, "What file extension is used for TypeScript files?", [".ts", ".tsx", ".type", ".tsc"], 0, "easy", "TypeScript"),
    Question(16, "What does TypeScript add to JavaScript?", ["Static typing", "More libraries", "Faster execution", "Database integration"], 0, "easy", "TypeScript"),
]

typescript_medium = [
    Question(17, "What is an interface in TypeScript?", ["A class implementation", "A type definition structure", "A module system", "A function type"], 1, "medium", "TypeScript"),
    Question(18, "Which symbol is used for optional properties in TypeScript interfaces?", ["?", "!", "*", "$"], 0, "medium", "TypeScript"),
    Question(19, "What is the 'any' type in TypeScript?", ["A type for numbers only", "A type for strings only", "A type that can be anything", "A type for functions"], 2, "medium", "TypeScript"),
    Question(20, "What are generics in TypeScript?", ["Global variables", "Type variables", "Special classes", "External modules"], 1, "medium", "TypeScript"),
]

typescript_hard = [
    Question(21, "What is a discriminated union in TypeScript?", ["A union with a common property", "A type for mathematical operations", "A special class hierarchy", "A module system"], 0, "hard", "TypeScript"),
    Question(22, "What is the 'never' type used for in TypeScript?", ["Values that never occur", "Infinite loops", "Undefined variables", "Type casting"], 0, "hard", "TypeScript"),
    Question(23, "What is a TypeScript decorator?", ["A special comment", "A design pattern", "A special function that can modify classes and members", "A type casting tool"], 2, "hard", "TypeScript"),
    Question(24, "What is the difference between 'interface' and 'type' in TypeScript?", ["Interfaces can be extended, types cannot", "Types can be used for primitives, interfaces cannot", "Interfaces are faster, types are slower", "There is no difference"], 1, "hard", "TypeScript"),
]

# Python Questions
python_easy = [
    Question(25, "What is Python?", ["A snake species", "A programming language", "A database system", "A web framework"], 1, "easy", "Python"),
    Question(26, "Who created Python?", ["Guido van Rossum", "Bill Gates", "Linus Torvalds", "Mark Zuckerberg"], 0, "easy", "Python"),
    Question(27, "Which symbol is used for comments in Python?", ["//", "/*", "#", "<!-- -->"], 2, "easy", "Python"),
    Question(28, "What data type is used to store multiple items in Python?", ["Array", "List", "Multiple", "Package"], 1, "easy", "Python"),
]

python_medium = [
    Question(29, "What is a lambda function in Python?", ["A named function", "An anonymous function", "A class method", "A module"], 1, "medium", "Python"),
    Question(30, "What does PEP 8 refer to in Python?", ["A security protocol", "A style guide", "A version of Python", "A standard library"], 1, "medium", "Python"),
    Question(31, "What is the purpose of __init__ method in Python?", ["To initialize class attributes", "To import modules", "To define iterators", "To terminate a program"], 0, "medium", "Python"),
    Question(32, "What is a decorator in Python?", ["A function that modifies another function", "A class attribute", "A type of comment", "A GUI element"], 0, "medium", "Python"),
]

python_hard = [
    Question(33, "What is a metaclass in Python?", ["A class that inherits from another class", "A class whose instances are classes", "A design pattern", "A type of function"], 1, "hard", "Python"),
    Question(34, "What is the Global Interpreter Lock (GIL) in Python?", ["A security feature", "A mutex that protects access to Python objects", "A compiler optimization", "A memory management technique"], 1, "hard", "Python"),
    Question(35, "What is a context manager in Python?", ["A tool for managing file contexts", "An object that manages the context of a block of code", "A function decorator", "A type of module"], 1, "hard", "Python"),
    Question(36, "What is a generator in Python?", ["A function that returns an iterator", "A class that generates random numbers", "A module that creates files", "A tool for creating GUI elements"], 0, "hard", "Python"),
]

all_questions = nextjs_easy + nextjs_medium + nextjs_hard + typescript_easy + typescript_medium + typescript_hard + python_easy + python_medium + python_hard

# === Cricket Game Data ===
cricket_actions = ["Bowl", "Bat", "Field"]
cricket_outcomes = {
    "Bowl": ["Wicket", "Dot ball", "Boundary", "Single", "Double", "No ball"],
    "Bat": ["Six", "Four", "Single", "Double", "Defended", "Out"],
    "Field": ["Catch", "Miss", "Run out", "Stumping", "Boundary save", "Overthrow"]
}

cricket_points = {
    "Wicket": 10, "Dot ball": 2, "Boundary": 1, "Single": 1, "Double": 1, "No ball": -1,
    "Six": 6, "Four": 4, "Single": 1, "Double": 2, "Defended": 0, "Out": -5,
    "Catch": 5, "Miss": -2, "Run out": 7, "Stumping": 6, "Boundary save": 3, "Overthrow": -3
}

# === Game Logic Functions ===
def create_user():
    st.title("🎮 Multi-Player Game Hub 🎮")
    
    with st.form("user_form"):
        name = st.text_input("Enter your name:")
        submit = st.form_submit_button("Join Games")
        
        if submit and name:
            # Format user ID with leading zeros
            user_id = st.session_state.next_user_id
            st.session_state.next_user_id += 1
            
            new_user = User(id=user_id, name=name)
            st.session_state.users[user_id] = new_user
            st.session_state.current_user = user_id
            
            # Only add to waiting users when they select a game
            st.success(f"Welcome {name}! Your user ID is: {user_id:02d}")
            st.rerun()

def quiz_game(user1, user2):
    st.title("🧠 Programming Quiz Battle 🧠")
    
    game_id = f"quiz_{user1}_{user2}"
    
    if game_id not in st.session_state.active_games:
        # Initialize the game
        st.session_state.active_games[game_id] = {
            "users": [user1, user2],
            "current_round": 1,
            "max_rounds": 12,
            "user_answers": {user1: {}, user2: {}},
            "questions": random.sample(all_questions, 12),
            "current_user_idx": 0,
            "game_over": False
        }
    
    game = st.session_state.active_games[game_id]
    current_user_id = game["users"][game["current_user_idx"]]
    opponent_id = game["users"][1 - game["current_user_idx"]]
    
    # Show game status
    st.info(f"Round {game['current_round']} of {game['max_rounds']}")
    
    user1_name = st.session_state.users[user1].name
    user2_name = st.session_state.users[user2].name
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"Player 1: {user1_name} (ID: {user1:02d})", 
                 value=sum(1 for q, a in game["user_answers"].get(user1, {}).items() 
                         if a == game["questions"][int(q)].correct_answer))
    
    with col2:
        st.metric(f"Player 2: {user2_name} (ID: {user2:02d})", 
                 value=sum(1 for q, a in game["user_answers"].get(user2, {}).items() 
                         if a == game["questions"][int(q)].correct_answer))
    
    # Check if the game is complete
    if game["current_round"] > game["max_rounds"]:
        if not game["game_over"]:
            # Calculate scores
            user1_score = sum(1 for q, a in game["user_answers"].get(user1, {}).items() 
                            if a == game["questions"][int(q)].correct_answer)
            user2_score = sum(1 for q, a in game["user_answers"].get(user2, {}).items() 
                            if a == game["questions"][int(q)].correct_answer)
            
            st.balloons()
            if user1_score > user2_score:
                st.success(f"🎉 Congratulations! {user1_name} (ID: {user1:02d}) wins with {user1_score} correct answers!")
            elif user2_score > user1_score:
                st.success(f"🎉 Congratulations! {user2_name} (ID: {user2:02d}) wins with {user2_score} correct answers!")
            else:
                st.success(f"🎉 It's a tie! Both players got {user1_score} correct answers!")
            
            # Update user scores
            st.session_state.users[user1].score += user1_score
            st.session_state.users[user2].score += user2_score
            
            # Mark game as over
            game["game_over"] = True
            
            if st.button("Return to Game Selection"):
                # Remove users from this game
                if user1 in st.session_state.waiting_users:
                    st.session_state.waiting_users.remove(user1)
                if user2 in st.session_state.waiting_users:
                    st.session_state.waiting_users.remove(user2)
                
                # Clean up the game
                del st.session_state.active_games[game_id]
                
                # Reset current game for both users
                st.session_state.users[user1].current_game = None
                st.session_state.users[user2].current_game = None
                
                st.rerun()
        
        return
    
    # Show the current question if it's this user's turn
    if st.session_state.current_user == current_user_id:
        current_q_idx = game["current_round"] - 1
        question = game["questions"][current_q_idx]
        
        st.subheader(f"Question {game['current_round']} ({question.category} - {question.difficulty})")
        st.write(question.text)
        
        answer = st.radio("Select your answer:", question.options, key=f"q_{current_q_idx}")
        answer_idx = question.options.index(answer)
        
        if st.button("Submit Answer"):
            # Record the answer
            game["user_answers"].setdefault(current_user_id, {})[str(current_q_idx)] = answer_idx
            
            # Switch to the next player or advance the round
            game["current_user_idx"] = 1 - game["current_user_idx"]
            if game["current_user_idx"] == 0:
                game["current_round"] += 1
            
            st.rerun()
    else:
        st.info(f"Waiting for {st.session_state.users[current_user_id].name} to answer...")
        time.sleep(1)  # Add a small delay to prevent too many reruns
        st.rerun()

def cricket_game(user1, user2):
    st.title("🏏 Cricket Showdown 🏏")
    
    game_id = f"cricket_{user1}_{user2}"
    
    if game_id not in st.session_state.active_games:
        # Initialize the game
        st.session_state.active_games[game_id] = {
            "users": [user1, user2],
            "current_round": 1,
            "max_rounds": 10,
            "scores": {user1: 0, user2: 0},
            "current_user_idx": 0,
            "game_over": False,
            "actions": {},
            "results": {}
        }
    
    game = st.session_state.active_games[game_id]
    current_user_id = game["users"][game["current_user_idx"]]
    opponent_id = game["users"][1 - game["current_user_idx"]]
    
    # Show game status
    st.info(f"Round {game['current_round']} of {game['max_rounds']}")
    
    user1_name = st.session_state.users[user1].name
    user2_name = st.session_state.users[user2].name
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"Player 1: {user1_name} (ID: {user1:02d})", value=game["scores"][user1])
    
    with col2:
        st.metric(f"Player 2: {user2_name} (ID: {user2:02d})", value=game["scores"][user2])
    
    # Show previous actions
    if len(game.get("results", {})) > 0:
        st.subheader("Match Summary")
        
        results_df = []
        for round_num in range(1, game["current_round"]):
            round_key = f"round_{round_num}"
            if round_key in game["results"]:
                user1_action = game["actions"].get(f"{user1}_{round_num}", "")
                user1_result = game["results"][round_key].get(user1, "")
                user1_points = cricket_points.get(user1_result, 0)
                
                user2_action = game["actions"].get(f"{user2}_{round_num}", "")
                user2_result = game["results"][round_key].get(user2, "")
                user2_points = cricket_points.get(user2_result, 0)
                
                results_df.append({
                    "Round": round_num,
                    f"{user1_name} Action": user1_action,
                    f"{user1_name} Result": f"{user1_result} ({user1_points} pts)",
                    f"{user2_name} Action": user2_action,
                    f"{user2_name} Result": f"{user2_result} ({user2_points} pts)"
                })
        
        if results_df:
            st.dataframe(pd.DataFrame(results_df))
    
    # Check if the game is complete
    if game["current_round"] > game["max_rounds"]:
        if not game["game_over"]:
            st.balloons()
            if game["scores"][user1] > game["scores"][user2]:
                st.success(f"🎉 Congratulations! {user1_name} (ID: {user1:02d}) wins with {game['scores'][user1]} points!")
            elif game["scores"][user2] > game["scores"][user1]:
                st.success(f"🎉 Congratulations! {user2_name} (ID: {user2:02d}) wins with {game['scores'][user2]} points!")
            else:
                st.success(f"🎉 It's a tie! Both players got {game['scores'][user1]} points!")
            
            # Update user scores
            st.session_state.users[user1].score += game["scores"][user1]
            st.session_state.users[user2].score += game["scores"][user2]
            
            # Mark game as over
            game["game_over"] = True
            
            if st.button("Return to Game Selection"):
                # Remove users from this game
                if user1 in st.session_state.waiting_users:
                    st.session_state.waiting_users.remove(user1)
                if user2 in st.session_state.waiting_users:
                    st.session_state.waiting_users.remove(user2)
                
                # Clean up the game
                del st.session_state.active_games[game_id]
                
                # Reset current game for both users
                st.session_state.users[user1].current_game = None
                st.session_state.users[user2].current_game = None
                
                st.rerun()
        
        return
    
    # Show the current action selection if it's this user's turn
    if st.session_state.current_user == current_user_id:
        st.subheader(f"Your turn, {st.session_state.users[current_user_id].name}!")
        
        action = st.selectbox("Choose your cricket action:", cricket_actions)
        
        if st.button("Submit Action"):
            # Record the action
            action_key = f"{current_user_id}_{game['current_round']}"
            game["actions"][action_key] = action
            
            # Determine the result
            result = random.choice(cricket_outcomes[action])
            
            # Record the result
            round_key = f"round_{game['current_round']}"
            if round_key not in game["results"]:
                game["results"][round_key] = {}
            
            game["results"][round_key][current_user_id] = result
            
            # Update score
            points = cricket_points.get(result, 0)
            game["scores"][current_user_id] += points
            
            # Switch to the next player or advance the round
            game["current_user_idx"] = 1 - game["current_user_idx"]
            if game["current_user_idx"] == 0:
                game["current_round"] += 1
            
            st.rerun()
    else:
        st.info(f"Waiting for {st.session_state.users[current_user_id].name} to take their turn...")
        time.sleep(1)  # Add a small delay to prevent too many reruns
        st.rerun()

def puzzle_game(user1, user2):
    st.title("🧩 Pattern Matching Duel 🧩")
    
    game_id = f"puzzle_{user1}_{user2}"
    
    if game_id not in st.session_state.active_games:
        # Generate patterns
        patterns = []
        for _ in range(10):
            pattern_type = random.choice(["number", "color", "shape"])
            
            if pattern_type == "number":
                start = random.randint(1, 20)
                step = random.randint(1, 5)
                pattern = [start + i*step for i in range(4)]
                answer = start + 4*step
                pattern_display = ", ".join(str(n) for n in pattern)
                pattern_desc = "What's the next number in this sequence?"
                options = [answer, answer + random.randint(1, 3), answer - random.randint(1, 3), answer + step*2]
            
            elif pattern_type == "color":
                colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
                pattern_length = random.randint(3, 5)
                pattern = [random.choice(colors) for _ in range(pattern_length)]
                # Repeat the pattern
                answer = pattern[0]
                pattern_display = " → ".join(pattern)
                pattern_desc = "If this pattern repeats, what comes next?"
                
                other_options = [c for c in colors if c != answer]
                random.shuffle(other_options)
                options = [answer] + other_options[:3]
            
            else:  # shape
                shapes = ["Circle", "Square", "Triangle", "Diamond", "Star", "Hexagon"]
                pattern = [random.choice(shapes) for _ in range(3)]
                answer = random.choice(shapes)
                pattern_display = " → ".join(pattern)
                pattern_desc = "What shape would best complete this pattern?"
                
                other_options = [s for s in shapes if s != answer]
                random.shuffle(other_options)
                options = [answer] + other_options[:3]
            
            random.shuffle(options)
            correct_idx = options.index(answer)
            
            patterns.append({
                "display": pattern_display,
                "desc": pattern_desc,
                "options": options,
                "correct_idx": correct_idx
            })
        
        # Initialize the game
        st.session_state.active_games[game_id] = {
            "users": [user1, user2],
            "current_round": 1,
            "max_rounds": 10,
            "patterns": patterns,
            "user_answers": {user1: {}, user2: {}},
            "current_user_idx": 0,
            "game_over": False
        }
    
    game = st.session_state.active_games[game_id]
    current_user_id = game["users"][game["current_user_idx"]]
    opponent_id = game["users"][1 - game["current_user_idx"]]
    
    # Show game status
    st.info(f"Round {game['current_round']} of {game['max_rounds']}")
    
    user1_name = st.session_state.users[user1].name
    user2_name = st.session_state.users[user2].name
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"Player 1: {user1_name} (ID: {user1:02d})", 
                 value=sum(1 for r, a in game["user_answers"].get(user1, {}).items() 
                         if a == game["patterns"][int(r)]["correct_idx"]))
    
    with col2:
        st.metric(f"Player 2: {user2_name} (ID: {user2:02d})", 
                 value=sum(1 for r, a in game["user_answers"].get(user2, {}).items() 
                         if a == game["patterns"][int(r)]["correct_idx"]))
    
    # Check if the game is complete
    if game["current_round"] > game["max_rounds"]:
        if not game["game_over"]:
            # Calculate scores
            user1_score = sum(1 for r, a in game["user_answers"].get(user1, {}).items() 
                            if a == game["patterns"][int(r)]["correct_idx"])
            user2_score = sum(1 for r, a in game["user_answers"].get(user2, {}).items() 
                            if a == game["patterns"][int(r)]["correct_idx"])
            
            st.balloons()
            if user1_score > user2_score:
                st.success(f"🎉 Congratulations! {user1_name} (ID: {user1:02d}) wins with {user1_score} correct answers!")
            elif user2_score > user1_score:
                st.success(f"🎉 Congratulations! {user2_name} (ID: {user2:02d}) wins with {user2_score} correct answers!")
            else:
                st.success(f"🎉 It's a tie! Both players got {user1_score} correct answers!")
            
            # Update user scores
            st.session_state.users[user1].score += user1_score
            st.session_state.users[user2].score += user2_score
            
            # Mark game as over
            game["game_over"] = True
            
            if st.button("Return to Game Selection"):
                # Remove users from this game
                if user1 in st.session_state.waiting_users:
                    st.session_state.waiting_users.remove(user1)
                if user2 in st.session_state.waiting_users:
                    st.session_state.waiting_users.remove(user2)
                
                # Clean up the game
                del st.session_state.active_games[game_id]
                
                # Reset current game for both users
                st.session_state.users[user1].current_game = None
                st.session_state.users[user2].current_game = None
                
                st.rerun()
        
        return
    
    # Show the current pattern if it's this user's turn
    if st.session_state.current_user == current_user_id:
        current_pattern = game["patterns"][game["current_round"] - 1]
        
        st.subheader(f"Pattern #{game['current_round']}")
        st.write(f"**{current_pattern['display']}**")
        st.write(current_pattern['desc'])
        
        answer = st.radio("Select your answer:", current_pattern["options"], key=f"pattern_{game['current_round']}")
        answer_idx = current_pattern["options"].index(answer)
        
        if st.button("Submit Answer"):
            # Record the answer
            game["user_answers"].setdefault(current_user_id, {})[str(game["current_round"] - 1)] = answer_idx
            
            # Switch to the next player or advance the round
            game["current_user_idx"] = 1 - game["current_user_idx"]
            if game["current_user_idx"] == 0:
                game["current_round"] += 1
            
            st.rerun()
    else:
        st.info(f"Waiting for {st.session_state.users[current_user_id].name} to answer...")
        time.sleep(1)  # Add a small delay to prevent too many reruns
        st.rerun()

def waiting_room():
    st.title("⏳ Waiting Room ⏳")
    
    user_id = st.session_state.current_user
    user = st.session_state.users[user_id]
    game_type = user.current_game
    
    # Show waiting message with current game selected
    if game_type == "quiz":
        game_name = "Programming Quiz"
    elif game_type == "cricket":
        game_name = "Cricket Game"
    else:
        game_name = "Pattern Matching"
        
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px; margin: 20px 0;">
        <h2>Waiting for another player to join...</h2>
        <p>You selected: <strong>{game_name}</strong></p>
        <p>Your User ID: <strong>{user_id:02d}</strong></p>
        <p>Your Name: <strong>{user.name}</strong></p>
        <p>Please wait until another player joins the game.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display animated waiting indicator
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 30px 0;">
        <div style="border: 16px solid #f3f3f3; border-top: 16px solid #3498db; border-radius: 50%; width: 80px; height: 80px; animation: spin 2s linear infinite;"></div>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Check every few seconds if a match is available
    time.sleep(2)
    st.rerun()

def game_selection():
    st.title("🎲 Game Selection 🎲")
    
    user_id = st.session_state.current_user
    user = st.session_state.users[user_id]
    
    st.info(f"Welcome, {user.name} (ID: {user_id:02d})!")
    
    st.write("Choose a game to play:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💻 Programming Quiz", key="quiz_btn"):
            user.current_game = "quiz"
            if user_id not in st.session_state.waiting_users:
                st.session_state.waiting_users.append(user_id)
            st.rerun()
    
    with col2:
        if st.button("🏏 Cricket Game", key="cricket_btn"):
            user.current_game = "cricket"
            if user_id not in st.session_state.waiting_users:
                st.session_state.waiting_users.append(user_id)
            st.rerun()
    
    with col3:
        if st.button("🧩 Pattern Matching", key="puzzle_btn"):
            user.current_game = "puzzle"
            if user_id not in st.session_state.waiting_users:
                st.session_state.waiting_users.append(user_id)
            st.rerun()
    
    # Show leaderboard
    st.subheader("🏆 Leaderboard 🏆")
    
    if st.session_state.users:
        users_list = sorted(st.session_state.users.values(), key=lambda u: u.score, reverse=True)
        leaderboard_data = [{"Rank": i+1, "Name": u.name, "ID": f"{u.id:02d}", "Score": u.score} 
                           for i, u in enumerate(users_list)]
        
        st.dataframe(pd.DataFrame(leaderboard_data))
    else:
        st.write("No players have joined yet.")

# === Main App Logic ===
def main():
    st.set_page_config(
        page_title="Multiplayer Game Hub",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Add custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #f5f7ff;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        height: 3em;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # If no user is logged in, show registration
    if not st.session_state.current_user:
        create_user()
        return
    
    # Current user exists, check status
    user_id = st.session_state.current_user
    user = st.session_state.users[user_id]
    
    # Check if the user is in an active game
    for game_id, game in st.session_state.active_games.items():
        if user_id in game["users"]:
            # Determine game type from game_id
            if game_id.startswith("quiz_"):
                user1, user2 = game_id.split("_")[1:]
                quiz_game(int(user1), int(user2))
            elif game_id.startswith("cricket_"):
                user1, user2 = game_id.split("_")[1:]
                cricket_game(int(user1), int(user2))
            elif game_id.startswith("puzzle_"):
                user1, user2 = game_id.split("_")[1:]
                puzzle_game(int(user1), int(user2))
            return
    
    # Check if the user is waiting for a game
    if user_id in st.session_state.waiting_users and user.current_game:
        # Find a matching user
        other_waiting_users = [u for u in st.session_state.waiting_users 
                              if u != user_id and 
                              st.session_state.users[u].current_game == user.current_game]
        
        if other_waiting_users:
            # Found a match!
            other_user_id = other_waiting_users[0]
            
            # Remove both users from waiting list
            st.session_state.waiting_users.remove(user_id)
            st.session_state.waiting_users.remove(other_user_id)
            
            # Create a game
            game_type = user.current_game
            game_id = f"{game_type}_{user_id}_{other_user_id}"
            
            # Add placeholder for the game
            st.session_state.active_games[game_id] = {
                "users": [user_id, other_user_id],
                "current_round": 1
            }
            
            st.rerun()
        else:
            # No match yet, show waiting screen
            waiting_room()
            return
    
    # If no active game or waiting, show game selection
    game_selection()

if __name__ == "__main__":
    main()