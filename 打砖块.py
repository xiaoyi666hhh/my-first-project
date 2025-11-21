def run():
    import pygame
    import sys
    import random

    # 初始化 Pygame
    pygame.init()

    # 确保中文正常显示
    pygame.font.init()
    font_path = pygame.font.match_font('simsun')  # 尝试匹配中文字体
    if not font_path:
        # 如果找不到中文字体，使用默认字体
        font_path = pygame.font.get_default_font()

    # 游戏常量
    WIDTH, HEIGHT = 800, 600
    PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
    BALL_SIZE = 15
    BRICK_WIDTH, BRICK_HEIGHT = 75, 25
    BRICK_ROWS = 5
    BRICK_COLS = 10
    PADDLE_SPEED = 8
    BALL_SPEED_X = 5
    BALL_SPEED_Y = 5
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)

    # 创建游戏窗口
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("打砖块游戏")

    # 定义游戏对象类
    class Paddle:
        def __init__(self):
            self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, 
                                   HEIGHT - PADDLE_HEIGHT - 10,
                                   PADDLE_WIDTH, PADDLE_HEIGHT)
            self.speed = PADDLE_SPEED
        
        def move(self, direction):
            # 改进移动逻辑，确保持续按键时能连续移动
            if direction == "left":
                self.rect.x -= self.speed
                # 确保不会移出左边界
                if self.rect.left < 0:
                    self.rect.left = 0
            if direction == "right":
                self.rect.x += self.speed
                # 确保不会移出右边界
                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH
            
        def draw(self):
            pygame.draw.rect(screen, GREEN, self.rect)
            # 添加发光效果
            glow_rect = self.rect.inflate(10, 10)
            pygame.draw.rect(screen, (0, 255, 0, 100), glow_rect, 2)

    class Ball:
        def __init__(self):
            self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                                   HEIGHT // 2 - BALL_SIZE // 2,
                                   BALL_SIZE, BALL_SIZE)
            self.speed_x = BALL_SPEED_X * random.choice((1, -1))
            self.speed_y = BALL_SPEED_Y * -1  # 初始向上运动
        
        def move(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        
            # 边界碰撞检测
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.speed_x *= -1
            if self.rect.top <= 0:
                self.speed_y *= -1
            
        def draw(self):
            pygame.draw.ellipse(screen, YELLOW, self.rect)
            # 添加发光效果
            glow_rect = self.rect.inflate(8, 8)
            pygame.draw.ellipse(screen, (255, 255, 0, 100), glow_rect, 2)
        
        def reset(self):
            self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                                   HEIGHT // 2 - BALL_SIZE // 2,
                                   BALL_SIZE, BALL_SIZE)
            self.speed_x = BALL_SPEED_X * random.choice((1, -1))
            self.speed_y = BALL_SPEED_Y * -1

    class Brick:
        def __init__(self, x, y, color):
            self.rect = pygame.Rect(x, y, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)  # -2 留出间隙
            self.color = color
            self.active = True
        
        def draw(self):
            if self.active:
                pygame.draw.rect(screen, self.color, self.rect)
                # 添加边框
                pygame.draw.rect(screen, WHITE, self.rect, 1)

    # 创建游戏对象
    paddle = Paddle()
    ball = Ball()

    # 创建砖块
    bricks = []
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * BRICK_WIDTH + 30  # 30 是左边距
            y = row * BRICK_HEIGHT + 50  # 50 是上边距
            color = colors[row % len(colors)]  # 每行使用不同颜色
            bricks.append(Brick(x, y, color))

    # 游戏变量
    score = 0
    lives = 3
    game_state = "start"  # start, playing, game_over, win
    
    # 字体设置
    def get_font(size):
        return pygame.font.Font(font_path, size)

    # 游戏主循环
    clock = pygame.time.Clock()
    running = True

    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == "start":
                    game_state = "playing"
                elif game_state in ["game_over", "win"]:
                    # 重置游戏
                    score = 0
                    lives = 3
                    ball.reset()
                    for brick in bricks:
                        brick.active = True
                    game_state = "playing"
    
        # 游戏逻辑
        if game_state == "playing":
            # 改进的移动控制 - 持续检测按键状态
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("left")
            if keys[pygame.K_RIGHT]:
                paddle.move("right")
            
            # 移动球
            ball.move()
        
            # 挡板和球的碰撞检测
            if ball.rect.colliderect(paddle.rect) and ball.speed_y > 0:
                # 根据碰撞位置调整球的水平速度
                hit_position = (ball.rect.centerx - paddle.rect.left) / paddle.rect.width
                ball.speed_x = BALL_SPEED_X * (2 * hit_position - 1) * 1.2  # 1.2 增加一点速度变化
                ball.speed_y *= -1
            
            # 砖块碰撞检测 - 修复了重复设置的问题
            for brick in bricks:
                if brick.active and ball.rect.colliderect(brick.rect):
                    score += 10
                    brick.active = False
                
                    # 确定碰撞方向
                    if ball.rect.bottom >= brick.rect.top and ball.rect.top <= brick.rect.top:
                        ball.speed_y *= -1  # 从上方碰撞
                    elif ball.rect.top <= brick.rect.bottom and ball.rect.bottom >= brick.rect.bottom:
                        ball.speed_y *= -1  # 从下方碰撞
                    elif ball.rect.right >= brick.rect.left and ball.rect.left <= brick.rect.left:
                        ball.speed_x *= -1  # 从左侧碰撞
                    elif ball.rect.left <= brick.rect.right and ball.rect.right >= brick.rect.right:
                        ball.speed_x *= -1  # 从右侧碰撞
        
            # 检查球是否落下（生命减少）
            if ball.rect.bottom >= HEIGHT:
                lives -= 1
                ball.reset()
                if lives <= 0:
                    game_state = "game_over"
                
            # 检查是否赢了游戏
            if all(not brick.active for brick in bricks):
                game_state = "win"
    
            # 绘制
        screen.fill(BLACK)
    
        # 绘制游戏对象
        paddle.draw()
        ball.draw()
        for brick in bricks:
           brick.draw()
    
        # 绘制分数和生命
        score_text = get_font(24).render(f"分数: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    
        lives_text = get_font(24).render(f"生命: {lives}", True, WHITE)
        screen.blit(lives_text, (WIDTH - 120, 10))
    
        # 绘制开始屏幕
        if game_state == "start":
            start_text = get_font(40).render("打砖块游戏", True, WHITE)
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 3))
        
            instruction_text = get_font(20).render("按任意键开始游戏", True, WHITE)
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
        
            control_text = get_font(16).render("使用左右方向键控制挡板", True, WHITE)
            screen.blit(control_text, (WIDTH // 2 - control_text.get_width() // 2, HEIGHT // 2 + 40))
    
        # 绘制游戏结束屏幕
        if game_state == "game_over":
            over_text = get_font(40).render("游戏结束", True, RED)
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))
        
            score_text = get_font(24).render(f"最终分数: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        
            restart_text = get_font(16).render("按任意键重新开始", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    
        # 绘制胜利屏幕
        if game_state == "win":
            win_text = get_font(40).render("恭喜胜利!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 3))
        
            score_text = get_font(24).render(f"最终分数: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        
            restart_text = get_font(16).render("按任意键再玩一次", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    
        # 更新屏幕
        pygame.display.flip()
        clock.tick(60)

    # 退出游戏
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    run()
