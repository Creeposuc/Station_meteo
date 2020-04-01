# import serial
from tkinter import *
from tkinter.messagebox import *
import time
from random import randint
import csv
import os
port="COM4"
liste_des_humiditees =[]
liste_des_temperature =[]

temperature_actuelle=0
humidite_actuelle=0
fenetre =Tk()
###########################  Affichage   #######################################
def Affichage_console(valeurs,moyenne, maximum, minimum):
    print("valeurs:", valeurs,"\nmoyenne:", moyenne,"\nmaximum:", maximum,"\nminimum:", minimum)
def affichage_tkinter():
    global case_nombre_mesure, valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite
    #############################menu déroulant  ###############################
    bar_de_menu = Menu(fenetre)

    Menu_fichier = Menu(bar_de_menu, tearoff=0)
    Menu_fichier.add_command(label = "Enregistrer")
    Menu_fichier.add_command(label = "Remise à zéro", command=remise_a_zero)
    Menu_fichier.add_separator()
    Menu_fichier.add_command(label = "Quitter", command=exit)
    bar_de_menu.add_cascade(label="Fichier", menu=Menu_fichier)

    Menu_aide = Menu(bar_de_menu, tearoff=0)
    Menu_aide.add_command(label = "Voir l'aide")
    Menu_aide.add_separator()
    Menu_aide.add_command(label = "Qui sommes nous ?")
    bar_de_menu.add_cascade(label="Aide", menu=Menu_aide)

    fenetre.config(menu=bar_de_menu)
    #############################zone de commande###############################
    titre1 =Label(fenetre, text="Zone de contrôle").grid(row=0 ,column=1, columnspan=2)

    case_nombre_mesure = Spinbox(fenetre, from_=1, to=43200 )# une journe de mesure maximum
    case_nombre_mesure.grid(row=1 ,column=0,columnspan=2)


    boutton_demarage = Button(fenetre, text = "Demarrer la mesure",command=demarrage, bg="red")
    boutton_demarage.grid(row=1 ,column=2, columnspan=2)

    ##########################zone d'affichage valeur simple####################
# def Affichage_une_mesure():
    titre_affichage_une_valeur = Label(fenetre, text="Valeur actuelle").grid(row=2   ,column=1, columnspan=2)

    affichage_temperature_une_valeur = Label(fenetre, text="Temperature :").grid(row=3 ,column=0, columnspan=2)

    valeur_temperature = Label(fenetre, text="-")
    valeur_temperature.grid(row=3, column=2)

    affichage_humidite_une_valeur = Label(fenetre, text="Taux d'humidite :").grid(row=4, column=0, columnspan=2 )

    valeur_humidite = Label(fenetre, text="-")
    valeur_humidite.grid(row=4, column=2)

    ##########################zone d'afichage plusieurs valeurs ################
# def Affichage_plusieurs_mesures():
    titre_affichage_plusieurs_valeurs = Label(fenetre, text="Analyse").grid(row=5   ,column=1, columnspan=2)

    affichage_temperature_plusieurs_valeur = Label(fenetre, text="Temperature :").grid(row=6 ,column=0)

    affichage_min_temperature = Label(fenetre, text="Valeurs minimum :").grid(row=6, column=1)

    valeur_min_temperature = Label(fenetre, text="-")
    valeur_min_temperature.grid(row=7, column=1)

    affichage_max_temperature = Label(fenetre, text="Valeurs maximum :").grid(row=6, column=2)

    valeur_max_temperature = Label(fenetre, text="-")
    valeur_max_temperature.grid(row=7, column=2)

    affichage_moyenne_temperature = Label(fenetre, text="Moyenne :").grid(row=6, column=3)

    valeur_moyenne_temperature = Label(fenetre, text="-")
    valeur_moyenne_temperature.grid(row=7, column=3)

    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    affichage_humidite_plusieurs_valeur = Label(fenetre, text="Taux d'humidite :").grid(row=8, column=0)

    affichage_min_humidite = Label(fenetre, text="Valeurs minimum :").grid(row=8, column=1)

    valeur_min_humidite = Label(fenetre, text="-")
    valeur_min_humidite.grid(row=9, column=1)

    affichage_max_humidite = Label(fenetre, text="Valeurs maximum :").grid(row=8, column=2)

    valeur_max_humidite = Label(fenetre, text="-")
    valeur_max_humidite.grid(row=9, column=2)

    affichage_moyenne_humidite = Label(fenetre, text="Moyenne :").grid(row=8, column=3)

    valeur_moyenne_humidite = Label(fenetre, text="-")
    valeur_moyenne_humidite.grid(row=9, column=3)

    fenetre.mainloop()
