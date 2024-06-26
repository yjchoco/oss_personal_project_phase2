import pygame
import sys
import os

# 파이게임 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 400, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stack Game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 블록 설정
initial_block_width = 100
block_height = 10

# 블록 이동 속도
speed = 1

# 점수
score = 0
highest_score = 0
score_file = 'scores.txt'
clock = pygame.time.Clock()

# 점수 파일 초기화
if not os.path.exists(score_file):
    with open(score_file, 'w') as file:
        file.write('')

# 점수 기록을 불러오기
def load_scores():
    with open(score_file, 'r') as file:
        scores = [int(line.strip()) for line in file if line.strip().isdigit()]
    return scores

# 점수 기록을 저장하기
def save_score(new_score):
    with open(score_file, 'a') as file:
        file.write(f"{new_score}\n")


# 블록 클래스
class Block:

    # 블록 초기화
    def __init__(self, x, y, color, speed, width):
        # 블록의 x 좌표
        self.x = x

        # 블록의 y 좌표
        self.y = y

        # 블록의 너비
        self.w = width

        # 블록의 높이
        self.h = block_height

        # 블록의 색
        self.color = color

        # 블록의 속도
        self.speed = speed

        # 블록의 방향 전환 횟수
        self.direction_changes = 0

    # 블록 그리기
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

    # 블록이 양쪽 화면에 닿으면 방향 전환
    def move(self):
        self.x += self.speed
        if self.x > screen_width or self.x + self.w < 1:
            self.speed *= -1
            self.direction_changes += 1  # 방향 전환 횟수를 추적하며,
            if self.direction_changes >= 3:  # 방향 전환 횟수가 3번 이상이면, 게임 오버
                ending()

        if self.speed != 0:
            # 움직이는 블록의 색깔을 초록색으로 바꿈
            self.color = GREEN
        else:
            self.color = RED

# 스택 클래스
class Stack:
    
    # 스택 초기화
    def __init__(self, block_width):
        self.stack = []

        # 쌓인 블록 수
        self.initSize = 20

        # 초기 블록 너비
        self.block_width = block_width

        # 초기 블록 세팅
        for i in range(self.initSize):
            newBlock = Block((screen_width - self.block_width) // 2, 590 - i * 10, RED, 0, self.block_width)
            self.stack.append(newBlock)

    # 초기 블록 세팅
    def show(self):
        for i in range(self.initSize):
            self.stack[i].draw()

    # 초기 블록 세팅
    def move(self):
        for i in range(self.initSize):
            self.stack[i].move()

    # 블록 추가하기
    def adding(self):
        global speed
        if score > 0 and score % 3 ==0:
            speed += 1
        newBlock = Block(0, 390, GREEN, speed, self.block_width)
        self.initSize += 1
        self.stack.append(newBlock)

    # 블록 쌓기 게임 진행
    def stacking(self):
        # 게임 진행 간 유지되어야 하는 점수 전역 변수 선언
        global score

        # 맨위 블록 인덱스
        lowerIndex = self.initSize - 2

        # 쌓일 블록 인덱스
        upperIndex = self.initSize - 1

        # 맨위 블록 선언
        lowerBlock = self.stack[lowerIndex]

        # 쌓일 블록 선언
        upperBlock = self.stack[upperIndex]

        # 블록을 미리 쌓은 경우
        if upperBlock.x <= lowerBlock.x and not (upperBlock.x + upperBlock.w < lowerBlock.x):
            self.stack[upperIndex].w = self.stack[upperIndex].x + self.stack[upperIndex].w - lowerBlock.x
            self.stack[upperIndex].x = lowerBlock.x
            if self.stack[upperIndex].w > lowerBlock.w:
                self.stack[upperIndex].w = lowerBlock.w
            self.stack[upperIndex].speed = 0
            # 정지되어 있는 블록은 빨간색으로 고정
            self.stack[upperIndex].color = RED
            score += 1

        # 블록을 늦게 쌓은 경우
        elif lowerBlock.x <= upperBlock.x <= lowerBlock.x + lowerBlock.w:
            self.stack[upperIndex].w = lowerBlock.x + lowerBlock.w - upperBlock.x
            self.stack[upperIndex].speed = 0
            # 정지되어 있는 블록은 빨간색으로 고정
            self.stack[upperIndex].color = RED
            score += 1
        
        # 겹치는 지점이 없게 쌓은 경우
        else:
            ending()
        
        # 한 블록 쌓일 때마다 스택 한 블록씩 내리기
        for i in range(self.initSize):
            self.stack[i].y += 10

        # 블록 너비 갱신
        self.block_width = self.stack[upperIndex].w

# 현재 점수판
def scoreboard():
    font = pygame.font.SysFont(None, 30)
    text = font.render(str(score), True, WHITE)
    screen.blit(text, (200, 10))

# 최고 기록 점수판
def highestboard():
    scores = load_scores()
    top_scores = sorted(scores, reverse=True)[:5]
    font = pygame.font.SysFont(None, 30)
    for i, top_score in enumerate(top_scores):
        text = font.render(f"RANK #{i + 1} : {top_score}", True, WHITE)
        screen.blit(text, (10, 10 + i * 30))

# 엔딩
def ending():
    global highest_score
    loop = True

    font = pygame.font.SysFont(None, 60)

    # 최고점 갱신
    if highest_score < score:
        highest_score = score
        save_score(score)
        text = font.render("New Record!", True, WHITE)
    else:
        text = font.render("Game Over!", True, WHITE)

    textRect = text.get_rect()
    textRect.center = (200, 300)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_SPACE:
                    game()
        screen.blit(text, textRect)

        pygame.display.update()
        clock.tick()

# 파이게임 종료
def close():
    pygame.quit()
    sys.exit()

# 조작키 설명
# 해당 함수에서 레벨 선택 화면 추가, 선택한 레벨에 따라 초기 블록의 넓이를 설정
def explain():
    global initial_block_width
    font1 = pygame.font.SysFont(None, 45)
    font2 = pygame.font.SysFont(None, 30)
    font3 = pygame.font.SysFont(None, 20)
    text1 = font1.render("Select Level:", True, WHITE)
    text2 = font2.render("Press 1 for Easy", True, WHITE)
    text3 = font2.render("Press 2 for Medium", True, WHITE)
    text4 = font2.render("Press 3 for Hard", True, WHITE)
    text5 = font3.render("Press Q to Quit", True, WHITE)
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    initial_block_width = 180  # Easy
                    loop = False
                if event.key == pygame.K_2:
                    initial_block_width = 100  # Medium
                    loop = False
                if event.key == pygame.K_3:
                    initial_block_width = 50  # Hard
                    loop = False
                if event.key == pygame.K_q:
                    close()
        
        screen.fill(BLACK)
        screen.blit(text1, (100, 150))
        screen.blit(text2, (100, 250))
        screen.blit(text3, (100, 300))
        screen.blit(text4, (100, 350))
        screen.blit(text5, (100, 500))
        pygame.display.update()
        clock.tick(60)


# 게임 루프
def game():
    global initial_block_width, block_height, speed, score
    loop = True

    # 세팅 초기화
    block_height = 10
    speed = 3
    score = 0
    stack = Stack(initial_block_width)
    stack.adding()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stack.stacking()
                    stack.adding()
                if event.key == pygame.K_q:
                    close()
        
        screen.fill(BLACK)
        stack.move()
        stack.show()
        scoreboard()
        highestboard()
        pygame.display.update()
        clock.tick(60)

# 실행
explain()
game()
