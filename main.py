import serial
import matplotlib.pyplot as plt
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import threading
import time
from random import randint
import csv
import datetime
from subprocess import run
import pyperclip

port="COM4"
liste_des_humiditees =[]
liste_des_temperature =[]
liste_des_dates_de_mesures = []
enregistrement=int(0)
temperature_actuelle=0
humidite_actuelle=0
fenetre =Tk()
###########################threads##############################################
def lancement_historique():
    run("python historique.py")
    # thread_historique=threading.Thread(target=historique)
    # thread_historique.start()

###########################  Affichage   #######################################
def Affichage_console(valeurs,moyenne, maximum, minimum):
    print("valeurs:", valeurs,"\nmoyenne:", moyenne,"\nmaximum:", maximum,"\nminimum:", minimum)
def affichage_tkinter():
    global case_dure_mesures, case_intervalle, valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite, value
    #############################menu déroulant  ###############################
    bar_de_menu = Menu(fenetre)

    Menu_fichier = Menu(bar_de_menu, tearoff=0)
    Menu_fichier.add_command(label = "Enregistrer en csv", command=enregistrement_CSV)
    Menu_fichier.add_command(label = "Enregistrer en texte", command=enregistrement_texte)
    Menu_fichier.add_command(label = "Copier les mesures dans le press papier pour regressi", command=enregistrement_reg)
    Menu_fichier.add_command(label = "Remise à zéro", command=remise_a_zero)
    Menu_fichier.add_command(label = "Historique", command=lancement_historique)
    Menu_fichier.add_command(label = "préference", command=preference)
    Menu_fichier.add_separator()
    Menu_fichier.add_command(label = "Quitter", command=quitter)
    bar_de_menu.add_cascade(label="Fichier", menu=Menu_fichier)

    Menu_aide = Menu(bar_de_menu, tearoff=0)
    Menu_aide.add_command(label = "Voir l'aide")
    Menu_aide.add_separator()
    Menu_aide.add_command(label = "Qui sommes nous ?")
    bar_de_menu.add_cascade(label="Aide", menu=Menu_aide)

    fenetre.config(menu=bar_de_menu)

    #nom_ducadre=Frame(fenetre, borderwidth=4, relief=GROOVE).grid(....)
    #titre1 =Label(Frame, text="Zone de contrôle").grid(row=0 ,column=0, columnspan=4)
    #############################zone de commande###############################
    cadre_zone_controle = Frame(fenetre, borderwidth=5, relief=GROOVE)
    cadre_zone_controle.grid(row=1, column=0)

    titre1 =Label(cadre_zone_controle, text="Zone de contrôle").grid(row=0, column=0, columnspan=3)

    ########################################radio ########################################################
    value=IntVar()
    value.set(1)
    cadre_boutton_radio = Frame(cadre_zone_controle, borderwidth=3, relief=GROOVE)
    cadre_boutton_radio.grid(row=1, column=0, columnspan=3)

    titre_boutton_radio = Label(cadre_boutton_radio, text="En quelle unitée est votre mesure ?")
    titre_boutton_radio.grid(row=0, column=0, columnspan=3)

    radio_seconde = Radiobutton(cadre_boutton_radio, text="En secondes", variable=value, value=1)
    radio_seconde.grid(row=1, column=0)

    radio_minute = Radiobutton(cadre_boutton_radio, text="En minutes", variable=value, value=60)
    radio_minute.grid(row=1, column=1)

    radio_heure = Radiobutton(cadre_boutton_radio, text="En heures", variable=value, value=3600)
    radio_heure.grid(row=1, column=2)
    ########################################fin radio###############################################################

    titre_case_nombre_mesure = Label(cadre_zone_controle, text="Durée de la mesure :").grid(row=2, column=0)

    titre_case_nombre_mesure_temps = Label(cadre_zone_controle, text="Intervalle de temps entre deux mesures :").grid(row=2, column=1)

    case_dure_mesures = Spinbox(cadre_zone_controle, from_=1, to=43200 )# une journe de mesure maximum
    case_dure_mesures.grid(row=3 ,column=0)

    case_intervalle = Spinbox(cadre_zone_controle, from_=1, to=43200 )# une journe de mesure maximum
    case_intervalle.grid(row=3 ,column=1)


    boutton_demarage = Button(cadre_zone_controle, text = "Demarrer la mesure",command=demarrage, bg="red")
    boutton_demarage.grid(row=3 ,column=2)

    ##########################zone d'affichage valeur simple####################
    cadre_valeur_actuelle = Frame(fenetre, borderwidth=5, relief=GROOVE)
    cadre_valeur_actuelle.grid(row=2, column=0)

    titre_affichage_une_valeur = Label(cadre_valeur_actuelle, text="Valeur actuelle").grid(row=3   ,column=0, columnspan=4)

    affichage_temperature_une_valeur = Label(cadre_valeur_actuelle, text="Temperature :").grid(row=4 ,column=0)

    valeur_temperature = Label(cadre_valeur_actuelle, text="-")
    valeur_temperature.grid(row=4, column=1)

    affichage_humidite_une_valeur = Label(cadre_valeur_actuelle, text="Taux d'humidite :").grid(row=5, column=0)

    valeur_humidite = Label(cadre_valeur_actuelle, text="-")
    valeur_humidite.grid(row=5, column=1)

    ##########################zone d'afichage plusieurs valeurs ################
    cadre_analyse = Frame(fenetre, borderwidth=5, relief=GROOVE)
    cadre_analyse.grid(row=3, column=0)

    titre_affichage_plusieurs_valeurs = Label(cadre_analyse, text="Analyse").grid(row=6   ,column=0, columnspan=4)

    affichage_temperature_plusieurs_valeur = Label(cadre_analyse, text="Temperature :").grid(row=7 ,column=0)

    affichage_min_temperature = Label(cadre_analyse, text="Valeurs minimum :").grid(row=7, column=1)

    valeur_min_temperature = Label(cadre_analyse, text="-")
    valeur_min_temperature.grid(row=8, column=1)

    affichage_max_temperature = Label(cadre_analyse, text="Valeurs maximum :").grid(row=7, column=2)

    valeur_max_temperature = Label(cadre_analyse, text="-")
    valeur_max_temperature.grid(row=8, column=2)

    affichage_moyenne_temperature = Label(cadre_analyse, text="Moyenne :").grid(row=7, column=3)

    valeur_moyenne_temperature = Label(cadre_analyse, text="-")
    valeur_moyenne_temperature.grid(row=8, column=3)

    # ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    affichage_humidite_plusieurs_valeur = Label(cadre_analyse, text="Taux d'humidite :").grid(row=9, column=0)

    affichage_min_humidite = Label(cadre_analyse, text="Valeurs minimum :").grid(row=9, column=1)


    valeur_min_humidite = Label(cadre_analyse, text="-")
    valeur_min_humidite.grid(row=10, column=1)

    affichage_max_humidite = Label(cadre_analyse, text="Valeurs maximum :").grid(row=9, column=2)

    valeur_max_humidite = Label(cadre_analyse, text="-")
    valeur_max_humidite.grid(row=10, column=2)

    affichage_moyenne_humidite = Label(cadre_analyse, text="Moyenne :").grid(row=9, column=3)

    valeur_moyenne_humidite = Label(cadre_analyse, text="-")
    valeur_moyenne_humidite.grid(row=10, column=3)

    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## #
    bouton_graph = Button(fenetre, text = "Afficher le graphique",command=graphique_redirection, bg="blue")
    bouton_graph.grid(row=11 ,column=0, columnspan=4)

    fenetre.mainloop()

