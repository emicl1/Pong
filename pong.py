#### Název souboru : pong.py
#### Popis programu: pong hra
#### Autor:  Alex Michaud
############################################################################
####### MODULY
import tkinter as tk  ### tkinter modul vložíme pod názvem "tk"


############################################################################
##### Deklarace tříd
##############################
class Palka(object):
    """
     objekt pálky - obdelník na canvase
    """

    def __init__(self, platno, x, y, s, v, barva, rychlost):
        self.platno = platno
        self.x, self.y = x, y
        self.vyska, self.sirka = s, y
        self.barva = barva
        self.id = self.platno.obdelnik(x, y, s, v, vypln=barva, barva=barva)
        self.rychlost = rychlost
        self.score = 0

    def krok(self):
        """
         pálka se posune ve směru vektoru rychlosti o jeden krok
        """
        self.x = self.x + self.rychlost[0]
        self.y = self.y + self.rychlost[1]
        self.platno.moveto(self.id, self.x, self.y )
        #self.platno.moveto(self.id, self.x - self.sirka / 2, self.y - self.vyska / 2)


    def set_rychlost(self, rychlost):
        """
         nastav vektor rychlosti pálky
        """
        self.rychlost = rychlost

    def otoc(self):
        """
         otočí směr vektoru rychlosti pálky
        """
        self.rychlost[0] = -self.rychlost[0]
        self.rychlost[1] = -self.rychlost[1]

    def get_pos(self):
        """
         získá polohu pálky
        """
        return self.x, self.y

    def get_score(self):
        return self.score

    def score_up(self):
        self.score += 1

class Micek(object):
    """
      pohybující se míček
    """

    def __init__(self, platno, x, y, r, barva, rychlost):
        self.platno = platno
        self.x, self.y = x, y
        self.r = r
        self.barva = barva
        self.id = self.platno.kruh(x, y, r, vypln=barva, barva=barva)
        self.rychlost = rychlost

    def krok(self):
        """
         učiní krok ve směru a velikosti vektoru rychlosti
        """
        self.x += self.rychlost[0]
        self.y += self.rychlost[1]
        self.platno.move(self.id, self.rychlost[0], self.rychlost[1])

    def get_pos(self):
        """
         získá pozici objektu
        """
        return self.x, self.y

    def odrazX(self):
        self.rychlost[0] = -self.rychlost[0]

    def odrazY(self):
        self.rychlost[1] = -self.rychlost[1]

    def start(self,x, y):
        self.rychlost[0] *= -1
        self.rychlost[1] *= -1
        self.x = x
        self.y = y
        self.platno.moveto(self.id, x - self.r, y - self.r)


class Platno(tk.Canvas):
    """
      Rozšíření třídy tkinter.Canvas o další způsoby kreslení tvarů prvků
    """

    def obdelnik(self, x, y, s, v, barva="black", vypln="white", obrys=1):
        """
         Podobné jako .create_rectangle() s tím, že se x,y je souřadnice středu obdélníka,
         a rozměry jsou zadány jeho šířkou "sirka" a výškou "vyska".
         Další nepovinné parametry: vypln ... barva výplně,
            barva ... barva obrysu
            obrys ... síla obrysu v pixelech
        Funkce vrací číslo objektu na canvasu - tj. stejnou hodnotu jako metoda create_rectangle()
        """
        return self.create_rectangle(x - s / 2, y - v / 2, x + s / 2, y + v / 2, fill=vypln, outline=barva, width=obrys)

    def kruh(self, x, y, r, barva="black", vypln="white", obrys=1):
        """
         Podobné jako .create_oval() s tím, že se jedná o kreslení kružnice (a kruhu),
         x,y jsou souřadnice jeho středu, a "r" je jeho poloměr.
         Další nepovinné parametry:
            vypln ... barva výplně,
            barva ... barva obrysu
            obrys ... síla obrysu v pixelech
        Funkce vrací číslo objektu na canvasu - tj. stejnou hodnotu jako metoda create_oval()
        """
        return self.create_oval(x - r, y - r, x + r, y + r, fill=vypln, outline=barva, width=obrys)

    def presun(self, objekt, new_x, new_y):
        """
         metoda podobná metodě .moveto() s tím, že pro nové souřadnice
         objektu je zvolnen střed bounding boxu objektu
        """
        x1, y1, x2, y2 = self.bbox(objekt)  # získání souřadnic bounding boxu
        s = abs(x2 - x1)  # výpočet šířky bounding boxu
        v = abs(y2 - y1)  # výpočet výšky bounding boxu
        self.moveto(objekt, new_x - s / 2, new_y - v / 2)  # posun na nové místo


