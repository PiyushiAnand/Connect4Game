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
# def check_points(board,row,col):
#     if board[row][col]!=0:
#         if row<len(board)-3 and board[row][col]==board[row+1][col]==board[row+2][col]==board[row+3][col]:
#             return True
#         for i in range(-3, 1):
#             if col + i >= 0 and col + i + 3 < len(board[0]) and board[row][col+i] == board[row][col+i+1] == board[row][col+i+2] == board[row][col+i+3] == board[row][col]:
#                 return True
#         if row<len(board)-3 and col-3>=0 and board[row][col]==board[row+1][col-1]==board[row+2][col-2]==board[row+3][col-3]:
#          return True
#         if row<len(board)-3 and col-3>=0 and board[row][col]==board[row-1][col+1]==board[row-2][col+2]==board[row-3][col+3]:
#          return True
        # for offset in range(-3, 1):
        #     if (
        #         row + 3*offset >= 0 and
        #         row + offset + 3 < len(board) and
        #         col - 3*offset >= 0 and  row + 3*offset <len(board) and col - 3*offset<len(board[0]) and 
        #         col - offset - 3 < len(board[0]) and
        #         board[row][col] == board[row + 1 * offset][col - 1 * offset] == board[row + 2 * offset][col - 2 * offset] == board[row + 3 * offset][col - 3 * offset]
        #     ):
        #         return True

    # return False
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

def play_game(screen,board,font):
    turn = 1
    winning_player=None
    while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = event.pos[0]
                        col = mouseX // SQUARESIZE
                        if is_valid(board, col):
                            row = get_next_row(board, col)
                            drop_piece(screen, board, row, col, turn)
                            turn = 3 - turn  # Switch player
                            print(board)
                            if check_points(board, row, col):
                                if board[row][col] == 1:
                                    winning_player = "RED"
                                elif board[row][col] == 2:
                                    winning_player = "YELLOW"

                            
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
# def handle_client(conn, addr):
#     print(f"New connection from {addr}")

#     while True:
#         data = conn.recv(1024)  # Receive data from client
#         if not data:
#             print(f"Client {addr} disconnected")
#             break
#         # Broadcast the received data to all clients
#         for client_socket in clients:
#             if client_socket != conn:
#                 client_socket.sendall(data)
#     conn.close()
# def send_game_data():
    
#     pass
# def receive_game_data():
#     pass
# def connect_it(serve):
#     if serve:
#         clients =[]
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind((HOST, PORT))
#         server_socket.listen()
#         print("Server is listening...")
#         conn, addr = server_socket.accept()
#         clients.append(conn)
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()
#     else:



def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(BLACK)
    play_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
    connect_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_button(screen, play_button, BLUE, "Start Game")
    #draw_button(screen, connect_button, BLUE, "Connect")
    font = pygame.font.Font(None, 36)
    pygame.display.flip()
    serve_addre=None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                    play_game(screen,board,font)
                    
                # elif connect_button.collidepoint(mouse_pos):
                #     serve_address = input("Enter server address: ")
                #     print("Server address:", serve_address)

if __name__ == '__main__':
    main()
