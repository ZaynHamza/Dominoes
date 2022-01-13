import random


class Domino:
    domino_list = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                   [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                   [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
                   [3, 3], [3, 4], [3, 5], [3, 6],
                   [4, 4], [4, 5], [4, 6],
                   [5, 5], [5, 6],
                   [6, 6]]

    def __init__(self):
        # Initialization
        self.computer = []
        self.player = []
        self.stock = []
        self.snake = []
        self.status = None
        # Just for calculations
        self.working_list = []
        self.count = []
        self.prepare()

    def __str__(self):
        return f'''Stock pieces: {self.stock}\nComputer pieces: {self.computer}\nPlayer pieces: {self.player}\nDomino 
        snake: {self.snake}\nStatus: {self.status} '''

    def init_count(self):
        self.count = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]

    def prepare(self):
        # Game lists preparation
        self.working_list = Domino.domino_list[::]
        random.shuffle(self.working_list)
        self.player = self.working_list[0:7]
        self.computer = self.working_list[7:14]
        self.stock = self.working_list[14:]

    def calc_initial_snake(self, player_list, computer_list):
        # define initial snake - here also defined -  need re-shuffle or not
        # consider player items
        # for first - just append - if founds after - need to replace
        for x in player_list:
            if int(x[0]) == int(x[1]):
                if len(self.snake) == 0:
                    self.snake.append(x)
                    self.status = "player"
                else:
                    if x[0] + x[1] > self.snake[0][0] + self.snake[0][1]:
                        self.snake[0] = x
                        self.status = "player"

        # consider computer items
        for x in computer_list:
            if x[0] == x[1]:
                if len(self.snake) == 0:
                    self.snake.append(x)
                    self.status = "computer"
                else:
                    if x[0] + x[1] > self.snake[0][0] + self.snake[0][1]:
                        self.snake[0] = x
                        self.status = "computer"

        # condition for re-shuffle - means that we not found item to start the game in lists (player and computer)
        if len(self.status) == 0:
            return False

        # item placed to snake - we need to remove it from player or computer list and swap move to correct side
        if self.status == "player":
            player_list.remove(self.snake[0])
            self.status = "computer"
        else:
            computer_list.remove(self.snake[0])
            self.status = "player"
        return True

    def snake_show(self):
        string = ""
        if len(self.snake) > 6:
            snake_left = self.snake[0:3]
            snake_right = self.snake[len(self.snake) - 3:]
            for x in snake_left:
                string += f"{x}"
            string += "..."
            for x in snake_right:
                string += f"{x}"
        else:
            for x in self.snake:
                string += f"{x}"
        return string

    def show_ui(self):
        # just output the state
        print("=" * 70)
        stock_size = len(self.stock)
        print(f"Stock size: {stock_size}")
        computer_pieces = len(self.computer)
        print(f"Computer pieces: {computer_pieces}")
        print()
        print(self.snake_show())
        print()
        print("Your pieces:")
        line = 1
        for x in self.player:
            print(f"{line}:{x}")
            line += 1
        print()

    def print_move_status(self):
        # in-game move status output
        if self.status == "player":
            print("Status: It's your turn to make a move. Enter your command.")
        else:
            print("Status: Computer is about to make a move. Press Enter to continue...")

    def print_end_status(self):
        # end game status output
        self.show_ui()
        if self.status == "player":
            print("Status: The game is over. You won!")
        elif self.status == "computer":
            print("Status: The game is over. The computer won!")
        else:
            print("Status: The game is over. It's a draw!")

    def is_game_ends(self):
        # conditions for end of game
        # 1. checks if player or computer has no items
        if len(self.player) == 0:
            self.status = "player"
            return True

        if len(self.computer) == 0:
            self.status = "computer"
            return True
        if len(self.snake) < 8:
            return False
        # 2. condition for draw
        snake_left = self.snake[0][0]
        snake_right = self.snake[len(self.snake) - 1][1]
        if snake_left == snake_right:
            check = self.snake[0][0]
            count = 0
            for x in self.snake:
                if x[0] == check:
                    count += 1
                if (x[1]) == check:
                    count += 1
            if count == 8:
                self.status = "draw"
                return True
        return False

    def check_move(self, move):
        # Rules for move
        # empty command
        if move == "":
            return False
        # command must be min 1 char and max 2 chars
        if len(move) > 2:
            return False
        # for 0 we need to check if stock not empty
        if move == "0":
            if len(self.stock) == 0:
                return False
            else:
                return True
        # left side of snake direction must be char '-'
        item_position = ''
        item_position = move[0]
        if len(move) == 2:
            if move[0] != '-':
                return False
            item_position = move[1]
        # check that position is correct
        try:
            item_position_int = int(item_position)
            if (item_position_int == 0) or (item_position_int > len(self.player)):
                return False
        except ValueError:
            return False
        return True

    def apply_move(self, move):
        # for 0 move - check if stock item contains values in snake
        # revert item if need it
        # if item values  not in snake ends - add it to player or computer pile
        if move == "0":
            item = self.stock.pop(0)
            if self.status == "player":
                self.player.append(item)
            else:
                self.computer.append(item)
            return

        if len(move) == 2:
            if self.status == "player":
                item = self.player.pop(int(move[1]) - 1)
            else:
                item = self.computer.pop(int(move[1]) - 1)
            if item[1] != self.snake[0][0]:
                new_item = [item[1], item[0]]
                item = new_item
            new_snake = [item]
            for x in self.snake:
                new_snake.append(x)
            self.snake = new_snake
        else:
            if self.status == "player":
                item = self.player.pop(int(move) - 1)
            else:
                item = self.computer.pop(int(move) - 1)
            if item[0] != self.snake[-1][1]:
                new_item = [item[1], item[0]]
                item = new_item
            self.snake.append(item)

    def check_is_move_legal(self, move):
        if move == "0":
            return True
        item = []
        item_check = []
        if len(move) == 2:
            item = self.snake[0]
            if self.status == "player":
                item_check = self.player[int(move[1]) - 1]
            else:
                item_check = self.computer[int(move[1]) - 1]
            if (item_check[0] == item[0]) or (item_check[1] == item[0]):
                return True
            else:
                return False
        else:
            item = self.snake[-1]
            if self.status == "player":
                item_check = self.player[int(move[0]) - 1]
            else:
                item_check = self.computer[int(move[0]) - 1]
            if (item_check[0] == item[1]) or (item_check[1] == item[1]):
                return True
            else:
                return False
        return False

    def calc_count(self):
        self.init_count()
        for x in self.snake:
            self.count[x[0]][1] += 1
            self.count[x[1]][1] += 1
        for x in self.computer:
            self.count[x[0]][1] += 1
            self.count[x[1]][1] += 1

    def create_computer_move(self):
        self.calc_count()
        items_scores = []
        item_pos = 0
        for x in self.computer:
            item_pos += 1
            score = [item_pos, self.count[x[0]][1] + self.count[x[1]][1]]
            items_scores.append(score)

        snake_left = self.snake[0][0]
        snake_right = self.snake[-1][1]

        while len(items_scores) > 0:
            max_score_item = 1
            score_items_max = 0
            counter = 0
            max_score = items_scores[0][1]
            for x in items_scores:
                if x[1] > max_score:
                    max_score = x[1]
                    max_score_item = x[0]
                    score_items_max = counter
                counter += 1
            if len(items_scores) > 0:
                items_scores.pop(score_items_max)
            else:
                return "0"
            item = self.computer[max_score_item - 1]
            if snake_left in item:
                return f"-{max_score_item}"
            if snake_right in item:
                return f"{max_score_item}"
        return "0"

    def do_computer_move(self):
        while True:
            input()
            move = self.create_computer_move()
            self.apply_move(move)
            break

    def do_player_move(self):
        while True:
            move = input()
            if not self.check_move(move):
                print("Invalid input. Please try again.")
                continue
            else:
                if not self.check_is_move_legal(move):
                    print("Illegal move. Please try again.")
                    continue
                self.apply_move(move)
                break

    def do_move(self):
        # select a move
        if self.status == "player":
            self.do_player_move()
        else:
            self.do_computer_move()

    def play(self):
        # initial shuffle
        while not self.calc_initial_snake(self.player, self.computer):
            self.prepare()

            # main loop
        while not self.is_game_ends():
            self.show_ui()
            self.print_move_status()
            self.do_move()
            # swap move
            if self.status == "player":
                self.status = "computer"
            else:
                self.status = "player"

        # end game message
        self.print_end_status()


# Game launches here
domino_game = Domino()
domino_game.play()
