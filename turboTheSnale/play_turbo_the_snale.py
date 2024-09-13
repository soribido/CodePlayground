import pygame
import random
import time
import tkinter as tk
from tkinter import simpledialog, messagebox

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 셀 크기
CELL_SIZE = 30
INFO_PANEL_WIDTH = 100  # Trial 표시를 위한 패널 너비

def create_board(rows, cols):
    """보드를 생성하고 규칙에 맞게 괴물을 배치합니다."""
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    available_cols = list(range(cols))
    
    # 각 행에 하나의 괴물을 배치 (첫 번째와 마지막 행 제외)
    for i in range(1, rows - 1):
        monster_col = available_cols.pop(random.randint(0, len(available_cols) - 1))
        board[i][monster_col] = 'M'
    
    return board

def draw_board(screen, board, turbo_position, trial, show_monsters=False):
    """보드를 그립니다."""
    rows = len(board)
    cols = len(board[0])

    screen.fill(WHITE)

    # 보드 그리기
    for i in range(rows):
        for j in range(cols):
            color = BLACK
            if (i, j) == turbo_position:
                pygame.draw.rect(screen, BLUE, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif board[i][j] == 'X':  # 괴물과 마주친 칸 (괴물 위치 유지)
                pygame.draw.rect(screen, RED, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif board[i][j] == 'M' and show_monsters:
                pygame.draw.rect(screen, WHITE, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, RED, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
            elif board[i][j] == 'M':
                pygame.draw.rect(screen, color, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            else:
                pygame.draw.rect(screen, color, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # 정보 패널 그리기
    font = pygame.font.Font(None, 36)
    text = font.render(f'Trial: {trial}', True, BLACK)
    screen.blit(text, (cols * CELL_SIZE + 10, 10))

    pygame.display.flip()

def show_message(trial):
    """게임 종료 후 메시지 창을 표시합니다."""
    root = tk.Tk()
    root.withdraw()  # 메인 창을 숨깁니다.

    msg = f"{trial} 회 만에 클리어 하셨습니다."
    result = messagebox.askquestion("게임 종료", msg + "\n다시 하시겠습니까?", icon='info')

    if result == 'yes':
        return 'retry'
    else:
        return 'quit'

def move_turbo(screen, board, start_col):
    """터보가 괴물을 피하면서 마지막 행으로 이동합니다."""
    rows = len(board)
    cols = len(board[0])
    turbo_position = (0, start_col)  # 터보의 초기 위치 (첫 번째 행의 start_col)
    trial = 1  # 초기 시도 횟수
    running = True

    while running:
        draw_board(screen, board, turbo_position, trial)
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_position = (turbo_position[0], max(0, turbo_position[1] - 1))
                elif event.key == pygame.K_RIGHT:
                    new_position = (turbo_position[0], min(cols - 1, turbo_position[1] + 1))
                elif event.key == pygame.K_UP:
                    new_position = (max(0, turbo_position[0] - 1), turbo_position[1])
                elif event.key == pygame.K_DOWN:
                    new_position = (min(rows - 1, turbo_position[0] + 1), turbo_position[1])
                elif event.key == pygame.K_F2:
                    draw_board(screen, board, turbo_position, trial, show_monsters=True)
                    pygame.time.delay(3000)
                    draw_board(screen, board, turbo_position, trial, show_monsters=False)
                    continue
                else:
                    new_position = turbo_position

                if board[new_position[0]][new_position[1]] in ['M', 'X']:
                    # 괴물을 만나면 칸을 빨간색으로 바꾸고 초기 위치로 돌아감
                    board[new_position[0]][new_position[1]] = 'X'
                    turbo_position = (0, start_col)
                    trial += 1
                else:
                    turbo_position = new_position

                draw_board(screen, board, turbo_position, trial)

        # 목표 도달 확인
        if turbo_position[0] == rows - 1:
            print("터보가 성공적으로 마지막 행에 도달했습니다!")
            running = False
            result = show_message(trial)
            if result == 'retry':
                return True
            else:
                return False

    pygame.quit()

def get_rows():
    """행의 개수를 입력받는 창을 띄웁니다."""
    root = tk.Tk()
    root.withdraw()  # 메인 창을 숨깁니다.
    
    rows = simpledialog.askinteger("행의 개수 입력", "행의 개수를 입력하세요 (첫 번째와 마지막 행 제외):", minvalue=1)
    
    root.destroy()  # 입력받은 후 창을 닫습니다.
    
    if rows is None:
        return None
    return rows + 2  # 첫 번째와 마지막 행을 포함하기 위해 2를 더합니다.

def main():
    pygame.init()

    while True:
        rows = get_rows()
        if rows is None:
            break

        cols = rows - 1
        board = create_board(rows, cols)

        start_col = random.randint(0, cols - 1)
        print(f"터보가 시작할 열: {start_col}")

        screen = pygame.display.set_mode((cols * CELL_SIZE + INFO_PANEL_WIDTH, rows * CELL_SIZE))
        pygame.display.set_caption("Turbo the Snail")

        if not move_turbo(screen, board, start_col):
            break

if __name__ == "__main__":
    main()
