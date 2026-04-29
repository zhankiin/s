import pygame

pygame.init()

# Размеры окна и холста
TOOLBAR_W = 180
CANVAS_W, CANVAS_H = 1100, 800
WIN_W, WIN_H = TOOLBAR_W + CANVAS_W, CANVAS_H
CANVAS_X = TOOLBAR_W

# Цвета интерфейса
BG, TOOLBAR, BORDER = (30,30,40), (22,22,32), (55,55,75)
ACCENT, WHITE, MUTED = (99,102,241), (255,255,255), (110,110,135)
CANVAS_C = (255,255,255)

# Палитра
PALETTE = [
    (255,0,0), (255,127,0), (255,255,0),
    (0,200,0), (0,0,255), (75,0,130), (148,0,211)
]

# Инструменты и горячие клавиши
TOOLS = ["freehand","line","rectangle","square","circle",
         "right_triangle","eq_triangle","rhombus","fill","text","eraser"]

TOOL_LABELS = {
    "freehand":"[H] Freehand","line":"[L] Line","rectangle":"[G] Rectangle",
    "square":"[S] Square","circle":"[C] Circle","right_triangle":"[R] Rt Triangle",
    "eq_triangle":"[T] Eq Triangle","rhombus":"[P] Rhombus","fill":"[F] Fill",
    "text":"[A] Text","eraser":"[E] Eraser"
}

KEY_TO_TOOL = {
    pygame.K_h:"freehand", pygame.K_l:"line", pygame.K_g:"rectangle",
    pygame.K_s:"square", pygame.K_c:"circle", pygame.K_r:"right_triangle",
    pygame.K_t:"eq_triangle", pygame.K_p:"rhombus", pygame.K_f:"fill",
    pygame.K_a:"text", pygame.K_e:"eraser"
}
