from tkinter import *
import math

TEXT = 30

render_data = {"canvas": None, "root": None, "stop": False,
               "start": False, "dim": (6, 7), "view": (500, 500), "text": {}}


def on_quit():
    """
    callback lors du click sur fermeture de fenêtre
    """
    render_data["stop"] = True


def write(i, j, number, color):
    canvas = render_data["canvas"]

    nbr = render_data["dim"][0]
    nbc = render_data["dim"][1]

    if i >= nbr or i < 0 or j < 0 or j >= nbc:
        return

    w = render_data["view"][0]
    h = render_data["view"][1]

    stepx = (w-TEXT)/nbc
    stepy = (h-TEXT)/nbr

    nombres = render_data["text"]
    if (i, j) in nombres:  # On a deja affiche quelque chose dans la case (x, y)
        id = nombres[i, j]
        canvas.itemconfig(id, text=str(number), fill=color)
    else:
        id = canvas.create_text(30+j*stepx+stepx/2, 30+i*stepy+stepy/2,
                                text=str(number), fill=color, font=("Purisa", int(stepx*.75)))
        nombres[i, j] = id

    canvas.update()


def erase(i, j):
    canvas = render_data["canvas"]
    nombres = render_data["text"]
    if (i, j) in nombres:
        canvas.delete(nombres[i, j])
    canvas.update()


def draw_grid():
    """
    trace le plateau de jeu (grille des disques donnée par render_data["grid"])
    """
    if render_data["stop"]:
        return None

    canvas = render_data["canvas"]
    canvas.delete("all")

    nbr = render_data["dim"][0]
    nbc = render_data["dim"][1]
    n = int(math.sqrt(nbr))
    w = render_data["view"][0]
    h = render_data["view"][1]

    stepx = (w-TEXT)/nbc
    stepy = (h-TEXT)/nbr

    for c in range(nbc+1):
        if c % n == 0:
            canvas.create_line(c*stepx+TEXT, TEXT, c*stepx +
                               TEXT, h, fill="black", width=3)
        else:
            canvas.create_line(c*stepx+TEXT, TEXT, c *
                               stepx+TEXT, h, fill="black")
    for r in range(nbr+1):
        if r % n == 0:
            canvas.create_line(TEXT, r*stepy+TEXT, w, r *
                               stepy+TEXT, fill="black", width=3)
        else:
            canvas.create_line(TEXT, r*stepy+TEXT, w, r *
                               stepy+TEXT, fill="black")

    for c in range(nbc):
        canvas.create_text(c*stepx+TEXT+stepx/2, TEXT/2, text=str(c),
                           width=stepx, font=("Purisa", int(stepx*.33)))
    for r in range(nbr):
        canvas.create_text(TEXT/2, r*stepy+TEXT+stepy/2, text=str(r),
                           width=stepx, font=("Purisa", int(stepx*.33)))

    canvas.update()


def configure_draw(n):
    """
    modifie les dimensions de l'affichage du plateau de jeu selon les nombres de ligne nr et colonne nc (tient compte du ratio largeur/hauteur de la fenêtre graphique)
    """
    nr, nc = n**2, n**2
    dim = (nr, nc)
    render_data["dim"] = dim

    render_data["grid"] = [[0 for i in range(nc)] for j in range(nr)]

    canvas = render_data["canvas"]
    view = (canvas.winfo_width(), canvas.winfo_height()-TEXT)
    dim = render_data["dim"]
    rx = view[0]/dim[1]
    ry = (view[1]-TEXT)/dim[0]
    if (rx < ry):
        v = (view[0], dim[0]*rx+TEXT)
    else:
        v = (dim[1]*ry, view[1])
    render_data["view"] = v


def wait_quit():
    """
    attend explicitement la fermeture de la fenêtre graphique
    """
    if (render_data["start"]):
        canvas = render_data["canvas"]
        while not(render_data["stop"]):
            canvas.update()
        root = render_data["root"]
        root.destroy()


def init_draw(w=450, h=480):
    """
    initialise la fenêtre graphique (canvas de largeur w et hauteur h)
    """
    render_data["view"] = (w, h-TEXT)

    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_quit)
    canvas = Canvas(root, width=w, height=h)
    canvas["background"] = "white"
    canvas.pack(fill=BOTH, expand=1)
    render_data["canvas"] = canvas
    render_data["root"] = root
    canvas.winfo_toplevel().title("Sudoku")
    canvas.update()
    render_data["start"] = True


def draw_sudoku_grid(n):
    """
    Trace a sudoku grid of order n
    """
    if not render_data["start"]:
        init_draw()

    configure_draw(n)

    draw_grid()


if __name__ == "__main__":
    draw_sudoku_grid(2)
    write(0, 0, "15", "red")
    write(3, 2, 12, "blue")
    write(0, 0, 2, "green")
    erase(0, 0)
    write(24, 24, 3, "blue")
    wait_quit()
