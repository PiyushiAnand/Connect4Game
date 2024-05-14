# import pygame
# import sys
# from time import sleep
# import socket
# import threading
# # Constants
# HOST = '127.0.0.1'
# PORT = 5555
# WINDOW_WIDTH = 700
# WINDOW_HEIGHT = 700
# ROW_COUNT = 6
# COLUMN_COUNT = 7
# BUTTON_WIDTH = 200
# BUTTON_HEIGHT = 50
# BLUE = (0, 0, 255)
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)
# SQUARESIZE = 100
# FONT_SIZE=36
# RADIUS = int(SQUARESIZE / 2 - 5)
# width = COLUMN_COUNT * SQUARESIZE
# height = (ROW_COUNT + 1) * SQUARESIZE
# size = (width, height)




# def draw_button(screen, rect, color, text):
#     pygame.draw.rect(screen, color, rect)
#     font = pygame.font.Font(None, 36)
#     text_surface = font.render(text, True, WHITE)
#     text_rect = text_surface.get_rect(center=rect.center)
#     screen.blit(text_surface, text_rect)
# def draw_board(screen, board,score1,score2):
#     font = pygame.font.Font(None, 36)
#     for row in range(ROW_COUNT):
#         for col in range(COLUMN_COUNT):
#             pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
#             pygame.draw.circle(screen, WHITE, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
#             if board[row][col] == 1:
#                 pygame.draw.circle(screen, RED, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
#             elif board[row][col] == 2:
#                 pygame.draw.circle(screen, YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
#     text1 = f"Player 1 Score: {score1}"
#     text_surface1 = font.render(text1, True, (255, 0, 0))
#     text_x1 = (WINDOW_WIDTH - text_surface1.get_width()) // 2 - 150
#     text_y1 = (WINDOW_HEIGHT - text_surface1.get_height()) // 2 - 300
#     screen.blit(text_surface1, (text_x1, text_y1))
                
#         # Display scores for Player 2
#     text2 = f"Player 2 Score: {score2}"
#     text_surface2 = font.render(text2, True, (255, 0, 0))
#     text_x2 = (WINDOW_WIDTH - text_surface2.get_width()) // 2 + 150
#     text_y2 = (WINDOW_HEIGHT - text_surface2.get_height()) // 2 - 300
#     screen.blit(text_surface2, (text_x2, text_y2))

# def drop_piece(screen, board, row, col, piece,score1,score2):
#     if row is not None:
#         falling_piece_y = 0
#         final_y = (row + 1) * SQUARESIZE + SQUARESIZE // 2

#         while falling_piece_y < final_y:
#             screen.fill(BLACK)
#             draw_board(screen, board,score1,score2)
#             # Draw the falling piece
#             pygame.draw.circle(screen, RED if piece == 1 else YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, falling_piece_y), RADIUS, width=0)
#             pygame.display.update()
#             falling_piece_y += 50  # Adjust the speed of falling here (larger value for faster)
#             pygame.time.delay(50)

#         board[row][col] = piece

# def is_valid(board, col):
#     return board[0][col] == 0

# def get_next_row(board, col):
#     for r in range(ROW_COUNT - 1, -1, -1):
#         if board[r][col] == 0:
#             return r
# def check_points(board, row, col):
#     # Check for horizontal, vertical, and diagonal (down-right and down-left) matches
#     for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
#         count = 0
#         r, c = row, col
#         while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == board[row][col]:
#             count += 1
#             r, c = r + dr, c + dc
#         r, c = row - dr, col - dc
#         while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == board[row][col]:
#             count += 1
#             r, c = r - dr, c - dc
#         if count >= 4:
#             return True
#     return False

# def send_game_data(row, col, client_socket):
#     data = f"{row},{col}"
#     client_socket.sendall(data.encode())

# def receive_game_data(client_socket):
#     try:
#         data = client_socket.recv(1024)
#         if data:
#             row, col = map(int, data.decode().split(","))
#             return row, col
#         else:
#             return None, None
#     except (OSError, ConnectionError) as e:
#         print("Error:", e)
#         return None, None

# # def play_game(screen, board, font, turn, addr, isserver, score1, score2):
# #     winning_player = None
# #     first = False
# #     current = turn

# #     while True:
# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 pygame.quit()
# #                 sys.exit()
# #             if event.type == pygame.MOUSEBUTTONDOWN:
# #                 if not first and not isserver:
# #                     n_r, n_c = receive_game_data(addr)
# #                     if n_c is not None:
# #                         drop_piece(screen, board, n_r, n_c, 3 - turn, score1, score2)

