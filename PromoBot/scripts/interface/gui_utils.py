autor = "Ursu Alin"
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
import os
import sys
from PIL import Image, ImageTk

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
datapath = path + "bin" + slash + "data" + slash

class browser():
    def __init__(self):
        if slash == "/":
            self.driverpath = datapath + "geckodriver"
        else:
            self.driverpath = datapath + "geckodriver.exe"
        self.driver = webdriver.Firefox(executable_path=self.driverpath, log_path=datapath + "geckodriver.log")
        marime = self.marime_monitor()
        #self.driver.set_window_position(0, 0)
        #self.driver.set_window_size(marime[0]-450, marime[1]-200)
        self.driver.set_window_size(marime[0], marime[1])

    def schimbare_link(self, link):
        self.driver.get(link)
    def asteptare(self, titlu_partial):
        assert titlu_partial in self.driver.title
    def marime_monitor(self):
        _ = Tk()
        lungime = _.winfo_screenwidth()
        latime = _.winfo_screenheight()
        _.destroy()
        return (lungime, latime)

    def inchidere(self):
        self.driver.close()


class buton(Button):
    def __init__(self, master):
        Button.__init__(self, master=master)
    def initializare(self, text, lungime, latime, fg=None, bg=None, font=None, buton=None, comanda=None):
        self.configure(text=text, width=lungime, height=latime)
        if fg != None:
            self.configure(fg=fg)
        if bg != None:
            self.configure(bg=bg)
        if font != None:
            self.configure(font=font)
        if buton != None and comanda != None:
            self.connect(buton, comanda)

    def plasare(self, x , y):
        self.place(x=x,y=y)
    def ascundere(self):
        self.place_forget()
    def editare_text(self, text):
        self.configure(text=text)
    def editare_marime(self, lungime=None, latime=None):
        if lungime != None:
            self.configure(width=lungime)
        if latime != None:
            self.configure(height=latime)
    def editare_culori(self, fg=None, bg=None):
        if fg != None:
            self.configure(fg=fg)
        if bg != None:
            self.configure(bg=bg)
    def editare_font(self, font):
        self.configure(font=font)
    def adaugare_comanda(self, buton, comanda):
        self.connect(buton, comanda)
    def dezactivare(self):
        self.configure(state="disabled")
    def activare(self):
        self.configure(state="normal")

    def connect(self, button, event):
        self.bind(button, event)

class label(Label):
    def __init__(self, master):
        Label.__init__(self, master=master)
    def initializare(self, text, fg=None, bg=None, font=None, buton=None, comanda=None):
        self.configure(text=text)
        if fg != None:
            self.configure(fg=fg)
        if bg != None:
            self.configure(bg=bg)
        if font != None:
            self.configure(font=font)
        if buton != None and comanda != None:
            self.connect( buton, comanda)


    def editare_text(self, text):
        self.configure(text=text)
    def editare_marime(self, lungime=None, latime=None):
        if lungime != None:
            self.configure(width=lungime)
        if latime != None:
            self.configure(height=latime)
    def editare_culori(self, fg=None, bg=None):
        if fg != None:
            self.configure(fg=fg)
        if bg != None:
            self.configure(bg=bg)
    def editare_font(self, font):
        self.configure(font=font)
    def adaugare_comanda(self, buton, comanda):
        self.connect(buton, comanda)


    def plasare(self, x , y, anchor=None):
        if anchor != None:
            self.place(x=x, y=y, anchor=anchor)
        else:
            self.place(x=x,y=y)
    def ascundere(self):
        self.place_forget()
    def connect(self, button, event):
        self.bind(button, event)

class txtbox(Entry):
    def __init__(self, master):
        Entry.__init__(self, master=master)
    def initializare(self, lungime, def_text=None, enabled=True, fg=None, bg=None, font=None, buton=None, comanda=None):
        self.configure(width=lungime)
        if def_text != None:
            self.insert(END, def_text)
        if enabled == False:
            self.config(state='disabled')
        if fg != None:
            self.configure(fg=fg)
        if bg != None:
            self.configure(bg=bg)
        if font != None:
            self.configure(font=font)
        if buton != None and comanda != None:
            self.connect(buton, comanda)

    def plasare(self, x , y):
        self.place(x=x,y=y)
    def ascundere(self):
        self.place_forget()
    def inserare_text(self, text):
        self.insert(END, text)
    def stergere_text(self):
        self.delete(0, 'end')
    def text(self):
        return self.get()
    def activare(self):
        self.configure(state='normal')
    def dezactivare(self):
        self.configure(state='disabled')
    def editare_marime(self, lungime=None):
        if lungime != None:
            self.configure(width=lungime)
    def editare_culori(self, fg=None, bg=None):
        if fg != None:
            self.configure(fg=fg)
        if bg != None:
            self.configure(bg=bg)
    def editare_font(self, font):
        self.configure(font=font)
    def adaugare_comanda(self, buton, comanda):
        self.connect(buton, comanda)

    def connect(self, button, event):
        self.bind(button, event)