def quitter():
    print(enregistrement)
    if enregistrement==0:
        if askyesno("Attention", "Aucunes mersures ne sera sauvegardées", icon="warning"):
            exit()
    elif enregistrement==1:#les mesures ont été enregistrées
        exit()

def preference():
    preference=Tk()
    titre_preference = Label(preference, text="Préférence de l'affichage",font=("bold",16)).grid(row=0, column=0)

    cadre_preference = Frame(preference, borderwidth=5, relief=GROOVE)
    cadre_preference.grid(row=1, column=0)

    titre_couleur_boutton = Label(cadre_preference, text="Couleur des bouttons :").grid(row=0, column=0)
    couleur=StringVar()
    couleur.set("red")
    boutton_rouge = Radiobutton(cadre_preference, text="Rouge",variable=couleur, value="red")
    boutton_rouge.grid(row=1, column=0)
    boutton_vert = Radiobutton(cadre_preference, text="Vert",variable=couleur, value="vert")
    boutton_vert.grid(row=2, column=0)
    boutton_bleu = Radiobutton(cadre_preference, text="bleu",variable=couleur, value="bleu")
    boutton_bleu.grid(row=3, column=0)
    boutton_jaune = Radiobutton(cadre_preference, text="Jaune",variable=couleur, value="jaune")
    boutton_jaune.grid(row=4, column=0)


    boutton_appliquer = Button(preference, text="Appliquer", command=appliquer_preference, bg="red").grid(row=2, column=0)

    preference.mainloop()
