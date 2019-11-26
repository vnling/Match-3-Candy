import random, os
path = os.getcwd()

WIDTH = 500
HEIGHT = 600
NUM_COLS = 10
NUM_ROWS = 10
DIM_COL = 60
DIM_ROW = 60

class Element:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.type = t
    
    #element is randomly loaded from a long image strip similar to the Mario thing
    def display_element(self):
        image(loadImage(path + "/images/actual_candies.png"), self.x, self.y, 50, 50, 50*self.type, 0, (50*self.type+50), 50)
        
class Board(list):
    #2D list initialization, I directly appended the elements as objects
    def __init__(self):
        for i in range(0, NUM_ROWS):
            lst = []
            for j in range(0, NUM_COLS):
                lst.append(Element(j*50, i*50, random.randint(0, 5)))
            self.append(lst)
        
    #loading images for each element    
    def display_board(self):
        image(loadImage(path + "/images/background.png"), 0, 0)
        for i in self:
            for j in i:
                j.display_element()

class Game:
    #I divided minutes and seconds because it makes for a really sexy clock with the 0:00 format, otherwise it would just be numbers
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.mins = 0
        self.secs = 0
        self.selected_r = None
        self.selected_c = None
        #self.selected_tile = None
    
    #the timing here is slightly off from an actual clock, I experimented with frameCount%5 and frameCount%6, both are slightly off
    #the fill/stroke/rect is necessary to wipe the board
    def timer(self):
        if frameCount%6 == 0:
            fill(255, 255, 255)
            stroke(255, 255, 255)
            rect(0, 500, 500, 100)
            if self.secs < 60:
                self.secs += 1
            elif self.secs == 60:
                self.secs = 0
                self.mins += 1
        
    def display_game(self):
        self.board.display_board()
        self.timer()
        #score and time display
        fill(0, 0, 0)
        textSize(15)
        text("Score: " + str(self.score), 420, 530)
        textSize(30)
        #more engineering for the sexy clock format
        if self.secs < 10:
            seconds = '0' + str(self.secs)
            text(str(self.mins) + ":" + seconds, 20, 550)
        elif self.secs >= 10:
            text(str(self.mins) + ":" + str(self.secs), 20, 550)
# CLICKED ALSO NEEDS FIXING            
    def clicked(self):
        c = mouseY // 50
        r = mouseX // 50
        
        stroke(0, 255, 0)
        noFill()
        strokeWeight(5)
        rect(r*50,c*50,50,50)
        self.selected_r = r
        self.selected_c = c
        
        self.selected_tile = self.board[r][c]
        
#SWAP NEEDS FIXING        
    def swap(self,dir):
        if dir == RIGHT:
            temp = self.selected_tile
            target = self.board[self.selected_c][self.selected_r+1]
            self.board[self.selected_c][self.selected_r+1] = self.selected_tile
            self.board[self.selected_c][self.selected_r] = target
            
        if dir == LEFT:
            temp = self.selected_tile
            target = self.board[self.selected_c][self.selected_r-1]
            self.board[self.selected_c][self.selected_r-1] = self.selected_tile
            self.board[self.selected_c][self.selected_r] = target
            
        if dir == UP:
            temp = self.selected_tile
            target = self.board[self.selected_c-1][self.selected_r]
            self.board[self.selected_c-1][self.selected_r] = self.selected_tile
            self.board[self.selected_c][self.selected_r] = target
            
        if dir == DOWN:
            temp = self.selected_tile
            target = self.board[self.selected_c+1][self.selected_r]
            self.board[self.selected_c+1][self.selected_r] = self.selected_tile
            self.board[self.selected_c][self.selected_r] = target
            
        


game = Game()

#I hard coded the dimensions because given we're loading images all over the place any attempt to change them will fuck them up bad anyway
def setup():
    size(500, 600)
    background(255, 255, 255)
    
def draw():
    game.display_game()
    
def mouseClicked():
    game.clicked()

def keyPressed():
    if keyCode == RIGHT:
        game.swap(RIGHT)
    elif keyCode == LEFT:
        game.swap(LEFT)
    elif keyCode == UP:
        game.swap(UP)
    elif keyCode == DOWN:
        game.swap(DOWN)
        
        
