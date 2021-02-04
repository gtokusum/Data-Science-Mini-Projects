'''
a cell can be dead or alive.
an alive cell will die in the next generation if less than 2 or more than 3
of its neighbors are alive then the cell will die.
if there are 2 or 3 alive cells in the neighbor the cell will live
if a dead cell has 3 alive neighbors that cell becomes alive. 
'''
import pygame

WIDTH = 1200
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Cellular Automata")


RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)


class Spot:

    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def is_block(self):
        return self.color == BLACK

    def get_pos(self):
        return self.row,self.col

    def reset(self):
        self.color = WHITE
    
    def make_block(self):
        self.color = BLACK
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_block() and grid[self.row][self.col].is_block():#down
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and grid[self.row - 1][self.col].is_block() and grid[self.row][self.col].is_block():#UP
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows -1 and grid[self.row ][self.col + 1].is_block() and grid[self.row][self.col].is_block():#RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and grid[self.row][self.col - 1].is_block() and grid[self.row][self.col].is_block():#LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        #DOWN RIGHT
        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and grid[self.row + 1][self.col + 1].is_block() and grid[self.row][self.col].is_block():
            self.neighbors.append(grid[self.row + 1][self.col + 1])
        
        #DOWN LEFT
        if self.row < self.total_rows - 1 and self.col > 0 and grid[self.row + 1][self.col - 1].is_block() and grid[self.row][self.col].is_block():
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        #UP RIGHT
        if self.row > 0 and self.col < self.total_rows - 1 and grid[self.row - 1][self.col + 1].is_block() and grid[self.row][self.col].is_block():
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        #UP LEFT
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col -1].is_block() and grid[self.row][self.col].is_block():
            self.neighbors.append(grid[self.row - 1][self.col - 1])
        
        self.not_neighbors = []

        #DOWN
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_block() and not grid[self.row][self.col].is_block():
            self.not_neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and grid[self.row - 1][self.col].is_block() and not grid[self.row][self.col].is_block():#UP
            self.not_neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows -1 and grid[self.row ][self.col + 1].is_block() and not grid[self.row][self.col].is_block():#RIGHT
            self.not_neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and  grid[self.row][self.col - 1].is_block() and not grid[self.row][self.col].is_block():#LEFT
            self.not_neighbors.append(grid[self.row][self.col - 1])

        #DOWN RIGHT
        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and grid[self.row + 1][self.col + 1].is_block() and not grid[self.row][self.col].is_block():
            self.not_neighbors.append(grid[self.row + 1][self.col + 1])
        
        #DOWN LEFT
        if self.row < self.total_rows - 1 and self.col > 0 and grid[self.row + 1][self.col - 1].is_block() and not grid[self.row][self.col].is_block():
            self.not_neighbors.append(grid[self.row + 1][self.col - 1])

        #UP RIGHT
        if self.row > 0 and self.col < self.total_rows - 1 and grid[self.row - 1][self.col + 1].is_block() and not grid[self.row][self.col].is_block():
            self.not_neighbors.append(grid[self.row - 1][self.col + 1])

        #UP LEFT
        if self.row > 0 and self.col > 0 and grid[self.row - 1][self.col -1].is_block() and not grid[self.row][self.col].is_block():
            self.not_neighbors.append(grid[self.row - 1][self.col - 1])

    

    


def make_grid(rows,width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)

    return grid

def draw_grid(win,rows,width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
    for j in range(rows):
        pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))
    
def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width//rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row,col


def game(draw,grid):
    gameStart = True
    # while gameStart:
    # for event in pygame.event.get():
    for row in grid:
        for spot in row:
            if len(spot.neighbors) < 2 or len(spot.neighbors) > 3:
                spot.reset()
            if len(spot.not_neighbors) == 3:
                spot.make_block()



def main(win,width):
    ROWS = 50
    grid = make_grid(ROWS,width)
    run = True
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #left click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col]
                spot.make_block()

        #right click
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col]
                spot.reset()

            if event.type == pygame.KEYDOWN:
            #start game with spacebar
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                
                    game(lambda: draw(win,grid,ROWS,width),grid)
            
            #clear grid with c
                if event.key == pygame.K_c:
                    grid = make_grid(ROWS,width)


    pygame.quit()


main(WIN,WIDTH)