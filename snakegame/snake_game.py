import pygame
import time
import random

# 初始化pygame
pygame.init()

# 定义颜色 - 确保有足够对比度
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)  # 改为纯红色
green = (0, 255, 0)  # 改为纯绿色
blue = (0, 0, 255)

# 设置显示窗口
display_width = 600
display_height = 400
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# 设置游戏时钟
clock = pygame.time.Clock()

# 蛇的大小和速度
snake_block = 10
snake_speed = 10

# 设置字体 - 使用系统默认字体避免乱码
font_style = pygame.font.SysFont(None, 30)  # 修改为None使用默认字体
score_font = pygame.font.SysFont(None, 35)


# 显示得分
def your_score(score):
    value = score_font.render("Score: " + str(score), True, black)  # 改为英文
    dis.blit(value, [10, 10])  # 调整位置


# 绘制蛇 - 添加边框使其更明显
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block], 1)  # 添加黑色边框


# 显示消息 - 改为英文
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    # 居中显示
    text_rect = mesg.get_rect(center=(display_width / 2, display_height / 2))
    dis.blit(mesg, text_rect)


# 主游戏循环
def gameLoop():
    game_over = False
    game_close = False

    # 初始化蛇的位置
    x1 = display_width / 2
    y1 = display_height / 2

    # 初始化蛇的移动方向
    x1_change = 0
    y1_change = 0

    # 初始化蛇的身体
    snake_List = []
    Length_of_snake = 1

    # 随机生成食物位置
    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(white)
            message("Game Over! Press Q-Quit or C-Play Again", red)  # 改为英文
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 检查是否撞到边界
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)

        # 绘制食物 - 添加边框使其更明显
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, black, [foodx, foody, snake_block, snake_block], 1)  # 添加黑色边框

        # 更新蛇的身体
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # 如果蛇的长度超过了应有的长度，删除多余的部分
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 绘制蛇和显示得分
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # 检查是否吃到食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # 控制游戏速度
        clock.tick(snake_speed)

    # 退出游戏
    pygame.quit()
    quit()


# 启动游戏
gameLoop()