import tkinter as tk
import math
import time

class Cube3D:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()
        
        self.fps_label = tk.Label(master, text="FPS: 0", font=("Helvetica", 12))
        self.fps_label.pack()

        self.control_frame = tk.Frame(master)
        self.control_frame.pack()

        self.start_stop_button = tk.Button(self.control_frame, text="Стоп", command=self.toggle_animation)
        self.start_stop_button.pack(side=tk.LEFT)

        self.speed_label = tk.Label(self.control_frame, text="Скорость:")
        self.speed_label.pack(side=tk.LEFT)

        self.speed_scale = tk.Scale(self.control_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_scale.set(10)  # Начальная скорость
        self.speed_scale.pack(side=tk.LEFT)

        self.angle_x = 0
        self.angle_y = 0
        self.last_time = time.time()
        self.frames = 0
        self.running = True
        self.speed = 0.01  # Начальная скорость вращения

        # Кэшируем координаты вершин куба
        size = 50
        self.points = [
            [-size, -size, -size],
            [size, -size, -size],
            [size, size, -size],
            [-size, size, -size],
            [-size, -size, size],
            [size, -size, size],
            [size, size, size],
            [-size, size, size],
        ]

        # Кэшируем рёбра куба
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        self.faces = [
            (0, 1, 2, 3),  # Задняя грань
            (4, 5, 6, 7),  # Передняя грань
            (0, 1, 5, 4),  # Левая грань
            (1, 2, 6, 5),  # Нижняя грань
            (2, 3, 7, 6),  # Правая грань
            (3, 0, 4, 7)   # Верхняя грань
        ]

        self.animate()

    def draw_line(self, x1, y1, x2, y2, color='black', style='solid'):
        if style == 'dashed':
            self.canvas.create_line(x1, y1, x2, y2, dash=(2, 2), fill=color)  # Пунктирная линия
        else:
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

    def project(self, x, y, z):
        scale = 200 / (200 + z)
        return x * scale + 200, -y * scale + 200

    def draw_cube(self):
        self.canvas.delete("all")

        cos_x = math.cos(self.angle_x)
        sin_x = math.sin(self.angle_x)
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)

        transformed_points = []
        for x, y, z in self.points:
            # Вращение по оси X
            y_rot = y * cos_x - z * sin_x
            z_rot = y * sin_x + z * cos_x
            # Вращение по оси Y
            x_rot = x * cos_y + z_rot * sin_y
            z_rot = -x * sin_y + z_rot * cos_y
            transformed_points.append((x_rot, y_rot, z_rot))

        # Отрисовка теней
        for face in self.faces:
            points = [self.project(transformed_points[i][0], transformed_points[i][1], transformed_points[i][2]) for i in face]
            self.canvas.create_polygon(points, fill='gray', outline='black', stipple='gray50')  # Полупрозрачные тени

        # Отрисовка граней
        for face in self.faces:
            points = [self.project(transformed_points[i][0], transformed_points[i][1], transformed_points[i][2]) for i in face]
            self.canvas.create_polygon(points, fill='lightblue', outline='black')  # Заполнение передних граней

        # Отрисовка рёбер
        for edge in self.edges:
            p1 = self.project(transformed_points[edge[0]][0], transformed_points[edge[0]][1], transformed_points[edge[0]][2])
            p2 = self.project(transformed_points[edge[1]][0], transformed_points[edge[1]][1], transformed_points[edge[1]][2])
            self.draw_line(p1[0], p1[1], p2[0], p2[1], color='black', style='solid')  # Отрисовка рёбер

    def animate(self):
        if self.running:
            self.angle_x += self.speed
            self.angle_y += self.speed
            self.draw_cube()
            self.frames += 1
            current_time = time.time()
            if current_time - self.last_time >= 1:
                self.fps_label.config(text=f"FPS: {self.frames}")
                self.frames = 0
                self.last_time = current_time
        self.canvas.after(16, self.animate)

    def toggle_animation(self):
        self.running = not self.running
        self.start_stop_button.config(text="Старт" if not self.running else "Стоп")

    def update_speed(self, value):
        self.speed = float(value) / 100  # Обновление скорости вращения

if __name__ == "__main__":
    root = tk.Tk()
    cube = Cube3D(root)
    root.mainloop()