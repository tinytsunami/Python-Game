import tkinter as tk
import random as rand

WINDOW_TITLE = "Python Connect 6"
CONNECT      = 6
MAP_WIDTH    = 19
MAP_HEIGHT   = 19
BLOCK_SIZE   = 24
BORDER_SIZE  = 15
TEXT_SIZE    = 23
WIDTH        = (MAP_WIDTH - 1) * BLOCK_SIZE + BORDER_SIZE * 2
HEIGHT       = (MAP_HEIGHT - 1) * BLOCK_SIZE + BORDER_SIZE * 2 + TEXT_SIZE
BG_COLOR     = "#AA8866"
TXT_COLOR    = "#FFFFFF"
TXT_BG_COLOR = "#000000"
WHITE_COLOR  = "#FFFFFF"
BLACK_COLOR  = "#000000"

chessMap = []
blackFlag = True
endding = False
w = [1, 1]
step = 0.8
computer = True

#tk initialize
root = tk.Tk()
root.title(WINDOW_TITLE)
root.maxsize(width=WIDTH, height=HEIGHT)
root.minsize(width=WIDTH, height=HEIGHT)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#canvas initialize
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.grid(column=0, row=0)

#initialize
def drawInit():
    global blackFlag, chessMap, endding
    blackFlag = True
    endding = False
    chessMap = [[0 for i in range(0, MAP_HEIGHT)] for i in range(0, MAP_WIDTH)]
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG_COLOR)
    canvas.create_rectangle(0, (HEIGHT - TEXT_SIZE), WIDTH, HEIGHT, fill=TXT_BG_COLOR)
    for i in range(0, MAP_HEIGHT):
        canvas.create_line(BORDER_SIZE, BORDER_SIZE + i * BLOCK_SIZE, WIDTH - BORDER_SIZE, BORDER_SIZE + i * BLOCK_SIZE)
    for i in range(0, MAP_WIDTH):
        canvas.create_line(BORDER_SIZE + i * BLOCK_SIZE, BORDER_SIZE, BORDER_SIZE + i * BLOCK_SIZE, HEIGHT - BORDER_SIZE - TEXT_SIZE)
    #computer first
    if computer:
        chess(rand.randint(0, MAP_WIDTH - 1), rand.randint(0, MAP_WIDTH - 1))
    pass
#show text
def drawText(message):
    canvas.create_rectangle(0, (HEIGHT - TEXT_SIZE), WIDTH, HEIGHT, fill=TXT_BG_COLOR)
    canvas.create_text(5, HEIGHT - 5, fill=TXT_COLOR, text=message, anchor=tk.SW)
    pass
#player add
def control(event):
    global endding
    if endding == True:
        drawInit()
        endding = False
    else:
        x = int((event.x - BORDER_SIZE) / BLOCK_SIZE + 0.5)
        y = int((event.y - BORDER_SIZE) / BLOCK_SIZE + 0.5)
        drawText('%s : add at (%s, %s)' % ("Black" if blackFlag == True else "White", x + 1, y + 1))
        r = chess(x, y)
        #computer calc
        if r == 0:
            c = search(1)
            p = search(2)
            if c[2] > p[2]:
                chess(c[0], c[1])
            else:
                chess(p[0], p[1])
            pass
    pass
#Add chess
def chess(x, y):
    global blackFlag, endding, computer
    if chessMap[x][y] == 0:
        chessMap[x][y] = 1 if blackFlag == True else 2
        px = BORDER_SIZE + x * BLOCK_SIZE - BLOCK_SIZE / 2
        py = BORDER_SIZE + y * BLOCK_SIZE - BLOCK_SIZE / 2
        color = BLACK_COLOR if blackFlag == True else WHITE_COLOR
        canvas.create_arc(px, py, px + BLOCK_SIZE, py + BLOCK_SIZE, start=0, extent=359, style=tk.CHORD, fill=color)
        flag = 1 if blackFlag == True else 2
        if result(x, y, flag) >= CONNECT:
            drawText("%s win! Please press key to replay." % ("Black" if blackFlag else "White"))
            endding = True
            computer = (not computer)
        blackFlag = (not blackFlag)
        return 0
    else:
        drawText("This location was already has chess.")
        return 1
    pass

#game result
def result(x, y, flag):
    assess = [1, 1, 1, 1]
    posiArr = [i for i in range(1, CONNECT)]
    negaArr = [-1 * i for i in range(1, CONNECT)]
    zeroArr = [0 for i in range(1, CONNECT)]
    #row
    assess[0] += check(x, y, posiArr, zeroArr, flag)
    assess[0] += check(x, y, negaArr, zeroArr, flag)
    #column
    assess[1] += check(x, y, zeroArr, posiArr, flag)
    assess[1] += check(x, y, zeroArr, negaArr, flag)
    #upper left & under right
    assess[2] += check(x, y, negaArr, negaArr, flag)
    assess[2] += check(x, y, posiArr, posiArr, flag)
    #upper right & under keft
    assess[3] += check(x, y, negaArr, posiArr, flag)
    assess[3] += check(x, y, posiArr, negaArr, flag)
    return findMax(assess)
    pass
def check(x, y, xRange, yRange, flag):
    count = 0
    for i in range(0, (CONNECT - 1)):
        nx = x + xRange[i]
        ny = y + yRange[i]
        if nx >= MAP_WIDTH or ny >= MAP_HEIGHT or nx < 0 or ny < 0:
            continue
        if chessMap[nx][ny] == flag:
            count += 1
        else:
            break
        pass
    return count
    pass
def findMax(arr):
    m = 0
    for i in arr:
        if i > m:
            m = i
    return m

def search(flag):
    score = [0, 0, 0]
    s = 0
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            s = result(x, y, flag)
            if score[2] < s and chessMap[x][y] == 0:
                score[0] = x
                score[1] = y 
                score[2] = s
    return score
    pass

#show initialize
drawInit()
drawText("Initialize.")

#set event
canvas.focus_set()
canvas.bind("<Button-1>", control)
root.mainloop()