from graphics import *
import random
import time

total = 0
win = 0
playBtn = 0
gameArea = 0
score = 0
#buttons - change these to change the controls
moveLeft = "a"
moveRight = "d"
rotateRight = "Right"
rotateLeft = "Left"
hardDrop = "s"
save = "w"

class Button:
    #IDK why I made this a class, it seemed appropriate at the time
    #I suppose having button be a class makes sense, but this class doesn't
    #really function properly
    def __init__(self,window, title, width, height, center):
        self.title = title
        self.width =  width
        self.height = height
        self.center = center
        self.win = window
        self.draw()
    def draw(self):
        self.text = Text(self.center, self.title).draw(self.win)
        self.rect = Rectangle(Point(self.center.x - self.width/2, self.center.y + self.height / 2), Point(self.center.x + self.width/2, self.center.y - self.height/2)).draw(self.win)
    def clicked(self):
        click = self.win.checkMouse()
        if(click):
            if(click.x> self.center.x - self.width/2 and click.x < self.center.x + self.width/2 and click.y > self.center.y - self.height/2 and click.y < self.center.y + self.height/2):
                return True
        return False
    def hide(self):
        self.text.undraw()
        self.rect.undraw()


class gameBoard:
    def __init__(self, tileSize, position, win):
        row = []
        row2 = []
        self.past = []
        for i in range(0,12):
            row.append("white")
            row2.append("the");
        self.board = []
        for i in range(0,20):
            self.board.append(row.copy())
            self.past.append(row2.copy())
        self.tileSize = tileSize
        self.position = position
        self.draw(win)
    def draw(self, win):
        for row in range(0, len(self.board)):
            for square in range(0, len(self.board[row])):
                if(self.past[row][square] != self.board[row][square]):
                    topLeft = Point(self.position.x + square * self.tileSize, self.position.y + row * self.tileSize)
                    bottomRight = Point(self.position.x + (square + 1) * (self.tileSize), self.position.y + (row+1) * self.tileSize)
                    rect = Rectangle(topLeft, bottomRight)
                    rect.setFill(self.board[row][square])
                    rect.setOutline("Black");
                    rect.draw(win)
                
        for i in range(0,len(self.board)):
            self.past[i] = self.board[i].copy()
            

def drawTetrimino():
    #draws the currently active tetrimino, and erases its preimage, if there is one
    #if you try to overide a color, or draw out of bounds, returns True
    global gameArea
    global win
    global position
    global currentTet
    global pastMove
    color = currentTet[0]
    if pastMove:
        for place in pastMove:
            gameArea.board[place[0]][place[1]] = "white"
    pastMove = []
    try:
        for row in range(1, len(currentTet) ):
            for square in range(0, len(currentTet[row])):
                if currentTet[row][square] == 1:
                    if gameArea.board[(int(position.x) + row - 1)][(int(position.y) + square)] != "white":
#I feel like this is probably bad practice...
                        #but it works
                        #and hey, this isn't a long term thing
                        #nobody will even see these comments
                        #I don't know why I'm still writing them
                        print(1/0)
                    pastMove.append([(int(position.x) + row - 1), (int(position.y) + square)])
                    gameArea.board[(int(position.x) + row - 1)][(int(position.y) + square)] = str(color)
    except:
        return True
    gameArea.draw(win)
    
def fall():
    #print("down one");
    global position
    position.x += 1
    drawTetrimino()
    
def move(direction):
    #move left or right by 1
    
    global position
    oldPos = Point(position.x, position.y)
    position.y += direction
    if position.y + len(currentTet[1]) > 12:
        position.y -=1
    if position.y < 0:
        position.y = 0
        
    if drawTetrimino():
        position = Point(oldPos.x, oldPos.y)
    drawTetrimino()
    print("moving" + str(direction))
