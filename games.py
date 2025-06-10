import tkinter as tk
from tkinter import messagebox
import pygame
from pygame.locals import *


class GameMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Игровое меню")
        self.root.geometry("300x300")
        self.root.resizable(False, False)

        self.setup_ui()

        # Привязка Escape
        self.root.bind("<Escape>", self.show_menu)

    def setup_ui(self):
        self.root.config(bg="white")
        title = tk.Label(
            self.root,
            text="Выберите игру",
            font=('Arial', 16),
            bg="white",
            fg="black"
        )
        title.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=10)

        order_chaos_btn = tk.Button(
            btn_frame,
            text="Порядок vs Хаос",
            command=self.start_order_vs_chaos,
            width=20,
            bg="lightgray",
            fg="black"
        )
        order_chaos_btn.pack(pady=5)

        tic_tac_toe_btn = tk.Button(
            btn_frame,
            text="Вложенные крестики-нолики",
            command=self.start_ultimate_tic_tac_toe,
            width=20,
            bg="lightgray",
            fg="black"
        )
        tic_tac_toe_btn.pack(pady=5)

        magic15_btn = tk.Button(
            btn_frame,
            text="Magic 15",
            command=self.start_magic15,
            width=20,
            bg="lightgray",
            fg="black"
        )
        magic15_btn.pack(pady=5)

        connect_dots_btn = tk.Button(
            btn_frame,
            text="Соединение точек 4x4",
            command=self.start_connect_dots,
            width=20,
            bg="lightgray",
            fg="black"
        )
        connect_dots_btn.pack(pady=5)

    def show_menu(self, event=None):
        menu = tk.Menu(self.root, tearoff=0, bg="lightgray", fg="black")
        menu.add_command(label="Порядок vs Хаос", command=self.start_order_vs_chaos)
        menu.add_command(label="Вложенные крестики-нолики", command=self.start_ultimate_tic_tac_toe)
        menu.add_command(label="Magic 15", command=self.start_magic15)
        menu.add_separator()
        menu.add_command(label="Выход", command=self.root.quit)
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def start_order_vs_chaos(self):
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        game = OrderVsChaos(game_window)
        game_window.protocol("WM_DELETE_WINDOW", lambda: self.on_game_close(game_window))

    def start_ultimate_tic_tac_toe(self):
        self.root.withdraw()
        pygame.init()
        UltimateTicTacToe().run()
        self.root.deiconify()

    def start_magic15(self):
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        game = Magic15Game(game_window)
        game_window.protocol("WM_DELETE_WINDOW", lambda: self.on_game_close(game_window))

    def start_connect_dots(self):
        self.root.withdraw()
        ConnectDotsGame(self.root)
        # Игра сама управляет своим закрытием и возвратом к меню

    def on_game_close(self, window):
        window.destroy()
        self.root.deiconify()


