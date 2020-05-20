#importe les différents modules utile au fonctionnement du programme
import webbrowser
try:# on essaie d'importer les modules suivant
    import serial#gère la connexion avec le capteur
    import matplotlib.pyplot as plt#grée l'affichage du graphique
    from tkinter import *#gère l'interface graphique
    from tkinter.messagebox import *#gère les fenêtre popup
    from tkinter.filedialog import *#gère les boîte de dialog pour selectionner un emplacement avec explorateur
    import os #module qui nous permet dans notre cas de vérifier la présence d'un fichier
    import time#module qui gère les pauses dans le programme
    from random import randint# utile pour la simulation de réception
    import csv# gère l'export en fichier csv
    import datetime#permet de récuperérer l'heure actuelle
    from subprocess import run#permet de lancer des sous processus
    import pyperclip#permet de copier un élément dans le press papier

except ModuleNotFoundError: # si il y a une erreur de module non trouvé
    webbrowser.open(os.getcwd()+"/web/aide.html")# on ouvre une page web d'aide
    exit()#on ferme le programme python


port="COM4" #définit le port de connexion  originale du capteur au port 4
liste_des_humiditees =[] # variable qui stock les humiditées mesurées
liste_des_temperature =[]# variable qui stock les températures mesurées
liste_des_dates_de_mesures = []# variable qui stock les dates de chaque mesures
enregistrement=int(0)# création de la valriable qui permet de bloqué la fermeture du programme si les valeurs ne sont pas enregistrées
temperature_actuelle=0# création de la variable qui enregistre la dernière valeur de température mesurée
humidite_actuelle=0 #création de la variable qui enregistre la dernière valeur de taux d'humidité mesurée
simu = 0 #valeurs qui indique si la mesure est une simulation ou non
fenetre =Tk()#création de la fenetre principale avec Tkinter
def recuperation_preferences():# fonction qui récupère les valeurs des préférences de l'utilisateur pour les appliquer dans le programme
    global couleur_boutton, couleur_courbe_humidite, couleur_courbe_temperature, aspect_courbe_temperature, aspect_courbe_humidite# définition des variable suivante en variable globales
    with open("savegarde_des_preference.txt","r") as save_pref:# ouvre le fichier qui contient les valeurs des préférences en lecture seule en tant que la variable save_pref
        interieur_save_pref = save_pref.read()# enregistre le contenue du fichier lu dans une variable
        couleur_boutton = interieur_save_pref[0:7]# enregistre la préférence sélectioné choisi par l'utilisateur dans une variable
        couleur_courbe_temperature = interieur_save_pref[8:15]
        couleur_courbe_humidite = interieur_save_pref[16:23]
        aspect_courbe_temperature = interieur_save_pref[24:26]
        #les condition suivantes permettent de "normaliser" les valeurs des préférences pour l'affichage du graphique
        if aspect_courbe_temperature=="tp": #si il est inscrit "tp" (trait plein) alors
            aspect_courbe_temperature="solid"# aspect_courbe_temperature prend la valeur "solid" (une valeur compréhensible pour le module matplotlib qui gère le graphique)
        else:
            aspect_courbe_temperature="dashed"#sinon aspect_courbe_temperature prend la valeur "dashed" (une valeur compréhensible pour le module matplotlib qui gère le graphique)
        aspect_courbe_humidite = interieur_save_pref[27:29]
        # la condition suivante a le même fonctionnement
        if aspect_courbe_humidite=="tp":
            aspect_courbe_humidite="solid"
        else:
            aspect_courbe_humidite="dashed"

recuperation_preferences()# on exécute la commande au début du programme
###########################threads##############################################
def lancement_historique():# permet de lancer la fenêtre de l'historique
    run("python historique.py")# lance la commande suivante dans un CMD afin de lancer le programme qui s'occupe de l'affichage et de la recherche dans l'historique
def lancement_preference():# permet de lancer la fenêtre des préférences
    run("python preference.py")# Même fonctionnement
