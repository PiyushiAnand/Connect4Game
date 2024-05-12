import pygame
import sys
from time import sleep
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
FONT_SIZE=36
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
def draw_board(screen, board):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS, width=0)

def drop_piece(screen, board, row, col, piece):
    if row is not None:
        falling_piece_y = 0
        final_y = (row + 1) * SQUARESIZE + SQUARESIZE // 2

        while falling_piece_y < final_y:
            screen.fill(BLACK)
            draw_board(screen, board)
            # Draw the falling piece
            pygame.draw.circle(screen, RED if piece == 1 else YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, falling_piece_y), RADIUS, width=0)
            pygame.display.update()
            falling_piece_y += 50  # Adjust the speed of falling here (larger value for faster)
            pygame.time.delay(50)

        board[row][col] = piece

def is_valid(board, col):
    return board[0][col] == 0

def get_next_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == 0:
            return r
def check_points(board, row, col):
    # Check for horizontal, vertical, and diagonal (down-right and down-left) matches
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

def send_game_data(row, col, client_socket):
    data = f"{row},{col}"
    client_socket.sendall(data.encode())

def receive_game_data(client_socket):
    try:
        data = client_socket.recv(1024)
        if data:
            row, col = map(int, data.decode().split(","))
            return row, col
        else:
            return None, None
    except (OSError, ConnectionError) as e:
        print("Error:", e)
        return None, None

def play_game(screen,board,font,turn,addr,isserver):
    winning_player=None
    first=False
    current = turn
    while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not isserver and not first:
                                n_r,n_c=receive_game_data(addr)
                                if n_c!=None:
                                    drop_piece(screen,board,n_r,n_c,3-turn)
                        mouseX = event.pos[0]
                        col = mouseX // SQUARESIZE
                        if is_valid(board, col):
                            row = get_next_row(board, col)
                            drop_piece(screen, board, row, col, turn)
                            
                            print(board)
                            if current == turn and check_points(board, row, col):
                                if board[row][col] == 1:
                                    winning_player = "RED"
                                elif board[row][col] == 2:
                                    winning_player = "YELLOW"
                                current = 3 - turn  # Switch player
                            send_game_data(row,col,addr)
                            n_r,n_c=receive_game_data(addr)
                            drop_piece(screen,board,n_r,n_c,3-turn)
                            first = True
                            break
                            
                if winning_player:
                    # Draw the background and board first
                    screen.fill(BLACK)
                    draw_board(screen, board)

                    # Render and blit the text
                    text = f"{winning_player} Wins"
                    text_surface = font.render(text, True, (0, 0, 0))
                    text_x = (WINDOW_WIDTH - text_surface.get_width()) // 2
                    text_y = (WINDOW_HEIGHT - text_surface.get_height()) // 2-150

                    # Blit the text onto the screen
                    screen.blit(text_surface, (text_x, text_y))
                    # Update the display
                    pygame.display.update()
                    # sleep(1)
                    # pygame.quit()
                    # sys.exit()

                else:
                    # Draw the board and update the display
                    screen.fill(BLACK)
                    draw_board(screen, board)
                    pygame.display.update()

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
    server_socket = None  # Initialize the server socket
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                if play_button.collidepoint(mouse_pos):
                    # Initialize the server socket
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket.bind((HOST, PORT))
                    print("Server listining...")
                    server_socket.listen(5)
                    # Accept incoming connections
                    client_socket, _ = server_socket.accept()
                    play_game(screen, board, font, 1, client_socket,True)
                    
                elif connect_button.collidepoint(mouse_pos):
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((HOST, PORT))
                    play_game(screen, board, font, 2, client_socket,False)

if __name__ == '__main__':
    main()