# --- Новая игра "Соединение точек 4x4" ---
class ConnectDotsGame:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel()
        self.window.title("Соединение точек 4x4 (2 игрока)")
        self.window.geometry("500x600")
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.canvas_size = 500
        self.margin = 50
        self.grid_size = 4
        self.point_radius = 8
        self.points = []  # координаты точек
        self.lines = []  # линии как пары индексов точек
        self.selected_point = None
        self.lines_set = set()  # для быстрого поиска пересечений
        self.current_player = 1  # 1 или 2
        self.player_colors = {1: "blue", 2: "red"}  # цвета для каждого игрока

        self.create_widgets()
        self.setup_points()  # создаем координаты точек
        self.draw_points()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.window, width=self.canvas_size, height=self.canvas_size + 50, bg='white')
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        # Фрейм для информации о игроках
        self.info_frame = tk.Frame(self.window, bg="white")
        self.info_frame.pack(pady=5)

        self.player1_label = tk.Label(
            self.info_frame,
            text="Игрок 1 (Синий): Ход",
            font=("Arial", 12),
            fg=self.player_colors[1],
            bg="white"
        )
        self.player1_label.pack(side=tk.LEFT, padx=10)

        self.player2_label = tk.Label(
            self.info_frame,
            text="Игрок 2 (Красный): Ожидание",
            font=("Arial", 12),
            fg=self.player_colors[2],
            bg="white"
        )
        self.player2_label.pack(side=tk.LEFT, padx=10)

        self.reset_btn = tk.Button(self.window, text="Новая игра", command=self.reset_game)
        self.reset_btn.pack(pady=5)

        self.status_label = tk.Label(
            self.window,
            text="Игрок 1, выбирайте первую точку",
            font=("Arial", 12),
            bg="white"
        )
        self.status_label.pack()

    def setup_points(self):
        # Расставляем точки по сетке 4x4
        spacing = (self.canvas_size - 2 * self.margin) // (self.grid_size - 1)
        self.points_coords = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                x = self.margin + j * spacing
                y = self.margin + i * spacing
                row.append((x, y))
            self.points_coords.append(row)

    def draw_points(self):
        self.canvas.delete("all")
        self.points = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x, y = self.points_coords[i][j]
                self.points.append((x, y))
                self.canvas.create_oval(
                    x - self.point_radius, y - self.point_radius,
                    x + self.point_radius, y + self.point_radius,
                    fill='black'
                )
        # рисуем линии
        for line in self.lines:
            p1 = self.points[line[0]]
            p2 = self.points[line[1]]
            player = line[2]  # получаем номер игрока из данных линии
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1],
                                    fill=self.player_colors[player],
                                    width=2)

    def on_click(self, event):
        # Определяем, какую точку кликнули
        clicked_point = None
        for idx, (x, y) in enumerate(self.points):
            dx = event.x - x
            dy = event.y - y
            if dx * dx + dy * dy <= self.point_radius * self.point_radius + 4:
                clicked_point = idx
                break
        if clicked_point is None:
            return

        if self.selected_point is None:
            # Выбираем первую точку
            self.selected_point = clicked_point
            self.status_label.config(text=f"Игрок {self.current_player}, выберите вторую точку")
        else:
            # Вторая точка
            if clicked_point == self.selected_point:
                # Нельзя соединять точку саму с собой
                return
            # Проверка, что линий между этими точками еще нет
            if (self.selected_point, clicked_point) in self.lines or (clicked_point, self.selected_point) in self.lines:
                return
            # Проверка, что новая линия не пересекается с существующими
            new_line = (self.selected_point, clicked_point)
            if self.line_intersects_existing(new_line):
                messagebox.showwarning("Недопустимый ход", "Линия пересекается с существующими линиями.")
                self.selected_point = None
                self.status_label.config(text=f"Игрок {self.current_player}, выберите первую точку")
                return
            # Добавляем линию с информацией о текущем игроке
            self.lines.append((self.selected_point, clicked_point, self.current_player))
            self.lines_set.add(tuple(sorted((self.selected_point, clicked_point))))
            last_player = self.current_player  # запомнить кто сделал ход
            self.selected_point = None
            self.draw_points()

            # Проверка, есть ли место для удлинения
            if not self.can_extend():
                # Игра завершена, определяем победителя
                winner = f"Игрок {last_player}"
                messagebox.showinfo("Конец игры", f"{winner} выиграл! Больше ходов сделать нельзя.")
                self.status_label.config(text=f"{winner} победил!")
                return

            # Переход хода
            self.current_player = 2 if self.current_player == 1 else 1
            self.update_player_turn()
            self.status_label.config(text=f"Игрок {self.current_player}, выберите первую точку")

    def update_player_turn(self):
        if self.current_player == 1:
            self.player1_label.config(text="Игрок 1 (Синий): Ход")
            self.player2_label.config(text="Игрок 2 (Красный): Ожидание")
        else:
            self.player1_label.config(text="Игрок 1 (Синий): Ожидание")
            self.player2_label.config(text="Игрок 2 (Красный): Ход")

    def line_intersects_existing(self, new_line):
        # Проверяет, пересекается ли новая линия с существующими
        p1_idx, p2_idx = new_line
        p1 = self.points[p1_idx]
        p2 = self.points[p2_idx]
        for line in self.lines:
            # Не проверяем пересечение с линиями, которые делят ту же пару точек
            if set(line[:2]) == set(new_line):
                continue
            q1_idx, q2_idx = line[:2]
            q1 = self.points[q1_idx]
            q2 = self.points[q2_idx]
            if self.check_lines_intersect(p1, p2, q1, q2):
                return True
        return False

    def check_lines_intersect(self, p1, p2, q1, q2):
        # Проверка пересечения двух линий
        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

        return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))

    def can_extend(self):
        # Проверяет, есть ли еще возможные удлинения
        # Возможность удлинения — есть две точки, не соединённые линией, и при этом линия между ними не пересекается с существующими
        n = len(self.points)
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in self.lines_set or (j, i) in self.lines_set:
                    continue
                if not self.line_intersects_existing((i, j)):
                    return True
        return False

    def reset_game(self):
        self.lines = []
        self.lines_set = set()
        self.selected_point = None
        self.current_player = 1
        self.update_player_turn()
        self.draw_points()
        self.status_label.config(text="Игрок 1, выбирайте первую точку")

    def close_window(self):
        self.window.destroy()
        self.parent.deiconify()

    def start_order_vs_chaos(self):
        """Запускает игру Порядок vs Хаос"""
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        game = OrderVsChaos(game_window)
        game_window.protocol("WM_DELETE_WINDOW", lambda: self.on_game_close(game_window))

    def start_ultimate_tic_tac_toe(self):
        """Запускает игру Вложенные крестики-нолики"""
        self.root.withdraw()
        pygame.init()
        UltimateTicTacToe().run()
        self.root.deiconify()

    def start_magic15(self):
        """Запускает игру Magic 15"""
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        game = Magic15Game(game_window)
        game_window.protocol("WM_DELETE_WINDOW", lambda: self.on_game_close(game_window))

    def on_game_close(self, window):
        """Обработчик закрытия окна игры"""
        window.destroy()
        self.root.deiconify()


