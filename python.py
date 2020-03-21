import serial
import tkinter
import time
import os
#########################initialisation################################

# def teste_emission():
#     communication_envoie = serial.Serial(port, 9600)
#     communication_envoie.write("15".encode())
#     time.sleep(1)

def configuration():#recherche la connexion série
    global port
    Systeme_exploitation = str(input("quel est votre sytème d'exploitation (w/l)?\n>>>"))
    if Systeme_exploitation=="l":
        port="/dev/ttyACM0"
    elif Systeme_exploitation=="w":
        port= "COM4"

def initialisation():
    pass

###########################communication #######################################
port="COM4"
def reception():
    communication_serie = serial.Serial(port, 9600)
    while True:
        valeur = communication_serie.readline()
        print(valeur)
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

def analyse_longue_periode(valeurs):
    sommes_des_valeurs=0
    for i in range(len(valeurs)):
        sommes_des_valeurs+=valeurs[i]
    moyenne=sommes_des_valeurs/(len(valeurs))
    maximum=max(valeurs)
    minimum=min(valeurs)
    Affichage_console(valeurs,moyenne, maximum, minimum)

###########################Affichage     #######################################
def Affichage_console(valeurs,moyenne, maximum, minimum):
    print("valeurs:", valeurs,"\nmoyenne:", moyenne,"\nmaximum:", maximum,"\nminimum:", minimum)

###########################communication #######################################
#reçois et envoie les informations
# def demande(type, dure, quantite):
#     if type==plusieurs_données:
#         communication_envoie.write("1{}{}".format(dure, quantite).encode())
#     elif type==longue_periode:
#         pass
#     elif type==donnees_unique:
#         pass
#     pass
#
# def recevoir():
#     reception=ser.readline()
#     if reception=="debut":
#         while reception=="Fin":
#             liste.append(reception)
#     print(reception)


######################################début ####################################
reception()
