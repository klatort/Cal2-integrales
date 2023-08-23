# libraries
import string
import threading
import time
import pyperclip
import matplotlib
import matplotlib.pyplot as plt
from sympy.integrals.manualintegrate import integral_steps
from sympy import *
from sympy.plotting import plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from dataclasses import dataclass

try:
    import tkinter as tk
except ImportError:
    import tkinter as tk
matplotlib.use('TkAgg')

# clases1
class GenerateSymbols(defaultdict):
    def __missing__(self, key):
        self[key] = Symbol(key)
        return self[key]

@dataclass
class equation:
    id: string
    ec: string

class textbox:
    ec = "x"
    height = 0.1
    width = 0.05

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_ec(self):
        self.ec = entry.get()
        self.width = len(self.ec) * 0.05

    def bbox(self, x, y):
        if((self.x - 0.05) <= x and (self.x + self.width - 0.025) >= x and (self.y - 0.05) <= y and (self.y + self.height - 0.025) >= y):
            return True
        else:
            return False


# functions

def plot_graph():

    expr = parse_expr(textboxes[0].ec.replace("^", "**"))
    symb = symb = next(iter(expr.free_symbols))
    a = plot(expr, (symb, -20, 20), label='$f(' +
             str(symb)+')$', legend=True, show=False)
    b = plot(Integral(expr).doit(), (symb, -20, 20),
             label='$F('+str(symb)+')$', legend=True, show=False)
    a.append(b[0])

    a.show()


def graph(event=None):
    tmptext = textboxes[0].ec
    textboxes[0].width = (len(textboxes[0].ec))*0.07
    isnon = True
    i = ""
    try:
        isnon = isinstance(float(simplify(tmptext)), str)
    except:
        z = 10    
    try:
        if isnon:
            i = latex(Integral(tmptext).doit()) + " + c"
            tmptext = latex(Integral(tmptext))
            if i.find("\int ") != -1:
                i = "No\,\,se\,\,ha\,\,podido\,\,resolver\,\,la\,\,integral"
        else:
            i = latex(Integral(tmptext, symbols("x")).doit()) + " + c"
            tmptext = latex(Integral(tmptext, symbols("x")))
        tmptext = "$" + tmptext + " = " + i + "$"
    except:
        tmptext = "Error de sintaxis."
    #print(integral_steps(parse_expr(textboxes[0].ec),symbols("x")))
    ax.text(textboxes[0].x, 1-textboxes[0].y, tmptext, fontsize=30)


def print_all():
    ax.clear()
    for i in textboxes[1:]:
        try:
            p_text = i.ec.replace("^", "**")
            p_text = p_text.replace("\int", "Integral")
            tmptext = "$" + latex(parse_expr(p_text)) + "$"
            ax.text(i.x, 1 - i.y, tmptext, fontsize=30)
        except:
            if i.ec.find("=") != -1:
                aux = i.ec.split('=')
                tmptext = "$" + \
                    latex(Eq(parse_expr(aux[0]), parse_expr(
                        aux[1].replace("^", "**")))) + "$"
                ax.text(i.x, 1 - i.y, tmptext, fontsize=30)
                symb = next(
                    iter(parse_expr(aux[1].replace("^", "**")).free_symbols))
                derivative = "$" + \
                    latex(
                        Eq(parse_expr("d"+aux[0]), diff(aux[1]))) + "d" + str(symb) + "$"
                ax.text(i.x, 1 - i.y - 0.1, derivative, fontsize=30)
            else:
                ax.text(i.x, 1 - i.y, "Error de sintaxis.", fontsize=30)
    graph()
    canvas.draw()


def print_one():
    if selected_box == textboxes[0]:
        graph()
    else:
        try:
            p_text = selected_box.ec.replace("^", "**")
            p_text = p_text.replace("\int", "Integral")
            tmptext = "$" + latex(parse_expr(p_text)) + "$"
            ax.text(selected_box.x, 1 - selected_box.y, tmptext, fontsize=30)
        except:
            if selected_box.ec.find("=") != -1:
                aux = selected_box.ec.split('=')
                tmptext = "$" + \
                    latex(Eq(parse_expr(aux[0]), parse_expr(aux[1]))) + "$"
                ax.text(selected_box.x, 1 - selected_box.y,
                        tmptext, fontsize=30)
            else:
                ax.text(selected_box.x, 1 - selected_box.y,
                        "Error de sintaxis.", fontsize=30)
    canvas.draw()


def get_latex():
    aux = entry.get().replace("^", "**")
    pyperclip.copy(latex(parse_expr(aux.replace("\int", "Integral"))))


def add_text(event):
    global root
    global selected_box
    x, y = root.winfo_pointerxy()
    widget = root.winfo_containing(x, y)
    if str(widget) == ".!canvas":
        x, y = event.x, event.y
        textboxes.append(textbox(1.285*x/(fig.get_size_inches()
                         [0]*100)-0.165, 1.285*y/(fig.get_size_inches()[1]*100)-0.12))
        entry.delete(0, "end")
        selected_box = textboxes[-1]
        entry.insert(0, selected_box.ec)
        print_one()


