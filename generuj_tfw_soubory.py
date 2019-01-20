'''
Created on Nov, 2018

@author: Liba Poustkova
'''

import math
import os
import re
#import generuj_klady as gen
from pathlib import Path

import tkinter
from tkinter import ttk
import sys
from tkinter import filedialog
from tkinter import *

def meritko_4x4(jmeno, dx, dy, fX,fY, delitko, cis, znaky):
    jmeno = jmeno + delitko + str(cis+1)
    if cis == 0:
        ffX = fX
        ffY = fY
    elif cis == 1:
        ffX = fX
        ffY = fY - dy

    elif cis == 2:
        ffX = fX  + dx
        ffY = fY

    elif cis == 3:
        ffX = fX + dx
        ffY = fY - dy
    return ffX, ffY, jmeno

def GenerujKlady(List_kladu, Mer, maplist,sourXY):
#generuje list naplneny mapovymi listy se souradnicemi levych rohu
    for i in range(10):
        for j in range(10):
            fsoub_jmeno_5 = maplist + '_' + str(i) + '_' + str(j)
            fX = sourXY[0] + 2000 * j
            fY = sourXY[1] + 2500 * (i + 1)
            if Mer<5000:
                for k in range(4):
                    fX_2,fY_2,fsoub_jmeno_2= meritko_4x4(fsoub_jmeno_5, 1000, 1250, fX,fY, '_',k, '1234')
                    if Mer<2000:
                        for l in range (4):
                            fX_1,fY_1,fsoub_jmeno_1= meritko_4x4(fsoub_jmeno_2, 500, 625,  fX_2,fY_2, '',l, '1234')
                            if Mer<1000:
                                for m in range(4):
                                    fX_500, fY_500, fsoub_jmeno_500 = meritko_4x4(fsoub_jmeno_1, 250,312.5, fX_1,fY_1, '',m, '1234')
                                    List_kladu.append([fX_500, fY_500, fsoub_jmeno_500])
                            else:List_kladu.append([fX_1, fY_1, fsoub_jmeno_1])
                    else:List_kladu.append([fX_2, fY_2, fsoub_jmeno_2])
            else:

                List_kladu.append([fX, fY, fsoub_jmeno_5])
    return List_kladu

def create_file_tfw(Y,X,pixel,jmeno):
#fce generuje vlastni tfw soubor
    jmeno=jmeno+'.tfw'
    cela_p=os.path.join(folder_path.get(),jmeno)
    try:
        with open(cela_p, mode='w', encoding='utf-8') as soubor:
            soubor.write(str(pixel)+'\n')
            soubor.write('0\n')
            soubor.write('0\n')
            soubor.write('-'+str(pixel)+'\n')
            soubor.write('-'+str(Y)+'\n')
            soubor.write('-'+str(X) +'\n')
            soubor.close()
    except:
        FileNotFoundError
        print('Cesta k souborům neexistuje')

def nacti_soubor(jmeno):
#it reads file with map. listy and coordinates
    try:
        soubor=open(jmeno,encoding='utf-8-sig')
        for radek in soubor:
            pom=radek.strip()
            ml, x, y= pom.split(";")
            MapL[ml]=[int(x),int(y)]
        soubor.close()
    except FileNotFoundError:
        print('Chybí soubor s mapovými listy')
    return MapL

#def on_select(event=None):
   # print('----------------------------')

 #   if event: # <-- this works only with bind because `command=` doesn't send event
  #      print("event.widget:", event.widget.get())

   # for i, x in enumerate(all_comboboxes):
    #    print("all_comboboxes[%d]: %s" % (i, x.get()))

def openFileDialog():
    folder_selected = filedialog.askdirectory()
    return folder_selected



def spust():
    maplist = all_comboboxes[0].get()
    meritko = int(all_comboboxes[1].get())
    pixel = float(all_comboboxes[2].get())/100
    sourXY = MapL[maplist]
    GenerujKlady(List_kladu, meritko, maplist, sourXY)
    p = folder_path

    for ml in List_kladu:
    # uprava souradnice leveho rohu na stred pixelu
        Yf = ml[1] - float(pixel) / 2
        Xf = ml[0] + float(pixel) / 2
        name = ml[2]
        create_file_tfw(Yf, Xf, pixel, name)
    List_kladu.clear()


def browse_button():
# Allow user to select a directory and store it in global var
# called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    return filename

def exit():
    sys.exit(0)

root = tkinter.Tk()
MapL={}
List_kladu = []

nacti_soubor('soubor.txt')
map_list=(tuple(MapL.keys()))
#print(map_list)
#empty list from select of combobox
all_comboboxes = []


cb1 = ttk.Combobox(root, values=sorted(map_list))
cb1.set("As")
all_comboboxes.append(cb1)

#combobox for scale
cb2 = ttk.Combobox(root, values=("5000", "2000", "1000", "500"))
cb2.set("5000")
#cb2.bind('<<ComboboxSelected>>', on_select)
all_comboboxes.append(cb2)
#b = tkinter.Button(root, text="Show all selections", command=on_select)
#combobox for size of pixel
cb3 = ttk.Combobox(root, values=(5, 10, 12.5,20,25,50))
cb3.set(5)
#cb3.bind('<<ComboboxSelected>>', on_select)
all_comboboxes.append(cb3)
folder_path = StringVar()
openFileButton = ttk.Button(root,text="Vyber adresář", command=browse_button)#openFileDialog)

style = ttk.Style()
style.theme_use("alt")
style.configure('Red.TButton', background='#ff8080')
style.configure('Green.TButton', background='#80ff80')

label1 = ttk.Label(root, text="Vyber mapový list:")
label2 = ttk.Label(root, text="Vyber měřítko:")
label3 = ttk.Label(root, text="Vyber velikost pixelu (v cm):")
quitButton = ttk.Button(root, text="Exit", style='Red.TButton',
                        command=exit)


button1 = ttk.Button(root, text="OK - vytvoř soubory",style='Green.TButton', command=spust)
#progres=ttk.Progressbar(root, orient='horizontal', mode='determinate')
#todo paralelni vlakno bude mit parametr progress bar, s krokem )0.5


label1.grid(column=1,row=1, sticky="we", padx=6, pady=6)
label2.grid(column=1,row=2, sticky="we", padx=6, pady=6)
label3.grid(column=1,row=3, sticky="we", padx=6, pady=6)


cb1.grid(column=2,row=1,sticky="we", padx=6, pady=6)
cb2.grid(column=2,row=2,sticky="we", padx=6, pady=6)
cb3.grid(column=2,row=3,sticky="we", padx=6, pady=6)

openFileButton.grid(column=1, row=4,sticky="we", padx=6, pady=6)
button1.grid(column=1, row=5, sticky="we", padx=6, pady=6)

quitButton.grid(column=1, row=7, sticky="we", padx=6, pady=6)

mainloop()