def appliquer_preference():
    pass
def sauvergarde_historique():
    with open("Historiques_des_valeurs_mesurées", "a") as fichier_texte:
        date =datetime.datetime.now()
        fichier_texte.write(f"{date.day}/{date.month}/{date.year} {date.hour}h{date.minute}m{date.second}s\n")
        for i in range(len(liste_des_humiditees)):
            fichier_texte.write(f"{liste_des_dates_de_mesures[i]}>>> humidite:{liste_des_humiditees[i]}% Temperature:{liste_des_temperature[i]}C\n")

def popup_enregistrement(extension):
    global emplacement
    emplacement =asksaveasfilename(title = "sauvegarder votre mesure", defaultextension=f".{extension}", initialfile="mesures")

def remise_a_zero():
    if askyesno("Attention", "Êtes vous sure de vouloir faire ça?", icon="warning"):
        liste_variable=[valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite]
        for i in liste_variable:
            i.config(text = "-")
        showinfo("information", "mis à zéro!")

def recuperation_valeurs():
    global nombre_de_mesures
    dure_mesure=int(case_dure_mesures.get())
    print(dure_mesure)
    intervalle_temps=int(case_intervalle.get())
    print(intervalle_temps)
    valeur=int(value.get())
    nombre_de_mesures = int(dure_mesure*int(valeur)/intervalle_temps)
    print(nombre_de_mesures)

def graphique(liste1, liste2, liste_des_dates_de_mesures):
    valeur_moyenne_temperature.cget("text")
    liste_numeros_des_mesures = []
    for i in range(nombre_de_mesures):
        liste_numeros_des_mesures.append(i+1)
    plt.title(f"Température et Taux d'humididté à partir de {liste_des_dates_de_mesures[0]}")
    plt.plot(liste_numeros_des_mesures, liste1, label="Taux d'humidité", marker="+")
    plt.plot(liste_numeros_des_mesures, liste2, label="Température", marker="+")
    plt.ylabel("valeur")
    plt.xlabel("numéro de la mesure")
    plt.legend()
    plt.grid(True)
    plt.show()

