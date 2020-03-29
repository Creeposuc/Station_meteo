# import serial
from tkinter import *
import time
from random import randint
import os
port="COM4"
liste_des_humiditees =[]
liste_des_temperature =[]

temperature_actuelle=0
humidité_actuelle=0

###########################Affichage     #######################################
def Affichage_console(valeurs,moyenne, maximum, minimum):
    print("valeurs:", valeurs,"\nmoyenne:", moyenne,"\nmaximum:", maximum,"\nminimum:", minimum)
def affichage_tkinter():
    global case_nombre_mesure
    fenetre =Tk()
    #############################zone de commande###############################
    titre1 =Label(fenetre, text="zone de contrôle")
    titre1.grid(row=0 ,column=0, columnspan=2)

    case_nombre_mesure = Spinbox(fenetre, from_=1, to=43200 )# une journé de mesure maximum
    case_nombre_mesure.grid(row=1 ,column=0)


    boutton_demarage = Button(fenetre, text = "Démarer la mesure",command=demarrage)
    boutton_demarage.grid(row=1 ,column=1)


    ##########################zone d'affichage valeur simple####################
    titre_affichage_une_valeur = Label(fenetre, text="Affichage des valeurs")
    titre_affichage_une_valeur.grid(row=2   ,column=0, columnspan=2)


    affichage_temperature_une_valeur = Label(fenetre, text="Température :")
    affichage_temperature_une_valeur.grid(row=3 ,column=0)

    valeur_temperature = Label(fenetre, text=temperature_actuelle)
    valeur_temperature.grid(row=3, column=1)


    affichage_humidite_une_valeur = Label(fenetre, text="Taux d'humidité :")
    affichage_humidite_une_valeur.grid(row=4, column=0 )

    valeur_humidite = Label(fenetre, text=humidité_actuelle)
    valeur_humidite.grid(row=4, column=1)

    ##########################zone d'afichage plusieurs valeurs ################
    titre_affichage_plusieurs_valeurs = Label(fenetre, text="Affichage des valeurs")
    titre_affichage_plusieurs_valeurs.grid(row=5   ,column=0, columnspan=2)


    affichage_min_temperature = Label(fenetre, text="Valeurs minimum :")
    affichage_min_temperature.grid(row=6, column=0)

    valeur_min_temperature = Label(fenetre, text=" 4")
    valeur_min_temperature.grid(row=7, column=0)

    affichage_max_temperature = Label(fenetre, text="Valeurs maximum :")
    affichage_max_temperature.grid(row=6, column=1)

    valeur_max_temperature = Label(fenetre, text=" ")
    valeur_max_temperature.grid(row=7, column=1)


    fenetre.mainloop()

def recuperation_valeurs():
    global nombre_de_mesures
    nombre_de_mesures=int(case_nombre_mesure.get())
#########################initialisation################################

# def teste_emission():
#     communication_envoie = serial.Serial(port, 9600)
#     communication_envoie.write("15".encode())
#     time.sleep(1)

def configuration():#recherche la connexion série
    global port, inter_exter
    Systeme_exploitation = str(input("quel est votre sytème d'exploitation (w/l)?\n>>>"))
    if Systeme_exploitation=="l":
        port="/dev/ttyACM0"
    elif Systeme_exploitation=="w":
        port= "COM4"
    inter_exter = str(input("Les mesures sont à l'interrieur ou à l'exterieur (i/e)? \n>>>"))

###########################communication #######################################

def reception():
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

def simulation_reception(): #simule la réception des données des capteur pour pouvoir coder sans arduino
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

##########################anlyse séparées#######################################
# traites les informations reçus: en liste, une par une, moyenne, max, minimum
def analyse_donnees_unique(valeur):
    pass

def analyse_plusieurs_donnees(valeurs):
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
    # /=configuration()
    recuperation_valeurs()
    simulation_reception()
    #reception()
    analyse_plusieurs_donnees(liste_des_humiditees)
    analyse_plusieurs_donnees(liste_des_temperature)

    temperature_actuelle=liste_des_temperature[len(liste_des_temperature)-1]
    humidité_actuelle=liste_des_humiditees[len(liste_des_humiditees)-1]
    fenetre.mainloop()

######################################début ####################################
affichage_tkinter()

os.system("pause")
