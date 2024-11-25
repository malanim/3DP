import tkinter as tk
import math
import time

class Cube3D:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()
        self.fps_label = tk.Label(master, text="FPS: 0", font=("Helvetica", 12))
        self.fps_label.pack()

        self.angle_x = 0
        self.angle_y = 0
        self.last_time = time.time()
        self.frames = 0
        self.animate()

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2)

    def draw_cube(self):
        self.canvas.delete("all")

        size = 50
        points = [
            [-size, -size, -size],
            [size, -size, -size],
            [size, size, -size],
            [-size, size, -size],
            [-size, -size, size],
            [size, -size, size],
            [size, size, size],
            [-size, size, size],
        ]

        transformed_points = []
        for point in points:
            x, y, z = point
            # Вращение по оси X
            y_rot = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)
            z_rot = y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
            y = y_rot
            z = z_rot
            
            # Вращение по оси Y
            x_rot = x * math.cos(self.angle_y) + z * math.sin(self.angle_y)
            z_rot = -x * math.sin(self.angle_y) + z * math.cos(self.angle_y)
            x = x_rot
            z = z_rot
            
            # Проекция на 2D
            scale = 200 / (200 + z)
            x_proj = x * scale + 200
            y_proj = -y * scale + 200
            transformed_points.append((x_proj, y_proj))

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        for edge in edges:
            x1, y1 = transformed_points[edge[0]]
            x2, y2 = transformed_points[edge[1]]
            self.draw_line(x1, y1, x2, y2)

    def animate(self):
        self.angle_x += 0.01
        self.angle_y += 0.01
        self.draw_cube()

        self.frames += 1
        current_time = time.time()
        if current_time - self.last_time >= 1:
            self.fps_label.config(text=f"FPS: {self.frames}")
            self.frames = 0
            self.last_time = current_time

        self.canvas.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = Cube3D(root)
    root.mainloop()