###########################  Affichage   #######################################
def affichage_tkinter():# fonction qui permet l'affichage de la fenêtre et des menus
    # la plupart des widget présent dans cette fonction ainsi que les placement de ces éléments ont une construction ressanblante, au moins un des widget de chaque type est commenté
    global case_dure_mesures, case_intervalle, valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite, nombre_seconde, mesure_termine# définition des variable suivante en variable globales
    bar_de_menu = Menu(fenetre)# création d'une barre de menu dans la fenêtre

    Menu_fichier = Menu(bar_de_menu, tearoff=0) # on créer une variable qui gère la barre de menu
    Menu_fichier.add_command(label = "Enregistrer en csv", command=enregistrement_CSV)# création d'un boutton dans le menu déroulant qui a un nom (Label) et une commande (une fonction)
    Menu_fichier.add_command(label = "Enregistrer en texte", command=enregistrement_texte)# même fonctionnement que précédement...
    Menu_fichier.add_command(label = "Copier les mesures dans le press papier pour regressi", command=enregistrement_reg)
    Menu_fichier.add_command(label = "Remise à zéro", command=remise_a_zero)
    Menu_fichier.add_command(label = "Historique", command=lancement_historique)
    Menu_fichier.add_command(label = "Préférence", command=lancement_preference)
    Menu_fichier.add_separator() #on ajoute un séparateur visuel dans le menue déroulan fichier
    Menu_fichier.add_command(label = "Simulation", command=redirection_simulation)
    Menu_fichier.add_command(label = "Quitter", command=quitter)
    bar_de_menu.add_cascade(label="Fichier", menu=Menu_fichier) #on donne le nom de "Fichier" au menu déroulant définit par Menu_fichier

    Menu_aide = Menu(bar_de_menu, tearoff=0)# même fonctionnement que pour le menu déroulant "Fichier"
    Menu_aide.add_command(label = "Voir l'aide", command=page_aide)# même fonctionnement que pour le menu déroulant "Fichier"
    Menu_aide.add_separator()
    Menu_aide.add_command(label = "Notre site internet", command=page_site)
    bar_de_menu.add_cascade(label="Aide", menu=Menu_aide)# même fonctionnement que pour le menu déroulant "Fichier"

    fenetre.config(menu=bar_de_menu)#on donne le menu précédent a la fenêtre de nom "fenetre"

    #############################zone de commande###############################
    cadre_zone_controle = Frame(fenetre, borderwidth=5, relief=GROOVE)# création d'un cadre qui est placé dans fenêtre et qui contiendra la zone de contrôle
    cadre_zone_controle.grid(row=1, column=0)

    titre1 =Label(cadre_zone_controle, text="Zone de contrôle").grid(row=0, column=0, columnspan=3)

    ########################################radio ##############################
    #boutton radio qui permettent de donner le choix à l'utilisateur de choisir l'ordre de grandeur de la durées des mesures
    nombre_seconde=IntVar()
    nombre_seconde.set(1)# on donne a la variable nombre_seconde la valeur "1"
    cadre_boutton_radio = Frame(cadre_zone_controle, borderwidth=3, relief=GROOVE)#création d'un cadre qui contient les bouttons radio dans la zone de contrôle
    cadre_boutton_radio.grid(row=1, column=0, columnspan=3)

    titre_boutton_radio = Label(cadre_boutton_radio, text="En quelle unitée est votre mesure ?")#titre au dessus des boutons radios, situé dans le cadre précédent et qui a pour texte "En quelle unitée est votre mesure ?"
    titre_boutton_radio.grid(row=0, column=0, columnspan=3)# même méthode de placement que précédement

    radio_seconde = Radiobutton(cadre_boutton_radio, text="En secondes", variable=nombre_seconde, value=1)# création d'un bouton radio, inscrit dans le cadre précédent, qui à pour texte/titre "En seconde", qui fait varier la variable "nombre_seconde" a 1
    radio_seconde.grid(row=1, column=0)

    radio_minute = Radiobutton(cadre_boutton_radio, text="En minutes", variable=nombre_seconde, value=60)
    radio_minute.grid(row=1, column=1)

    radio_heure = Radiobutton(cadre_boutton_radio, text="En heures", variable=nombre_seconde, value=3600)
    radio_heure.grid(row=1, column=2)
    ########################################fin radio###########################

    titre_case_nombre_mesure = Label(cadre_zone_controle, text="Durée de la mesure :").grid(row=2, column=0)

    titre_case_nombre_mesure_temps = Label(cadre_zone_controle, text="Intervalle de temps entre deux mesures :").grid(row=2, column=1)

    case_dure_mesures = Spinbox(cadre_zone_controle, from_=1, to=43200 )#création d'un champ de saisie de valeur numérique qui va de 1 a 43200
    case_dure_mesures.grid(row=3 ,column=0)

    case_intervalle = Spinbox(cadre_zone_controle, from_=1, to=43200 )
    case_intervalle.grid(row=3 ,column=1)


    boutton_demarage = Button(cadre_zone_controle, text = "Demarrer la mesure",command=demarrage, bg=couleur_boutton)# création d'un boutton qui a pour texte "Démarrer la mesure", qui a pour commande "démarrage", et qui a une couleur de fond défini par la variable couleur_boutton
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
    bouton_graph = Button(fenetre, text="Afficher le graphique",command=graphique_redirection, bg=couleur_boutton)# création d'un boutton qui a pour texte "Démarrer la mesure", qui a pour commande "graphique redirection"
    bouton_graph.grid(row=4 ,column=0)

    fenetre.mainloop()#lancement et ouverture de la fenêtre
