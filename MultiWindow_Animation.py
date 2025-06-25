from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDockWidget, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QSound, QSoundEffect
import sys
import random as rnd
import os

global width, height
width = 50
height = 50

class Ball():
    def __init__(self, x, y, dx, dy, ball_id):
        self.X = x
        self.Y = y
        self.dx = dx
        self.dy = dy
        self.ball_id = ball_id
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile("bounce.wav"))  
        self.sound_effect.setVolume(0.5) 
        self.bounce_count = 0
    
    def bounce(self):
        play_sound = False
        if self.X + self.dx <= 0 or self.X + self.dx >= 1920 - width:
            self.dx *= -1
            play_sound = True
        if self.Y + self.dy <= 0 or self.Y + self.dy >= 1200 - height:
            self.dy *= -1
            play_sound = True
        
        if play_sound:
            self.bounce_count += 1
            self.sound_effect.play()
            
    def move_ball(self):
        self.X += self.dx
        self.Y += self.dy



class MainWindow(QMainWindow):
    def __init__(self, window_id=1):
        super().__init__()
        self.window_id = window_id
        self.setWindowTitle(f"Окно {window_id}")
        self.setGeometry(100 + window_id * 50, 100 + window_id * 50, 400, 300)
        self.animation_order_count = 1
        self.sprites = []
        
    def create_sprite(self, ball_id):
        self.sprites.append(QLabel(self))
        self.sprites[ball_id].setFixedSize(width, height)

    def move_sprite(self, X, Y, ball_id):
        x = X - self.x()
        y = Y - self.y()
        self.sprites[ball_id].move(x, y)
        
    def animation_1(self, dx, dy, ball_id):
        self.animation_order_count += 1
        self.animation_order_count %= 4
        if dx > 0 and dy > 0:
            pixmap = QPixmap(f'Clownfish_{self.animation_order_count}_rd.png')
        if dx < 0 and dy > 0:
            pixmap = QPixmap(f'Clownfish_{self.animation_order_count}_ld.png')
        if dx < 0 and dy < 0:
            pixmap = QPixmap(f'Clownfish_{self.animation_order_count}_lu.png')
        if dx > 0 and dy < 0:
            pixmap = QPixmap(f'Clownfish_{self.animation_order_count}_ru.png')
            
        scaled_pixmap = pixmap.scaled(
            width, 
            height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.sprites[ball_id].setPixmap(scaled_pixmap)

def repulsion(b):
    for ball in balls:
        for ball2 in balls:
            if ball.ball_id != ball2.ball_id:
                if ball.X + ball.dx + width >= ball2.X + ball2.dx and ball.X + ball.dx <= ball2.X + ball2.dx + width and ball.Y + ball.dy - height <= ball2.Y + ball2.dx and ball.Y + ball.dy >= ball2.Y + ball2.dy - height:
                    if ball.dy * ball2.dy < 0:
                        ball.dy *= -1
                        ball2.dy *= -1
                    elif ball.dx * ball2.dx < 0:
                        ball.dx *= -1
                        ball2.dx *= -1
                    elif ball.dx * ball.dy < 0:
                        if (ball.Y - ball2.Y) * ball.dy < 0:
                            ball.dx *= -1
                        else:
                            ball2.dx *= -1
                    elif (ball.Y - ball2.Y) * ball.dy > 0:
                        ball.dx *= -1
                    else:
                        ball2.dx *= -1

class StatsWindow(QDockWidget):
    def __init__(self, ball):
        super().__init__(f"Статистика шара {ball.ball_id}")
        self.ball = ball
        self.stats_widget = QTextEdit()
        self.stats_widget.setReadOnly(True)
        self.setWidget(self.stats_widget)

    def update_status(self, windows):
        speed = (self.ball.dx ** 2 + self.ball.dy ** 2) ** 0.5

        stats_text = [
            f"Скорость: {speed:.1f} px/сек",
            f"Координаты: ({self.ball.X}, {self.ball.Y})",
            f"Отскоков: {self.ball.bounce_count}"
        ]

        self.stats_widget.setPlainText('\n'.join(stats_text))


def update():
    for window in windows:
        for ball in balls:
            window.move_sprite(ball.X, ball.Y, ball.ball_id)
            window.animation_1(ball.dx, ball.dy, ball.ball_id)
    repulsion(balls)
    for ball in balls:
        ball.bounce()
        ball.move_ball()
    for stats_window in stats_windows:
        stats_window.update_status(windows)
    

if __name__ == "__main__":
    app = QApplication([])
    
    windows = [MainWindow(1), MainWindow(2), MainWindow(3)]
    balls = [Ball(rnd.randint(100,1500), rnd.randint(100,900), 
                rnd.choice([1,-1]) * rnd.randint(15,25), 
                rnd.choice([1,-1]) * rnd.randint(15,25), i) for i in range(5)]
    stats_windows = []
    
    for window in windows:
        for ball in balls:
            window.create_sprite(ball.ball_id)
        window.show()

    for ball in balls:
        stats_window = StatsWindow(ball)
        stats_window.setFloating(True)
        stats_window.show()
        stats_windows.append(stats_window)

    
    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(70)  
    
    app.exec_()