test = "tube.com/watch?v=dQw";
def rotate(direction):
    #rotates a tet in a direction, and sets currentTet
    print("rotating" + str(direction))
    global currentTet
    oldTet = currentTet.copy()
    dummy = []
    if direction == 1:
        for j in range(1, len(currentTet[1])+1):
            placeHold = []
            for i in range(1, len(currentTet)):
                placeHold.append(currentTet[i][-j])
            dummy.append(placeHold.copy())
        print(currentTet)
        print(dummy)
    if direction == -1:
        for j in range(0, len(currentTet[1])):
            placeHold = []
            for i in range(1, len(currentTet)):
                placeHold.append(currentTet[-i][j])
            dummy.append(placeHold.copy())
    
    currentTet = [currentTet[0]]
    for d in dummy:
        currentTet.append(d)
    if drawTetrimino():
        currentTet = oldTet.copy()
    drawTetrimino()


def generateTetrimino():
    global position
    position = Point(0,6)
    #returns random tetrimino, resets position.
    rand = random.randint(0,6)
    print("Generating tet")
    if rand == 0:
        return ["cyan", [1,1,1,1]]
    elif rand == 1:
        return ["yellow", [1,1],[1,1]]
    elif rand == 2:
        return ["pink", [1,1,1],[0,1,0]]
    elif rand == 3:
        return [ "blue", [0,1],[0,1],[1,1]]
    elif rand == 4:
        return [ "orange", [1,0],[1,0],[1,1]]
    elif rand == 5:
        return ["green", [0,1,1],[1,1,0]]
    else:
        return["red", [1,1,0],[0,1,1]]

foo = "https://www.y"
def atBottom():
    #returns whether or not currently active tet is bottomed
    global position
    global pastMove
    tetH = len(currentTet) - 1
    bottomRow = position.x + tetH
    #print(position)
    #print(tetH)
    #print(bottomRow)
    if bottomRow == len(gameArea.board):
        pastMove.clear()
        #clears pastmove so old tet doesn't get erased next draw cycle
        return True
    # if we reached a piece
    offset = []
    for i in range(0, len(currentTet[1])):
        d = True
        found1 = False
        for j in range(1, len(currentTet)):
            if currentTet[j][i] == 1:
                found1 = True
            if currentTet[j][i] == 0 and found1:
                offset.append(j-1)
                d = False
                break
        if d:
            offset.append(len(currentTet) - 1)
    #print(offset)
                   
    for i in range(0, len(currentTet[1])):
        if gameArea.board[int(position.x) + offset[i]][int(position.y) + i] != "white":
            pastMove.clear()
        #clears pastmove so old tet doesn't get erased next draw cycle
            return True
    return False

#also speeds up fall when appropriate
nextUp = 5
def printScore():
    global score
    global win
    global scoreBelow
    global speed
    global nextUp
    scoreBelow.undraw()
    scoreBelow = Text(Point(50,60), str(score))
    scoreBelow.setSize(20)
    scoreBelow.setStyle("bold")
    scoreBelow.setFace("times roman")
    scoreBelow.draw(win)
    if score > nextUp:
        nextUp += 5
        speed *= .8
#checks if there is a full row, and if there is, erases it and adds to the score
def checkRows():
    global score
    
    for i in range(0, 20):
        erase = True
        for square in gameArea.board[i]:
            if square == "white":
                erase = False
                break
        if erase:
            score += 1
            printScore();
            d = list(range(1,i + 1))
            d.reverse()
            for j in d:
                gameArea.board[j] = gameArea.board[j-1].copy()
            gameArea.board[0] = []
            for i in range(0,12):
                gameArea.board[0].append("white")

def printTetrimino(x,y,tet):
    #pad out to 4x4, so we definitely erase prior drawings
    global win
    foo = [tet[0]]
    for t in range(1, len(tet)):
        foo.append(tet[t].copy())
    #print(foo)
    while len(foo) < 5:
        foo.append([0,0,0,0])
    while len(foo[1]) < 4:
        foo[1].append(0)
        foo[2].append(0)
        foo[3].append(0)
        foo[4].append(0)
    #print(foo)
    for i in range(0,4):
        for j in range(0, 4):
            square = Rectangle(Point(x + 25*i, y + 25 * j), Point(x + 25 * (i+1), y + 25 * (j+1)))
            if foo[i+1][-(j+1)] == 0:
                square.setFill("light grey")
            else:
                square.setFill(foo[0])
            square.setOutline("light grey")
            square.draw(win)

