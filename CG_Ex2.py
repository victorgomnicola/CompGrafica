import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from screeninfo import get_monitors
import os




class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.pos = []
        self.master.title("Exercicio 2 de Computacao grafica")
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        # File Bar
        file = Menu(menu)
        file.add_command(label="Abrir imagem", command=self.abrirImagem)
        menu.add_cascade(label="File", menu=file)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.image = None
        self.im = None
        self.im2 = None

        tamanho = str(get_monitors())
        tamanho = tamanho.split('monitor(')
        tamanho = tamanho[1].split('+')
        tamanho = tamanho[0].split('x')

        largura = int(tamanho[0])
        altura = int(tamanho[1])
        self.width = largura
        self.height = altura

    def abrirImagem(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecione uma imagem .jpg",
                                              filetypes=[("Jpeg Files", "*.jpg")])
        if not filename:
            return

        self.im = Image.open(filename)
        w, h = self.im.size

        if w > (self.width / 3):
            proporcao = (self.width / 3) / w
            w = int(self.width / 3)
            h = int(h * proporcao)

        if h > int(3 * self.height / 4):
            proporcao = (3 * self.height / 4) / h
            w = int(w * proporcao)
            h = int(3 * self.height / 4)

        self.im = self.im.resize((w, h), Image.ANTIALIAS)

        self.render = ImageTk.PhotoImage(self.im)
        self.image = self.canvas.create_image((w/2, h/2), image=self.render)

        self.render2 = ImageTk.PhotoImage(self.im)
        self.image2 = self.canvas.create_image((w/2, h/2), image=self.render2)

        self.canvas.move(self.image2, w + self.width / 3, 0)

        fields = 'Grau de Vermelho', 'Grau de Verde', 'Grau de Azul'
        ents = self.makeform(root, fields)
        root.bind('<Return>', (lambda event, e=ents: self.GerarNovaImagem(e, w, h)))
        b1 = Button(root, text='Gerar nova imagem',
                    command=(lambda e=ents: self.GerarNovaImagem(e, w, h)))

        b1.pack(side=LEFT, padx=5, pady=5)

        b2 = Button(root, text='Gerar histograma',
                    command=(lambda e=ents: self.GerarNovaImagem(e, w, h)))

        b2.pack(side=LEFT, padx=5, pady=5)

        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        self.canvas.pack(side="bottom", fill="both", expand="yes")

    def GerarNovaImagem(self, entries, w, h):

        entry_red = entries[0]
        entry_green = entries[1]
        entry_blue = entries[2]

        factor_red = int(entry_red[1].get())
        factor_green = int(entry_green[1].get())
        factor_blue = int(entry_blue[1].get())
        matrix = list(self.im.getdata())
        self.im2 = self.modifica_pixels(matrix, factor_red,factor_green, factor_blue)

        self.render = ImageTk.PhotoImage(self.im)
        self.image = self.canvas.create_image((w/2, h/2), image=self.render)

        self.render2 = ImageTk.PhotoImage(self.im2)
        self.image2 = self.canvas.create_image((w / 2, h / 2), image=self.render2)
        self.canvas.move(self.image2, w + self.width/3, 0)

    def makeform(self, root, fields):
        tamanho = str(get_monitors())
        tamanho = tamanho.split('monitor(')
        tamanho = tamanho[1].split('+')
        tamanho = tamanho[0].split('x')

        largura = int(tamanho[0])
        altura = int(tamanho[1])

        entries = []
        for field in fields:
            row = Frame(root)
            lab = Label(row, width=15, height=2, text=field, anchor='w')
            ent = Entry(row)
            ent.insert(END,'0')
            row.pack(side=BOTTOM, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=LEFT, expand=NO, fill=X)
            entries.append((field, ent))
        return entries

    def modifica_pixels(self, matrix, factor_red, factor_green, factor_blue):
        c = 0

        for pixel in matrix:

            # Verificando limites do vermelho
            if (pixel[0] + factor_red > 255):
                new_red = 255
            elif pixel[0] + factor_red < 0:
                new_red = 0
            else:
                new_red = pixel[0] + factor_red

                # Verificando limites do verde
            if (pixel[1] + factor_green > 255):
                new_green = 255
            elif pixel[1] + factor_green < 0:
                new_green = 0
            else:
                new_green = pixel[1] + factor_green

                # Verificando limites do azul
            if (pixel[2] + factor_blue > 255):
                new_blue = 255
            elif pixel[2] + factor_blue < 0:
                new_blue = 0
            else:
                new_blue = pixel[2] + factor_blue

            pixels = (new_red, new_green, new_blue)

            matrix[c] = pixels
            c += 1

        new_im = Image.new(self.im.mode, self.im.size)
        new_im.putdata(matrix)
        return new_im



tamanho = str(get_monitors())
tamanho = tamanho.split('monitor(')
tamanho = tamanho[1].split('+')
tamanho = tamanho[0].split('x')

largura = int(tamanho[0])
altura = int(tamanho[1])

root = tk.Tk()
root.geometry("%dx%d" % (largura, altura))
root.title("Selecione uma imagem")
app = Window(root)
app.pack(fill=tk.BOTH, expand=1)

root.mainloop()