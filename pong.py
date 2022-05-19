#### Název souboru : gui_aplikace.py
#### Popis programu: vzorová aplikace v tkinter psaná objektově
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

    def krok(self):
        """
         pálka se posune ve směru vektoru rychlosti o jeden krok
        """
        self.x += self.rychlost[0]
        self.y += self.rychlost[1]
        self.platno.move(self.id, self.rychlost[0], self.rychlost[1])

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
        self.rychlost[0] = self.rychlost[0] * -1

    def odrazY(self):
        self.rychlost[1] = self.rychlost[1] * -1


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
        return self.create_oval(x - r / 2, y - r / 2, x + r / 2, y + r / 2, fill=vypln, outline=barva, width=obrys)

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
        self.title(titulek)  ##### vlastní nastavení titulku okna
        self.geometry(f"{self.W}x{self.H}+1200+200")  # nastavení velikosti a polohy okna
        ### vložení widgetů do okna
        #####
        # vložení naší verze canvasu (Platno) do vytvořeného okna aplikace
        self.canvas = Platno(self, width=self.W, height=self.H, background=barva)
        self.canvas.pack()  # zobrazení widgetu canvas v okně
        #### vykreslení prvků na plátno
        ## nakreslení pálky
        self.palka = Palka(self.canvas, 10, 100, 20, 50, "blue", [0, 0])
        ## nakreslení míčku
        self.micek = Micek(self.canvas, 30, 40, 20, "yellow", [1, 1])
        ## nakreslení nápisu
        self.napis = self.canvas.create_text(20, 20, text="00", font="Arial 20 bold", anchor=tk.W)
        ### navazani udalostí na obsluhy
        # vazby pro celý canvas
        self.canvas.bind("<KeyPress-Up>", self.palka_up)
        self.canvas.bind("<KeyPress-Down>", self.palka_down)
        self.canvas.bind("<KeyRelease-Up>", self.palka_stop)
        self.canvas.bind("<KeyRelease-Down>", self.palka_stop)
        self.canvas.bind("<KeyPress-w>", self.palka_up)
        self.canvas.bind("<KeyPress-x>", self.palka_down)
        self.canvas.bind("<KeyRelease-w>", self.palka_stop)
        self.canvas.bind("<KeyRelease-x>", self.palka_stop)
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

    ###################################################
    def udelej_krok(self):
        """
         posun  micku a palky o jeden krok ve směru vektoru rychlosti daného objektu
        """
        x, y = self.micek.get_pos()     #získání pozice míčku
        if x + (1/2*self.micek.r) >= self.W or x - (1/2*self.micek.r)<= 0:      #zkontrolování jestli míček neprojel x
            self.odraz_x()  #odražení míčku
        if y + (1/2*self.micek.r) >= self.H or y - (1/2*self.micek.r)<= 0:      #zkontrolování jestli míček neprojel y
            self.odraz_y()  #odražení míčku
        self.micek.krok()
        px, py = self.palka.get_pos()
        if (py <= 0) or (py >= self.H):
            self.palka.otoc()
            self.palka.krok()
            self.palka.krok()
        else:
            self.palka.krok()
        self.after(20, self.udelej_krok)

    def palka_up(self, udalost):
        self.palka.set_rychlost([0, -5])

    def palka_down(self, udalost):
        self.palka.set_rychlost([0, 5])

    def palka_stop(self, udalost):
        self.palka.set_rychlost([0, 0])

    def odraz_x(self):
        self.micek.rychlost[0] = self.micek.rychlost[0] * -1        #přenastavení rychlosti ve směru x na opačnou hodnotu

    def odraz_y(self):
        self.micek.rychlost[1] = self.micek.rychlost[1] * -1        #přenastavení rychlosti ve směru x na opačnou hodnotu


####################################################################
##### HLAVNÍ PROGRAM
if __name__ == "__main__":
    # vytvoříme aplikaci GUI, titulek okna je "Moje okno"
    #    okno má rozměry 400, 300 a barvu pozadí "dark green"
    app = App("Pong", 400, 300, barva="dark green")
    # rozběhneme aplikaci
    app.run()
#### KONEC SOUBORU


