import pygame
import random
import os
import sys

# 初始化pygame
pygame.init()

# 定義顏色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 設置顯示視窗大小
display_width = 800
display_height = 600
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game with Images')

# 設置遊戲時鐘
clock = pygame.time.Clock()

# 蛇的尺寸和速度
snake_block = 30
snake_speed = 15

# 設置字體
font_style = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 35)


# 載入圖片函式
def load_image(name, size=None):
    try:
        possible_paths = [
            name,
            os.path.join("images", name),
            os.path.join("..", "images", name),
        ]

        image_path = None
        for path in possible_paths:
            if os.path.exists(path):
                image_path = path
                break

        if image_path is None:
            print(f"圖片不存在: {name}，嘗試的路徑: {possible_paths}")
            surf = pygame.Surface((snake_block, snake_block))
            surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            return surf

        print(f"成功載入圖片: {image_path}")
        image = pygame.image.load(image_path)
        if size:
            image = pygame.transform.scale(image, size)
        return image.convert_alpha()
    except pygame.error as e:
        print(f"無法載入圖片: {name}, 錯誤: {e}")
        surf = pygame.Surface((snake_block, snake_block))
        surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return surf


# 載入圖片
snake_head_img = load_image("snake_head.png", (snake_block, snake_block))
snake_body_img = load_image("snake_body.png", (snake_block, snake_block))
fruit_imgs = [
    load_image("apple.png", (snake_block, snake_block)),
    load_image("banana.png", (snake_block, snake_block)),
    load_image("orange.png", (snake_block, snake_block))
]


# 顯示分數
def your_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [10, 10])


# 繪製蛇身
def our_snake(snake_block, snake_list, direction):
    for i, segment in enumerate(snake_list):
        if i == len(snake_list) - 1:  # 蛇頭
            rotated_head = snake_head_img
            if direction == "RIGHT":
                rotated_head = pygame.transform.rotate(snake_head_img, 270)
            elif direction == "LEFT":
                rotated_head = pygame.transform.rotate(snake_head_img, 90)
            elif direction == "UP":
                rotated_head = snake_head_img
            elif direction == "DOWN":
                rotated_head = pygame.transform.rotate(snake_head_img, 180)
            dis.blit(rotated_head, (segment[0], segment[1]))
        else:
            dis.blit(snake_body_img, (segment[0], segment[1]))


# 顯示訊息
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(display_width / 2, display_height / 2))
    dis.blit(mesg, text_rect)


# 生成食物位置
def generate_food(snake_list=None):
    if snake_list is None:
        snake_list = []

    while True:
        foodx = random.randrange(0, display_width - snake_block, snake_block)
        foody = random.randrange(0, display_height - snake_block, snake_block)

        # 確保食物不會生成在蛇身上
        if [foodx, foody] not in snake_list:
            return foodx, foody


# 重置遊戲狀態
def reset_game():
    x1 = display_width / 2
    y1 = display_height / 2
    x1_change = 0
    y1_change = 0
    direction = "RIGHT"
    snake_List = []
    Length_of_snake = 1

    foodx, foody = generate_food()
    food_type = random.randint(0, len(fruit_imgs) - 1)

    return x1, y1, x1_change, y1_change, direction, snake_List, Length_of_snake, foodx, foody, food_type


# 主遊戲循環
def gameLoop():
    game_over = False
    game_close = False

    # 初始化遊戲狀態
    x1, y1, x1_change, y1_change, direction, snake_List, Length_of_snake, foodx, foody, food_type = reset_game()

    # 添加輸入緩衝區
    input_buffer = []

    # 移動計時器
    move_timer = 0
    move_delay = 150  # 毫秒

    while not game_over:
        current_time = pygame.time.get_ticks()

        # 遊戲結束畫面
        while game_close:
            dis.fill(white)
            message("Game Over! Press Q-Quit or C-Play Again", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        x1, y1, x1_change, y1_change, direction, snake_List, Length_of_snake, foodx, foody, food_type = reset_game()
                        game_close = False
                        input_buffer = []

        # 處理所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                input_buffer.append(event.key)

                if event.key == pygame.K_q:
                    game_over = True

        # 處理輸入緩衝區中的按鍵
        if input_buffer:
            key = input_buffer.pop(0)

            if key == pygame.K_LEFT and direction != "RIGHT":
                x1_change = -snake_block
                y1_change = 0
                direction = "LEFT"
            elif key == pygame.K_RIGHT and direction != "LEFT":
                x1_change = snake_block
                y1_change = 0
                direction = "RIGHT"
            elif key == pygame.K_UP and direction != "DOWN":
                y1_change = -snake_block
                x1_change = 0
                direction = "UP"
            elif key == pygame.K_DOWN and direction != "UP":
                y1_change = snake_block
                x1_change = 0
                direction = "DOWN"

        # 根據計時器移動蛇
        if current_time - move_timer > move_delay:
            move_timer = current_time

            # 移動蛇
            x1 += x1_change
            y1 += y1_change

            # 檢查邊界碰撞
            if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
                game_close = True

            # 清空畫面
            dis.fill(white)

            # 繪製食物
            dis.blit(fruit_imgs[food_type], (foodx, foody))

            # 更新蛇的位置
            snake_Head = [x1, y1]
            snake_List.append(snake_Head)

            # 保持蛇的長度
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            # 檢查自我碰撞
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            # 繪製蛇
            our_snake(snake_block, snake_List, direction)

            # 顯示分數
            your_score(Length_of_snake - 1)

            # 檢查是否吃到食物 - 修復後的碰撞檢測
            # 使用矩形碰撞檢測而不是精確座標匹配
            head_rect = pygame.Rect(x1, y1, snake_block, snake_block)
            food_rect = pygame.Rect(foodx, foody, snake_block, snake_block)

            if head_rect.colliderect(food_rect):
                print(f"吃到食物！蛇頭位置: ({x1}, {y1}), 食物位置: ({foodx}, {foody})")
                print(f"吃之前的長度: {Length_of_snake}")

                # 生成新食物
                foodx, foody = generate_food(snake_List)
                food_type = random.randint(0, len(fruit_imgs) - 1)

                # 增加蛇的長度
                Length_of_snake += 1
                print(f"吃之後的長度: {Length_of_snake}")

            # 更新畫面
            pygame.display.update()

        # 控制幀率
        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()


# 啟動遊戲
if __name__ == "__main__":
    gameLoop()