def page_aide():
    webbrowser.open(os.getcwd()+"/web/aide.html")# on ouvre une page web d'aide
def page_site():
    webbrowser.open(os.getcwd()+"/web/index.html")# on ouvre page la page du site web
def quitter():# fonction qui permet de fermer le programme lorsqu'on click sur "quitter" dans le menue déroulant "fichier"
    if enregistrement==0:#si aucun enregistrement n'as été effectué
        if Menu_fichier.add_command(label = "Préférence", command=lancement_preference):#un message d'alerte s'affiche
            exit()#si l'utilisateur appuie sur oui, alors le programe se ferme avec la fonction "exit"
    elif enregistrement==1:#les mesures ont été enregistrées
        exit() #alors le programe se ferme avec la fonction "exit"

def redirection_simulation():
    global simu
    simu=1
    demarrage()

def sauvergarde_historique():#fonction qui permet d'enregistrer toutes les mesures effectuer par l'utilisateur dans l'historique
    with open("Historiques_des_valeurs_mesurées", "a") as fichier_texte:
        date =datetime.datetime.now()
        fichier_texte.write(f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}\n")
        for i in range(len(liste_des_humiditees)):
            fichier_texte.write(f"{liste_des_dates_de_mesures[i]}>>> humidite:{liste_des_humiditees[i]}% Temperature:{liste_des_temperature[i]}C\n")
        if len(liste_des_dates_de_mesures)>1:
            fichier_texte.write(f"Humidité>>> moyenne:{moy_humidite}% minimum:{min_humidite}% maximum:{max_humidite}%\n")
            fichier_texte.write(f"Température>>> moyenne:{moy_temperature}C minimum:{min_temperature}C maximum:{max_temperature}C\n")

def popup_enregistrement(extension):
    global emplacement # définition des variable suivante en variable globales
    emplacement =asksaveasfilename(title = "sauvegarder votre mesure", defaultextension=f".{extension}", initialfile="mesures")

def remise_a_zero():# on créer une fonction permettant de réinitialiser les valeurs mesurés
    if askyesno("Attention", "Êtes vous sûre de vouloir faire ça?", icon="warning"): #ouvre une fenêtre d'alerte demandant a l'utilisateur si il est certain de vouloir réinitialiser ses valeurs
        liste_variable=[valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite]# création d'une liste incluant toutes les valeurs à réinitialiser
        for i in liste_variable: #on parcourt les élément de la liste
            i.config(text = "-")# on enleve toutes les valeurs de la liste et on les remplace par "-" comme initialement
        showinfo("information", "mis à zéro!")# ouvre une fenêtre d'alerte pour confirmer a l'utilisateur que les valeurs ont bien été mises a zéro

