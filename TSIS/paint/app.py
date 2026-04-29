import pygame, sys
from config import *
from draw_utils import *
from ui import Palette, Button


class PaintApp:
    def __init__(self):
        # окно и холст
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Paint")
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(CANVAS_C)

        # состояния рисования
        self.tool = "freehand"
        self.color = (0, 0, 0)
        self.brush_size = 4
        self.fill_shapes = False
        self.drawing = False
        self.start_pos = None
        self.last_pos = None
        self.prev_canvas = None

        # текстовый инструмент
        self.typing = False
        self.text_input = ""
        self.text_pos = None
        self.font_size = 26
        self.text_font = pygame.font.SysFont("Arial", self.font_size)

        # шрифты UI
        self.font_ui = pygame.font.SysFont("Segoe UI", 14)
        self.font_bold = pygame.font.SysFont("Segoe UI", 14, bold=True)
        self.font_title = pygame.font.SysFont("Segoe UI", 17, bold=True)

        self.palette = Palette(PALETTE)
        self._setup_ui()

    # ---------- интерфейс ----------
    def _setup_ui(self):
        self.tool_rects = {t: pygame.Rect(8, 46 + i * 36, TOOLBAR_W - 16, 30)
                           for i, t in enumerate(TOOLS)}
        self.pal_top = 46 + len(TOOLS) * 36 + 20
        self.btn_save = Button(pygame.Rect(8, WIN_H - 46, TOOLBAR_W - 16, 32),
                               "Save  Ctrl+S", self.font_bold)

    def _draw_toolbar(self):
        pygame.draw.rect(self.screen, TOOLBAR, (0, 0, TOOLBAR_W, WIN_H))
        pygame.draw.line(self.screen, BORDER, (TOOLBAR_W - 1, 0),
                         (TOOLBAR_W - 1, WIN_H), 2)
        t = self.font_title.render("Paint", True, ACCENT)
        self.screen.blit(t, (8, 10))

        mx, my = pygame.mouse.get_pos()
        for name, rect in self.tool_rects.items():
            active = (name == self.tool)
            hovered = rect.collidepoint(mx, my) and not active
            bg = ACCENT if active else ((55, 55, 80) if hovered else (38, 38, 54))
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            lbl = (self.font_bold if active else self.font_ui).render(
                TOOL_LABELS[name], True, WHITE if active else MUTED)
            self.screen.blit(lbl, (rect.x+6, rect.centery - lbl.get_height()//2))

        # палитра
        self.screen.blit(self.font_ui.render("Colours", True, MUTED),
                         (8, self.pal_top - 16))
        self.palette.draw(self.screen, self.color, self.pal_top)

        # размер кисти и кнопка Save
        dot_y = self.pal_top + 36
        pygame.draw.rect(self.screen, self.color,
                         pygame.Rect(8, dot_y, 22, 16), border_radius=3)
        info = self.font_ui.render(f"size: {self.brush_size}", True, MUTED)
        self.screen.blit(info, (36, dot_y))
        self.btn_save.draw(self.screen, ACCENT)

    # ---------- фигуры ----------
    def _render_shape(self, surf, tool, sx, sy, ex, ey, col, size, fill):
        if tool == "line":
            pygame.draw.line(surf, col, (sx, sy), (ex, ey), size)
        elif tool == "rectangle":
            x, y, w, h = min(sx, ex), min(sy, ey), abs(ex - sx), abs(ey - sy)
            pygame.draw.rect(surf, col, (x, y, w, h), 0 if fill else size)
        elif tool == "square":
            side = min(abs(ex - sx), abs(ey - sy))
            x = sx if ex >= sx else sx - side
            y = sy if ey >= sy else sy - side
            pygame.draw.rect(surf, col, (x, y, side, side), 0 if fill else size)
        elif tool == "circle":
            cx, cy = (sx + ex)//2, (sy + ey)//2
            rx, ry = abs(ex - sx)//2, abs(ey - sy)//2
            rect = pygame.Rect(cx - rx, cy - ry, rx*2, ry*2)
            pygame.draw.ellipse(surf, col, rect, 0 if fill else size)
        elif tool == "right_triangle":
            draw_right_triangle(surf, col, (sx, sy), (ex, ey), size, fill)
        elif tool == "eq_triangle":
            draw_eq_triangle(surf, col, (sx, sy), (ex, ey), size, fill)
        elif tool == "rhombus":
            draw_rhombus(surf, col, (sx, sy), (ex, ey), size, fill)

    # ---------- ввод текста ----------
    def _commit_text(self):
        if self.text_input and self.text_pos:
            rendered = self.text_font.render(self.text_input, True, self.color)
            self.canvas.blit(rendered, self.text_pos)
        self.typing = False
        self.text_input = ""
        self.text_pos = None

    def _draw_text_overlay(self):
        if not self.typing or not self.text_pos:
            return
        rendered = self.text_font.render(self.text_input, True, self.color)
        cx = self.text_pos[0] + rendered.get_width() + 1
        cy = self.text_pos[1]
        self.screen.blit(rendered, (CANVAS_X + self.text_pos[0], self.text_pos[1]))
        # мигающий курсор
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.line(self.screen, self.color,
                             (CANVAS_X + cx, cy),
                             (CANVAS_X + cx, cy + self.font_size), 2)

    # ---------- обработка событий ----------
    def _handle_event(self, e):
        mx, my = pygame.mouse.get_pos()
        cx, cy = mx - CANVAS_X, my

        # клавиатура при вводе текста
        if self.typing:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self._commit_text()
                elif e.key == pygame.K_ESCAPE:
                    self.typing = False
                    self.text_input = ""
                elif e.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                else:
                    self.text_input += e.unicode
            return

        # обычная клавиатура
        if e.type == pygame.KEYDOWN:
            ctrl = bool(pygame.key.get_mods() & pygame.KMOD_CTRL)
            if ctrl and e.key == pygame.K_s:
                save_file(self.canvas)
                return
            elif e.key in KEY_TO_TOOL:
                self.tool = KEY_TO_TOOL[e.key]
                return
            elif e.key in (pygame.K_PLUS, pygame.K_EQUALS):
                self.brush_size = min(50, self.brush_size + 2)
            elif e.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.brush_size = max(1, self.brush_size - 2)

        # мышь нажата
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            # кнопки
            for name, r in self.tool_rects.items():
                if r.collidepoint(mx, my):
                    self.tool = name
                    return
            for i, r in enumerate(self.palette.rects):
                if r.collidepoint(mx, my):
                    self.color = self.palette.colors[i]
                    return
            if self.btn_save.rect.collidepoint(mx, my):
                save_file(self.canvas)
                return

            # клик по холсту
            if mx >= CANVAS_X:
                if self.tool == "fill":
                    flood_fill(self.canvas, cx, cy, self.color)
                elif self.tool == "text":
                    self.typing = True
                    self.text_input = ""
                    self.text_pos = (cx, cy)
                elif self.tool in ("freehand", "eraser"):
                    self.drawing = True
                    self.last_pos = (cx, cy)
                else:
                    self.drawing = True
                    self.start_pos = (cx, cy)
                    self.prev_canvas = self.canvas.copy()

        # движение мыши
        if e.type == pygame.MOUSEMOTION and e.buttons[0]:
            if not self.drawing or mx < CANVAS_X:
                return
            if self.tool == "freehand":
                pygame.draw.line(self.canvas, self.color, self.last_pos, (cx, cy), self.brush_size)
                self.last_pos = (cx, cy)
            elif self.tool == "eraser":
                pygame.draw.circle(self.canvas, CANVAS_C, (cx, cy), self.brush_size)
                self.last_pos = (cx, cy)

        # отпускание кнопки мыши
        if e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.drawing:
            if self.tool not in ("freehand", "eraser", "fill", "text"):
                if self.prev_canvas:
                    self.canvas.blit(self.prev_canvas, (0, 0))
                self._render_shape(self.canvas, self.tool,
                                   *self.start_pos, cx, cy,
                                   self.color, self.brush_size, self.fill_shapes)
            self.drawing = False
            self.prev_canvas = None

    # ---------- главный цикл ----------
    def run(self):
        clock = pygame.time.Clock()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                self._handle_event(e)

            self.screen.fill(BG)
            self.screen.blit(self.canvas, (CANVAS_X, 0))
            pygame.draw.rect(self.screen, BORDER,
                             (CANVAS_X - 1, -1, CANVAS_W + 2, CANVAS_H + 2), 1)
            self._draw_toolbar()
            # текст поверх холста
            self._draw_text_overlay()
            pygame.display.flip()
            clock.tick(120)
