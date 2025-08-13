import streamlit as st
import random
import time
from collections import deque
import numpy as np

class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = deque([(self.width // 2, self.height // 2)])
        self.direction = (1, 0)  # Start moving right
        self.food = self.generate_food()
        self.score = 0
        self.high_score = max(self.score, getattr(self, 'high_score', 0))
        self.game_over = False
        self.paused = False
        self.speed = 0.3  # Initial speed (seconds between moves)
    
    def generate_food(self):
        """Generate food at random position"""
        while True:
            food = (random.randint(0, self.width - 1), 
                   random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        """Move the snake and check collisions"""
        if self.game_over or self.paused:
            return
        
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.appendleft(new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.high_score = max(self.score, self.high_score)
            self.food = self.generate_food()
            # Increase speed slightly
            self.speed = max(0.1, self.speed - 0.02)
        else:
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent 180-degree turns)"""
        if (new_direction[0] != -self.direction[0] or 
            new_direction[1] != -self.direction[1]):
            self.direction = new_direction
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused

def create_game_board(game):
    """Create the game board array"""
    board = np.zeros((game.height, game.width), dtype=int)
    
    # Place snake
    for i, segment in enumerate(game.snake):
        if i == 0:  # Head
            board[segment[1], segment[0]] = 2
        else:  # Body
            board[segment[1], segment[0]] = 1
    
    # Place food
    board[game.food[1], game.food[0]] = 3
    
    return board

def render_game_board(board):
    """Render the game board as HTML"""
    board_html = "<div style='display: flex; justify-content: center; margin: 20px 0;'>"
    board_html += "<div style='border: 3px solid #333; background: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>"
    
    for row in board:
        board_html += "<div style='display: flex;'>"
        for cell in row:
            if cell == 0:  # Empty
                board_html += "<div style='width: 25px; height: 25px; background: #e9ecef; border: 1px solid #dee2e6; border-radius: 3px; margin: 1px;'></div>"
            elif cell == 1:  # Snake body
                board_html += "<div style='width: 25px; height: 25px; background: #28a745; border: 1px solid #1e7e34; border-radius: 3px; margin: 1px;'></div>"
            elif cell == 2:  # Snake head
                board_html += "<div style='width: 25px; height: 25px; background: #20c997; border: 1px solid #13855c; border-radius: 3px; margin: 1px;'></div>"
            elif cell == 3:  # Food
                board_html += "<div style='width: 25px; height: 25px; background: #dc3545; border: 1px solid #c82333; border-radius: 50%; margin: 1px;'></div>"
        board_html += "</div>"
    
    board_html += "</div></div>"
    return board_html

def main():
    st.set_page_config(
        page_title="🐍 Snake Game",
        page_icon="🐍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E7D32;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .game-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .control-button {
        margin: 5px;
    }
    .game-status {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🐍 Snake Game</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'game' not in st.session_state:
        st.session_state.game = SnakeGame()
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    
    # Sidebar with game info and controls
    with st.sidebar:
        st.header("📊 Game Statistics")
        
        # Game stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score", st.session_state.game.score)
            st.metric("Snake Length", len(st.session_state.game.snake))
        with col2:
            st.metric("High Score", st.session_state.game.high_score)
            st.metric("Speed", f"{1/st.session_state.game.speed:.1f} moves/sec")
        
        st.markdown("---")
        
        # Game controls
        st.header("🎮 Controls")
        
        # Direction controls
        st.subheader("Direction")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⬆️ Up", key="up_btn", use_container_width=True):
                st.session_state.game.change_direction((0, -1))
        
        with col2:
            if st.button("⏸️ Pause", key="pause_btn", use_container_width=True):
                st.session_state.game.toggle_pause()
        
        with col3:
            if st.button("🔄 Restart", key="restart_btn", use_container_width=True):
                st.session_state.game.reset_game()
                st.rerun()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Left", key="left_btn", use_container_width=True):
                st.session_state.game.change_direction((-1, 0))
        
        with col2:
            if st.button("⬇️ Down", key="down_btn", use_container_width=True):
                st.session_state.game.change_direction((0, 1))
        
        with col3:
            if st.button("➡️ Right", key="right_btn", use_container_width=True):
                st.session_state.game.change_direction((1, 0))
        
        st.markdown("---")
        
        # Game settings
        st.header("⚙️ Settings")
        
        # Speed control
        speed_value = st.slider("Game Speed", 0.1, 0.5, st.session_state.game.speed, 0.01)
        st.session_state.game.speed = speed_value
        
        # Board size control
        board_size = st.selectbox("Board Size", [15, 20, 25, 30], index=1)
        if board_size != st.session_state.game.width:
            st.session_state.game = SnakeGame(board_size, board_size)
            st.rerun()
        
        st.markdown("---")
        
        # Instructions
        st.header("📖 How to Play")
        st.markdown("""
        **Objective**: Eat the red food to grow and score points!
        
        **Controls**:
        - Use the direction buttons or keyboard
        - Arrow keys: ↑ ↓ ← →
        - WASD: W A S D
        
        **Rules**:
        - Don't hit the walls
        - Don't hit your own body
        - Eat food to grow and score
        - Each food = 10 points
        """)
    
    # Main game area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Game board
        game_board = create_game_board(st.session_state.game)
        board_html = render_game_board(game_board)
        st.markdown(board_html, unsafe_allow_html=True)
        
        # Game status
        if st.session_state.game.game_over:
            st.error("💀 Game Over! Click 'Restart' to play again.", icon="💀")
        elif st.session_state.game.paused:
            st.warning("⏸️ Game Paused. Click 'Pause' to continue.", icon="⏸️")
        else:
            st.success("🎮 Game Running! Use the controls to move the snake.", icon="🎮")
    
    # Game loop simulation
    current_time = time.time()
    if (current_time - st.session_state.last_update > st.session_state.game.speed and 
        not st.session_state.game.game_over and not st.session_state.game.paused):
        st.session_state.game.move_snake()
        st.session_state.last_update = current_time
        st.rerun()
    
    # Additional controls at the bottom
    st.markdown("---")
    st.header("🎯 Quick Actions")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⬆️ Move Up", key="quick_up", use_container_width=True):
            st.session_state.game.change_direction((0, -1))
    
    with col2:
        if st.button("⬅️ Move Left", key="quick_left", use_container_width=True):
            st.session_state.game.change_direction((-1, 0))
    
    with col3:
        if st.button("⏸️ Pause/Resume", key="quick_pause", use_container_width=True):
            st.session_state.game.toggle_pause()
    
    with col4:
        if st.button("➡️ Move Right", key="quick_right", use_container_width=True):
            st.session_state.game.change_direction((1, 0))
    
    with col5:
        if st.button("⬇️ Move Down", key="quick_down", use_container_width=True):
            st.session_state.game.change_direction((0, 1))
    
    # Game information
    st.markdown("---")
    st.markdown("""
    ### 🎮 Game Information
    
    **Current Game State:**
    - **Snake Position**: Head at coordinates {}
    - **Food Position**: At coordinates {}
    - **Current Direction**: {}
    - **Game Speed**: {:.1f} moves per second
    
    **Tips for High Score:**
    1. Plan your route ahead to avoid trapping yourself
    2. Use the full game area efficiently
    3. Don't let the game get too fast too quickly
    4. Take breaks by pausing when needed
    """.format(
        st.session_state.game.snake[0] if st.session_state.game.snake else "None",
        st.session_state.game.food,
        ["Right", "Left", "Up", "Down"][
            [(1,0), (-1,0), (0,-1), (0,1)].index(st.session_state.game.direction)
        ] if st.session_state.game.direction in [(1,0), (-1,0), (0,-1), (0,1)] else "Unknown",
        1/st.session_state.game.speed
    ))

if __name__ == "__main__":
    main() 