class Magic15Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Magic 15 Game")

        # Игровые данные
        self.player1_numbers = []
        self.player2_numbers = []
        self.used_numbers = set()
        self.current_player = 1

        # Выигрышные комбинации (сумма = 15)
        self.winning_combinations = [
            {1, 5, 9}, {1, 6, 8}, {2, 4, 9}, {2, 5, 8},
            {2, 6, 7}, {3, 4, 8}, {3, 5, 7}, {4, 5, 6}
        ]

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для кнопок с цифрами
        self.numbers_frame = tk.Frame(self.root)
        self.numbers_frame.pack(pady=10)

        # Кнопки цифр от 1 до 9
        self.number_buttons = []
        for i in range(1, 10):
            btn = tk.Button(
                self.numbers_frame,
                text=str(i),
                width=5,
                height=2,
                command=lambda num=i: self.select_number(num),
                state=tk.NORMAL,
                font=("Arial", 12)
            )
            btn.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)
            self.number_buttons.append(btn)

        # Информация о текущем игроке
        self.status_label = tk.Label(
            self.root,
            text=f"Ход игрока {self.current_player}",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=10)

        # Поле для отображения выбранных чисел
        self.player1_label = tk.Label(
            self.root,
            text="Игрок 1: []",
            font=("Arial", 12)
        )
        self.player1_label.pack()

        self.player2_label = tk.Label(
            self.root,
            text="Игрок 2: []",
            font=("Arial", 12)
        )
        self.player2_label.pack()

        # Кнопка новой игры
        self.new_game_btn = tk.Button(
            self.root,
            text="Новая игра",
            command=self.reset_game,
            font=("Arial", 12)
        )
        self.new_game_btn.pack(pady=10)

    def select_number(self, number):
        if number in self.used_numbers:
            messagebox.showwarning("Ошибка", "Это число уже выбрано!")
            return

        # Добавляем число текущему игроку
        if self.current_player == 1:
            self.player1_numbers.append(number)
            self.player1_label.config(text=f"Игрок 1: {self.player1_numbers}")
        else:
            self.player2_numbers.append(number)
            self.player2_label.config(text=f"Игрок 2: {self.player2_numbers}")

        # Помечаем число как использованное
        self.used_numbers.add(number)
        self.number_buttons[number - 1].config(state=tk.DISABLED, relief=tk.SUNKEN)

        # Проверка на победу
        if self.check_win():
            messagebox.showinfo("Победа!", f"Игрок {self.current_player} победил!")
            self.reset_game()
            return

        # Проверка на ничью
        if len(self.used_numbers) == 9:
            messagebox.showinfo("Ничья", "Все числа использованы, но никто не победил!")
            self.reset_game()
            return

        # Переход хода
        self.current_player = 2 if self.current_player == 1 else 1
        self.status_label.config(text=f"Ход игрока {self.current_player}")

    def check_win(self):
        current_numbers = self.player1_numbers if self.current_player == 1 else self.player2_numbers
        if len(current_numbers) < 3:
            return False

        for comb in self.winning_combinations:
            if comb.issubset(set(current_numbers)):
                return True
        return False

    def reset_game(self):
        # Сброс всех данных игры
        self.player1_numbers = []
        self.player2_numbers = []
        self.used_numbers = set()
        self.current_player = 1

        # Обновление интерфейса
        for btn in self.number_buttons:
            btn.config(state=tk.NORMAL, relief=tk.RAISED)
        self.player1_label.config(text="Игрок 1: []")
        self.player2_label.config(text="Игрок 2: []")
        self.status_label.config(text=f"Ход игрока {self.current_player}")


