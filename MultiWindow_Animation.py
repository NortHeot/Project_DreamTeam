from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QSound, QSoundEffect
import sys
import random as rnd
import os

global width, height
width = 38
height = 38

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
    
    def bounce(self):
        play_sound = False
        if self.X <= 0 or self.X >= 1920 - width*self.ball_id:
            self.dx *= -1
            play_sound = True
        if self.Y <= 0 or self.Y >= 1200 - height*self.ball_id:
            self.dy *= -1
            play_sound = True
        
        if play_sound:
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
        self.sprites[ball_id].setFixedSize(width * int((ball_id+1)**(0.5)), height * int((ball_id+1)**(0.5)))

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
            width * int((ball_id+1)**(0.5)), 
            height * int((ball_id+1)**(0.5)),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.sprites[ball_id].setPixmap(scaled_pixmap)


def update():
    for window in windows:
        for ball in balls:
            window.move_sprite(ball.X, ball.Y, ball.ball_id)
            window.animation_1(ball.dx, ball.dy, ball.ball_id)
    for ball in balls:
        ball.bounce()
        ball.move_ball()

if __name__ == "__main__":
    app = QApplication([])
    
    windows = [MainWindow(1), MainWindow(2), MainWindow(3)]
    balls = [Ball(rnd.randint(100,1500), rnd.randint(100,900), 
                rnd.choice([1,-1]) * rnd.randint(15,25), 
                rnd.choice([1,-1]) * rnd.randint(15,25), i) for i in range(5)]
    
    for window in windows:
        for ball in balls:
            window.create_sprite(ball.ball_id)
        window.show()
    
    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(70)  
    
    app.exec_()