class imagine(Label):
    def __init__(self, master):
        Label.__init__(self, master=master)
    def initializare(self, path, lungime=None, latime=None, border=None):
        self.path = path
        self.img = Image.open(self.path)
        if lungime != None and latime != None:
            self.modificare_marime(lungime, latime)
        self.img = ImageTk.PhotoImage(self.img)
        self.configure(image=self.img)
        if border == None:
            self.fara_margini()

    def modificare_marime(self, lungime, latime):
        self.img = self.img.resize((lungime, latime), Image.ANTIALIAS)
    def modificare_imagine_director(self, imgpath, lungime=None, latime=None, border=None):
        self.path = imgpath
        self.img = Image.open(self.path)
        if lungime != None and latime != None:
            self.modificare_marime(lungime, latime)
        self.img = ImageTk.PhotoImage(self.img)
        self.configure(image=self.img)
        if border == None:
            self.fara_margini()
    def modificare_imagine(self, imagine):
        self.img = imagine
        self.configure(image=self.img)
    def fara_margini(self):
        self.configure(borderwidth=0, highlightthickness=0)

    def plasare(self, x, y):
        self.place(x=x, y=y)
    def ascundere(self):
        self.place_forget()
    def adaugare_comanda(self, Buton, comanda):
        self.bind(Buton, comanda)

class font(Font):
    def __init__(self):
        Font.__init__(self)
    def initializare(self, familie, marime_text):
        self.configure(family=familie, size=marime_text)

class treeview(ttk.Treeview):
    def __init__(self, master):
        ttk.Treeview.__init__(self, master=master)
        self.master = master
        self.imgs = {}
    def initializare(self, Buton, comanda, rowheight):
        self.style = ttk.Style(self.master)
        self.style.configure("Treeview", rowheight=rowheight)
        self.bind(Buton, comanda)

    def add_imagine(self, imgdesc, imgpath, lungime, latime):
        self.imgs[imgdesc] = ImageTk.PhotoImage(Image.open(imgpath).resize((lungime, latime), Image.ANTIALIAS))
    def add_imgs(self):
        for key in self.imgs:
            text = "{}".format(key)
            self.insert('', self.imgs[key], values=[text], text='', open=True, image=self.imgs[key])


    def plasare(self, x, y):
        self.place(x=x, y=y)
    def ascundere(self):
        self.place_forget()

class dropdown(OptionMenu):
    def __init__(self, master, elemente, lungime=None, fg=None, bg=None):
        self.var = StringVar(master)
        self.elemente = elemente
        self.var.set(self.elemente[0])
        OptionMenu.__init__(self, master, self.var, *self.elemente)
        if lungime != None:
            self.modificare_lungime(lungime)
        if fg != None:
            self.configure(fg=fg)
        if bg != None:
            self.configure(bg=bg)

    def element_selectat(self):
        return self.var.get()
    def modificare_lungime(self, lungime):
        self.configure(width=lungime)

    def plasare(self, x, y):
        self.place(x=x, y=y)
    def ascundere(self):
        self.place_forget()
    def adaugare_comanda(self, Buton, comanda):
        self.bind(Buton, comanda)