class OrderVsChaos:
    def __init__(self, root):
        self.root = root
        self.root.title("Порядок vs Хаос 6x6")

        # Настройки игры
        self.board_size = 6
        self.win_length = 5
        self.current_player = "Order"  # Order или Chaos
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        # Фиксированный размер кнопок
        self.cell_size = 50

        self.create_widgets()
        self.set_window_size()

    def set_window_size(self):
        """Устанавливаем размер окна для квадратного поля"""
        total_size = self.board_size * self.cell_size
        self.root.geometry(f"{total_size}x{total_size + 50}")
        self.root.resizable(False, False)

    def create_widgets(self):
        # Создаем игровое поле
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j] = tk.Button(
                    self.root,
                    text="",
                    font=('Arial', 16),
                    width=3,
                    height=1,
                    bg="white",
                    fg="black",
                    borderwidth=1,
                    highlightthickness=0,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j, padx=0, pady=0, sticky="nsew")

            self.root.grid_rowconfigure(i, weight=1, minsize=self.cell_size)
            self.root.grid_columnconfigure(i, weight=1, minsize=self.cell_size)

        # Панель управления
        self.control_frame = tk.Frame(self.root, bg="white")
        self.control_frame.grid(row=self.board_size, column=0, columnspan=self.board_size, pady=5, sticky="nsew")

        # Кнопки выбора символа
        self.symbol_var = tk.StringVar(value="X")

        tk.Label(
            self.control_frame,
            text="Выберите символ:",
            bg="white",
            fg="black"
        ).pack(side=tk.LEFT, padx=5)

        tk.Radiobutton(
            self.control_frame,
            text="X",
            variable=self.symbol_var,
            value="X",
            fg="red",
            bg="white",
            selectcolor="lightgray"
        ).pack(side=tk.LEFT)

        tk.Radiobutton(
            self.control_frame,
            text="O",
            variable=self.symbol_var,
            value="O",
            fg="blue",
            bg="white",
            selectcolor="lightgray"
        ).pack(side=tk.LEFT)

        # Статус игры
        self.status_label = tk.Label(
            self.control_frame,
            text=f"Ход: {self.current_player}",
            font=('Arial', 12),
            bg="white",
            fg="hotpink" if self.current_player == "Order" else "limegreen"
        )
        self.status_label.pack(side=tk.LEFT, padx=20)

        # Кнопка сброса
        self.new_game_btn = tk.Button(
            self.control_frame,
            text="Новая игра",
            command=self.reset_game,
            bg="lightgray",
            fg="black"
        )
        self.new_game_btn.pack(side=tk.RIGHT)

    def on_click(self, row, col):
        if self.board[row][col] == "":
            symbol = self.symbol_var.get()
            player = self.current_player

            self.board[row][col] = symbol
            self.buttons[row][col].config(
                text=symbol,
                fg="red" if symbol == "X" else "blue",
                bg="#FFD1DC" if player == "Order" else "#D1FFD1",
                state=tk.DISABLED
            )

            # Проверяем победу Порядка
            if player == "Order" and self.check_any_win(row, col):
                messagebox.showinfo("Победа!", "Порядок победил")
                self.reset_game()
                return

            # Проверяем победу Хаоса
            if self.is_board_full():
                messagebox.showinfo("Победа!", "Хаос победил")
                self.reset_game()
                return

            self.current_player = "Chaos" if player == "Order" else "Order"
            self.update_status()

    def check_any_win(self, row, col):
        """Проверяет, есть ли линия из 5 одинаковых символов"""
        symbol = self.board[row][col]
        if symbol == "":
            return False

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1

            r, c = row + dr, col + dc
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == symbol:
                count += 1
                r += dr
                c += dc

            r, c = row - dr, col - dc
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == symbol:
                count += 1
                r -= dr
                c -= dc

            if count >= self.win_length:
                return True

        return False

    def is_board_full(self):
        for row in self.board:
            if "" in row:
                return False
        return True

    def update_status(self):
        color = "hotpink" if self.current_player == "Order" else "limegreen"
        self.status_label.config(
            text=f"Ход: {self.current_player}",
            fg=color
        )

    def reset_game(self):
        self.current_player = "Order"
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(
                    text="",
                    fg="black",
                    bg="white",
                    state=tk.NORMAL
                )

        self.update_status()