# #                 mouseX = event.pos[0]
# #                 col = mouseX // SQUARESIZE
# #                 if is_valid(board, col):
# #                     row = get_next_row(board, col)
# #                     drop_piece(screen, board, row, col, turn, score1, score2)
# #                     print(board)
# #                     if current == turn and check_points(board, row, col):
# #                         winning_player = "RED" if turn == 1 else "YELLOW"
# #                         if turn == 1:
# #                             score1 += 1
# #                         elif turn == 2:
# #                             score2 += 1
# #                         current = 3 - turn  # Switch player
# #                     send_game_data(row, col, addr)
# #                     n_r, n_c = receive_game_data(addr)
# #                     drop_piece(screen, board, n_r, n_c, 3 - turn, score1, score2)
# #                     first = True
# #                     break

# #         # Display the board and scores
# #         screen.fill(BLACK)
# #         draw_board(screen, board, score1, score2)
# #         pygame.display.update()

# #         if winning_player:
# #             # Update scores and reset winning player
# #             send_game_data(score1, score2, addr)
# #             score1_r, score2_r = receive_game_data(addr)
# #             score1 = max(score1, score1_r)
# #             score2 = max(score2, score2_r)
# #             winning_player = None
# def play_game(screen, board, font, turn, client_socket, isserver, score1, score2):
#     winning_player = None
#     current_turn = turn

#     def receive_thread(client_socket):
#         nonlocal winning_player, current_turn, score1, score2
#         while True:
#             data = receive_game_data(client_socket)
#             if data:
#                 n_r, n_c = data
#                 if n_r is not None and n_c is not None:
#                     drop_piece(screen, board, n_r, n_c, 3 - turn, score1, score2)
#                     if check_points(board, n_r, n_c):
#                         winning_player = "RED" if turn == 1 else "YELLOW"
#                         if turn == 1:
#                             score1 += 1
#                         elif turn == 2:
#                             score2 += 1
#                     current_turn = turn  # Switch player back

#     threading.Thread(target=receive_thread, args=(client_socket,), daemon=True).start()

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN and current_turn == turn:
#                 mouseX = event.pos[0]
#                 col = mouseX // SQUARESIZE
#                 if is_valid(board, col):
#                     row = get_next_row(board, col)
#                     drop_piece(screen, board, row, col, turn, score1, score2)
#                     if check_points(board, row, col):
#                         winning_player = "RED" if turn == 1 else "YELLOW"
#                         if turn == 1:
#                             score1 += 1
#                         elif turn == 2:
#                             score2 += 1
#                     send_game_data(row,col, client_socket)
#                     current_turn = 3 - turn  # Switch player

#         screen.fill(BLACK)
#         draw_board(screen, board, score1, score2)
#         pygame.display.update()

#         if winning_player:
#             send_game_data(score1,score2, client_socket)
#             # score1_r, score2_r = receive_game_data(client_socket)
#             # if score1_r and score2_r:
#             #     score1 = max(score1, score1_r)
#             #     score2 = max(score2, score2_r)
#             winning_player = None



# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#     screen.fill(BLACK)
#     play_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
#     connect_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
#     draw_button(screen, play_button, BLUE, "Start Game")
#     draw_button(screen, connect_button, BLUE, "Connect")
#     font = pygame.font.Font(None, 36)
#     pygame.display.flip()
#     server_socket = None  # Initialize the server socket
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = pygame.mouse.get_pos()
#                 board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
#                 if play_button.collidepoint(mouse_pos):
#                     # Initialize the server socket
#                     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                     server_socket.bind((HOST, PORT))
#                     print("Server listining...")
#                     server_socket.listen(5)
#                     # Accept incoming connections
#                     client_socket, _ = server_socket.accept()
#                     play_game(screen, board, font, 1, client_socket,True,0,0)
                    
#                 elif connect_button.collidepoint(mouse_pos):
#                     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                     client_socket.connect((HOST, PORT))
#                     play_game(screen, board, font, 2, client_socket,False,0,0)

# if __name__ == '__main__':
#     main()
import pygame
import sys
import socket
import threading

# Constants
HOST = '127.0.0.1'
PORT = 5555
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
ROW_COUNT = 6
COLUMN_COUNT = 7
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
FONT_SIZE = 36
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