def graphique_redirection():
    if len(liste_des_humiditees)<=1:
        showinfo("Valeurs vide !", "Vous n'avez pas mesuré assé de valeur pour afficher le graphique")
    else:
        graphique(liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures)
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
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures
    a=0
    communication_serie = serial.Serial(port, 9600)
    for i in range(nombre_de_mesures*3):
        valeur = communication_serie.readline()
        valeur = str(valeur)
        if ">>>" in valeur:
            date = datetime.datetime.now()
            liste_des_dates_de_mesures.append(str(f"{date.hour}h{date.minute}m{date.second}s"))
            print(str(f"{date.hour}h{date.minute}m{date.second}s"))
            a=0
            a+=1
        elif a==1:
            liste_des_humiditees.append(float(valeur[2:][:5]))
            print(valeur)
            a+=1
        elif a==2:
            liste_des_temperature.append(float(valeur[2:][:5]))
            a=0
            print(valeur)
            time.sleep(int(case_intervalle.get()))
         #####################################################################################################################################################
    print("liste de dates:", liste_des_dates_de_mesures)

def simulation_reception(): #simule la reception des donnees des capteur pour pouvoir coder sans arduino
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures
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
            date = datetime.datetime.now()
            liste_des_dates_de_mesures.append(str(f"{date.hour}h{date.minute}m{date.second}s"))
            print(str(f"{date.hour}h{date.minute}m{date.second}s"))

            a=0
            a+=1
        elif a==1:
            liste_des_humiditees.append(float(valeur))
            a+=1
        elif a==2:
            liste_des_temperature.append(float(valeur))
            a=0
            time.sleep(int(case_intervalle.get()))
    print("liste de dates:", liste_des_dates_de_mesures)

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

############################### eregristrement #################################

def enregistrement_texte():
    global enregistrement
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectué de mesures")
    else:
        popup_enregistrement("txt")
        if askyesno("Enregistrement", "Vous êtes sûr le point d'enregistrer votre dernière mesure, si vous avez déjà enregister vos valeur dans un même emplacement avec un même nom, cette nouvelle mesure y sera ajouté.", icon="info"):
            with open(emplacement, "a") as fichier_texte:
                date = datetime.datetime.now()
                fichier_texte.write(f"date: {date.day}/{date.month}/{date.year}\n")
                for i in range(len(liste_des_humiditees)):
                    fichier_texte.write(f"{liste_des_dates_de_mesures[i]} >>> humidité: {liste_des_humiditees[i]}%   Température: {liste_des_temperature[i]}C\n")



def enregistrement_CSV():#rajouter les espaces pour taux d'humidite, selectionné l'emplacement, info avec séparation utf8
    global enregistrement
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectué de mesures")
    else:
        if askyesno("Enregistrement", "Vous êtes sûr le point d'enregistrer votre dernière mesure, si vous avez déjà enregister vos valeur dans un même emplacement avec un même nom, cette nouvelle mesure y sera ajouté.", icon="info"):
            popup_enregistrement("csv")
            with open(emplacement, "a") as ficher_csv:
                ecrire = csv.writer(ficher_csv, delimiter=" ")
                ecrire.writerow("")
                ecrire.writerow("Heure,Taux_d'humidite,Temperature")
                for i in range(len(liste_des_humiditees)):
                    ecrire.writerow(f"{liste_des_dates_de_mesures[i]},{liste_des_humiditees[i]}%,{liste_des_temperature[i]}C")

def enregistrement_reg():
    global enregistrement
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectué de mesures")
    else:
        date = datetime.datetime.now()
        pressepapier="mesure(numero) temperature(c) humidite(taux)\n"
        for i in range(len(liste_des_humiditees)):
            pressepapier=pressepapier + f"{i}  {liste_des_temperature[i]}  {liste_des_humiditees[i]}\n"
        print(pressepapier)
        pyperclip.copy(pressepapier)
        spam = pyperclip.paste()

##################################demarrage mesure et analyse ##################
def demarrage():
    # configuration()
    enregistrement=0
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures
    liste_des_humiditees = []
    liste_des_temperature = []
    liste_des_dates_de_mesures = []
    recuperation_valeurs()
    simulation_reception()

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
    sauvergarde_historique()

    print("liste de dates:", liste_des_dates_de_mesures)
    fenetre.mainloop()
######################################debut ####################################
affichage_tkinter()