class UltimateTicTacToe:
    def __init__(self):
        # Константы
        self.WIDTH, self.HEIGHT = 800, 850
        self.LINE_WIDTH = 5
        self.BIG_ROWS, self.BIG_COLS = 3, 3
        self.SMALL_ROWS, self.SMALL_COLS = 3, 3
        self.BIG_SQUARE_SIZE = self.WIDTH // self.BIG_COLS
        self.SMALL_SQUARE_SIZE = self.BIG_SQUARE_SIZE // self.SMALL_COLS

        # Цвета
        self.BG_COLOR = (250, 248, 239)
        self.BIG_LINE_COLOR = (0, 0, 0)
        self.SMALL_LINE_COLOR = (200, 200, 200)
        self.X_COLOR = (70, 130, 180)
        self.O_COLOR = (220, 20, 60)
        self.TEXT_COLOR = (50, 50, 50)
        self.INFO_AREA_COLOR = (230, 230, 230)
        self.DARKEN_COLOR = (100, 100, 100, 150)

        # Инициализация pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Вложенные крестики-нолики (свободный режим)')

        # Доски
        self.big_board = [[None for _ in range(self.BIG_COLS)] for _ in range(self.BIG_ROWS)]
        self.small_boards = [[[[None for _ in range(self.SMALL_COLS)] for _ in range(self.SMALL_ROWS)]
                              for _ in range(self.BIG_COLS)] for _ in range(self.BIG_ROWS)]

        # Текущий игрок
        self.current_player = 'X'

        # Победители маленьких досок
        self.board_winners = [[None for _ in range(self.BIG_COLS)] for _ in range(self.BIG_ROWS)]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        winner = self.check_big_board_winner()
                        if winner is None:
                            self.handle_click(event.pos)

                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.reset_game()

            # Отрисовка
            self.screen.fill(self.BG_COLOR)
            self.draw_lines()
            self.draw_figures()
            self.draw_board_winners()
            self.draw_player_info()

            # Проверка на победу
            winner = self.check_big_board_winner()
            if winner is not None:
                self.draw_game_over(winner)

            pygame.display.update()

    def draw_lines(self):
        # Основные линии
        for i in range(1, self.BIG_ROWS):
            pygame.draw.line(self.screen, self.BIG_LINE_COLOR,
                             (0, i * self.BIG_SQUARE_SIZE),
                             (self.WIDTH, i * self.BIG_SQUARE_SIZE), self.LINE_WIDTH)
            pygame.draw.line(self.screen, self.BIG_LINE_COLOR,
                             (i * self.BIG_SQUARE_SIZE, 0),
                             (i * self.BIG_SQUARE_SIZE, self.HEIGHT - 50), self.LINE_WIDTH)

        # Линии маленьких досок
        for big_row in range(self.BIG_ROWS):
            for big_col in range(self.BIG_COLS):
                start_x = big_col * self.BIG_SQUARE_SIZE
                start_y = big_row * self.BIG_SQUARE_SIZE

                for i in range(1, self.SMALL_ROWS):
                    pygame.draw.line(self.screen, self.SMALL_LINE_COLOR,
                                     (start_x, start_y + i * self.SMALL_SQUARE_SIZE),
                                     (start_x + self.BIG_SQUARE_SIZE, start_y + i * self.SMALL_SQUARE_SIZE),
                                     self.LINE_WIDTH // 2)
                    pygame.draw.line(self.screen, self.SMALL_LINE_COLOR,
                                     (start_x + i * self.SMALL_SQUARE_SIZE, start_y),
                                     (start_x + i * self.SMALL_SQUARE_SIZE, start_y + self.BIG_SQUARE_SIZE),
                                     self.LINE_WIDTH // 2)

    def draw_figures(self):
        for big_row in range(self.BIG_ROWS):
            for big_col in range(self.BIG_COLS):
                for small_row in range(self.SMALL_ROWS):
                    for small_col in range(self.SMALL_COLS):
                        if self.small_boards[big_row][big_col][small_row][small_col] is not None:
                            x = big_col * self.BIG_SQUARE_SIZE + small_col * self.SMALL_SQUARE_SIZE + self.SMALL_SQUARE_SIZE // 2
                            y = big_row * self.BIG_SQUARE_SIZE + small_row * self.SMALL_SQUARE_SIZE + self.SMALL_SQUARE_SIZE // 2

                            if self.small_boards[big_row][big_col][small_row][small_col] == 'X':
                                pygame.draw.line(self.screen, self.X_COLOR,
                                                 (x - self.SMALL_SQUARE_SIZE // 3, y - self.SMALL_SQUARE_SIZE // 3),
                                                 (x + self.SMALL_SQUARE_SIZE // 3, y + self.SMALL_SQUARE_SIZE // 3),
                                                 self.LINE_WIDTH)
                                pygame.draw.line(self.screen, self.X_COLOR,
                                                 (x + self.SMALL_SQUARE_SIZE // 3, y - self.SMALL_SQUARE_SIZE // 3),
                                                 (x - self.SMALL_SQUARE_SIZE // 3, y + self.SMALL_SQUARE_SIZE // 3),
                                                 self.LINE_WIDTH)
                            else:
                                pygame.draw.circle(self.screen, self.O_COLOR, (x, y), self.SMALL_SQUARE_SIZE // 3,
                                                   self.LINE_WIDTH)

    def draw_board_winners(self):
        font = pygame.font.SysFont('Arial', self.BIG_SQUARE_SIZE // 2)
        for big_row in range(self.BIG_ROWS):
            for big_col in range(self.BIG_COLS):
                if self.board_winners[big_row][big_col] is not None:
                    s = pygame.Surface((self.BIG_SQUARE_SIZE, self.BIG_SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill(self.DARKEN_COLOR)
                    self.screen.blit(s, (big_col * self.BIG_SQUARE_SIZE, big_row * self.BIG_SQUARE_SIZE))

                    x = big_col * self.BIG_SQUARE_SIZE + self.BIG_SQUARE_SIZE // 2
                    y = big_row * self.BIG_SQUARE_SIZE + self.BIG_SQUARE_SIZE // 2

                    if self.board_winners[big_row][big_col] == 'X':
                        text = font.render('X', True, self.X_COLOR)
                    elif self.board_winners[big_row][big_col] == 'O':
                        text = font.render('O', True, self.O_COLOR)
                    else:
                        text = font.render('D', True, (200, 200, 200))

                    text_rect = text.get_rect(center=(x, y))
                    self.screen.blit(text, text_rect)

    def draw_player_info(self):
        info_rect = pygame.Rect(0, self.HEIGHT - 50, self.WIDTH, 50)
        pygame.draw.rect(self.screen, self.INFO_AREA_COLOR, info_rect)

        font = pygame.font.SysFont('Arial', 30)
        player_text = f"Сейчас ходит: {'Крестик (X)' if self.current_player == 'X' else 'Нолик (O)'}"
        text_surface = font.render(player_text, True, self.TEXT_COLOR)
        self.screen.blit(text_surface, (20, self.HEIGHT - 40))

        instr_text = "R - рестарт | Клик - поставить символ"
        instr_surface = font.render(instr_text, True, self.TEXT_COLOR)
        self.screen.blit(instr_surface, (self.WIDTH - 350, self.HEIGHT - 40))

    def handle_click(self, pos):
        x, y = pos

        if y > self.HEIGHT - 50:
            return

        big_col = x // self.BIG_SQUARE_SIZE
        big_row = y // self.BIG_SQUARE_SIZE

        if self.board_winners[big_row][big_col] is not None:
            return

        x_in_big = x % self.BIG_SQUARE_SIZE
        y_in_big = y % self.BIG_SQUARE_SIZE
        small_col = x_in_big // self.SMALL_SQUARE_SIZE
        small_row = y_in_big // self.SMALL_SQUARE_SIZE

        if self.small_boards[big_row][big_col][small_row][small_col] is not None:
            return

        self.small_boards[big_row][big_col][small_row][small_col] = self.current_player

        winner = self.check_small_board_winner(big_row, big_col)
        if winner is not None:
            self.board_winners[big_row][big_col] = winner

        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_small_board_winner(self, big_row, big_col):
        board = self.small_boards[big_row][big_col]

        for row in range(self.SMALL_ROWS):
            if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
                return board[row][0]

        for col in range(self.SMALL_COLS):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
                return board[0][col]

        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]

        for row in range(self.SMALL_ROWS):
            for col in range(self.SMALL_COLS):
                if board[row][col] is None:
                    return None

        return 'D'

    def check_big_board_winner(self):
        for row in range(self.BIG_ROWS):
            if self.board_winners[row][0] == self.board_winners[row][1] == self.board_winners[row][2] and \
                    self.board_winners[row][0] is not None:
                return self.board_winners[row][0]

        for col in range(self.BIG_COLS):
            if self.board_winners[0][col] == self.board_winners[1][col] == self.board_winners[2][col] and \
                    self.board_winners[0][col] is not None:
                return self.board_winners[0][col]

        if self.board_winners[0][0] == self.board_winners[1][1] == self.board_winners[2][2] and self.board_winners[0][
            0] is not None:
            return self.board_winners[0][0]
        if self.board_winners[0][2] == self.board_winners[1][1] == self.board_winners[2][0] and self.board_winners[0][
            2] is not None:
            return self.board_winners[0][2]

        for row in range(self.BIG_ROWS):
            for col in range(self.BIG_COLS):
                if self.board_winners[row][col] is None:
                    return None

        return 'D'

    def draw_game_over(self, winner):
        s = pygame.Surface((self.WIDTH, self.HEIGHT - 50), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))

        font = pygame.font.SysFont('Arial', 50)
        if winner == 'D':
            text = font.render('Ничья! Нажмите R для рестарта', True, (255, 255, 255))
        else:
            text = font.render(f'Игрок {winner} победил! Нажмите R для рестарта', True,
                               self.X_COLOR if winner == 'X' else self.O_COLOR)
        text_rect = text.get_rect(center=(self.WIDTH // 2, (self.HEIGHT - 50) // 2))
        pygame.draw.rect(self.screen, (70, 70, 70), text_rect.inflate(20, 20))
        self.screen.blit(text, text_rect)

    def reset_game(self):
        self.small_boards = [[[[None for _ in range(self.SMALL_COLS)] for _ in range(self.SMALL_ROWS)]
                              for _ in range(self.BIG_COLS)] for _ in range(self.BIG_ROWS)]
        self.board_winners = [[None for _ in range(self.BIG_COLS)] for _ in range(self.BIG_ROWS)]
        self.current_player = 'X'


if __name__ == "__main__":
    root = tk.Tk()
    app = GameMenu(root)
    root.mainloop()