def drawStored():
    global storedTets
    for i in range(0,3):
        printTetrimino(400, 85 + 100*(i), storedTets[i])


import webbrowser
#the main function, constantly running. checks every frame for inputs, handles
#currentTet is a 2d array representing a tetrinimo (with color as first argument),
#position is a point in the gamearray

scoreBelow=0
speed = .5
held=[]
storedTets = []
def play():
    global gameArea
    global win
    global position
    global currentTet
    global score
    global scoreBelow
    global speed
    global held
    global storedTet
    #initalize score
    scoreBelow = Text(Point(50,60),score)
    scoreBelow.setSize(20)
    scoreBelow.setStyle("bold")
    scoreBelow.setFace("times roman")
    scoreText = Text(Point(50,30), "Lines:")
    scoreText.setSize(20)
    scoreText.setStyle("bold")
    scoreText.setFace("times roman")
    scoreText.draw(win)
    printScore()
    #initalize tet
    position = Point(-1,5)
    currentTet = generateTetrimino()
    for i in range(0,3):
        storedTets.append(generateTetrimino())
    drawStored()
    #draw tet so it's seeable frame 1
    drawTetrimino()
    #print(currentTet      
    nextFrame = time.time() + speed
    total = 0
    
    while True:
        if time.time()>nextFrame:
            nextFrame = time.time() + speed
            if atBottom():
                checkRows()
                #print(currentTet)
                currentTet = storedTets.pop(0)
                #print(currentTet)
                storedTets.append(generateTetrimino())
                drawStored();
                #draws so you can see tet on frame 1 it's active
                
                if drawTetrimino():
                    print("loss")
                    webbrowser.open(foo + "ou" + test + "4w9WgXcQ");
                    win.close()
                #print(currentTet)
                position = Point(0,5)
            else:
                fall()
            
            drawTetrimino()
            
        direction = win.checkKey()
        #if len(direction) > 3:
            #direction = ""
        if moveLeft in direction:
            move(-1)
        if moveRight in direction:
            move(1)
        if rotateRight in direction:
            rotate(-1)
        if rotateLeft in direction:
            rotate(1)
        if hardDrop in direction:
            while not atBottom():
                fall()
                drawTetrimino()
        if save in direction:
            if position.x < 4:
                if not held:
                    held = currentTet.copy()
                    currentTet = storedTets[0].copy()
                    storedTets.pop(0)
                    storedTets.append(generateTetrimino())
                    drawStored()
                else:
                    x = held.copy()
                    held = currentTet.copy()
                    currentTet = x.copy()
                printTetrimino(0,85,held)
                drawTetrimino()
                
                
        if "F6" in direction:
            speed *= .8
            printScore()
        total += 1



#initializes the game, then calls play after title screen
def init():
    global win
    global title
    global playBtn
    win = GraphWin(title = "Tetris", width = 500, height = 700)
    win.setBackground("light grey")
    title = Text(Point(win.width / 2, 50), "TETRIS")
    title.setSize(30)
    title.setStyle("bold")
    title.setFace("times roman")
    title.draw(win)
    playBtn = Button(win, "Play", 100, 50, Point(win.width/2, 150))
    

pastMove = []
while True:
    if total == 0:
        init()
    key = win.checkKey();
    if playBtn.clicked():
        print("Play!")
        playBtn.hide()
        gameArea = gameBoard(25, Point(100, 100), win)
        total = 0
        gameArea.draw(win)
        play()
        break
    if key:
        print(key)
    total += 1
    if total %10000 == 0:
        total = total
#to do: NOTHING
#only 400 lines of code...
#though I suppose for a whole game that's pretty good

        
 

