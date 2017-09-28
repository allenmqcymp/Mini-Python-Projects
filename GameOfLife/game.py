# Allen Ma
# September 2017
# A crude simulation of Conway's Game of Life using Tkinter
# For Python 2.7.10
# left click to set active cells
# right click to start the simulation

from Tkinter import *
from cell import *


INIT_WIDTH = 600
INIT_HEIGHT = 600

class Grid():

    def __init__(self, root):
        self.root = root
        self.c = ResizingCanvas(self.root, width=INIT_WIDTH, height=INIT_HEIGHT, highlightthickness=0)
        self.square_size = 20
        self.cell_list = []
        self.rec_id_list = []

        # draw horizontal and vertical squares representing the grid
        for i in range(0, INIT_WIDTH, self.square_size):
            for x in range(0, INIT_HEIGHT, self.square_size):
                id = self.c.create_rectangle(i, x, i+self.square_size, x+self.square_size, fill="blue")
                self.rec_id_list.append(id)
                # add each cell object to a cell list
                self.cell_list.append(Cell(id))


        # bind all the rectangle ids onto left mouseclick event
        for id in self.rec_id_list:
            self.c.tag_bind(id, '<Button-1>', self.on_click)

        # useless
        self.c.addtag_all("all")

        self.c.pack(fill=BOTH, expand=YES)

    def get_cell_List(self):
        return self.cell_list


    def on_click(self, event):
        # get item by current tag
        item = self.c.find_withtag("current")[0]

        # redraw the item on the canvas with a different color
        coords = self.c.coords(item)
        x1, y1, x2, y2 = coords

        self.c.itemconfig(item, fill="red")

        # set the square that just got filled red to be alive
        for cell in self.get_cell_List():
            if cell.id == item:
                cell.setAlive()



    @staticmethod
    def center_rect(x1, y1, x2, y2):
        ''' returns (x, y) representing the center coordinate
            of a rectangle on the canvas
            This is simply a convenience method
        '''
        return float(x1 + x2) / 2, float(y1 + y2) / 2


    def get_neighbours(self, id):
        ''' given the id of a cell/rectangle on the canvas
            return the ids of its neighbouring cells in an
            8-tuple
        '''
        coords = self.c.coords(id)

        x1, y1, x2, y2 = coords
        centerx, centery = Grid.center_rect(x1, y1, x2, y2)

        # to avoid multiple objects returned from specifying
        # find_closest on a corner
        # specify the center of a rectangle

        # bottom left
        bl = self.c.find_closest(centerx - self.square_size, centery + self.square_size)
        # bottom middle
        bm = self.c.find_closest(centerx, centery + self.square_size)
        # bottom right
        br = self.c.find_closest(centerx + self.square_size, centery + self.square_size)
        # middle left
        ml = self.c.find_closest(centerx - self.square_size, centery)
        # middle right
        mr = self.c.find_closest(centerx + self.square_size, centery)
        # top left
        tl  = self.c.find_closest(centerx - self.square_size, centery - self.square_size)
        # top middle
        tm = self.c.find_closest(centerx, centery - self.square_size)
        # top right
        tr = self.c.find_closest(centerx + self.square_size, centery - self.square_size)

        return (bl, bm, br, ml, mr, tl, tm, tr)



class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind('<Configure>', self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        wscale = float(event.width) / float(self.width)
        hscale = float(event.height) / float(self.height)

        self.width = event.width
        self.height = event.height

        # scale the canvas
        self.config(width=self.width, height=self.height)

        self.scale("all", 0, 0, wscale, hscale)

class Simulation():
    def __init__(self, root):
        self.root = root
        self.grid = Grid(root)

        self.grid.c.bind("<Button-2>", self.start_simulation)

    @staticmethod
    def lookupCell(id, list):
        ''' takes a list of cell ids, and returns the
            cell that matches the id given
        '''
        for cell in list:
            if cell.getId() == id:
                return cell

        return False


    def start_simulation(self, event=None):
        # make a grid object
        # get the cells
        cells = self.grid.get_cell_List()

        # Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        for cell in cells:
            cell_id = cell.id
            alive_count = 0
            for neighbour_tuple in self.grid.get_neighbours(cell_id):
                (neighbour_id,) = neighbour_tuple
                for c in cells:
                    if neighbour_id == c.id:
                        neighbour_cell = c
                if neighbour_cell.getAlive():
                    alive_count += 1

            if not cell.getAlive() and alive_count == 3:
                cell.setAlive()
                self.grid.c.itemconfig(cell_id, fill="red")

            if alive_count < 2 and cell.getAlive():
                cell.clearAlive()
                # update the draw method to dead
                self.grid.c.itemconfig(cell_id, fill="blue")
            elif (alive_count == 2 or alive_count == 3) and cell.getAlive():
                # cell is lives on:
                cell.setAlive()
                self.grid.c.itemconfig(cell_id, fill="red")
            elif alive_count > 3 and cell.getAlive():
                cell.clearAlive()
                self.grid.c.itemconfig(cell_id, fill="blue")

        self.root.after(100, self.start_simulation)








def main():
    root = Tk()
    simulation = Simulation(root)
    root.mainloop()

if __name__ == "__main__":
    main()



