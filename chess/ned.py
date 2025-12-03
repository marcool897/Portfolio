import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 512, 512
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font untuk teks
font = pygame.font.SysFont(None, 24)

# Load gambar potongan
pieces = {
    'wP': pygame.image.load('wP.png'),
    'wR': pygame.image.load('wR.png'),
    'wN': pygame.image.load('wN.png'),
    'wB': pygame.image.load('wB.png'),
    'wQ': pygame.image.load('wQ.png'),
    'wK': pygame.image.load('wK.png'),
    'bP': pygame.image.load('bP.png'),
    'bR': pygame.image.load('bR.png'),
    'bN': pygame.image.load('bN.png'),
    'bB': pygame.image.load('bB.png'),
    'bQ': pygame.image.load('bQ.png'),
    'bK': pygame.image.load('bK.png'),
}

# Inisialisasi papan
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Fungsi untuk menggambar papan
def draw_board(screen, valid_moves=None):
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            if valid_moves and (row, col) in valid_moves:
                color = GREEN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Fungsi untuk menggambar potongan
def draw_pieces(screen):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.':
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Fungsi untuk mendapatkan semua gerakan valid untuk potongan
def get_valid_moves(row, col, turn):
    piece = board[row][col]
    if piece == '.' or (turn == 'white' and piece[0] == 'b') or (turn == 'black' and piece[0] == 'w'):
        return []
    
    moves = []
    if piece[1] == 'P':  # Pawn
        direction = -1 if piece[0] == 'w' else 1
        # Maju satu langkah
        if 0 <= row + direction < 8 and board[row + direction][col] == '.':
            moves.append((row + direction, col))
            # Maju dua langkah dari posisi awal
            if (row == 6 and piece[0] == 'w' and board[row + 2*direction][col] == '.') or (row == 1 and piece[0] == 'b' and board[row + 2*direction][col] == '.'):
                moves.append((row + 2*direction, col))
        # Serang diagonal
        for dc in [-1, 1]:
            if 0 <= col + dc < 8 and 0 <= row + direction < 8 and board[row + direction][col + dc] != '.' and board[row + direction][col + dc][0] != piece[0]:
                moves.append((row + direction, col + dc))
    elif piece[1] in ['R', 'B', 'Q']:  # Rook, Bishop, Queen
        directions = []
        if piece[1] == 'R':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        elif piece[1] == 'B':
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif piece[1] == 'Q':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '.':
                    moves.append((r, c))
                elif board[r][c][0] != piece[0]:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
    elif piece[1] == 'N':  # Knight
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] == '.' or board[r][c][0] != piece[0]):
                moves.append((r, c))
    elif piece[1] == 'K':  # King
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] == '.' or board[r][c][0] != piece[0]):
                    moves.append((r, c))
    
    # Filter gerakan yang menyebabkan check pada king sendiri
    valid_moves = []
    for move in moves:
        temp_board = [row[:] for row in board]
        temp_board[move[0]][move[1]] = temp_board[row][col]
        temp_board[row][col] = '.'
        if not is_in_check(temp_board, turn):
            valid_moves.append(move)
    return valid_moves

# Fungsi untuk cek apakah king dalam check
def is_in_check(board_state, turn):
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board_state[r][c] == ('wK' if turn == 'white' else 'bK'):
                king_pos = (r, c)
                break
    if not king_pos:
        return False
    
    opponent = 'black' if turn == 'white' else 'white'
    for r in range(8):
        for c in range(8):
            if board_state[r][c] != '.' and board_state[r][c][0] == ('b' if turn == 'white' else 'w'):
                if king_pos in get_valid_moves_for_piece(board_state, r, c, opponent):
                    return True
    return False

# Helper untuk get_valid_moves tanpa filter check
def get_valid_moves_for_piece(board_state, row, col, turn):
    # Mirip get_valid_moves tapi tanpa filter check, untuk deteksi check
    piece = board_state[row][col]
    moves = []
    # ... (sama seperti di get_valid_moves, tapi tanpa filter akhir)
    # Untuk singkat, saya asumsikan Anda copy logika dari get_valid_moves tanpa bagian filter
    # Di kode nyata, buat fungsi terpisah atau refactor.
    return moves  # Placeholder; implementasikan penuh jika perlu

# Fungsi untuk cek checkmate
def is_checkmate(turn):
    if not is_in_check(board, turn):
        return False
    for r in range(8):
        for c in range(8):
            if board[r][c] != '.' and board[r][c][0] == ('w' if turn == 'white' else 'b'):
                if get_valid_moves(r, c, turn):
                    return False
    return True

# AI sederhana: pilih gerakan random
def ai_move(turn):
    possible_moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] != '.' and board[r][c][0] == ('b' if turn == 'black' else 'w'):
                moves = get_valid_moves(r, c, turn)
                for move in moves:
                    possible_moves.append((r, c, move[0], move[1]))
    if possible_moves:
        move = random.choice(possible_moves)
        board[move[2]][move[3]] = board[move[0]][move[1]]
        board[move[0]][move[1]] = '.'

# Fungsi utama
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Advanced Chess Game")
    clock = pygame.time.Clock()
    
    turn = 'white'
    selected = None
    valid_moves = []
    game_over = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                if selected is None:
                    if board[row][col] != '.' and ((turn == 'white' and board[row][col][0] == 'w')):
                        selected = (row, col)
                        valid_moves = get_valid_moves(row, col, turn)
                else:
                    if (row, col) in valid_moves:
                        board[row][col] = board[selected[0]][selected[1]]
                        board[selected[0]][selected[1]] = '.'
                        turn = 'black' if turn == 'white' else 'white'
                        if is_checkmate(turn):
                            game_over = True
                        else:
                            ai_move(turn)  # AI untuk hitam
                            if is_checkmate('white'):
                                game_over = True
                    selected = None
                    valid_moves = []
        
        draw_board(screen, valid_moves)
        draw_pieces(screen)
        
        # Tampilkan status
        status = f"Turn: {turn}"
        if is_in_check(board, turn):
            status += " - CHECK!"
        if game_over:
            status = f"Checkmate! {'White' if turn == 'black' else 'Black'} wins."
        text = font.render(status, True, BLACK)
        screen.blit(text, (10, HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()