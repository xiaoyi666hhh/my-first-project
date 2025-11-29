import turtle
import time

def setup_screen():
    # 设置窗口
    screen = turtle.Screen()
    screen.title("勾股定理动画证明：a² + b² = c²")
    screen.setup(width=800, height=600)
    screen.bgcolor("white")
    return screen

def create_turtle():
    # 创建海龟对象
    t = turtle.Turtle()
    t.speed(0)  # 最快速度
    t.hideturtle()
    return t

def draw_square(t, x, y, side_length, color, fill_color=None):
    # 绘制正方形
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    if fill_color:
        t.begin_fill()
        t.fillcolor(fill_color)
    
    for _ in range(4):
        t.forward(side_length)
        t.left(90)
    
    if fill_color:
        t.end_fill()

def draw_text(t, x, y, text, size=12, color="black"):
    # 绘制文本
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.write(text, align="center", font=("SimHei", size, "normal"))

def interpolate(x1, y1, x2, y2, t):
    # 线性插值函数
    # t是[0,1]之间的值，表示插值比例
    return (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)

def draw_line(t, x1, y1, x2, y2, color="black", width=1, dashed=False):
    # 绘制直线
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.color(color)
    t.width(width)
    
    if dashed:
        # 绘制虚线
        distance = ((x2 - x1)**2 + (y2 - y1)** 2)**0.5
        segment_length = 10
        segments = int(distance / segment_length)
        
        for i in range(segments):
            # 计算当前段的终点
            px = x1 + (x2 - x1) * (i + 0.5) / segments
            py = y1 + (y2 - y1) * (i + 0.5) / segments
            
            t.goto(px, py)
            t.penup()
            
            next_x = x1 + (x2 - x1) * (i + 1) / segments
            next_y = y1 + (y2 - y1) * (i + 1) / segments
            t.goto(next_x, next_y)
            t.pendown()
    else:
        t.goto(x2, y2)
    
    t.width(1)  # 重置线宽
def draw_triangle(t, x1, y1, x2, y2, x3, y3, color, fill_color=None):
    # 绘制三角形
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.color(color)
    
    if fill_color:
        t.begin_fill()
        t.fillcolor(fill_color)
    
    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x1, y1)
    
    if fill_color:
        t.end_fill()

def draw_quadrilateral(t, x1, y1, x2, y2, x3, y3, x4, y4, color, fill_color=None):
    # 绘制四边形
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.color(color)
    
    if fill_color:
        t.begin_fill()
        t.fillcolor(fill_color)
    
    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x4, y4)
    t.goto(x1, y1)
    
    if fill_color:
        t.end_fill()

def clear_screen(t):
    # 清空屏幕
    t.clear()