class toplevel(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
    def initializare(self, titlu, geometry, resizable=0):
        self.title(titlu)
        self.geometry(geometry)
        if resizable == 0:
            self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.event_inchidere)
    def centrare(self):
        self.update_idletasks()
        ecran_latime = self.winfo_screenwidth()
        ecran_inaltime = self.winfo_screenheight()
        marime = tuple(int(_) for _ in self.geometry().split("+")[0].split("x"))

        x = ecran_latime/2 - marime[0]/2
        y = ecran_inaltime/2 - marime[1]/2

        self.geometry("+%d+%d" % (x,y))

    def add_button(self, text, lungime, latime, fg=None, bg=None, font=None, Buton=None, comanda=None):
        bttn = buton(self)
        bttn.initializare(text, lungime, latime, fg, bg, font, Buton, comanda)
        return bttn
    def add_label(self, text, fg=None, bg=None, font=None, buton=None, comanda=None):
        lbl = label(self)
        lbl.initializare(text, fg, bg, font, buton, comanda)
        return lbl
    def add_textbox(self, lungime, def_text=None, enabled=True, fg=None, bg=None, font=None, buton=None, comanda=None):
        tbox = txtbox(self)
        tbox.initializare(lungime, def_text, enabled, fg, bg, font, buton, comanda)
        return tbox
    def add_imagine(self, imgpath, lungime=None, latime=None):
        img = imagine(self)
        img.initializare(imgpath, lungime, latime)
        return img
    def add_tree(self, Buton, comanda, rowheight):
        tree = treeview(self)
        tree.initializare(Buton, comanda, rowheight)
        return tree
    def add_dropdown(self, elemente, lungime=None):
        ddown = dropdown(self, elemente, lungime)
        return ddown
    def add_combobox(self, valori, lungime=None, latime=None, fg=None, bg=None, font=None):
        cbox = combobox(self, valori)
        cbox.initializare(lungime, latime, font)
        return cbox
    def creare_font(self, familie, marime_text):
        f = font()
        f.initializare(familie, marime_text)
        return f
    def messagebox(self, tip, titlu, text):
        if tip == 0:
            messagebox.showinfo(title=titlu, message=text, master=self)
        elif tip == 1:
            messagebox.showwarning(title=titlu, message=text, master=self)
        elif tip == 2:
            messagebox.showerror(title=titlu, message=text, master=self)
        elif tip == 3:
            return messagebox.askyesno(title=titlu, message=text, master=self)

    def connect(self, widget, button, event):
        widget.bind(button, event)
    def event_inchidere(self):
        if self.messagebox(3, "Confirmare", "Doriti sa inchideti programul?"):
            self.inchidere()
    def inchidere(self):
        self.destroy()

class textwidget(Text):
    def __init__(self, master):
        Text.__init__(self, master=master)
    def initializare(self, lungime=None, latime=None, bg=None, fg=None, font=None):
        if lungime != None:
            self.configure(width=lungime)
        if latime != None:
            self.configure(height=latime)
        if bg != None:
            self.configure(bg=bg)
        if fg != None:
            self.configure(fg=fg)
        if font != None:
            self.configure(font=font)

    def adaugare_text(self, text):
        self.insert("end", text)
    def dezactivare(self):
        self.configure(state="disabled")
    def activare(self):
        self.configure(state="normal")

    def text(self):
        return self.get("1.0", END)
    def plasare(self, x, y):
        self.place(x=x, y=y)
    def ascundere(self):
        self.place_forget()
    def adaugare_comanda(self, Button, comanda):
        self.bind(Button, comanda)

class combobox(ttk.Combobox):
    def __init__(self, master, valori):
        ttk.Combobox.__init__(self, master=master)
        self.valori = valori
        self.Variabila = StringVar(master=master)
        self.Variabila.set(self.valori[0])
        self.configure(textvariable=self.Variabila, values=self.valori)
    def initializare(self, lungime=None, latime=None, font=None):

        if lungime != None:
            self.configure(width=lungime)
        if latime != None:
            self.configure(height=latime)
        if font != None:
            self.configure(font=font)

    def adaugare_text(self, text):
        self.insert("end", text)
    def dezactivare(self):
        self.configure(state="readonly")
    def activare(self):
        self.configure(state="normal")
    def stilzare(self, bg, bg_select, bg_field, fg):
        self.setari_stilizare = {"TCombobox":
                                     {"configure":
                                          {
                                              "background": bg,
                                              "selectbackground": bg_select,
                                              "fieldbackground": bg_field,
                                              "foreground":fg
                                        }}}
        self.style = ttk.Style()
        self.style.theme_create('combostyle', parent='alt', settings=self.setari_stilizare)
        self.style.theme_use('combostyle')
    def schimbare_valori(self, valori):
        self.config(values=valori)
        self.Variabila.set(valori[0])

    def plasare(self, x, y):
        self.place(x=x, y=y)
    def ascundere(self):
        self.place_forget()
    def adaugare_comanda(self, Button, comanda):
        self.bind(Button, comanda)

class progressbar(ttk.Progressbar):
    def __init__(self, master):
        ttk.Progressbar.__init__(self, master=master)
    def initializare(self, lungime, orientare):
        self.lungime = lungime
        self.configure(length=lungime, orient=orientare, mode='determinate')

    def redimensionare(self, lungime):
        self.configure(length=lungime)
    def stilizare(self, bg):
        self.style= ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('style.Horizontal.TProgressbar', background=bg)
        self.configure(style="style.Horizontal.TProgressbar")
    def incrementare(self, valoare):
        for i in range(0, valoare):
            self.step()
    def setare_valoare_maxima(self, valoare):
        self["maximum"] = valoare
    def valoarea_actuala(self):
        return self["value"]

    def plasare(self, x, y):
        self.place(x=x, y=y)
    def ascundere(self):
        self.place_forget()