####################################################################
class App(tk.Tk):
    """
    Třída odvozená od třídy tkinter.Tk, tj. hlavní třídy pro tvorbu grafických aplikací
    pomocí frameworku "tkinter".
    Použije se k vytvoření a nastavení hlavního okna aplikace, v konstruktoru třídy,
    metoda .run() poté slouží ke spuštění vlastní aplikace
    """

    def __init__(self, titulek, sirka, vyska, barva="white"):
        """
         upravený konstruktor pro novou třídu
        """
        super().__init__()  ### zavolání původního konstruktoru
        ## uložení hodnot pro další použití
        self.W = sirka  # šířka okna
        self.H = vyska  # výška okna
        self.titulek = titulek  # titulek okna
          ##### vlastní nastavení titulku okna
        self.geometry(f"{self.W }x{self.H+60}+1600+400")  # nastavení velikosti a polohy okna
        self.menubar = tk.Menu(self)
        #### rolovací menu SOUBOR
        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        #self.fileMenu.add_command(label="Nová hra", command=self.new_game, state=tk.DISABLED)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Konec", command=self.konec)
        #### rolovací menu Nástroje
        self.setMenu = tk.Menu(self.menubar, tearoff=0)
        #self.setMenu.add_command(label="Nová hra", command=self.new_game)
        #### napojení rolovacích menu na hlavní menu okna (menubar)
        ### vložení widgetů do okna
        self.skupinaHorni = tk.Frame(self)
        self.skupinaDolni = tk.Frame(self)
        self.skupinaHorni.pack()
        self.skupinaDolni.pack()
        ##### NAPIS - widget LABEL
        self.nadpis = tk.Label(self.skupinaHorni, text="kdo první dostane 3 body vyhrál", background="red", foreground="yellow",
                               font="Arial 15 bold")
        self.nadpis.pack(fill=tk.BOTH, side=tk.TOP)
        ##### CANVAS
        # vložení naší verze canvasu (Platno) do vytvořeného okna aplikace
        self.canvas = Platno(self.skupinaHorni, width=self.W, height=self.H, background=barva)
        self.canvas.pack(side=tk.TOP)  # zobrazení widgetu canvas v okně
        ##### TLACIKA - widgety
        self.quitButton = tk.Button(self.skupinaDolni, text="Konec", command=self.konec)
        self.quitButton.pack(side=tk.LEFT)
        ################# KRESLIME NA CANVAS
        ## přerušovaná čára
        self.cara = self.canvas.create_line(self.W / 2, 0, self.W / 2, self.H, fill="gray", width=5, dash=(30, 10))
        #### vykreslení prvků na plátno
        ## nakreslení pálky
        self.palka = Palka(self.canvas, 10, 100, 20, 50, "blue", [0, 0])
        ## nakreslení palky 2
        self.palka_2 = Palka(self.canvas, self.W - 30, self.H / 2, 20, 50, "blue", [0, 0])
        ## nakreslení míčku
        self.micek = Micek(self.canvas, 30, 40, 10, "yellow", [1, 1])
        ## nakreslení nápisu
        #vytvoření textu
        self.text = self.canvas.create_text(self.W/2, 30, text="00:00", font="Arial 20 bold")
        ### navazani udalostí na obsluhy
        # vazby pro celý canvas
        self.canvas.bind("<KeyPress-Up>", self.palka_up)
        self.canvas.bind("<KeyPress-Down>", self.palka_down)
        self.canvas.bind("<KeyRelease-Up>", self.palka_stop)
        self.canvas.bind("<KeyRelease-Down>", self.palka_stop)
        self.canvas.bind("<KeyPress-w>", self.palka_up2)
        self.canvas.bind("<KeyPress-s>", self.palka_down2)
        self.canvas.bind("<KeyRelease-w>", self.palka_stop2)
        self.canvas.bind("<KeyRelease-s>", self.palka_stop2)
        self.canvas.bind("q", self.konec_2)
        self.canvas.bind("p", self.stop)
        self.running = True
        self.canvas.focus_set()  # nastavení canvasu jako příjemce událostí stisků klávesy
        ### spuštění časovače pro posun kolečka
        self.after(20, self.udelej_krok)


    ###################################################
    def run(self):
        """
        metoda pro spuštění aplikace
        """
        ##### Hlavní smyčka Tk (čekání na události)
        self.mainloop()

    def konec(self):
        self.destroy()

    def konec_2(self, udalost):
        self.destroy()

    def stop(self, udalost):
        self.running = not self.running

    def stop_2(self):
        self.running = not self.running

