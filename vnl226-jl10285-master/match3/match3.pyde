import random, os
import time
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
        if self.type != False:
            self.img = loadImage(path + "/images/" + str(self.type) + ".png")
        else:
            self.img = None
        
    #Fixed the pixel part: now they're all separate image files
    def display_element(self):
        image(self.img, self.x, self.y, 50, 50)
        
class Board(list):
    #2D list initialization, I directly appended the elements as objects
    def __init__(self):
        for i in range(0, NUM_ROWS):
            lst = []
            for j in range(0, NUM_COLS):
                lst.append(Element(j*50, i*50, random.randint(1, 6)))
            self.append(lst)
        
    #loading images for each element    
    def display_board(self):
        image(loadImage(path + "/images/background.png"), 0, 0)
        for i in self:
            for j in i:
                if j.type != False:
                    j.display_element()

class Game:
    #I divided minutes and seconds because it makes for a really sexy clock with the 0:00 format, otherwise it would just be numbers
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.mins = 0
        self.secs = 0
        #Added couple of new attirbutes for checking whether a tile is clicked and where the clicked tile is
        self.selected_r = None
        self.selected_c = None
        self.selected_tile = None
        self.is_clicked = False

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
        self.pop_candy()
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
            
        #Continually prints the selected tile rectangle    
        if self.is_clicked == True:
            stroke(0,255,0)
            noFill()
            strokeWeight(5)
            rect(self.selected_r*50,self.selected_c*50,50,50)

            
    #Function for selecting a tile through click    
    def clicked(self):
        c = mouseY // 50
        r = mouseX // 50
        
        stroke(0, 255, 0)
        noFill()
        strokeWeight(5)
        rect(r*50,c*50,50,50)
        self.selected_r = r
        self.selected_c = c
        
        self.is_clicked = True
        self.selected_tile = self.board[self.selected_c][self.selected_r]
               
    # Swap FUnction
    def swap(self,dir):
        if dir == RIGHT:
            if self.is_clicked == True:
            #Swaps the target and selected tile's types
                target_type = self.board[self.selected_c][self.selected_r + 1].type
                self.board[self.selected_c][self.selected_r + 1].type = self.selected_tile.type
                self.board[self.selected_c][self.selected_r].type = target_type
            
            #Swaps the target and selected tile's coordinates
                target_x = self.board[self.selected_c][self.selected_r + 1].x 
                target_y = self.board[self.selected_c][self.selected_r + 1].y
                self.board[self.selected_c][self.selected_r + 1].x = self.selected_tile.x
                self.board[self.selected_c][self.selected_r + 1].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y

                self.selected_tile = None
                self.is_clicked = False
            
        if dir == LEFT:    
            if self.is_clicked == True:
                target_type = self.board[self.selected_c][self.selected_r - 1].type
                self.board[self.selected_c][self.selected_r - 1].type = self.selected_tile.type
                self.board[self.selected_c][self.selected_r].type = target_type
            
            #Swaps the target and selected tile's coordinates
                target_x = self.board[self.selected_c][self.selected_r - 1].x 
                target_y = self.board[self.selected_c][self.selected_r - 1].y
                self.board[self.selected_c][self.selected_r - 1].x = self.selected_tile.x
                self.board[self.selected_c][self.selected_r - 1].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y          
            
            
                self.selected_tile = None
                self.is_clicked = False
            
        if dir == UP:
            if self.is_clicked == True:
                target_type = self.board[self.selected_c - 1][self.selected_r].type
                self.board[self.selected_c - 1][self.selected_r].type = self.selected_tile.type
                self.board[self.selected_c][self.selected_r].type = target_type
            
                target_x = self.board[self.selected_c - 1][self.selected_r].x 
                target_y = self.board[self.selected_c - 1][self.selected_r].y
                self.board[self.selected_c - 1][self.selected_r].x = self.selected_tile.x
                self.board[self.selected_c - 1][self.selected_r].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y
            
                self.selected_tile = None
                self.is_clicked = False
            
        if dir == DOWN:        
            if self.is_clicked == True:
                target_type = self.board[self.selected_c + 1][self.selected_r].type
                self.board[self.selected_c + 1][self.selected_r].type = self.selected_tile.type
                self.board[self.selected_c][self.selected_r].type = target_type
            
                target_x = self.board[self.selected_c + 1][self.selected_r].x 
                target_y = self.board[self.selected_c + 1][self.selected_r].y
                self.board[self.selected_c + 1][self.selected_r].x = self.selected_tile.x
                self.board[self.selected_c + 1][self.selected_r].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y
           
                self.selected_tile = None
                self.is_clicked = False
    
    
    #Pop function (implementation of word search)        
    def pop_candy(self):
        directions = [[0,-1],[1,0],[0,1],[-1,0]]
            
        #Goes through every section of the board    
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                for dir in directions:
                    cnt = 0
                    if self.board[col][row].type != False:
                        type = self.board[col][row].type
                        
                        #Searches the surrounding tiles to see if they are the same type
                        for i in range(3):
                            r = row + dir[0]*i
                            c = col + dir[1]*i
                            if r < NUM_ROWS and c < NUM_COLS:
                                if self.board[c][r].type != False:
                                    
                                    if type == self.board[c][r].type:
                                        cnt += 1
                                        
                        #Okay so here's the incomplete part: I just replaced the boards with " " so the next part is moving all the above tiles to where the " " is one by one which would be the falling
                            if cnt == 3:
                                for j in range(3):
                                    nr = row + dir[0]*j
                                    nc = col + dir[1]*j
                                    self.board[nc][nr].type = False
                    else:
                        pass

            
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
        
        