def recuperation_valeurs():#cette fonction nous permet de faire la liaison entre la "zone de contrôle" de l'interface graphique et les autres fonctions du programme. Elle permet nottamment de récupérer les valeur des boutons radio et champs de saisie
    global nombre_de_mesures # définition des variable suivante en variable globales
    dure_mesure=int(case_dure_mesures.get())#récupère la valeure de la variable dure_mesure
    intervalle_temps=int(case_intervalle.get())#même fonctionnement que précédement
    nombre_de_seconde=int(nombre_seconde.get())#même fonctionnement que précédement
    nombre_de_mesures = int(dure_mesure*int(nombre_de_seconde)/intervalle_temps)#fait le calcul du nombre de mesures en fontion de la durée de la mesure, du nombre de seconde et de l'intervalle de temps

def graphique(liste1, liste2, liste_des_dates_de_mesures):# fonction permettant l'affichage et la modification ,via le menu préférence ,du graphique
    liste_numeros_des_mesures = []# création d'une liste qui remplace les dates mises initialement sur l'axe des abscisses par des numéros pour espacés les mesures
    for i in range(nombre_de_mesures):
        liste_numeros_des_mesures.append(i+1)
    plt.title(f"Température et Taux d'humididté à partir de {liste_des_dates_de_mesures[0]}") #titre du graphique(il contient la date de la première mesure)
    plt.plot(liste_numeros_des_mesures, liste1, label="Taux d'humidité",linestyle=f"{aspect_courbe_humidite}", marker="+", color=f"{couleur_courbe_humidite}")#
    plt.plot(liste_numeros_des_mesures, liste2, label="Température",linestyle=f"{aspect_courbe_temperature}", marker="+", color=f"{couleur_courbe_temperature}")
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

# def configuration():#recherche la connexion serie
#     global port
#     for num_port in range(6):
#         try:
#             num_port=str(num_port)
#             test_port = "COM" + num_port
#             print(test_port)
#             communication_serie = serial.Serial(port, 9600)
#             time.sleep(1)
#             valeur = communication_serie.readline()
#             print(test_port)
#             if ">>>" in valeur:
#                 port = "COM" + num_port
#         except:
#             print("except")

###########################communication #######################################

def reception():
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures# définition des variable suivante en variable globales
    a=0
    communication_serie = serial.Serial(port, 9600)
    for i in range(nombre_de_mesures*3):
        valeur = communication_serie.readline()
        valeur = str(valeur)
        if ">>>" in valeur:
            date = datetime.datetime.now()
            liste_des_dates_de_mesures.append(str(f"{date.hour}h{date.minute}m{date.second}s"))
            a=0
            a+=1
        elif a==1:
            liste_des_humiditees.append(float(valeur[2:][:5]))
            a+=1
        elif a==2:
            liste_des_temperature.append(float(valeur[2:][:5]))
            a=0
            time.sleep(int(case_intervalle.get()))
         #####################################################################################################################################################

def simulation_reception(): #simule la reception des donnees des capteur pour pouvoir coder sans capteur programmable
    showinfo("simulation","la simulation permet de simuler une mesure. Elle est fonctionnelle sans capteur et donne des valeurs aléatoire. Elle utilise les valeurs présentes dans zone de contrôle")
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures, nombre_de_mesures# définition des variable suivante en variable globales
    a=0
    for i in range(nombre_de_mesures*3):
        if a==0:
            valeur = ">>>"
        else:
            valeur = randint(0,100)
            valeur = str(valeur)
        if ">>>" in valeur:
            date = datetime.datetime.now()
            liste_des_dates_de_mesures.append(str(f"{date.hour}h{date.minute}m{date.second}s"))
            a=0
            a+=1
        elif a==1:
            liste_des_humiditees.append(float(valeur))
            a+=1
        elif a==2:
            liste_des_temperature.append(float(valeur))
            a=0
            time.sleep(int(case_intervalle.get()))

################################# analyse #######################################
# traites les informations reçus: en liste, une par une, moyenne, max, minimum
def analyse_donnees(valeurs):
    global maximum, minimum, moyenne # définition des variable suivante en variable globales
    sommes_des_valeurs=0
    for i in range(len(valeurs)):
        sommes_des_valeurs+=valeurs[i]
    moyenne=round(sommes_des_valeurs/(len(valeurs)),2)
    maximum=max(valeurs)
    minimum=min(valeurs)

    # if inter_exter=="e":
    #     pass #moyennes de saisons

############################### eregristrement #################################

