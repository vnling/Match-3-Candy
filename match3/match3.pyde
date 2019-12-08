add_library('minim')
import random, os
import time
path = os.getcwd()
player = Minim(this)

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
        self.img = loadImage(path + "/images/" + str(self.type) + ".png")

    #Fixed the pixel part: now they're all separate image files
    def display_element(self):
        image(self.img, self.x, self.y, 50, 50)

    def update_element(self):
        self.img = loadImage(path + "/images/" + str(self.type) + ".png")
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
                j.display_element()

    def update(self):
        for i in self:
            for j in i:
                j.update_element()


class Game:
    #I divided minutes and seconds because it makes for a really sexy clock with the 0:00 format, otherwise it would just be numbers
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.required_score = 10
        self.secs = 59
        #Added couple of new attirbutes for checking whether a tile is clicked and where the clicked tile is
        self.selected_r = None
        self.selected_c = None
        self.selected_tile = None
        self.is_clicked = 0
        self.lost = False
        
        # Music Part
        self.background_music = player.loadFile(path + "/sounds/background.mp3")
        self.background_music.rewind()
        self.background_music.play()

    #the timing here is slightly off from an actual clock
    #the fill/stroke/rect is necessary to wipe the board
    def timer(self):
        if frameCount%2 == 0:
            fill(255, 255, 255)
            stroke(255, 255, 255)
            rect(0, 500, 500, 100)
            self.secs -= 1

    def display_game(self):
        self.board.display_board()
        self.timer()
        if self.secs == 0:
            self.game_over_check()
        if self.lost == True:
            fill(255, 255, 255)
            stroke(255, 255, 255)
            rect(0, 0, 500, 600)
            fill(0, 0, 0)
            textSize(50)
            text("You lost!", 150, 250)
            textSize(20)
            text("You did not make the required number \nof matches :(", 60, 300)
            self.background_music.rewind()
            return
        self.pop_candy()
        self.gravity()
        self.make_candy()
        self.board.update()
        #score and time display
        fill(0, 0, 0)
        textSize(15)
        text("Score: " + str(self.score), 420, 530)
        text("Goal: " + str(self.required_score), 420, 560)
        textSize(30)
        #more engineering for the sexy clock format
        if self.secs < 10:
            seconds = '0' + str(self.secs)
            text("0:" + seconds, 20, 550)
        elif self.secs >= 10:
            text("0:" + str(self.secs), 20, 550)

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

    # Swap Function
    def swap(self,dir):
        if dir == RIGHT:
            if self.is_clicked == True:
            #Swaps the target and selected tile
                target_x = self.board[self.selected_c][self.selected_r + 1].x 
                target_y = self.board[self.selected_c][self.selected_r + 1].y
                self.board[self.selected_c][self.selected_r + 1].x = self.selected_tile.x
                self.board[self.selected_c][self.selected_r + 1].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y          
                temp = self.board[self.selected_c][self.selected_r + 1]
                self.board[self.selected_c][self.selected_r + 1] = self.board[self.selected_c][self.selected_r]
                self.board[self.selected_c][self.selected_r] = temp

                self.board.update()

                self.selected_tile = None
                self.is_clicked = 0

        if dir == LEFT:    
            if self.is_clicked == True:
                target_x = self.board[self.selected_c][self.selected_r - 1].x 
                target_y = self.board[self.selected_c][self.selected_r - 1].y
                self.board[self.selected_c][self.selected_r - 1].x = self.selected_tile.x
                self.board[self.selected_c][self.selected_r - 1].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y          
                temp = self.board[self.selected_c][self.selected_r - 1]
                self.board[self.selected_c][self.selected_r - 1] = self.board[self.selected_c][self.selected_r]
                self.board[self.selected_c][self.selected_r] = temp

                self.board.update()

                self.selected_tile = None
                self.is_clicked = 0

        if dir == UP:
            if self.is_clicked == True:
                target_x = self.board[self.selected_c - 1][self.selected_r].x 
                target_y = self.board[self.selected_c - 1][self.selected_r].y
                self.board[self.selected_c - 1][self.selected_r].x = self.selected_tile.x
                self.board[self.selected_c - 1][self.selected_r].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y          
                temp = self.board[self.selected_c - 1][self.selected_r]
                self.board[self.selected_c - 1][self.selected_r] = self.board[self.selected_c][self.selected_r]
                self.board[self.selected_c][self.selected_r] = temp

                self.board.update()

                self.selected_tile = None
                self.is_clicked = 0

        if dir == DOWN:        
            if self.is_clicked == True:
                target_x = self.board[self.selected_c + 1][self.selected_r].x 
                target_y = self.board[self.selected_c + 1][self.selected_r].y
                self.board[self.selected_c + 1][self.selected_r].x = self.selected_tile.x
                self.board[self.selected_c + 1][self.selected_r].y = self.selected_tile.y
                self.board[self.selected_c][self.selected_r].x = target_x
                self.board[self.selected_c][self.selected_r].y = target_y          
                temp = self.board[self.selected_c + 1][self.selected_r]
                self.board[self.selected_c + 1][self.selected_r] = self.board[self.selected_c][self.selected_r]
                self.board[self.selected_c][self.selected_r] = temp

                self.board.update()

                self.selected_tile = None
                self.is_clicked = 0


    #Pop function (implementation of word search)        
    def pop_candy(self):
        directions = [[0,-1],[1,0],[0,1],[-1,0]]

        #Goes through every section of the board    
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                for dir in directions:
                    cnt = 0
                    if self.board[col][row].type != 0:
                        type = self.board[col][row].type

                        #Searches the surrounding tiles to see if they are the same type
                        for i in range(3):
                            r = row + dir[0]*i
                            c = col + dir[1]*i
                            if r < NUM_ROWS and r >= 0 and c < NUM_COLS and c >= 0:
                                if self.board[c][r].type != 0:
                                    if type == self.board[c][r].type:
                                        cnt += 1

                        #Okay so here's the incomplete part: I just replaced the boards with 0 so the next part is moving all the above tiles to where the 0 is one by one which would be the falling
                            if cnt == 3:
                                for j in range(3):
                                    nr = row + dir[0]*j
                                    nc = col + dir[1]*j
                                    self.board[nc][nr].type = 0
                                self.score += 1

                    else:
                        pass

    #Gravity function
    def gravity(self):
        for r in range(NUM_ROWS - 1, -1, -1):
            for c in range(NUM_COLS):
                if self.board[r][c].type == 0:
                    self.board[r][c].type = self.board[r - 1][c].type
                    self.board[r - 1][c].type = 0
    
    #candy generation function
    def make_candy(self):
        for r in range(NUM_ROWS - 1, -1, -1):
            for c in range(NUM_COLS):
                if self.board[r][c].type == 0:
                    self.board[r][c].type = random.randint(1,6)

    #game win/lose checking function
    def game_over_check(self):
        if self.score >= self.required_score:
            self.score = 0
            self.required_score += 5
            self.secs = 59
        elif self.score < self.required_score:
            self.lost = True
        
game = Game()

#I hard coded the dimensions because given we're loading images all over the place any attempt to change them will mess them up bad anyway
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
