import streamlit as st
import random

# ---------- Initialize session state ----------
if "menu" not in st.session_state:
    st.session_state.menu = "main"   # main=menu, name=name input, game=playing
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "play_with_ai" not in st.session_state:
    st.session_state.play_with_ai = False
if "player1" not in st.session_state:
    st.session_state.player1 = "Player 1"
if "player2" not in st.session_state:
    st.session_state.player2 = "Player 2"


# ---------- Reset game ----------
def reset():
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None


# ---------- Check winner ----------
def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None


# ---------- AI move ----------
def ai_move():
    empty = [i for i in range(9) if st.session_state.board[i] == ""]
    if empty:
        move = random.choice(empty)
        st.session_state.board[move] = "O"


# ---------- Menu Screen ----------
if st.session_state.menu == "main":
    st.title("🎮 Tic Tac Toe")
    st.write("Choose a game mode:")

    if st.button("👥 Play vs Friend"):
        st.session_state.play_with_ai = False
        st.session_state.menu = "name"

    if st.button("🤖 Play vs Computer"):
        st.session_state.play_with_ai = True
        st.session_state.menu = "name"

    if st.button("🚪 Exit Game"):
        st.stop()


# ---------- Name Input Screen ----------
elif st.session_state.menu == "name":
    st.title("📝 Enter Player Name(s)")

    st.session_state.player1 = st.text_input("Enter Player 1 Name:", "Player 1")

    if st.session_state.play_with_ai:
        st.session_state.player2 = "Computer 🤖"
    else:
        st.session_state.player2 = st.text_input("Enter Player 2 Name:", "Player 2")

    if st.button("✅ Start Game"):
        reset()
        st.session_state.menu = "game"

    if st.button("⬅️ Back to Menu"):
        st.session_state.menu = "main"


# ---------- Game Screen ----------
elif st.session_state.menu == "game":
    st.title("🎮 Tic Tac Toe")

    # Draw 3x3 board
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if st.button(st.session_state.board[i] or " ", key=i, use_container_width=True):
                if st.session_state.board[i] == "" and st.session_state.winner is None:
                    # Player move
                    st.session_state.board[i] = st.session_state.turn
                    st.session_state.winner = check_winner(st.session_state.board)

                    # Switch turn
                    if st.session_state.winner is None:
                        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"

                        # AI move if enabled
                        if st.session_state.play_with_ai and st.session_state.turn == "O":
                            ai_move()
                            st.session_state.winner = check_winner(st.session_state.board)
                            st.session_state.turn = "X"

    # Status message
    if st.session_state.winner is None:
        current = st.session_state.player1 if st.session_state.turn == "X" else st.session_state.player2
        st.write(f"👉 {current}'s turn ({st.session_state.turn})")
    elif st.session_state.winner == "Draw":
        st.success("It's a Draw! 🤝")
    else:
        winner = st.session_state.player1 if st.session_state.winner == "X" else st.session_state.player2
        st.success(f"🎉 {winner} wins!")

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Game"):
            reset()
    with col2:
        if st.button("⬅️ Back to Menu"):
            reset()
            st.session_state.menu = "main"