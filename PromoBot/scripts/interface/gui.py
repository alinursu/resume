autor = "Ursu Alin"
import sys
import os
from tkinter import *
import threading

from scripts.interface.gui_utils import App, browser
from scripts import utils
from scripts.scrappers.altex import html_part_link as altex_categ
from scripts.scrappers.cel import html_part_link as cel_categ
from scripts.scrappers.emag import html_part_link as emag_categ
from scripts.scrappers.sportvision import html_part_link as sportvision_categ
from scripts.CEL.cel_string import formare_link_partial_cautare_personalizata as cel_link_partial
from scripts.EMAG.emag_string import formare_link_partial_cautare_personalizata as emag_link_partial
from scripts.SPORTVISION.sportivision_string import formare_link_partial_cautare_personalizata as sportvision_link_partial
from scripts.scrappers.altex import Altex
from scripts.scrappers.cel import Cel
from scripts.scrappers.constantinnautics import ConstantinNautics
from scripts.scrappers.emag import Emag
from scripts.scrappers.sportvision import Sportvision
from scripts.scrappers.lavas import Lavas
from scripts.scrappers.pronutrition import ProNutrition

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
logopath = path + "bin" + slash + "data" + slash + "logo" + slash
logos = {"Altex":logopath + "altex.png",
         "Cel":logopath + "cel.png",
         "Constantinnautics":logopath+"constantinnautics.png",
         "Emag":logopath + "emag.png",
         "Sportvision":logopath + "sportvision.png"}
htmlpath = path + "bin" + slash + "html" + slash
datapath = path + "bin" + slash + "data" + slash
smallbackground = "small.png"
largebackground = "large.png"
color_magenta = "#b20837"
color_black = "#292728"
color_gray = "#e7e7e7"

def fereastra_vizualizare():
    """
    Fereastra prin care utilizatorul vizualizeaza fisierele HTML.
    :return:
    """
    global htmls
    htmls = os.listdir(htmlpath)
    global n
    n = 0
    link = "file://" + htmlpath + "{}"
    def event_urmator(event):
        global n
        if n == len(htmls)-1:
            n = 0
        else:
            n = n + 1
        br.schimbare_link(link.format(htmls[n]))
    def event_anterior(event):
        global n
        if n == 0:
            n = len(htmls)-1
        else:
            n = n - 1
        br.schimbare_link(link.format(htmls[n]))
    def event_stergere(event):
        if root.messagebox(3, "Confirmare", "Doriti sa stergeti acest produs din lista?") == True:
            global htmls
            global n
            os.chdir(htmlpath)
            os.remove(htmls[n])
            os.chdir(path)
            htmls = os.listdir(htmlpath)
            if n == len(htmls):
                n = 0
            br.schimbare_link(link.format(htmls[n]))
    def event_inchidere(event):
        try:
            br.inchidere()
        except:
            pass
        root.inchidere()
    br = browser()
    br.schimbare_link(link.format(htmls[n]))

    root = App("Vizualizare fisiere HTML", "450x200+150+150")
    root.amplasare_colt_dreapta_sus()

    font = root.creare_font("Times New Roman", 13)
    fundal = root.add_imagine(datapath + smallbackground, lungime=451, latime=201)
    btn_urmatorul = root.add_button("Urmatorul →", font=font, lungime=10, latime=1, bg=color_magenta, fg=color_gray)
    btn_anteriorul = root.add_button("← Anteriorul", font=font, lungime=10, latime=1, bg=color_magenta, fg=color_gray)
    btn_stergere = root.add_button("Stergere ↑", font=font, lungime=10, latime=1, bg=color_magenta, fg=color_gray)
    btn_inchidere = root.add_button("Inchidere", font=font, lungime=10, latime=1, bg=color_magenta, fg=color_gray)
    root.adaugare_comanda("<Right>", event_urmator)
    root.adaugare_comanda("<Left>", event_anterior)
    root.adaugare_comanda("<Up>", event_stergere)
    btn_urmatorul.adaugare_comanda("<Button-1>", event_urmator)
    btn_anteriorul.adaugare_comanda("<Button-1>", event_anterior)
    btn_stergere.adaugare_comanda("<Button-1>", event_stergere)
    btn_inchidere.adaugare_comanda("<Button-1>", event_inchidere)

    btn_stergere.plasare(x=225, y=30)
    btn_anteriorul.plasare(x=150, y=70)
    btn_urmatorul.plasare(x=300, y=70)
    btn_inchidere.plasare(x=225, y=140)

    fundal.plasare(x=-1, y=-1)

    root.mainloop()

