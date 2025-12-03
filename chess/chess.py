import time
import pygame

#boardnya
board = ["bR","bH","bB", "bQ", "bK", "bB", "bH", "bR",
         ["bP"] *8,
         [None] *8,
         [None] *8,
         [None] *8,
         [None] *8,
         ["wP"] *8,
         "wR","wH","wB", "wQ", "wK", "wB", "wH", "wR",
         ]


pygame.init()
kotak = 80
disp = pygame.display.set_mode(kotak * 8, kotak*8)

pieces ={
    "bR" : pygame.image.load("assets/rook-b.svg"),
    "bH" : pygame.image.load("assets/knight-b.svg"),
    "bB" : pygame.image.load("assets/bishop-b.svg"),
    "bQ" : pygame.image.load("assets/queen-b.svg"),
    "bK" : pygame.image.load("assets/king-b.svg"),
    "bP" : pygame.image.load("assets/pawn-b.svg"),
    "wR" : pygame.image.load("assets/rook-w.svg"),
    "wH" : pygame.image.load("assets/knight-w.svg"),
    "wB" : pygame.image.load("assets/bishop-w.svg"),
    "wQ" : pygame.image.load("assets/queen-w.svg"),
    "wK" : pygame.image.load("assets/king-w.svg"),
    "wP" : pygame.image.load("assets/pawn-w.svg"),
}

    

pygame.quit()
