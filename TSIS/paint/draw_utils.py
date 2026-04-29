import pygame, math, tkinter as tk
from tkinter import filedialog

# Базовые фигуры
def draw_eq_triangle(surf, col, p1, p2, size, fill=False):
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    length = math.hypot(dx,dy) or 1
    bx, by = p2[0]-dx/2, p2[1]-dy/2
    perp_x, perp_y = -dy/length*(math.sqrt(3)/2*length), dx/length*(math.sqrt(3)/2*length)
    pts = [p1, (int(bx+perp_x/2), int(by+perp_y/2)), (int(bx-perp_x/2), int(by-perp_y/2))]
    pygame.draw.polygon(surf, col, pts, 0 if fill else max(1,size))

def draw_right_triangle(surf, col, p1, p2, size, fill=False):
    pts = [p1, (p1[0], p2[1]), p2]
    pygame.draw.polygon(surf, col, pts, 0 if fill else max(1,size))

def draw_rhombus(surf, col, p1, p2, size, fill=False):
    cx, cy = (p1[0]+p2[0])//2, (p1[1]+p2[1])//2
    w2, h2 = abs(p2[0]-p1[0])//2, abs(p2[1]-p1[1])//2
    pts = [(cx,cy-h2),(cx+w2,cy),(cx,cy+h2),(cx-w2,cy)]
    pygame.draw.polygon(surf, col, pts, 0 if fill else max(1,size))

# Простейшая реализация заливки
def flood_fill(surface, x, y, new_col):
    old_col = surface.get_at((x,y))[:3]
    if old_col == new_col: return
    w,h = surface.get_size()
    stack, visited = [(x,y)], set()
    surface.lock()
    while stack:
        cx,cy = stack.pop()
        if (cx,cy) in visited or not (0<=cx<w and 0<=cy<h): continue
        if surface.get_at((cx,cy))[:3] != old_col: continue
        surface.set_at((cx,cy), new_col)
        visited.add((cx,cy))
        stack += [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]
    surface.unlock()

# Сохранение изображения
def save_file(canvas):
    root = tk.Tk(); root.withdraw()
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG","*.png"),("JPEG","*.jpg"),("BMP","*.bmp")],
        title="Сохранить изображение")
    root.destroy()
    if path: pygame.image.save(canvas, path)