###################################################

    def udelej_krok(self):
        """
         posun  micku a palky o jeden krok ve směru vektoru rychlosti daného objektu
        """
        #### test behu animace
        if not self.running:
            self.after(10, self.udelej_krok)
            self.canvas.delete(self.palka)
            return

        px, py = self.palka.get_pos()
        if (py <= 0) or (py >= self.H):
            self.palka.otoc()
            self.palka.krok()
            self.palka.krok()
        else:
            self.palka.krok()
        px_1, py_1 = self.palka_2.get_pos()
        if (py_1 <= 0) or (py_1 >= self.H):
            self.palka_2.otoc()
            self.palka_2.krok()
            self.palka_2.krok()
        else:
            self.palka_2.krok()
        #### micek
        self.micek.krok()
        mx, my = self.micek.get_pos()
        ### horní a dolní
        if (my <= self.micek.r) or (my >= (self.H - self.micek.r)):
            self.micek.odrazY()
        ### prava
        if (mx >= (self.W - self.micek.r)):
            self.palka.score_up()
            self.micek.start(self.H/2, self.W/2)
            self.canvas.itemconfig(self.text, text=f"{self.palka.score:02d}:{self.palka_2.score:02d}")

            pass
        ### leva
        if (mx <= self.micek.r):
            self.palka_2.score_up()
            self.micek.start(self.H / 2, self.W / 2)
            self.canvas.itemconfig(self.text, text=f"{self.palka.score:02d}:{self.palka_2.score:02d}")

            pass
        ### bbox pálky?
        x1, y1, x2, y2 = self.canvas.bbox(self.palka.id)
        if self.micek.id in self.canvas.find_overlapping(x1, y1, x2, y2):
            self.micek.odrazX()

        x3, y3, x4, y4 = self.canvas.bbox(self.palka_2.id)
        if self.micek.id in self.canvas.find_overlapping(x3, y3, x4, y4):
            self.micek.odrazX()
        self.after(10, self.udelej_krok)

        if self.palka_2.score > 2:      #počítaní scoré a následné vyhlášení vítěze
            self.palka_2.x = 100000
            self.palka.x = 100000
            self.micek.rychlost = None
            self.win_text = self.canvas.create_text(self.W/2, 60, text="hráč číslo dvě vyhrál", font="Arial 20 bold")

        if self.palka.score > 2:      #počítaní scoré a následné vyhlášení vítěze
            self.palka_2.x = 100000
            self.palka.x = 100000
            self.micek.rychlost = None
            self.win_text = self.canvas.create_text(self.W/2, 60, text="hráč číslo jedna vyhrál", font="Arial 20 bold")


        ######################################

    def palka_up(self, udalost):
        self.palka.set_rychlost([0, -5])

    def palka_down(self, udalost):
        self.palka.set_rychlost([0, 5])

    def palka_stop(self, udalost):
        self.palka.set_rychlost([0, 0])

    def palka_up2(self, udalost):
        self.palka_2.set_rychlost([0, -5])

    def palka_down2(self, udalost):
        self.palka_2.set_rychlost([0, 5])

    def palka_stop2(self, udalost):
        self.palka_2.set_rychlost([0, 0])

    def won_title_1(self):
        self.nadpis = tk.Label(self.skupinaHorni, text="kdo první l", background="red",
                               foreground="yellow",
                               font="Arial 15 bold")
        self.nadpis.pack(fill=tk.BOTH, side=tk.TOP)
        #self.nadpis = tk.Label(self.skupinaHorni, text="Vyhrál číslo 2", background="red",
                              # foreground=yellow,
                             #  font=Arial 15 bold)


    def won_title_2(self):

        self.nadpis = tk.Label(self.skupinaHorni, text="kdo první l", background="red",
                               foreground="yellow",
                               font="Arial 15 bold")
        self.nadpis.pack(fill=tk.BOTH, side=tk.TOP)




    ############
    def klik_pravym(self, udalost):
        """
           výpis souřadnic na canvase při kliknutí na canvas pravým myším tlačítkem
        """

        self.canvas.itemconfig(self.napis, text=f"{udalost.x},{udalost.y}")

    ############
    def klik_prostrednim(self, udalost):
        """
           přesun kolečka na místo kliknutí prostředním tlačítkem
        """
        self.canvas.presun(self.kolecko, udalost.x, udalost.y)

    ############
    def klik_obdelnik(self, udalost):
        """
           výpis nápisu "Obdélník" po kliknutí na obdélník
        """
        self.canvas.itemconfig(self.napis, text="Obdelník")

    ############
    def klik_kolecko(self, udalost):
        """
           výpis nápisu "Kolečko" po kliknutí na kolečko
        """
        self.canvas.itemconfig(self.napis, text="Kolečko")

    ############
    def kolecko_left(self, udalost):
        """
           posun kolecka o -5px v ose x (doleva)
        """
        self.canvas.move(self.kolecko, -5, 0)

    ############
    def kolecko_right(self, udalost):
        """
           posun kolecka o +5px v ose x (doprava)
        """
        self.canvas.move(self.kolecko, +5, 0)

    ############
    def obdelnik_left(self, udalost):
        """
           posun obdélníku o -5px v ose x (doleva)
        """
        self.canvas.move(self.obdelnik, -5, 0)

    ############
    def obdelnik_right(self, udalost):
        """
           posun obdélníku o +5px v ose x (doprava)
        """
        self.canvas.move(self.obdelnik, +5, 0)


####################################################################
##### HLAVNÍ PROGRAM
if __name__ == "__main__":
    # vytvoříme aplikaci GUI, titulek okna je "Moje okno"
    #    okno má rozměry 400, 300 a barvu pozadí "dark green"
    app = App("Pong", 400, 300, barva="dark green")
    # rozběhneme aplikaci
    app.run()
#### KONEC SOUBORU

