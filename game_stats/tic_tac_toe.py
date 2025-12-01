import os
import random

board = []
size = 3
player = 'X'
mode = 1
stats = {"games": 0, "wins_X": 0, "wins_O": 0, "draws": 0}
stats_file = "papka/sohr_rez.txt"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_stats():
    global stats
    try:
        os.makedirs("papka", exist_ok=True)
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if "Всего игр:" in line:
                        stats["games"] = int(line.split(":")[1].strip())
                    elif "Побед X:" in line:
                        stats["wins_X"] = int(line.split(":")[1].strip())
                    elif "Побед O:" in line:
                        stats["wins_O"] = int(line.split(":")[1].strip())
                    elif "Ничьих:" in line:
                        stats["draws"] = int(line.split(":")[1].strip())
    except:
        pass

def save_stats(winner):
    global stats
    stats["games"] += 1
    if winner == 'X':
        stats["wins_X"] += 1
    elif winner == 'O':
        stats["wins_O"] += 1
    else:
        stats["draws"] += 1
        
    try:
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(f"Всего игр: {stats['games']}\n")
            f.write(f"Побед X: {stats['wins_X']}\n")
            f.write(f"Побед O: {stats['wins_O']}\n")
            f.write(f"Ничьих: {stats['draws']}\n")
    except:
        pass

def setup():
    global board, size
    board = [[' ' for _ in range(size)] for _ in range(size)]

def show():
    clear()
    print(f"\n{' КРЕСТИКИ-НОЛИКИ ':=^30}")
    print(f"Игрок: {player}")
    print()
    
    for i in range(size):
        print(" " + " | ".join(board[i]))
        if i < size - 1:
            print("-" * (size * 4 - 1))
    print()

def check_win():
    global board, player, size
    for i in range(size):
        if all(board[i][j] == player for j in range(size)) and board[i][0] != ' ':
            return True
        if all(board[j][i] == player for j in range(size)) and board[0][i] != ' ':
            return True

    if all(board[i][i] == player for i in range(size)) and board[0][0] != ' ':
        return True
    if all(board[i][size-1-i] == player for i in range(size)) and board[0][size-1] != ' ':
        return True
    
    return False

def check_full():
    global board
    return all(cell != ' ' for row in board for cell in row)

def make_move(row, col):
    global board, player, size
    if 0 <= row < size and 0 <= col < size and board[row][col] == ' ':
        board[row][col] = player
        return True
    return False

def bot_move():
    global board, size

    empty = [(i, j) for i in range(size) for j in range(size) if board[i][j] == ' ']
    if empty:
        row, col = random.choice(empty)
        board[row][col] = 'O'
        return True
    return False

def change_player():
    global player
    player = 'O' if player == 'X' else 'X'

def show_stats():
    clear()
    print(f"\n{' СТАТИСТИКА ':=^30}")
    print(f"Игр: {stats['games']}")
    print(f"Побед X: {stats['wins_X']}")
    print(f"Побед O: {stats['wins_O']}")
    print(f"Ничьих: {stats['draws']}")
    
    if stats['games'] > 0:
        print(f"\n% побед X: {(stats['wins_X']/stats['games'])*100:.1f}")
        print(f"% побед O: {(stats['wins_O']/stats['games'])*100:.1f}")
        print(f"% ничьих: {(stats['draws']/stats['games'])*100:.1f}")
    
    input("\nEnter - назад")

def choose_size():
    global size
    clear()
    print(f"\n{' РАЗМЕР ПОЛЯ ':=^30}")
    print("1. 3x3")
    print("2. 4x4")
    print("3. 5x5")
    print("0. Назад")
    
    choice = input("\nВыбор: ").strip()
    if choice == '1': 
        size = 3
        return True
    elif choice == '2': 
        size = 4
        return True
    elif choice == '3': 
        size = 5
        return True
    elif choice == '0': 
        return False
    return True

def choose_mode():
    global mode
    clear()
    print(f"\n{' РЕЖИМ ИГРЫ ':=^30}")
    print("1. Игрок vs Игрок")
    print("2. Игрок vs Бот")
    print("0. Назад")
    
    choice = input("\nВыбор: ").strip()
    if choice == '1': 
        mode = 1
        return True
    elif choice == '2': 
        mode = 2
        return True
    elif choice == '0': 
        return False
    return True

def play_game():
    global player, mode, size
    player = random.choice(['X', 'O'])
    setup()
    active = True
    
    while active:
        show()
        
        if check_full():
            print("Ничья!")
            save_stats(None)
            break
        
        try:
            if mode == 2 and player == 'O':
                print("Ход бота...")
                bot_move()
            else:
                print(f"Игрок {player}")
                row = int(input(f"Строка (1-{size}): ")) - 1
                col = int(input(f"Столбец (1-{size}): ")) - 1
                
                if not make_move(row, col):
                    print("Ошибка! Повторите.")
                    input()
                    continue
            
            if check_win():
                show()
                print(f"Победил {player}!")
                save_stats(player)
                break
            else:
                change_player()
                
        except:
            print("Ошибка ввода!")
            input()
    
    again = input("\nЕще раз? (д/н): ").lower()
    return again in ['д', 'да', 'y', 'yes']

def main_menu():
    while True:
        clear()
        print(f"\n{' МЕНЮ ':=^30}")
        print("1. Новая игра")
        print("2. Статистика")
        print("0. Выход")
        
        choice = input("\nВыбор: ").strip()
        
        if choice == '1':
            if not choose_mode(): 
                continue
            if not choose_size(): 
                continue
            
            while play_game():
                pass
                
        elif choice == '2':
            show_stats()
        elif choice == '0':
            print("\nДо свидания!")
            break

def main():
    load_stats()
    main_menu()
    
main()