def animate_pythagoras():
    # 勾股定理的边长：3, 4, 5
    a = 100  # 缩放因子，使图形更大
    b = 133  # 保持3:4的比例
    c = 166  # 保持3:4:5的比例
    
    screen = setup_screen()
    t = create_turtle()
    
    # 动画步骤
    steps = [
        "初始状态：两个正方形，面积分别为a²和b²",
        "切两刀：沿着红线切割",
        "切割后的四个部分",
        "开始拼接：移动第一部分",
        "继续拼接：移动第二部分",
        "继续拼接：移动第三部分",
        "继续拼接：移动第四部分",
        "拼接完成：形成c²正方形！",
        "验证：a² + b² = c²！"
    ]
    
    # 动画帧数设置（增加平滑度）
    animation_frames = 30  # 每个移动步骤的插值帧数
    
    # 显示标题
    draw_text(t, 0, 250, "勾股定理动画证明", 20, "blue")
    screen.update()
    time.sleep(1)  # 短暂显示标题
    
    screen.tracer(0)  # 关闭自动刷新，手动控制绘制
    
    for step_idx, step_text in enumerate(steps):
        clear_screen(t)
        
        # 显示步骤文本
        draw_text(t, 0, 250, f"步骤 {step_idx + 1}: {step_text}", 16, "blue")
        
        if step_idx == 0:
            # 步骤1: 显示初始两个正方形
            # 绘制边长为a的正方形（青色）
            draw_square(t, -200, -100, a, "cyan", "#e6f7ff")
            # 绘制边长为b的正方形（橙色）
            draw_square(t, -200 + a, -100 + a, b, "orange", "#fff7e6")
            
            # 添加标签
            draw_text(t, -200 + a/2, -100 - 30, f"a = 3", 14)
            draw_text(t, -200 + a + b/2, -100 + a - 30, f"b = 4", 14)
            
            # 添加面积标签
            draw_text(t, -200 + a/2, -100 + a/2, f"a²\n(3² = 9)", 12)
            draw_text(t, -200 + a + b/2, -100 + a + b/2, f"b²\n(4² = 16)", 12)
            
        elif step_idx == 1:
            # 步骤2: 显示切割线
            # 先绘制两个正方形
            draw_square(t, -200, -100, a, "cyan", "#e6f7ff")
            draw_square(t, -200 + a, -100 + a, b, "orange", "#fff7e6")
            
            # 绘制切割线
            # 垂直线
            draw_line(t, -200 + a, -100, -200 + a, -100 + a, "red", 2, True)
            # 水平线
            draw_line(t, -200, -100 + a, -200 + a + b, -100 + a, "red", 2, True)
            
            # 添加面积标签
            draw_text(t, -200 + a/2, -100 + a/2, f"a²\n(3² = 9)", 12)
            draw_text(t, -200 + a + b/2, -100 + a + b/2, f"b²\n(4² = 16)", 12)
            
        elif step_idx == 2:
            # 步骤3: 显示切割后的四个部分
            # 部分1: 左上角三角形
            draw_triangle(t, -200, -100, -200 + a, -100, -200, -100 + a, "cyan", "#e6f7ff")
            # 部分2: 右上角四边形
            draw_quadrilateral(t, -200 + a, -100, -200 + a, -100 + a, -200 + a + b, -100 + a, -200 + a, -100 + a + b, "orange", "#fff7e6")
            # 部分3: 左下角四边形
            draw_quadrilateral(t, -200, -100, -200, -100 + a, -200 + a, -100 + a, -200, -100 + a + b, "cyan", "#e6f7ff")
            # 部分4: 右下角三角形
            draw_triangle(t, -200 + a, -100 + a + b, -200 + a + b, -100 + a, -200 + a + b, -100 + a + b, "orange", "#fff7e6")
            
        elif step_idx == 3:
            # 步骤4: 开始拼接 - 移动第一部分（左上角三角形）到右上角
            # 使用插值动画平滑移动第一部分
            for frame in range(animation_frames + 1):
                t.clear()
                # 显示步骤文本
                draw_text(t, 0, 250, f"步骤 {step_idx + 1}: {step_text}", 16, "blue")
                
                # 计算插值比例
                ratio = frame / animation_frames
                
                # 源位置
                src_x1, src_y1 = -200, -100
                src_x2, src_y2 = -200 + a, -100
                src_x3, src_y3 = -200, -100 + a
                
                # 目标位置
                dst_x1, dst_y1 = 100, -150
                dst_x2, dst_y2 = 100 + a, -150
                dst_x3, dst_y3 = 100, -150 + a
                
                # 插值计算当前位置
                curr_x1, curr_y1 = interpolate(src_x1, src_y1, dst_x1, dst_y1, ratio)
                curr_x2, curr_y2 = interpolate(src_x2, src_y2, dst_x2, dst_y2, ratio)
                curr_x3, curr_y3 = interpolate(src_x3, src_y3, dst_x3, dst_y3, ratio)
                
                # 绘制其他三个原始部分
                draw_quadrilateral(t, -200 + a, -100, -200 + a, -100 + a, -200 + a + b, -100 + a, -200 + a, -100 + a + b, "orange", "#fff7e6")
                draw_quadrilateral(t, -200, -100, -200, -100 + a, -200 + a, -100 + a, -200, -100 + a + b, "cyan", "#e6f7ff")
                draw_triangle(t, -200 + a, -100 + a + b, -200 + a + b, -100 + a, -200 + a + b, -100 + a + b, "orange", "#fff7e6")
                
                # 绘制正在移动的第一部分
                if ratio < 1:
                    # 显示移动轨迹
                    draw_line(t, src_x1, src_y1, dst_x1, dst_y1, "blue", 1, True)
                    draw_line(t, src_x2, src_y2, dst_x2, dst_y2, "blue", 1, True)
                    draw_line(t, src_x3, src_y3, dst_x3, dst_y3, "blue", 1, True)
                    draw_text(t, -50, -125, "→", 14, "blue")
                
                # 根据动画进度改变颜色亮度
                color_ratio = 0.5 + ratio * 0.5
                fill_color = "#e6f7ff" if ratio < 0.5 else "#d1ebff"
                draw_triangle(t, curr_x1, curr_y1, curr_x2, curr_y2, curr_x3, curr_y3, "cyan", fill_color)
                
                # 更新屏幕
                screen.update()
                time.sleep(0.05)  # 控制每帧的显示时间
            
        elif step_idx == 4:
            # 步骤5: 继续拼接 - 第一部分到达位置，移动第二部分（右上角四边形）到左下角
            # 使用插值动画平滑移动第二部分
            for frame in range(animation_frames + 1):
                t.clear()
                # 显示步骤文本
                draw_text(t, 0, 250, f"步骤 {step_idx + 1}: {step_text}", 16, "blue")
                
                # 计算插值比例
                ratio = frame / animation_frames
                
                # 源位置
                src_x1, src_y1 = -200 + a, -100
                src_x2, src_y2 = -200 + a, -100 + a
                src_x3, src_y3 = -200 + a + b, -100 + a
                src_x4, src_y4 = -200 + a, -100 + a + b
                
                # 目标位置
                dst_x1, dst_y1 = -200, -150
                dst_x2, dst_y2 = -200, -150 + b
                dst_x3, dst_y3 = -200 + a, -150 + b
                dst_x4, dst_y4 = -200, -150 + a + b
                
                # 插值计算当前位置
                curr_x1, curr_y1 = interpolate(src_x1, src_y1, dst_x1, dst_y1, ratio)
                curr_x2, curr_y2 = interpolate(src_x2, src_y2, dst_x2, dst_y2, ratio)
                curr_x3, curr_y3 = interpolate(src_x3, src_y3, dst_x3, dst_y3, ratio)
                curr_x4, curr_y4 = interpolate(src_x4, src_y4, dst_x4, dst_y4, ratio)
                
                # 第一部分已经到位
                draw_triangle(t, 100, -150, 100 + a, -150, 100, -150 + a, "cyan", "#b3e5fc")
                
                # 显示其他两个原始部分
                draw_quadrilateral(t, -200, -100, -200, -100 + a, -200 + a, -100 + a, -200, -100 + a + b, "cyan", "#e6f7ff")
                draw_triangle(t, -200 + a, -100 + a + b, -200 + a + b, -100 + a, -200 + a + b, -100 + a + b, "orange", "#fff7e6")
                
                # 绘制正在移动的第二部分
                if ratio < 1:
                    # 显示移动轨迹
                    draw_line(t, src_x1, src_y1, dst_x1, dst_y1, "blue", 1, True)
                    draw_line(t, src_x3, src_y3, dst_x3, dst_y3, "blue", 1, True)
                    draw_text(t, -150, -125, "→", 14, "blue")
                
                # 根据动画进度改变颜色亮度
                fill_color = "#fff7e6" if ratio < 0.5 else "#fff0cc"
                draw_quadrilateral(t, curr_x1, curr_y1, curr_x2, curr_y2, curr_x3, curr_y3, curr_x4, curr_y4, "orange", fill_color)
                
                # 更新屏幕
                screen.update()
                time.sleep(0.05)
            
        elif step_idx == 5:
            # 步骤6: 继续拼接 - 第二部分到达位置，移动第三部分（左下角四边形）到左上角
            # 使用插值动画平滑移动第三部分
            for frame in range(animation_frames + 1):
                t.clear()
                # 显示步骤文本
                draw_text(t, 0, 250, f"步骤 {step_idx + 1}: {step_text}", 16, "blue")
                
                # 计算插值比例
                ratio = frame / animation_frames
                
                # 源位置
                src_x1, src_y1 = -200, -100
                src_x2, src_y2 = -200, -100 + a
                src_x3, src_y3 = -200 + a, -100 + a
                src_x4, src_y4 = -200, -100 + a + b
                
                # 目标位置
                dst_x1, dst_y1 = 100, -150 + a
                dst_x2, dst_y2 = 100, -150 + c
                dst_x3, dst_y3 = 100 + a, -150 + c
                dst_x4, dst_y4 = 100 + a, -150 + a
                
                # 插值计算当前位置
                curr_x1, curr_y1 = interpolate(src_x1, src_y1, dst_x1, dst_y1, ratio)
                curr_x2, curr_y2 = interpolate(src_x2, src_y2, dst_x2, dst_y2, ratio)
                curr_x3, curr_y3 = interpolate(src_x3, src_y3, dst_x3, dst_y3, ratio)
                curr_x4, curr_y4 = interpolate(src_x4, src_y4, dst_x4, dst_y4, ratio)
                
                # 前两部分已经到位
                draw_triangle(t, 100, -150, 100 + a, -150, 100, -150 + a, "cyan", "#b3e5fc")
                draw_quadrilateral(t, -200, -150, -200, -150 + b, -200 + a, -150 + b, -200, -150 + a + b, "orange", "#ffecb3")
                
                # 显示最后一个原始部分
                draw_triangle(t, -200 + a, -100 + a + b, -200 + a + b, -100 + a, -200 + a + b, -100 + a + b, "orange", "#fff7e6")
                
                # 绘制正在移动的第三部分
                if ratio < 1:
                    # 显示移动轨迹
                    draw_line(t, src_x1, src_y1, dst_x1, dst_y1, "blue", 1, True)
                    draw_line(t, src_x3, src_y3, dst_x3, dst_y3, "blue", 1, True)
                    draw_text(t, -50, -50, "→", 14, "blue")
                
                # 根据动画进度改变颜色亮度
                fill_color = "#e6f7ff" if ratio < 0.5 else "#d1ebff"
                draw_quadrilateral(t, curr_x1, curr_y1, curr_x2, curr_y2, curr_x3, curr_y3, curr_x4, curr_y4, "cyan", fill_color)
                
                # 更新屏幕
                screen.update()
                time.sleep(0.05)
            
        elif step_idx == 6:
            # 步骤7: 继续拼接 - 第三部分到达位置，移动第四部分（右下角三角形）到右下角
            # 使用插值动画平滑移动第四部分
            for frame in range(animation_frames + 1):
                t.clear()
                # 显示步骤文本
                draw_text(t, 0, 250, f"步骤 {step_idx + 1}: {step_text}", 16, "blue")
                
                # 计算插值比例
                ratio = frame / animation_frames
                
                # 源位置
                src_x1, src_y1 = -200 + a, -100 + a + b
                src_x2, src_y2 = -200 + a + b, -100 + a
                src_x3, src_y3 = -200 + a + b, -100 + a + b
                
                # 目标位置
                dst_x1, dst_y1 = -200 + a, -150
                dst_x2, dst_y2 = -200 + a, -150 + b
                dst_x3, dst_y3 = -200 + c, -150 + b
                
                # 插值计算当前位置
                curr_x1, curr_y1 = interpolate(src_x1, src_y1, dst_x1, dst_y1, ratio)
                curr_x2, curr_y2 = interpolate(src_x2, src_y2, dst_x2, dst_y2, ratio)
                curr_x3, curr_y3 = interpolate(src_x3, src_y3, dst_x3, dst_y3, ratio)
                
                # 前三部分已经到位
                draw_triangle(t, 100, -150, 100 + a, -150, 100, -150 + a, "cyan", "#b3e5fc")
                draw_quadrilateral(t, -200, -150, -200, -150 + b, -200 + a, -150 + b, -200, -150 + a + b, "orange", "#ffecb3")
                draw_quadrilateral(t, 100, -150 + a, 100, -150 + c, 100 + a, -150 + c, 100 + a, -150 + a, "cyan", "#b3e5fc")
                
                # 绘制正在移动的第四部分
                if ratio < 1:
                    # 显示移动轨迹
                    draw_line(t, src_x1, src_y1, dst_x1, dst_y1, "blue", 1, True)
                    draw_line(t, src_x3, src_y3, dst_x3, dst_y3, "blue", 1, True)
                    draw_text(t, -175, -125, "↓", 14, "blue")
                
                # 根据动画进度改变颜色亮度
                fill_color = "#fff7e6" if ratio < 0.5 else "#fff0cc"
                draw_triangle(t, curr_x1, curr_y1, curr_x2, curr_y2, curr_x3, curr_y3, "orange", fill_color)
                
                # 更新屏幕
                screen.update()
                time.sleep(0.05)
            
        elif step_idx == 7:
            # 步骤8: 拼接完成 - 所有部分到达位置，形成c²正方形
            # 使用动画展示c²正方形的形成过程
            t.clear()
            # 显示步骤文本
            draw_text(t, 0, 250, f"步骤 {step_idx + 1}: {step_text}", 16, "blue")
            
            # 初始化所有部分到位
            draw_triangle(t, 100, -150, 100 + a, -150, 100, -150 + a, "cyan", "#b3e5fc")
            draw_quadrilateral(t, -200, -150, -200, -150 + b, -200 + a, -150 + b, -200, -150 + a + b, "orange", "#ffecb3")
            draw_quadrilateral(t, 100, -150 + a, 100, -150 + c, 100 + a, -150 + c, 100 + a, -150 + a, "cyan", "#b3e5fc")
            draw_triangle(t, -200 + a, -150, -200 + a, -150 + b, -200 + c, -150 + b, "orange", "#ffecb3")
            
            # 动画绘制c²正方形的边框，强调形成了边长为c的正方形
            # 先显示边框路径（虚线）
            t.penup()
            t.goto(-200, -150)
            t.pendown()
            t.color("gray")
            t.pensize(1)
            draw_line(t, -200, -150, -200 + c, -150, "gray", 1, True)
            draw_line(t, -200 + c, -150, -200 + c, -150 + c, "gray", 1, True)
            draw_line(t, -200 + c, -150 + c, -200, -150 + c, "gray", 1, True)
            draw_line(t, -200, -150 + c, -200, -150, "gray", 1, True)
            
            # 然后用实线动画绘制边框
            t.penup()
            t.goto(-200, -150)
            t.pendown()
            t.color("red")
            t.pensize(3)
            
            # 动画绘制边框的四条边
            for i in range(4):
                # 每条边分成多段绘制，形成动画效果
                for j in range(20):
                    t.forward(c / 20)
                    screen.update()
                    time.sleep(0.01)
                t.left(90)
            
            # 恢复画笔设置
            t.pensize(1)
            
            # 动画显示c²标签
            for size in range(1, 15):
                # 清除旧标签
                t.penup()
                t.goto(-200 + c/2, -150 + c/2)
                t.color("white")  # 使用背景色覆盖
                t.write(f"c²\n(5² = 25)", align="center", font=("SimHei", size-1, "bold"))
                
                # 绘制新标签，逐步增大
                t.penup()
                t.goto(-200 + c/2, -150 + c/2)
                t.color("red")
                t.write(f"c²\n(5² = 25)", align="center", font=("SimHei", size, "bold"))
                screen.update()
                time.sleep(0.05)
            
        elif step_idx == 8:
            # 步骤9: 验证勾股定理
            # 显示最终的c²正方形
            draw_triangle(t, 100, -150, 100 + a, -150, 100, -150 + a, "cyan", "#b3e5fc")
            draw_quadrilateral(t, -200, -150, -200, -150 + b, -200 + a, -150 + b, -200, -150 + a + b, "orange", "#ffecb3")
            draw_quadrilateral(t, 100, -150 + a, 100, -150 + c, 100 + a, -150 + c, 100 + a, -150 + a, "cyan", "#b3e5fc")
            draw_triangle(t, -200 + a, -150, -200 + a, -150 + b, -200 + c, -150 + b, "orange", "#ffecb3")
            draw_square(t, -200, -150, c, "green", None)
            draw_text(t, -200 + c/2, -150 + c/2, f"c²\n(5² = 25)", 14, "green")
            
            # 最终显示公式（使用加粗效果）
            draw_text(t, 0, 200, f"3² + 4² = 5²", 22, "red")
            draw_text(t, 0, 170, "9 + 16 = 25", 18, "red")
            
        # 对于不需要插值动画的步骤，简单更新屏幕
        if step_idx < 3 or step_idx >= 7:
            # 更新屏幕
            screen.update()
            
            # 等待一段时间
            if step_idx < len(steps) - 1:
                time.sleep(1.0)  # 基础等待时间
            else:
                # 最终步骤停留更长时间
                time.sleep(3)
    
    # 最终说明
    clear_screen(t)
    draw_text(t, 0, 100, "勾股定理动画演示完成！", 20, "blue")
    draw_text(t, 0, 50, "两个小正方形通过切两刀并重新排列，", 16)
    draw_text(t, 0, 20, "完美组合成一个大正方形！", 16)
    draw_text(t, 0, -50, "这证明了：a² + b² = c²", 18, "red")
    draw_text(t, 0, -100, "按任意键退出", 14, "gray")
    screen.update()
    
    # 等待用户按键退出
    screen.exitonclick()

# 运行动画
if __name__ == "__main__":
    animate_pythagoras()