def enregistrement_texte():
    global enregistrement# définition des variable suivante en variable globales
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez- pas enregistrer car vous n'avez pas effectué de mesures")
    else:
        popup_enregistrement("txt")
        if os.path.isfile(emplacement):
            os.remove(emplacement)
        with open(emplacement, "x") as fichier_texte:
          date = datetime.datetime.now()
          fichier_texte.write(f"date: {date.day}/{date.month}/{date.year}\n")
          for i in range(len(liste_des_humiditees)):
              fichier_texte.write(f"{liste_des_dates_de_mesures[i]} >>> humidité: {liste_des_humiditees[i]}%   Température: {liste_des_temperature[i]}C\n")
          if len(liste_des_dates_de_mesures)>1:
              fichier_texte.write(f"Humidité>>> moyenne:{moy_humidite}% minimum:{min_humidite}% maximum:{max_humidite}%\n")
              fichier_texte.write(f"Température>>> moyenne:{moy_temperature}C minimum:{min_temperature}C maximum:{max_temperature}C\n")
def enregistrement_CSV():#rajouter les espaces pour taux d'humidite, selectionné l'emplacement, info avec séparation utf8
    global enregistrement# définition des variable suivante en variable globales
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectué de mesures")
    else:
        popup_enregistrement("csv")
        if os.path.isfile(emplacement):
            os.remove(emplacement)
        with open(emplacement, "a", newline="") as ficher_csv:
            ecrire = csv.writer(ficher_csv, delimiter=" ")
            ecrire.writerow("Heure,Taux_d'humidite,Temperature")
            for i in range(len(liste_des_humiditees)):
                ecrire.writerow(f"{liste_des_dates_de_mesures[i]},{liste_des_humiditees[i]}%,{liste_des_temperature[i]}C")
            if len(liste_des_dates_de_mesures)>1:
                ecrire.writerow(f"Humidite>>>,moyenne:{moy_humidite}%,minimum:{min_humidite}%,maximum:{max_humidite}%")
                ecrire.writerow(f"Température>>>,moyenne:{moy_temperature}C,minimum:{min_temperature}C,maximum:{max_temperature}C")

def enregistrement_reg():
    global enregistrement# définition des variable suivante en variable globales
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectué de mesures")
    else:
        date = datetime.datetime.now()
        pressepapier="mesure(numero) temperature(c) humidite(taux)\n"
        for i in range(len(liste_des_humiditees)):
            pressepapier=pressepapier + f"{i}  {liste_des_temperature[i]}  {liste_des_humiditees[i]}\n"
        pyperclip.copy(pressepapier)

##################################demarrage mesure et analyse ##################
def demarrage():
    enregistrement=0
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures# définition des variable suivante en variable globales
    global min_humidite, max_humidite, moy_humidite, min_temperature, max_temperature, moy_temperature# définition des variable suivante en variable globales
    global simu
    liste_des_humiditees = []
    liste_des_temperature = []
    liste_des_dates_de_mesures = []
    recuperation_valeurs()
    if simu==1:
        simulation_reception()
    else:
        reception()
    simu = 0
    temperature_actuelle=liste_des_temperature[len(liste_des_temperature)-1]
    humidite_actuelle=liste_des_humiditees[len(liste_des_humiditees)-1]
    valeur_temperature.config( text =  temperature_actuelle)
    valeur_humidite.config( text =  humidite_actuelle)

    if nombre_de_mesures!=1:
        analyse_donnees(liste_des_temperature)
        valeur_min_temperature.config(text = minimum)
        min_temperature = minimum
        valeur_max_temperature.config(text = maximum)
        max_temperature = maximum
        valeur_moyenne_temperature.config(text = moyenne)
        moy_temperature = moyenne
        analyse_donnees(liste_des_humiditees)
        valeur_min_humidite.config(text = minimum)
        min_humidite=minimum
        valeur_max_humidite.config(text = maximum)
        max_humidite=maximum
        valeur_moyenne_humidite.config(text = moyenne)
        moy_humidite=moyenne
    sauvergarde_historique()
    showinfo("Mesures terminées", "vos mesures ont été effectuées")
######################################debut ####################################
# configuration()
affichage_tkinter()