def remise_a_zero():
    if askyesno("Attention", "Êtes vous sure de vouloir faire ça?", icon="warning"):
        liste_variable=[valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite]
        for i in liste_variable:
            i.config(text = "-")
        showinfo("information", "mis à zéro!")
def recuperation_valeurs():
    global nombre_de_mesures
    nombre_de_mesures=int(case_nombre_mesure.get())
#########################initialisation########################################

def configuration():#recherche la connexion serie
    global port, inter_exter
    Systeme_exploitation = str(input("quel est votre sytème d'exploitation (w/l)?\n>>>"))
    if Systeme_exploitation=="l":
        port="/dev/ttyACM0"
    elif Systeme_exploitation=="w":
        port= "COM4"
    inter_exter = str(input("Les mesures sont à l'interrieur ou à l'exterieur (i/e)? \n>>>"))

###########################communication #######################################

def reception():
    global liste_des_humiditees, liste_des_temperature
    a=0
    communication_serie = serial.Serial(port, 9600)
    while len(liste_des_humiditees)<nombre_de_mesures and len(liste_des_temperature)<nombre_de_mesures:
        valeur = communication_serie.readline()
        valeur = str(valeur)
        print(valeur)
        if ">>>" in valeur:
            a=0
            a+=1
        elif a==1:
            liste_des_humiditees.append(float(valeur[2:][:5]))
            a+=1
        elif a==2:
            liste_des_temperature.append(float(valeur[2:][:5]))
            a=0

def simulation_reception(): #simule la reception des donnees des capteur pour pouvoir coder sans arduino
    global liste_des_humiditees, liste_des_temperature
    a=0
    for i in range(nombre_de_mesures*3):
        if a==0:
            valeur = ">>>"
            print(">>>")
        else:
            valeur = randint(0,100)
            valeur = str(valeur)
            print(valeur)
        if ">>>" in valeur:
            a=0
            a+=1
        elif a==1:
            liste_des_humiditees.append(float(valeur))
            a+=1
        elif a==2:
            liste_des_temperature.append(float(valeur))
            a=0
            # time.sleep(2)

################################# analyse #######################################
# traites les informations reçus: en liste, une par une, moyenne, max, minimum
def analyse_donnees(valeurs):
    global maximum, minimum, moyenne
    sommes_des_valeurs=0
    for i in range(len(valeurs)):
        sommes_des_valeurs+=valeurs[i]
    moyenne=round(sommes_des_valeurs/(len(valeurs)),2)
    maximum=max(valeurs)
    minimum=min(valeurs)
    Affichage_console(valeurs,moyenne, maximum, minimum)


    # if inter_exter=="e":
    #     pass #moyennes de saisons

##################################demarrage mesure et analyse ##################
def demarrage():
    # configuration()
    global liste_des_humiditees, liste_des_temperature
    liste_des_humiditees = []
    liste_des_temperature = []
    recuperation_valeurs()
    simulation_reception() #

    temperature_actuelle=liste_des_temperature[len(liste_des_temperature)-1]
    humidite_actuelle=liste_des_humiditees[len(liste_des_humiditees)-1]
    valeur_temperature.config( text =  temperature_actuelle)
    valeur_humidite.config( text =  humidite_actuelle)
    if nombre_de_mesures!=1:
        analyse_donnees(liste_des_temperature)
        valeur_min_temperature.config(text = minimum)
        valeur_max_temperature.config(text = maximum)
        valeur_moyenne_temperature.config(text = moyenne)
        analyse_donnees(liste_des_humiditees)
        valeur_min_humidite.config(text = minimum)
        valeur_max_humidite.config(text = maximum)
        valeur_moyenne_humidite.config(text = moyenne)

    fenetre.mainloop()
######################################debut ####################################
affichage_tkinter()

os.system("pause")
