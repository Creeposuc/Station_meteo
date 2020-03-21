import serial
import tkinter
import time
port="COM4"
liste_des_luminosite =[]
liste_des_temperature =[]
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

def reception():
    a=0
    communication_serie = serial.Serial(port, 9600)
    while len(liste_des_luminosite)<10:
        valeur = communication_serie.readline()
        valeur = str(valeur)
        print(valeur)
        if ">>>" in valeur:
            a=0
            a+=1
        elif a==1:
            liste_des_luminosite.append(float(valeur[2:][:6]))
            a+=1
        elif a==2:
            liste_des_temperature.append(float(valeur[2:][:6]))
            a=0

    print(">>>",liste_des_luminosite,"\n", liste_des_temperature)
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
configuration()
reception()
analyse_plusieurs_donnees(liste_des_luminosite)
analyse_plusieurs_donnees(liste_des_temperature)