def wait():
    time.sleep(1.5)
    selected_box.set_ec()
    try:
        if selected_box.ec.find("=") != -1:
            found = False
            aux = selected_box.ec.split("=")

            for i in declared_vars:
                if aux[0] == i.id:
                    i.ec = aux[1].replace("^", "**")
                    found = True
                    break
            if found == False:
                declared_vars.append(equation(aux[0], aux[1]))

    except:
        print("error")
    print_all()


def callback(var):
    t = threading.Thread(target=wait)
    t.start()

def select(event):
    global root
    global selected_box
    x, y = root.winfo_pointerxy()
    widget = root.winfo_containing(x, y)
    if str(widget) == ".!canvas":
        x, y = event.x, event.y
        btn3.configure(bg='SystemButtonFace')
        for i in textboxes:
            if i.bbox(1.285*x/(fig.get_size_inches()[0]*100)-0.165, 1.285*y/(fig.get_size_inches()[1]*100)-0.12):
                entry.delete(0, "end")
                selected_box = i
                entry.insert(0, selected_box.ec)


def get_int(eq):
    aux_string = ""
    cont = 0
    for i in eq[8:]:
        aux_string = aux_string + i
        if i == "(":
            cont += 1
        if i == ")":
            cont -= 1
        if cont == 0:
            break
    return ["Integral" + aux_string, eq.replace("Integral" + aux_string, "")]


def parse_func(eq):
    aux = eq.replace("Integral", "!Integral")
    aux = aux.split("!")

    for i in range(len(aux)):
        if aux[i].find("Integral") != -1:
            a = get_int(aux[i])
            b = aux[i+1:]
            aux[i] = a[0]
            if i+1 >= len(aux):
                aux.append(a[1])
            else:
                aux[i+1] = a[1]
            
            for j in range(i+2, i+2+len(b)):
                if j >= len(aux):
                    aux.append(b[j-(i+2)])
                else:
                    aux[j] = b[j-(i+2)]
    print(aux)
    print(declared_vars)
    has_changed = False
    for i in range(len(aux)):
        for j in declared_vars:
            if aux[i][8:].find(j.id) != -1 and aux[i].find("Integral") != -1:
                print(j.id + " " + aux[i])
                a = parse_expr(aux[i])
                a = a.transform(parse_expr(j.id), parse_expr(j.ec))
                variable = str(next(iter(a.free_symbols)))
                a = str(a)
                a = a[0: 9:] + a[9: -(len(variable) + 3)] + ")"
                aux[i] = a
                has_changed = True
            elif aux[i][8:].find(j.id) != -1:
                aux[i] = aux[i].replace(j.id, j.ec)
                has_changed = True
                print(aux)
    if has_changed == True:
        print(aux)
        return parse_func("".join(aux))
    else:
        return parse_expr("".join(aux))


def check():
    global btn3
    completed_eq = selected_box.ec.replace("^", "**")
    completed_eq = parse_func(completed_eq.replace("\int", "Integral"))

    if simplify(completed_eq.doit()-Integral(parse_expr(textboxes[0].ec.replace("^", "**"))).doit()) == 0:
        btn3.configure(bg='green')
    else:
        btn3.configure(bg='red')


def eliminar():
    global selected_box, textboxes
    for i in textboxes[1:]:
        if selected_box == i:
            if i.ec.find("=") == 1:
                for j in declared_vars:
                    if i.ec == (j.id + "="+j.ec):
                        declared_vars.remove(j)
                        break
            selected_box = textboxes[textboxes.index(i) - 1]
            textboxes.remove(i)
            entry.delete(0, "end")
            print_all()
            entry.insert(0, selected_box.ec)
            return


# Maincode

textboxes = []
textboxes.append(textbox(-0.165, -0.05))

textboxes[0].ec = "x"
selected_box = textboxes[0]

declared_vars = []

root = tk.Tk()
root.title("Calculadora de integrales! :)")

mainframe = tk.Frame(root)
mainframe.pack(side='top')

temp = tk.StringVar()
temp.trace("w", lambda name, index, mode, temp=temp: callback(temp))
entry = tk.Entry(mainframe, width=70, textvariable=temp)
entry.pack(side='left')

btn1 = tk.Button(mainframe, command=eliminar, text="Eliminar")
btn1.pack(side='left')

btn2 = tk.Button(mainframe, command=get_latex, text="Ecuación en latex")
btn2.pack(side='left')

btn3 = tk.Button(mainframe, command=check, text="Comprobar ecuación")
btn3.pack(side='left')

btn4 = tk.Button(mainframe, command=plot_graph, text="Dibujar función")
btn4.pack(side='left')

label = tk.Label(mainframe)
label.pack()

fig = plt.figure(figsize=(12.8, 7.2))
ax = fig.add_subplot(frameon=False)

canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
canvas._tkcanvas.pack(side="left", fill="both", expand=True)


ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

graph()
root.bind("<Return>", lambda event: print_all())
root.bind("<Button-1>", select)
root.bind("<Button-3>", add_text)

root.mainloop()