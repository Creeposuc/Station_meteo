import serial
from tkinter import *
import time
from random import randint
port="COM4"
liste_des_humiditees =[]
liste_des_temperature =[]

#########################initialisation################################

# def teste_emission():
#     communication_envoie = serial.Serial(port, 9600)
#     communication_envoie.write("15".encode())
#     time.sleep(1)

def configuration():#recherche la connexion série
    global port, nombre_de_mesures, inter_exter
    Systeme_exploitation = str(input("quel est votre sytème d'exploitation (w/l)?\n>>>"))
    if Systeme_exploitation=="l":
        port="/dev/ttyACM0"
    elif Systeme_exploitation=="w":
        port= "COM4"
    nombre_de_mesures=int(input("le nombre de mesures à effectuer: \n>>>"))
    inter_exter = str(input("Les mesures sont à l'interrieur ou à l'exterieur (i/e)? \n>>>"))
def initialisation():
    pass

###########################communication #######################################

def reception():
    a=0
    communication_serie = serial.Serial(port, 9600)
    while len(liste_des_humiditees)<nombre_de_mesures:
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

    print(">>>",liste_des_humiditees,"\n", liste_des_temperature)

def simulation_reception(): #simule la réception des données des capteur pour pouvoir coder sans arduino
        a=0
        while len(liste_des_humiditees)<nombre_de_mesures:
            if a==0:
                valeur = ">>>"
                print("premier passage")
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

        print(">>>",liste_des_humiditees,"\n", liste_des_temperature)
##########################anlyse séparées#######################################
# traites les informations reçus: en liste, une par une, moyenne, max, minimum
def analyse_donnees_unique(valeur):
    pass

def analyse_plusieurs_donnees(valeurs):
    sommes_des_valeurs=0
    for i in range(len(valeurs)):
        sommes_des_valeurs+=valeurs[i]
    moyenne=sommes_des_valeurs/(len(valeurs))
    maximum=max(valeurs)
    minimum=min(valeurs)
    Affichage_console(valeurs,moyenne, maximum, minimum)
    if inter_exter=="e":
        pass #moyennes de saisons
###########################Affichage     #######################################
def Affichage_console(valeurs,moyenne, maximum, minimum):
    print("valeurs:", valeurs,"\nmoyenne:", moyenne,"\nmaximum:", maximum,"\nminimum:", minimum)
def affichage_tkinter():
    fenetre =Tk()

    titre1 =Label(fenetre, text="zone de contrôle")
    titre1.grid(row=0 ,column=0, columnspan=2)

    nombre_de_mesures = Spinbox(fenetre, from_=0, to=43200 )# une journé de mesure maximum
    nombre_de_mesures.grid(row=1 ,column=0)

    boutton_demarage = Button(fenetre, text = "Démarer la mesure")
    boutton_demarage.grid(row=1 ,column=1)


    fenetre.mainloop()


######################################début ####################################
#affichage_tkinter()
configuration()
simulation_reception()
analyse_plusieurs_donnees(liste_des_humiditees)
analyse_plusieurs_donnees(liste_des_temperature)