def fereastra_cautare(setari):
    """
    Functie ce efectueaza cautarea in timp ce se afiseaza progresul acesteia.
    :param setari:
    :return:
    """
    def scrapper(setari):
        """
        Functie ce va fi folosit ca si thread 1 ce are rolul de a face cautarile.
        :param setari:
        :return:
        """
        if setari["tip_cautare"] == "categorie":
            if setari["site"] == "Altex":
                Altex(setari["categorie"][-1], setari["suma"][-1], setari["pagini"][-1])
            elif setari["site"] == "Cel":
                Cel(setari["categorie"][-1], setari["pagini"][-1])
            elif setari["site"] == "ConstantinNautics":
                ConstantinNautics()
            elif setari["site"] == "Emag":
                Emag(setari["categorie"][-1], setari["suma"][-1], setari["pagini"][-1])
            elif setari["site"] == "Sportvision":
                Sportvision(setari["categorie"][-1], setari["pagini"][-1])
            elif setari["site"] == "Lavas":
                Lavas()
            elif setari["site"] == "Pro Nutrition":
                ProNutrition(setari["pagini"][-1])
        elif setari["tip_cautare"] == "personalizata":
            if setari["site"] == "Emag":
                Emag(emag_link_partial(setari["cuvinte"][-1]), None, setari["pagini"][-1], cautare="personalizata")
            elif setari["site"] == "Cel":
                Cel(cel_link_partial(setari["cuvinte"][-1]), setari["pagini"][-1], cautare="personalizata")
            elif setari["site"] == "Sportvision":
                Sportvision(sportvision_link_partial(setari["cuvinte"][-1]), setari["pagini"][-1], cautare="personalizata")
    def app(setari):
        """
        Functie ce are rolul de a afisa progresul cautarii.
        :param setari:
        :return:
        """
        def event_gif(n=0):
            global timer_id
            gif = giflist[n%len(giflist)]
            canvas.stergere_elemente()
            canvas.creare_imagine(imagine=gif, lungime=gif.width()//2, latime=gif.height()//2)
            if t1.is_alive():
                timer_id = root.after(100, event_gif, n+1)
            else:
                canvas.stergere_elemente()
                root.after_cancel(timer_id)
                canvas.ascundere()
                img_finalizat.plasare(x=395, y=30)
                lbl_finalizat.plasare(x=390, y=183)
                dupa = utils.numar_fisiere_html_prezente()
                lbl_numar_gasite.configure(text="Au fost gasite {} produse conform preferintelor.".format(dupa-inainte))
                lbl_numar_gasite.plasare(x=270, y=205)
                btn_finalizare.activare()
                root.modificare_titlu("Cautare finalizata!")
                for lbl in lbl_info:
                    lbl.ascundere()

        def event_btn(event):
            if not t1.is_alive():
                root.inchidere()
                if utils.numar_fisiere_html_prezente() != 0:
                    fereastra_vizualizare()

        gifpath = datapath + "gif" + slash
        _ = ["frame_{}.png".format(i) for i in range(1, 25)]
        imgfn = "checked.png"
        global timer_id
        timer_id = "after#0"
        inainte = utils.numar_fisiere_html_prezente()

        font = root.creare_font("Times New Roman", 15)
        font2 = root.creare_font("Times New Roman", 12)
        fundal = root.add_imagine(datapath + smallbackground, lungime=742, latime=301)


        __ = PhotoImage(file="{}{}".format(gifpath, _[0]))
        canvas = root.add_canvas(lungime=300, latime=198)

        # O lista cu elemente de tip LABEL, fiecare element continand cate o informatie despre procesul de cautare
        lbl_info = []
        __ = root.add_label("Site: {}".format(setari["site"]), fg=color_magenta, bg=color_gray, font=font2)
        lbl_info.append(__)
        if setari["tip_cautare"] == "categorie":
            __ = root.add_label("Tip cautare: normala", fg=color_magenta, bg=color_gray, font=font2)
        else:
            __ = root.add_label("Tip cautare: {}".format(setari["tip_cautare"]), fg=color_magenta, bg=color_gray, font=font2)
        lbl_info.append(__)
        if "categorie" in setari.keys():
            if setari["categorie"][0] == True:
                __ = root.add_label("Categorie: {}".format(setari["categorie"][1]), fg=color_magenta, bg=color_gray, font=font2)
                lbl_info.append(__)
        elif "cuvinte" in setari.keys():
            if setari["cuvinte"][0] == True:
                __ = root.add_label("Cuvinte cheie: {}".format(setari["cuvinte"][1]), fg=color_magenta, bg=color_gray, font=font2)
                lbl_info.append(__)
        if setari["pagini"][0] == True:
            __ = root.add_label("Numar pagini: {}".format(setari["pagini"][1]), fg=color_magenta, bg=color_gray, font=font2)
            lbl_info.append(__)
        if setari["suma"][0] == True:
            __ = root.add_label("Suma maxima: {}".format(setari["suma"][1]), fg=color_magenta, bg=color_gray, font=font2)
            lbl_info.append(__)
        _y = 170
        for lbl in lbl_info:
            lbl.plasare(x=30, y=_y)
            _y = _y + 20

        giflist = []
        for img in _:
            photo = PhotoImage(file="{}{}".format(gifpath, img))
            giflist.append(photo)

        img_finalizat = root.add_imagine(datapath + imgfn, lungime=150, latime=150)
        lbl_finalizat = root.add_label("Cautare finalizata!", fg=color_magenta, bg=color_gray, font=font)
        lbl_numar_gasite = root.add_label("Au fost gasite {} produse conform preferintelor.", fg=color_magenta, bg=color_gray, font=font)
        btn_finalizare = root.add_button("Finalizare", 10, 1, fg=color_gray, bg=color_magenta, font=font)
        btn_finalizare.adaugare_comanda("<Button-1>", event_btn)
        btn_finalizare.dezactivare()

        fundal.plasare(x=-1, y=-1)
        canvas.plasare(x=318, y=30)
        btn_finalizare.plasare(x=403, y=235)

        root.after(100, event_gif)


    root = App("Cautare...", "741x300+100+100")
    root.centrare()
    t1 = threading.Thread(target=scrapper, args=[setari])
    t2 = threading.Thread(target=app, args=[setari])

    t2.start()
    t1.start()

    root.mainloop()

    t2.join()
    t1.join()

def fereastra_aplicatie():
    """
    Fereastra in care utilizatorul alege site-ul de pe care vor fi cautate informatii.
    :return:
    """
    # Valorile "settings":
    #   - 0 : nu necesita setari
    #   - 1 : necesita doar alegerea sumei maxime
    #   - 2 : necesita doar alegerea numarului de pagini
    #   - 3 : necesita doar alegerea categoriei
    #   - 4 : necesita doar alegerea sumei maxime si a categoriei
    #   - 5 : necesita doar alegerea numarului de pagini si a categoriei
    #   - 9 : necesita alegerea tuturor setarilor
    # Valorile "personalizata":
    #   - 0 : nu suporta cautarea personalizata
    #   - 1 : suporta cautarea personalizata
    data = {
        1: {"title": "Altex", "categorie": "Electronice si electrocasnice", "img": "altex.png", "pozitie": [88, 280],
            "settings": 9, "el_per_pag": 48, "personalizata": 0, "pozitie_img":[30, 310], "img_pixeli":350,
            "categorii":[key for key in altex_categ.keys()]},
        2: {"title": "Cel", "categorie": "Electronice si electrocasnice", "img": "cel.png", "pozitie": [88, 280],
            "settings": 5, "el_per_pag": 35, "personalizata": 1, "pozitie_img":[30, 310], "img_pixeli":350,
            "categorii": [key for key in cel_categ.keys()]},
        3: {"title": "ConstantinNautics", "categorie": "Accesorii", "img": "constantinnautics.png",
            "pozitie": [166, 240], "settings": 0, "el_per_pag": 40, "personalizata": 0, "pozitie_img":[30, 270],
            "img_pixeli":350, "categorii":['--------------']},
        4: {"title": "Emag", "categorie": "Electronice si electrocasnice", "img": "emag.png", "pozitie": [88, 280],
            "settings": 9, "el_per_pag": 60, "personalizata": 1, "pozitie_img":[30, 310], "img_pixeli":350,
            "categorii": [key for key in emag_categ.keys()]},
        5: {"title": "Sportvision", "categorie": "Imbracaminte si incaltaminte", "img": "sportvision.png",
            "pozitie": [86, 280], "settings": 5, "el_per_pag": 48, "personalizata": 1, "pozitie_img":[30, 310],
            "img_pixeli":350, "categorii":[key for key in sportvision_categ.keys()]},
        6: {"title": "Lavas", "categorie": "Accesorii", "img": "lavas.png", "pozitie": [167, 223], "settings": 0,
            "el_per_pag": 30, "personalizata": 0, "pozitie_img":[100, 250], "img_pixeli":210,
            "categorii":['--------------']},
        7: {"title": "Pro Nutrition", "categorie": "Suplimente nutritive", "img": "pronutrition.png",
            "pozitie": [121, 240], "settings": 2, "el_per_pag": 12, "personalizata": 0, "pozitie_img":[100, 271],
            "img_pixeli":210, "categorii":['--------------']}
        }
    global d
    d = 1

    def ultimul_index_data():
        _ = 0
        for key in data.keys():
            _ = key
        return _

    def event_next(event):
        global d
        global img
        if d == ultimul_index_data():
            d = 1
        else:
            d = d + 1
        # Actualizez descrierea site-ului, repozitionez textul si modific imaginea
        lbl_categorie.editare_text(data[d]["categorie"])
        lbl_categorie.plasare(x=data[d]["pozitie"][0], y=data[d]["pozitie"][1])
        img.place_forget()
        _ = utils.redimensionare_imagine2(logopath + data[d]["img"], data[d]["img_pixeli"])
        img = root.add_imagine(logopath + data[d]["img"], lungime=_[0], latime=_[1])
        img.plasare(x=data[d]["pozitie_img"][0], y=data[d]["pozitie_img"][1])
        cbox_categ.schimbare_valori(data[d]["categorii"])

        # Actualizez elementele aplicatiei in functie de 'settings'
        if data[d]["settings"] == 5:
            tbox_suma.dezactivare()
            tbox_pagini.activare()
        elif data[d]["settings"] == 0:
            tbox_suma.dezactivare()
            tbox_pagini.dezactivare()
        elif data[d]["settings"] == 2:
            tbox_suma.dezactivare()
            tbox_pagini.activare()
        elif data[d]["settings"] == 9:
            tbox_suma.activare()
            tbox_pagini.activare()
        if data[d]["personalizata"] == 0:
            tbox_pagini_2.dezactivare()
            tbox_cuvinte.dezactivare()
            btn_personalizata.dezactivare()
        elif data[d]["personalizata"] == 1:
            tbox_pagini_2.activare()
            tbox_cuvinte.activare()
            btn_personalizata.activare()

    def event_previous(event):
        global d
        global img
        if d == 1:
            d = ultimul_index_data()
        else:
            d = d - 1
        # Actualizez descrierea site-ului, repozitionez textul si modific imaginea
        lbl_categorie.editare_text(data[d]["categorie"])
        lbl_categorie.plasare(x=data[d]["pozitie"][0], y=data[d]["pozitie"][1])
        img.place_forget()
        _ = utils.redimensionare_imagine2(logopath + data[d]["img"], data[d]["img_pixeli"])
        img = root.add_imagine(logopath + data[d]["img"], lungime=_[0], latime=_[1])
        img.plasare(x=data[d]["pozitie_img"][0], y=data[d]["pozitie_img"][1])
        cbox_categ.schimbare_valori(data[d]["categorii"])

        # Actualizez elementele aplicatiei in functie de 'settings'
        if data[d]["settings"] == 5:
            tbox_suma.dezactivare()
            tbox_pagini.activare()
        elif data[d]["settings"] == 0:
            tbox_suma.dezactivare()
            tbox_pagini.dezactivare()
        elif data[d]["settings"] == 2:
            tbox_suma.dezactivare()
            tbox_pagini.activare()
        elif data[d]["settings"] == 9:
            tbox_suma.activare()
            tbox_pagini.activare()
        if data[d]["personalizata"] == 0:
            tbox_pagini_2.dezactivare()
            tbox_cuvinte.dezactivare()
            btn_personalizata.dezactivare()
        elif data[d]["personalizata"] == 1:
            tbox_pagini_2.activare()
            tbox_cuvinte.activare()
            btn_personalizata.activare()

    def event_cautare_categorie(event):
        global d
        ok = 1
        setari = {"site":data[d]["title"],"tip_cautare":"categorie"}
        if data[d]["settings"] == 0:
            setari["suma"] = [False]
            setari["pagini"] = [False]
            setari["categorie"] = [False]
        elif data[d]["settings"] == 2:
            pagini = tbox_pagini.text()

            if len(pagini) == 0:
                root.messagebox(1, "Atentie!", "Va rog sa completati toate campurile disponibile!")
                ok = 0
            else:
                if int(pagini) > 10:
                    root.messagebox(1, "Atentie!", "Numarul de pagini ales este prea mare!")
                    ok = 0
                else:
                    setari["suma"] = [False]
                    setari["pagini"] = [True, int(pagini)]
                    setari["categorie"] = [False]
        elif data[d]["settings"] == 5:
            pagini = tbox_pagini.text()
            categ = cbox_categ.Variabila.get()

            if len(pagini) == 0 or len(categ) == 0:
                root.messagebox(1, "Atentie!", "Va rog sa completati toate campurile disponibile!")
                ok = 0
            else:
                if int(pagini) > 10:
                    root.messagebox(1, "Atentie!", "Numarul de pagini ales este prea mare!")
                    ok = 0
                else:
                    setari["suma"] = [False]
                    setari["pagini"] = [True, int(pagini)]
                    setari["categorie"] = [True, categ]
        elif data[d]["settings"] == 9:
            suma = tbox_suma.text()
            pagini = tbox_pagini.text()
            categ = cbox_categ.Variabila.get()

            if len(suma) == 0 or len(pagini) == 0 or len(categ) == 0:
                root.messagebox(1, "Atentie!", "Va rog sa completati toate campurile disponibile!")
                ok = 0
            else:
                if int(suma) > 999999:
                    root.messagebox(1, "Atentie!", "Suma maxima aleasa este prea mare!")
                    ok = 0
                elif int(pagini) > 10:
                    root.messagebox(1, "Atentie!", "Numarul de pagini ales este prea mare!")
                    ok = 0
                else:
                    setari["suma"] = [True, int(suma)]
                    setari["pagini"] = [True, int(pagini)]
                    setari["categorie"] = [True, categ]

        if ok == 1:
            root.inchidere()
            fereastra_cautare(setari)

    def event_cautare_personalizata(event):
        global d
        ok = 1
        setari = {"site": data[d]["title"], "tip_cautare":"personalizata"}
        if data[d]["personalizata"] == 0:
            root.messagebox(1, "Atentie!", "Pe acest site nu se poate efectua o cautare personalizata!")
            ok = 0
        else:
            keywords = tbox_cuvinte.text()
            pagini = tbox_pagini_2.text()

            if len(keywords) == 0 or len(pagini) == 0:
                root.messagebox(1, "Atentie!", "Va rog sa completati toate campurile disponibile!")
                ok = 0
            else:
                if int(pagini) > 10:
                    root.messagebox(1, "Atentie!", "Numarul de pagini ales este prea mare!")
                    ok = 0
                else:
                    setari["cuvinte"] = [True, keywords]
                    setari["pagini"] = [True, int(pagini)]

        if ok == 1:
            setari["suma"] = [False]
            root.inchidere()
            fereastra_cautare(setari)


    root = App("Selectare site", "1000x550+100+100")
    root.centrare()

    font = root.creare_font("Times New Roman", 15)
    fundal = root.add_imagine(datapath + largebackground, lungime=1001, latime=551)
    _ = utils.redimensionare_imagine2(logopath + data[d]["img"], data[d]["img_pixeli"])
    global img
    img = root.add_imagine(logopath + data[d]["img"], lungime=_[0], latime=_[1])
    next_btn = root.add_button("Inainte →", lungime=10, latime=1, bg=color_magenta, fg="white", font=font)
    prev_btn = root.add_button("← Inapoi", lungime=10, latime=1, bg=color_magenta, fg="white", font=font)
    next_btn.adaugare_comanda("<Button-1>", event_next)
    prev_btn.adaugare_comanda("<Button-1>", event_previous)
    lbl_categorie = root.add_label(data[d]["categorie"], fg=color_magenta, bg=color_gray, font=font)
    root.adaugare_comanda("<Right>", event_next)
    root.adaugare_comanda("<Left>", event_previous)

    fundal.plasare(x=-1, y=-1)
    img.plasare(x=data[d]["pozitie_img"][0], y=data[d]["pozitie_img"][1])
    prev_btn.plasare(x=35, y=470)
    next_btn.plasare(x=235, y=470)
    lbl_categorie.plasare(x=data[d]["pozitie"][0], y=data[d]["pozitie"][1])

    # Cautare dupa categorie
    frame_categ = root.add_imagine(datapath + "frame.png", 300, 170)
    lbl_info_1 = root.add_label("Cautare dupa categorie", fg=color_magenta, bg=color_gray, font=font)
    lbl_suma = root.add_label("Suma maxima: ", fg=color_magenta, bg=color_gray, font=font)
    tbox_suma = root.add_textbox(lungime=14, font=font, bg=color_magenta, fg="white")
    lbl_pagini = root.add_label("Numar pagini: ", fg=color_magenta, bg=color_gray, font=font)
    tbox_pagini = root.add_textbox(lungime=14, font=font, bg=color_magenta, fg="white")
    lbl_categ = root.add_label("Categorie: ", fg=color_magenta, bg=color_gray, font=font)
    cbox_categ = root.add_combobox(data[d]["categorii"], lungime=13, font=font)
    cbox_categ.stilzare(bg=color_magenta, bg_select=color_magenta, bg_field=color_magenta, fg=color_gray)
    cbox_categ.dezactivare()
    btn_categ = root.add_button("Cautare", 11, 1, fg=color_gray, bg=color_magenta, font=font)
    btn_categ.adaugare_comanda("<Button-1>",event_cautare_categorie)

    frame_categ.plasare(x=412, y=90)
    lbl_info_1.plasare(x=470, y=95)
    lbl_suma.plasare(x=425, y=125)
    tbox_suma.plasare(x=552, y=126)
    lbl_pagini.plasare(x=429, y=155)
    tbox_pagini.plasare(x=552, y=156)
    lbl_categ.plasare(x=461, y=185)
    cbox_categ.plasare(x=552, y=186)
    btn_categ.plasare(x=495, y=215)

    # Cautare personalizata
    frame_personalizata= root.add_imagine(datapath + "frame.png", 300, 140)
    lbl_info_2 = root.add_label("Cautare personalizata", fg=color_magenta, bg=color_gray, font=font)
    lbl_cuvinte = root.add_label("Cuvinte cheie: ", fg=color_magenta, bg=color_gray, font=font)
    tbox_cuvinte = root.add_textbox(lungime=14, font=font, bg=color_magenta, fg="white")
    lbl_pagini_2 = root.add_label("Numar pagini: ", fg=color_magenta, bg=color_gray, font=font)
    tbox_pagini_2 = root.add_textbox(lungime=14, font=font, bg=color_magenta, fg="white")
    btn_personalizata = root.add_button("Cautare", 11, 1, fg=color_gray, bg=color_magenta, font=font)
    btn_personalizata.adaugare_comanda("<Button-1>", event_cautare_personalizata)

    if data[d]["personalizata"] == 0:
        tbox_cuvinte.dezactivare()
        tbox_pagini_2.dezactivare()
        btn_personalizata.dezactivare()

    frame_personalizata.plasare(x=412, y=325)
    lbl_info_2.plasare(x=477, y=330)
    lbl_cuvinte.plasare(x=429, y=360)
    tbox_cuvinte.plasare(x=552, y=361)
    lbl_pagini_2.plasare(x=429, y=390)
    tbox_pagini_2.plasare(x=552, y=391)
    btn_personalizata.plasare(x=495, y=421)


    root.mainloop()

def vizualizare_html_vechi():
    """
    O fereastra a aplicatiei prin care utilizatorul alege sa vizualizeze produsele gasite din cautarile anterioare sau
    sa caute alte produse. Fereastra se deschide doar daca acesta opteaza pentru a nu se stearga vechile produse
    gasite.
    :return:
    """
    def event_btn_da(event):
        root.inchidere()
        fereastra_vizualizare()

    def event_btn_nu(event):
        root.inchidere()
        fereastra_aplicatie()

    root = App("Vizualizare fisiere HTML vechi", "500x200+100+100")
    root.centrare()

    font = root.creare_font("Times New Roman", 16)
    fundal = root.add_imagine(datapath + smallbackground, lungime=501, latime=201)
    lbl_intrebare = root.add_label(text="Doriti sa vizualizati fisierele HTML", font=font, bg=color_gray, fg=color_magenta)
    lbl_intrebare2 = root.add_label(text="din cautarile anterioare?", font=font, bg=color_gray, fg=color_magenta)
    btn_da = root.add_button("DA", lungime=8, latime=1, font=font, bg=color_magenta, fg="white")
    btn_nu = root.add_button("NU", lungime=8, latime=1, font=font, bg=color_magenta, fg="white")
    btn_da.adaugare_comanda("<Button-1>", event_btn_da)
    btn_nu.adaugare_comanda("<Button-1>", event_btn_nu)

    fundal.plasare(x=-1, y=-1)
    lbl_intrebare.plasare(x=160, y=50)
    lbl_intrebare2.plasare(x=207, y=73)
    btn_da.plasare(x=150, y=140)
    btn_nu.plasare(x=360, y=140)


    root.mainloop()

def stergere_html_vechi():
    """
    O fereastra a aplicatiei prin care utilizatorul alege daca se vor sterge html-urile formate in cautarile anterioare,
    alaturi de imaginile asociate acestora, sau daca nu.
    :return:
    """
    def apasare_btn_nu(event):
        root.inchidere()
        vizualizare_html_vechi()
    def apasare_btn_da(event):
        utils.stergere_html()
        root.inchidere()
        fereastra_aplicatie()
    root = App("Stergere fisiere HTML vechi", "500x200+100+100")
    root.centrare()

    font = root.creare_font("Times New Roman", 16)
    fundal = root.add_imagine(datapath + smallbackground, lungime=501, latime=201)
    lbl_detect = root.add_label(text="Au fost detectate fisiere HTML din", font=font, fg=color_magenta, bg=color_gray)
    lbl_detect2 = root.add_label(text="cautarile anterioare.", font=font, fg=color_magenta, bg=color_gray)
    lbl_intrebare = root.add_label(text="Doriti ca aceste fisiere sa fie sterse?", font=font, fg=color_magenta, bg=color_gray)
    btn_da = root.add_button("DA", lungime=8, latime=1, font=font, fg="white", bg=color_magenta)
    btn_nu = root.add_button("NU", lungime=8, latime=1, font=font, fg="white", bg=color_magenta)
    btn_da.adaugare_comanda("<Button-1>", apasare_btn_da)
    btn_nu.adaugare_comanda("<Button-1>", apasare_btn_nu)

    fundal.plasare(x=-1, y=-1)
    lbl_detect.plasare(x=165, y=30)
    lbl_detect2.plasare(x=230, y=53)
    lbl_intrebare.plasare(x=165, y=90)
    btn_da.plasare(x=150, y=140)
    btn_nu.plasare(x=360, y=140)

    root.mainloop()

def fereastra_autor():
    """
    Fereastra in care se afiseaza informatii despre autor.
    :return:
    """
    def event_btn(event):
        if utils.numar_fisiere_html_prezente() != 0:
            root.inchidere()
            stergere_html_vechi()
        else:
            root.inchidere()
            fereastra_aplicatie()

    root = App("Autor", "500x200+100+100")
    root.centrare()

    font = root.creare_font("Times New Roman", 16)
    fundal = root.add_imagine(datapath + smallbackground, lungime=501, latime=201)
    lbl_autor = root.add_label("Autor: Ursu Alin", fg=color_magenta, bg=color_gray, font=font)
    btn_continuare = root.add_button("Continuare", 10, 1, bg=color_magenta, fg="white", font=font)
    btn_continuare.adaugare_comanda("<Button-1>", event_btn)

    fundal.plasare(x=-1, y=-1)
    lbl_autor.plasare(x=240, y=60)
    btn_continuare.plasare(x=245, y=130)

    root.mainloop()

def GUI(afisare_fereastra_autor):
    """
    Programul principal in formatul aplicatiei.
    :param afisare_fereastra_autor:
    :return:
    """
    if afisare_fereastra_autor == True:
        fereastra_autor()
    else:
        if utils.numar_fisiere_html_prezente() != 0:
            stergere_html_vechi()
        else:
            fereastra_aplicatie()
