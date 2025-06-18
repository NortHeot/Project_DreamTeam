from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QGraphicsPixmapItem
import sys
global width, height
width = 38
height = 38
class Ball():
    def __init__(self, x, y, dx, dy):
        self.X = x
        self.Y = y
        self.dx = dx
        self.dy = dy
    
    def bounce(self):
        if self.X <= 0 or self.X >= 1920 - width:
            self.dx *= -1
        if self.Y <= 0 or self.Y >= 1200 - height:
            self.dy *= -1
            
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

        self.sprite = QLabel(self)
        self.sprite.setFixedSize(width * 2, height * 2)

    def move_sprite(self,X,Y):
        x = X - self.x()
        y = Y - self.y()
        self.sprite.move(x, y)
        
    def animation_1(self,dx,dy):
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
                width * 2, 
                height * 2,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        self.sprite.setPixmap(scaled_pixmap)
        
def update():
    for window in windows:
        window.move_sprite(ball.X, ball.Y)
        window.animation_1(ball.dx, ball.dy)
    ball.bounce()
    ball.move_ball()
    

app = QApplication([])
    
windows = [MainWindow(1), MainWindow(2), MainWindow(3)]
ball = Ball(100,100,20,20)
for window in windows:
    window.show()
    
timer = QTimer()
timer.timeout.connect(update)
timer.start(100)  
    
app.exec_()