def draw_button(screen, rect, color, text):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_board(screen, board, score1, score2):
    font = pygame.font.Font(None, 36)
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
    text1 = f"Player 1 Score: {score1}"
    text_surface1 = font.render(text1, True, (255, 0, 0))
    text_x1 = (WINDOW_WIDTH - text_surface1.get_width()) // 2 - 150
    text_y1 = (WINDOW_HEIGHT - text_surface1.get_height()) // 2 - 300
    screen.blit(text_surface1, (text_x1, text_y1))

    text2 = f"Player 2 Score: {score2}"
    text_surface2 = font.render(text2, True, (255, 0, 0))
    text_x2 = (WINDOW_WIDTH - text_surface2.get_width()) // 2 + 150
    text_y2 = (WINDOW_HEIGHT - text_surface2.get_height()) // 2 - 300
    screen.blit(text_surface2, (text_x2, text_y2))

def drop_piece(screen, board, row, col, piece, score1, score2):
    if row is not None:
        falling_piece_y = 0
        final_y = (row + 1) * SQUARESIZE + SQUARESIZE // 2

        while falling_piece_y < final_y:
            screen.fill(BLACK)
            draw_board(screen, board, score1, score2)
            pygame.draw.circle(screen, RED if piece == 1 else YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, falling_piece_y), RADIUS, width=0)
            pygame.display.update()
            falling_piece_y += 50
            pygame.time.delay(50)

        board[row][col] = piece

def is_valid(board, col):
    return board[0][col] == 0

def get_next_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == 0:
            return r

def check_points(board, row, col):
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        count = 0
        r, c = row, col
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == board[row][col]:
            count += 1
            r, c = r + dr, c + dc
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == board[row][col]:
            count += 1
            r, c = r - dr, c - dc
        if count >= 4:
            return True
    return False

def send_game_data(data, client_socket):
    client_socket.sendall(data.encode())

def receive_game_data(client_socket):
    try:
        data = client_socket.recv(1024)
        if data:
            return tuple(map(int, data.decode().split(",")))
        else:
            return None
    except (OSError, ConnectionError) as e:
        print("Error:", e)
        return None

def play_game(screen, board, font, turn, client_socket, isserver, score1, score2):
    winning_player = None
    current_turn = turn

    def receive_thread(client_socket):
        nonlocal winning_player, current_turn, score1, score2
        while True:
            data = receive_game_data(client_socket)
            if data:
                if len(data) == 2:
                    n_r, n_c = data
                    if n_r is not None and n_c is not None:
                        drop_piece(screen, board, n_r, n_c, 3 - turn, score1, score2)
                        if check_points(board, n_r, n_c):
                            winning_player = "RED" if turn == 1 else "YELLOW"
                            if turn == 2:
                                score1 += 1
                            elif turn == 1:
                                score2 += 1
                        current_turn = turn  # Switch player back
                elif len(data) == 4:
                    _, _, new_score1, new_score2 = data
                    score1 = max(score1, new_score1)
                    score2 = max(score2, new_score2)

    threading.Thread(target=receive_thread, args=(client_socket,), daemon=True).start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and current_turn == turn:
                mouseX = event.pos[0]
                col = mouseX // SQUARESIZE
                if is_valid(board, col):
                    row = get_next_row(board, col)
                    drop_piece(screen, board, row, col, turn, score1, score2)
                    if check_points(board, row, col):
                        winning_player = "RED" if turn == 1 else "YELLOW"
                        if turn == 1:
                            score1 += 1
                        elif turn == 2:
                            score2 += 1
                    send_game_data(f"{row},{col}", client_socket)
                    current_turn = 3 - turn  # Switch player

        screen.fill(BLACK)
        draw_board(screen, board, score1, score2)
        pygame.display.update()

        if winning_player:
            send_game_data(f"{-1},-1,{score1},{score2}", client_socket)
            winning_player = None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(BLACK)
    play_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
    connect_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_button(screen, play_button, BLUE, "Start Game")
    draw_button(screen, connect_button, BLUE, "Connect")
    font = pygame.font.Font(None, 36)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                if play_button.collidepoint(mouse_pos):
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket.bind((HOST, PORT))
                    server_socket.listen(1)
                    print("Server listening...")
                    client_socket, _ = server_socket.accept()
                    play_game(screen, board, font, 1, client_socket, True, 0, 0)
                elif connect_button.collidepoint(mouse_pos):
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((HOST, PORT))
                    play_game(screen, board, font, 2, client_socket, False, 0, 0)

if __name__ == '__main__':
    main()
