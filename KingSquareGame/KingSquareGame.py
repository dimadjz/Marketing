import tkinter as tk
from tkinter import messagebox, ttk
import os


class RoyalSquareGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Королевский квадрат")
        self.root.geometry("700x800")
        self.root.configure(bg="#2e2e2e")

        self.board_size = 5
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1
        self.player_scores = [0, 0]
        self.game_started = False
        self.dictionary = self.load_dictionary()
        self.used_words = set()

        self.setup_ui()
        self.center_board()

    def load_dictionary(self):
        """
        Загружает словарь слов из файла. Если файл не существует, создает его
        с базовым набором слов на русском языке.
        """
        default_words = [
            'балда', 'игра', 'слово', 'квадрат', 'король',
            'буква', 'доска', 'ход', 'очки', 'победа',
            'рука', 'нос', 'дом', 'сад', 'лес',
            'река', 'море', 'земля', 'небо', 'солнце'
        ]
        if not os.path.exists('dictionary.txt'):
            with open('dictionary.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(default_words))
        with open('dictionary.txt', 'r', encoding='utf-8') as f:
            return set(line.strip().lower() for line in f if line.strip())

    def setup_ui(self):
        """
        Создает пользовательский интерфейс игры с элементами управления,
        игровой доской и панелью ввода. Все выполнено в черно-серо-белом стиле.
        """
        title_label = tk.Label(
            self.root,
            text="КОРОЛЕВСКИЙ КВАДРАТ",
            font=("Arial", 20, "bold"),
            bg="#2e2e2e",
            fg="white"
        )
        title_label.pack(pady=15)

        info_frame = tk.Frame(self.root, bg="#2e2e2e")
        info_frame.pack(pady=5)

        self.player_label = tk.Label(
            info_frame,
            text="Игрок 1",
            font=("Arial", 14, "bold"),
            bg="#2e2e2e",
            fg="#cccccc"
        )
        self.player_label.pack()

        self.score_label = tk.Label(
            info_frame,
            text="Очки: 0 | 0",
            font=("Arial", 12),
            bg="#2e2e2e",
            fg="#aaaaaa"
        )
        self.score_label.pack()

        btn_frame = tk.Frame(self.root, bg="#2e2e2e")
        btn_frame.pack(pady=10)

        btn_style = {
            "font": ("Arial", 10, "bold"),
            "width": 14,
            "height": 1,
            "relief": "raised",
            "bd": 1,
            "bg": "#444444",
            "fg": "white",
            "activebackground": "#555555"
        }

        tk.Button(btn_frame, text="Новая игра", command=self.new_game, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Проверить слово", command=self.check_word, **btn_style).pack(side=tk.LEFT, padx=5)

        board_container = tk.Frame(self.root, bg="#333333", relief="solid", bd=2)
        board_container.pack(pady=20)

        self.board_frame = tk.Frame(board_container, bg="#333333")
        self.board_frame.pack(padx=10, pady=10)

        self.buttons = []
        button_width = 6
        button_height = 3
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                btn = tk.Button(
                    self.board_frame,
                    width=button_width,
                    height=button_height,
                    font=("Arial", 14, "bold"),
                    bg="#f0f0f0",
                    fg="black",
                    relief="solid",
                    bd=1,
                    command=lambda r=i, c=j: self.select_cell(r, c)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        input_frame = tk.Frame(self.root, bg="#2e2e2e")
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Введите слово:", bg="#2e2e2e", fg="#cccccc", font=("Arial", 11)).grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=5)

        self.word_entry = tk.Entry(
            input_frame,
            width=22,
            font=("Arial", 11),
            bg="#444444",
            fg="white",
            insertbackground="white",
            relief="solid",
            bd=1
        )
        self.word_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Направление:", bg="#2e2e2e", fg="#cccccc", font=("Arial", 11)).grid(row=0, column=2,
                                                                                                        padx=5)

        self.direction_var = tk.StringVar(value="горизонтально")
        direction_combo = ttk.Combobox(
            input_frame,
            textvariable=self.direction_var,
            values=["горизонтально", "вертикально"],
            state="readonly",
            width=14,
            font=("Arial", 10)
        )
        direction_combo.grid(row=0, column=3, padx=5)

        tk.Button(
            input_frame,
            text="Сделать ход",
            command=self.make_move,
            font=("Arial", 11, "bold"),
            width=12,
            height=1,
            bg="#ff9800",
            fg="white",
            activebackground="#f57c00",
            relief="raised",
            bd=1
        ).grid(row=0, column=4, padx=10)

        self.selected_row = None
        self.selected_col = None

    def center_board(self):
        """
        Устанавливает начальное состояние доски - пустая доска 5x5.
        """
        self.update_board_display()

    def new_game(self):
        """
        Начинает новую игру: очищает доску, сбрасывает счет, очищает
        список использованных слов и сбрасывает состояние игры.
        """
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1
        self.player_scores = [0, 0]
        self.game_started = True
        self.used_words.clear()
        self.selected_row = None
        self.selected_col = None
        self.center_board()
        self.update_ui()
        messagebox.showinfo("Новая игра", "Новая игра началась!", parent=self.root)

    def update_board_display(self):
        """
        Обновляет отображение игровой доски, показывая буквы в ячейках
        и подсвечивая выбранную ячейку.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                text = self.board[i][j] if self.board[i][j] else ""
                if i == self.selected_row and j == self.selected_col:
                    bg_color = "#d0d0d0"
                    fg_color = "black"
                else:
                    bg_color = "#f0f0f0"
                    fg_color = "black"

                self.buttons[i][j].config(text=text, bg=bg_color, fg=fg_color)

    def update_ui(self):
        """
        Обновляет пользовательский интерфейс: имя текущего игрока
        и счет, а также отображение доски.
        """
        self.player_label.config(text=f"Игрок {self.current_player}")
        self.score_label.config(text=f"Очки: {self.player_scores[0]} | {self.player_scores[1]}")
        self.update_board_display()

    def select_cell(self, row, col):
        """
        Обрабатывает выбор ячейки на доске. Подсвечивает выбранную
        ячейку и сохраняет ее координаты для последующего хода.
        """
        self.selected_row = row
        self.selected_col = col
        self.update_board_display()

    def validate_move(self, word, start_row, start_col, direction):
        """
        Проверяет правильность хода: соответствие слов словарю,
        возможность размещения на доске, связь с существующими буквами
        и уникальность слова (не использовалось ранее).
        """
        word = word.strip().lower()
        if not word:
            return False, "Слово не может быть пустым"

        if word in self.used_words:
            return False, "Это слово уже использовалось"

        if word not in self.dictionary:
            return False, "Слово отсутствует в словаре"

        word_len = len(word)
        if direction == "горизонтально":
            if start_col + word_len > self.board_size:
                return False, "Слово выходит за пределы доски"
        else:
            if start_row + word_len > self.board_size:
                return False, "Слово выходит за пределы доски"

        is_connected = False
        for i in range(word_len):
            r = start_row if direction == "горизонтально" else start_row + i
            c = start_col + i if direction == "горизонтально" else start_col

            if self.board[r][c]:
                if self.board[r][c].lower() != word[i]:
                    return False, f"Несовпадение в позиции ({r + 1},{c + 1})"
            else:
                if self.is_connected_to_existing(r, c):
                    is_connected = True

        if sum(self.player_scores) == 0:
            center = self.board_size // 2
            if direction == "горизонтально":
                if start_row == center and start_col <= center < start_col + word_len:
                    is_connected = True
            else:
                if start_col == center and start_row <= center < start_row + word_len:
                    is_connected = True

        if not is_connected and sum(self.player_scores) > 0:
            return False, "Слово должно быть связано с существующими буквами"

        return True, "Ход допустим"

    def is_connected_to_existing(self, row, col):
        """
        Проверяет, есть ли соседние буквы вокруг указанной ячейки.
        Необходимо для проверки связи новых слов с уже размещенными.
        """
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                if self.board[nr][nc]:
                    return True
        return False

    def place_word_on_board(self, word, start_row, start_col, direction):
        """
        Размещает слово на доске в указанном направлении,
        начиная с заданной позиции.
        """
        word_len = len(word)
        for i in range(word_len):
            r = start_row if direction == "горизонтально" else start_row + i
            c = start_col + i if direction == "горизонтально" else start_col
            if not self.board[r][c]:
                self.board[r][c] = word[i].upper()

    def calculate_score(self, word, start_row, start_col, direction):
        """
        Рассчитывает очки за ход: суммирует длину слова и длины
        пересекающихся слов, если они есть в словаре.
        """
        score = len(word)
        word_len = len(word)

        for i in range(word_len):
            r = start_row if direction == "горизонтально" else start_row + i
            c = start_col + i if direction == "горизонтально" else start_col

            cross_word = self.get_cross_word(r, c, direction)
            if len(cross_word) > 1 and cross_word.lower() in self.dictionary:
                score += len(cross_word)

        return score

    def get_cross_word(self, row, col, direction):
        """
        Получает слово, которое образуется в перпендикулярном направлении
        относительно текущего хода. Используется для расчета очков.
        """
        parts = [self.board[row][col]]

        r, c = row, col
        while True:
            if direction == "горизонтально":
                c -= 1
            else:
                r -= 1
            if r < 0 or c < 0 or not self.board[r][c]:
                break
            parts.insert(0, self.board[r][c])

        r, c = row, col
        while True:
            if direction == "горизонтально":
                c += 1
            else:
                r += 1
            if r >= self.board_size or c >= self.board_size or not self.board[r][c]:
                break
            parts.append(self.board[r][c])

        return ''.join(parts)

    def make_move(self):
        """
        Обрабатывает выполнение хода: проверяет валидность,
        размещает слово на доске, начисляет очки и переключает игрока.
        """
        if not self.game_started:
            messagebox.showwarning("Игра не начата", "Сначала нажмите «Новая игра»", parent=self.root)
            return

        word = self.word_entry.get().strip()
        if not word:
            messagebox.showwarning("Ошибка", "Введите слово!", parent=self.root)
            return

        if self.selected_row is None or self.selected_col is None:
            messagebox.showwarning("Ошибка", "Выберите начальную ячейку!", parent=self.root)
            return

        direction = self.direction_var.get()
        is_valid, msg = self.validate_move(word, self.selected_row, self.selected_col, direction)

        if is_valid:
            self.place_word_on_board(word, self.selected_row, self.selected_col, direction)
            score = self.calculate_score(word, self.selected_row, self.selected_col, direction)
            self.player_scores[self.current_player - 1] += score

            self.used_words.add(word.lower())

            self.update_board_display()
            self.update_ui()

            messagebox.showinfo("Ход принят", f"Очки за ход: {score}\nСлово '{word}' добавлено", parent=self.root)

            self.current_player = 2 if self.current_player == 1 else 1
            self.selected_row = None
            self.selected_col = None
            self.word_entry.delete(0, tk.END)

        else:
            messagebox.showerror("Ошибка", msg, parent=self.root)

    def check_word(self):
        """
        Проверяет, содержится ли введенное слово в словаре.
        Также указывает, если слово уже использовалось в игре.
        """
        word = self.word_entry.get().strip().lower()
        if word in self.dictionary:
            if word in self.used_words:
                messagebox.showinfo("✅", f"'{word}' есть в словаре, но уже использовалось", parent=self.root)
            else:
                messagebox.showinfo("✅", f"'{word}' есть в словаре", parent=self.root)
        else:
            messagebox.showerror("❌", f"'{word}' не найдено", parent=self.root)

    def run(self):
        """
        Запускает главный цикл игры и отображает окно приложения.
        """
        self.root.mainloop()


if __name__ == "__main__":
    game = RoyalSquareGame()
    game.run()