class canvas(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master=master)
    def initializare(self, lungime, latime, border=None):
        self.configure(width=lungime, height=latime)
        if border == None:
            self.configure(highlightthickness=0)

    def creare_imagine(self, imagine, lungime, latime):
        self.create_image(lungime, latime, image=imagine)
    def stergere_elemente(self):
        self.delete(ALL)

    def plasare(self, x, y):
        self.place(x=x, y=y)
    def ascundere(self):
        self.place_forget()


class App(Tk):
    def __init__(self, titlu, geometry, resizable=0):
        Tk.__init__(self)
        self.title(titlu)
        self.geometry(geometry)
        if resizable == 0:
            self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.event_inchidere)
    def modificare_titlu(self, titlu):
        self.title(titlu)
    def modificare_icon(self, path):
        self.iconbitmap(path)
    def centrare(self):
        self.update_idletasks()
        ecran_lungime = self.winfo_screenwidth()
        ecran_latime = self.winfo_screenheight()
        marime = tuple(int(_) for _ in self.geometry().split("+")[0].split("x"))

        x = ecran_lungime/2 - marime[0]/2
        y = ecran_latime/2 - marime[1]/2

        self.geometry("+%d+%d" % (x,y))
    def amplasare_colt_dreapta_jos(self):
        self.update_idletasks()
        ecran_lungime = self.winfo_screenwidth()
        ecran_latime = self.winfo_screenheight()
        marime = tuple(int(_) for _ in self.geometry().split("+")[0].split("x"))

        x = ecran_lungime - marime[0]
        y = ecran_latime - marime[1]

        self.geometry("+%d+%d" % (x, y))
    def amplasare_colt_dreapta_sus(self):
        self.update_idletasks()
        ecran_lungime = self.winfo_screenwidth()
        ecran_latime = self.winfo_screenheight()
        marime = tuple(int(_) for _ in self.geometry().split("+")[0].split("x"))

        x = ecran_lungime - marime[0]
        y = 0

        self.geometry("+%d+%d" % (x, y))

    def add_button(self, text, lungime, latime, fg=None, bg=None, font=None, Buton=None, comanda=None):
        bttn = buton(self)
        bttn.initializare(text, lungime, latime, fg, bg, font, Buton, comanda)
        return bttn
    def add_label(self, text, fg=None, bg=None, font=None, buton=None, comanda=None):
        lbl = label(self)
        lbl.initializare(text, fg, bg, font, buton, comanda)
        return lbl
    def add_textbox(self, lungime, def_text=None, enabled=True, fg=None, bg=None, font=None, buton=None, comanda=None):
        tbox = txtbox(self)
        tbox.initializare(lungime, def_text, enabled, fg, bg, font, buton, comanda)
        return tbox
    def add_imagine(self, imgpath, lungime=None, latime=None):
        img = imagine(self)
        img.initializare(imgpath, lungime, latime)
        return img
    def add_tree(self, Buton, comanda, rowheight):
        tree = treeview(self)
        tree.initializare(Buton, comanda, rowheight)
        return tree
    def add_dropdown(self, elemente, lungime=None, fg=None, bg=None):
        ddown = dropdown(self, elemente, lungime)
        return ddown
    def add_toplevel(self, titlu, geometry):
        tlevel = toplevel(self)
        tlevel.initializare(titlu=titlu, geometry=geometry)
        return tlevel
    def add_textwidget(self, lungime=None, latime=None, fg=None, bg=None, font=None):
        twidget = textwidget(self)
        twidget.initializare(lungime, latime, fg, bg, font)
        return twidget
    def add_combobox(self, valori, lungime=None, latime=None, font=None):
        cbox = combobox(self, valori)
        cbox.initializare(lungime, latime, font)
        return cbox
    def add_progressbar(self, lungime, orientare):
        pbar = progressbar(self)
        pbar.initializare(lungime, orientare)
        return pbar
    def add_canvas(self, lungime, latime, border=None):
        cnvs = canvas(self)
        cnvs.initializare(lungime=lungime, latime=latime, border=border)
        return cnvs
    def creare_font(self, familie, marime_text):
        f = font()
        f.initializare(familie, marime_text)
        return f
    def messagebox(self, tip, titlu, text):
        if tip == 0:
            messagebox.showinfo(title=titlu, message=text, master=self)
        elif tip == 1:
            messagebox.showwarning(title=titlu, message=text, master=self)
        elif tip == 2:
            messagebox.showerror(title=titlu, message=text, master=self)
        elif tip == 3:
            return messagebox.askyesno(title=titlu, message=text, master=self)

    def connect(self, widget, button, event):
        widget.bind(button, event)
    def adaugare_comanda(self, button, event):
        self.bind(button, event)
    def event_inchidere(self):
        if self.messagebox(3, "Confirmare", "Doriti sa inchideti programul?"):
            self.inchidere()
    def inchidere(self):
        self.destroy()
