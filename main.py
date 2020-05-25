#importe les differents modules utile au fonctionnement du programme
import webbrowser
try:# on essaie d'importer les modules suivant
    import serial#gere la connexion avec le capteur
    import matplotlib.pyplot as plt#gree l'affichage du graphique
    from tkinter import *#gere l'interface graphique
    from tkinter.messagebox import *#gere les fenêtre popup
    from tkinter.filedialog import *#gere les boîte de dialog pour selectionner un emplacement avec explorateur
    import os #module qui nous permet dans notre cas de verifier la presence d'un fichier
    import time#module qui gere les pauses dans le programme
    from random import randint# utile pour la simulation de reception
    import csv# gere l'export en fichier csv
    import datetime#permet de recupererer l'heure actuelle
    from subprocess import run#permet de lancer des sous processus
    import pyperclip#permet de copier un element dans le press papier
except ModuleNotFoundError: # si il y a une erreur de module non trouve
    webbrowser.open(os.getcwd()+"/web/aide.html")# on ouvre une page web d'aide
    exit()#on ferme le programme python


port="COM4" #definit le port de connexion  originale du capteur au port 4
liste_des_humiditees =[] # variable qui stock les humiditees mesurees
liste_des_temperature =[]# variable qui stock les temperatures mesurees
liste_des_dates_de_mesures = []# variable qui stock les dates de chaque mesures
enregistrement=int(0)# creation de la valriable qui permet de bloque la fermeture du programme si les valeurs ne sont pas enregistrees
temperature_actuelle=0# creation de la variable qui enregistre la derniere valeur de temperature mesuree
humidite_actuelle=0 #creation de la variable qui enregistre la derniere valeur de taux d'humidite mesuree
simu = 0 #valeurs qui indique si la mesure est une simulation ou non
fenetre =Tk()#creation de la fenetre principale avec Tkinter
def recuperation_preferences():# fonction qui recupere les valeurs des preferences de l'utilisateur pour les appliquer dans le programme
    global couleur_boutton, couleur_courbe_humidite, couleur_courbe_temperature, aspect_courbe_temperature, aspect_courbe_humidite# definition des variable suivante en variable globales
    with open("savegarde_des_preference.txt","r") as save_pref:# ouvre le fichier qui contient les valeurs des preferences en lecture seule en tant que la variable save_pref
        interieur_save_pref = save_pref.read()# enregistre le contenue du fichier lu dans une variable
        couleur_boutton = interieur_save_pref[0:7]# enregistre la preference selectione choisi par l'utilisateur dans une variable
        couleur_courbe_temperature = interieur_save_pref[8:15]
        couleur_courbe_humidite = interieur_save_pref[16:23]
        aspect_courbe_temperature = interieur_save_pref[24:26]
        #les condition suivantes permettent de "normaliser" les valeurs des preferences pour l'affichage du graphique
        if aspect_courbe_temperature=="tp": #si il est inscrit "tp" (trait plein) alors
            aspect_courbe_temperature="solid"# aspect_courbe_temperature prend la valeur "solid" (une valeur comprehensible pour le module matplotlib qui gere le graphique)
        else:
            aspect_courbe_temperature="dashed"#sinon aspect_courbe_temperature prend la valeur "dashed" (une valeur comprehensible pour le module matplotlib qui gere le graphique)
        aspect_courbe_humidite = interieur_save_pref[27:29]
        # la condition suivante a le même fonctionnement
        if aspect_courbe_humidite=="tp":
            aspect_courbe_humidite="solid"
        else:
            aspect_courbe_humidite="dashed"

recuperation_preferences()# on execute la commande au debut du programme
###########################threads##############################################
def lancement_historique():# permet de lancer la fenêtre de l'historique
    run("python historique.py")#permet de lancer des sous processus


def lancement_preference():# permet de lancer la fenêtre des preferences
    run("python preference.py")#permet de lancer des sous processus

    #Même fonctionnement
###########################  Affichage   #######################################
def affichage_tkinter():# fonction qui permet l'affichage de la fenêtre et des menus
    # la plupart des widget present dans cette fonction ainsi que les placement de ces elements ont une construction ressanblante, au moins un des widget de chaque type est commente
    global case_dure_mesures, case_intervalle, valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite, nombre_seconde, mesure_termine# definition des variable suivante en variable globales
    bar_de_menu = Menu(fenetre)# creation d'une barre de menu dans la fenêtre

    Menu_fichier = Menu(bar_de_menu, tearoff=0) # on creer une variable qui gere la barre de menu
    Menu_fichier.add_command(label = "Enregistrer en csv", command=enregistrement_CSV)# creation d'un boutton dans le menu deroulant qui a un nom (Label) et une commande (une fonction)
    Menu_fichier.add_command(label = "Enregistrer en texte", command=enregistrement_texte)# même fonctionnement que precedement...
    Menu_fichier.add_command(label = "Copier les mesures dans le press papier pour regressi", command=enregistrement_reg)
    Menu_fichier.add_command(label = "Remise à zero", command=remise_a_zero)
    Menu_fichier.add_command(label = "Historique", command=lancement_historique)
    Menu_fichier.add_command(label = "Preference", command=lancement_preference)
    Menu_fichier.add_separator() #on ajoute un separateur visuel dans le menue deroulan fichier
    Menu_fichier.add_command(label = "Simulation", command=redirection_simulation)
    Menu_fichier.add_command(label = "Quitter", command=quitter)
    bar_de_menu.add_cascade(label="Fichier", menu=Menu_fichier) #on donne le nom de "Fichier" au menu deroulant definit par Menu_fichier

    Menu_aide = Menu(bar_de_menu, tearoff=0)# même fonctionnement que pour le menu deroulant "Fichier"
    Menu_aide.add_command(label = "Voir l'aide", command=page_aide)# même fonctionnement que pour le menu deroulant "Fichier"
    Menu_aide.add_separator()
    Menu_aide.add_command(label = "Notre site internet", command=page_site)
    bar_de_menu.add_cascade(label="Aide", menu=Menu_aide)# même fonctionnement que pour le menu deroulant "Fichier"

    fenetre.config(menu=bar_de_menu)#on donne le menu precedent a la fenêtre de nom "fenetre"

    #############################zone de commande###############################
    cadre_zone_controle = Frame(fenetre, borderwidth=5, relief=GROOVE)# creation d'un cadre qui est place dans fenêtre et qui contiendra la zone de contrôle
    cadre_zone_controle.grid(row=1, column=0)

    titre1 =Label(cadre_zone_controle, text="Zone de contrôle").grid(row=0, column=0, columnspan=3)

    ########################################radio ##############################
    #boutton radio qui permettent de donner le choix à l'utilisateur de choisir l'ordre de grandeur de la durees des mesures
    nombre_seconde=IntVar()
    nombre_seconde.set(1)# on donne a la variable nombre_seconde la valeur "1"
    cadre_boutton_radio = Frame(cadre_zone_controle, borderwidth=3, relief=GROOVE)#creation d'un cadre qui contient les bouttons radio dans la zone de contrôle
    cadre_boutton_radio.grid(row=1, column=0, columnspan=3)

    titre_boutton_radio = Label(cadre_boutton_radio, text="En quelle unitee est votre mesure ?")#titre au dessus des boutons radios, situe dans le cadre precedent et qui a pour texte "En quelle unitee est votre mesure ?"
    titre_boutton_radio.grid(row=0, column=0, columnspan=3)# même methode de placement que precedement

    radio_seconde = Radiobutton(cadre_boutton_radio, text="En secondes", variable=nombre_seconde, value=1)# creation d'un bouton radio, inscrit dans le cadre precedent, qui à pour texte/titre "En seconde", qui fait varier la variable "nombre_seconde" a 1
    radio_seconde.grid(row=1, column=0)

    radio_minute = Radiobutton(cadre_boutton_radio, text="En minutes", variable=nombre_seconde, value=60)
    radio_minute.grid(row=1, column=1)

    radio_heure = Radiobutton(cadre_boutton_radio, text="En heures", variable=nombre_seconde, value=3600)
    radio_heure.grid(row=1, column=2)
    ########################################fin radio###########################

    titre_case_nombre_mesure = Label(cadre_zone_controle, text="Duree de la mesure :").grid(row=2, column=0)

    titre_case_nombre_mesure_temps = Label(cadre_zone_controle, text="Intervalle de temps entre deux mesures :").grid(row=2, column=1)

    case_dure_mesures = Spinbox(cadre_zone_controle, from_=1, to=43200 )#creation d'un champ de saisie de valeur numerique qui va de 1 a 43200
    case_dure_mesures.grid(row=3 ,column=0)

    case_intervalle = Spinbox(cadre_zone_controle, from_=1, to=43200 )
    case_intervalle.grid(row=3 ,column=1)


    boutton_demarage = Button(cadre_zone_controle, text = "Demarrer la mesure",command=demarrage, bg=couleur_boutton)# creation d'un boutton qui a pour texte "Demarrer la mesure", qui a pour commande "demarrage", et qui a une couleur de fond defini par la variable couleur_boutton
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

    bouton_graph = Button(fenetre, text="Afficher le graphique",command=graphique, bg=couleur_boutton)# creation d'un boutton qui a pour texte "Demarrer la mesure", qui a pour commande "graphique redirection"
    bouton_graph.grid(row=4 ,column=0)

    fenetre.mainloop()#lancement et ouverture de la fenêtre
def page_aide():
    webbrowser.open(os.getcwd()+"/web/aide.html")# on ouvre une page web d'aide
def page_site():
    webbrowser.open(os.getcwd()+"/web/index.html")# on ouvre page la page du site web
def quitter():# fonction qui permet de fermer le programme lorsqu'on click sur "quitter" dans le menue deroulant "fichier"
    if enregistrement==0:#si aucun enregistrement n'as ete effectue
        if askyesno("fermer sans enregistrer ?", "voulez vous fermer sans enregistrer?"):#un message d'alerte s'affiche
            exit()#si l'utilisateur appuie sur oui, alors le programe se ferme avec la fonction "exit"
    elif enregistrement==1:#les mesures ont ete enregistrees
        exit() #alors le programe se ferme avec la fonction "exit"

def redirection_simulation():
    global simu
    simu=1
    demarrage()

def sauvergarde_historique():#fonction qui permet d'enregistrer toutes les mesures effectuer par l'utilisateur dans l'historique (plus exactement dans un fichier)
    with open("Historiques_des_valeurs_mesurees", "a") as fichier_texte: # on ouvre le fichier en tant que "fichier_texte"
        date =datetime.datetime.now()#on recupere la date et l'heure actuelle
        fichier_texte.write(f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}\n") #on l'ecrit dans le fichier
        for i in range(len(liste_des_humiditees)): #une boucle qui fait un tour par mesure
            fichier_texte.write(f"{liste_des_dates_de_mesures[i]}>>> humidite:{liste_des_humiditees[i]}% Temperature:{liste_des_temperature[i]}C\n") #on écrit les différentes valeurs dans le fichier (date, taux d'humidite et temperature)
        if len(liste_des_dates_de_mesures)>1: #si on a plus d'une valeur dans la mesure alors on ajoute les différentes moyennes au fichier
            fichier_texte.write(f"Humidite>>> moyenne:{moy_humidite}% minimum:{min_humidite}% maximum:{max_humidite}%\n")
            fichier_texte.write(f"Temperature>>> moyenne:{moy_temperature}C minimum:{min_temperature}C maximum:{max_temperature}C\n")

def popup_enregistrement(extension):#ouvre une fenêtre Popup qui creer une variable contennant un emplacement et un nom de fichier (avec son extension) - utile ur les modules d'exportation des valeur
    global emplacement # definition des variable suivante en variable globales
    emplacement =asksaveasfilename(title = "sauvegarder votre mesure", defaultextension=f".{extension}", initialfile="mesures") #enregistre un emplacement et un nom de fichier dans la variable, par le biais d'un explorateur de fichier.

def remise_a_zero():# on creer une fonction permettant de reinitialiser les valeurs mesures
    if askyesno("Attention", "Êtes vous sûre de vouloir faire ça?", icon="warning"): #ouvre une fenêtre d'alerte demandant a l'utilisateur si il est certain de vouloir reinitialiser ses valeurs
        liste_variable=[valeur_temperature, valeur_humidite, valeur_min_temperature, valeur_max_temperature, valeur_moyenne_temperature, valeur_min_humidite, valeur_max_humidite, valeur_moyenne_humidite]# creation d'une liste incluant toutes les valeurs à reinitialiser
        for i in liste_variable: #on parcourt les element de la liste
            i.config(text = "-")# on enleve toutes les valeurs de la liste et on les remplace par "-" comme initialement
        showinfo("information", "mis à zero!")# ouvre une fenêtre d'alerte pour confirmer a l'utilisateur que les valeurs ont bien ete mises a zero

def recuperation_valeurs():#cette fonction nous permet de faire la liaison entre la "zone de contrôle" de l'interface graphique et les autres fonctions du programme. Elle permet nottamment de recuperer les valeur des boutons radio et champs de saisie
    global nombre_de_mesures # definition des variable suivante en variable globales
    dure_mesure=int(case_dure_mesures.get())#recupere la valeure de la variable dure_mesure
    intervalle_temps=int(case_intervalle.get())#même fonctionnement que precedement
    nombre_de_seconde=int(nombre_seconde.get())#même fonctionnement que precedement
    nombre_de_mesures = int(dure_mesure*int(nombre_de_seconde)/intervalle_temps)#fait le calcul du nombre de mesures en fontion de la duree de la mesure, du nombre de seconde et de l'intervalle de temps

def graphique():# fonction permettant l'affichage et la modification ,via le menu preference ,du graphique
    if len(liste_des_humiditees)<=1:
        showinfo("Valeurs vide !", "Vous n'avez pas mesure asse de valeur pour afficher le graphique")
    else:
        liste_numeros_des_mesures = []# creation d'une liste qui remplace les dates mises initialement sur l'axe des abscisses par des numeros pour espaces les mesures
        for i in range(len(liste_des_dates_de_mesures)):
            liste_numeros_des_mesures.append(i+1)
        plt.title(f"Temperature et Taux d'humididte à partir de {liste_des_dates_de_mesures[0]}") #titre du graphique(il contient la date de la premiere mesure)
        plt.plot(liste_numeros_des_mesures, liste_des_humiditees, label="Taux d'humidite",linestyle=f"{aspect_courbe_humidite}", marker="+", color=f"{couleur_courbe_humidite}")#on ajoute la courbe qui montre les taux d'humidite en fonction des numeros des mesures. Cette courbe s'appelle "Taux d'humidite", elle à un aspect(linestyle) qui varie suivant les prefernce et les points sont notees par des "+"
        plt.plot(liste_numeros_des_mesures, liste_des_temperature, label="Temperature",linestyle=f"{aspect_courbe_temperature}", marker="+", color=f"{couleur_courbe_temperature}") #même fonctionnement
        plt.ylabel("valeur")#le nom de l'ordonnee
        plt.xlabel("numero de la mesure")#le nom de l'abssice
        plt.legend()#on indique qu'il faut afficher la legende de courbes
        plt.grid(True)#on affiche la grille
        plt.show()#on montre le graphique

###########################communication #######################################

def reception():#fonction qui permet de recevoir les valeurs mesurees par le capteur programmable
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures# definition des variable suivante en variable globales
    compteur=0#compteur qui permet determiner si les valeurs mesurees sont des taux d'humiditees ou des temperatures
    communication_serie = serial.Serial(port, 9600)#on demarre la connexion avec le capteur, en utilisant le module serial, par le port  port="COM4" à 9600 bit par secondes
    for i in range(nombre_de_mesures*3):#on lance une boucle qui fait nombre_de_mesures*3 tour, car chaque information envoyer par le capteur contient 3 information: une chaîne de debut (>>>), la temperature et l'humidite
        valeur = communication_serie.readline()#on lit la valeur  envoyer par le capteur
        valeur = str(valeur)#on la convertit en la valeur en chaîne de carractere
        if ">>>" in valeur:
            date = datetime.datetime.now()#on prends la date actuelle
            liste_des_dates_de_mesures.append(str(f"{date.hour}h{date.minute}m{date.second}s"))#on l'ajoute a la liste_des_dates_de_mesures
            compteur=0
            compteur+=1
        elif compteur==1:
            liste_des_humiditees.append(float(valeur[2:][:5]))#on ajoute à la liste d'humiditee en enlevant les 2 premier et 5 dernier carractere (ils sont inutiles pour nous)
            compteur+=1
        elif compteur==2:
            liste_des_temperature.append(float(valeur[2:][:5]))
            compteur=0
            time.sleep(int(case_intervalle.get()))# on attend le temps present dans la case "case_intervalle" avant d'effectuer une nouvelle mesure

def simulation_reception(): #simule la reception des donnees des capteur pour pouvoir coder sans capteur programmable
    showinfo("simulation","la simulation permet de simuler une mesure. Elle est fonctionnelle sans capteur et donne des valeurs aleatoire. Elle utilise les valeurs presentes dans zone de contrôle")
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures, nombre_de_mesures# definition des variable suivante en variable globales
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
def analyse_donnees(valeurs):#on cree une fonction qui a une liste de valeur defini/calcul une moyenne, un minimum et un maximum
    global maximum, minimum, moyenne # definition des variables suivantes en variable globales
    sommes_des_valeurs=0# on defini la sommme des valeurs
    for i in range(len(valeurs)):
        sommes_des_valeurs+=valeurs[i]#on ajoute tout les termes de la liste des valeurs dans la somme des valeurs
    moyenne=round(sommes_des_valeurs/(len(valeurs)),2)#on calcul la moyenne des valeurs mesurees
    maximum=max(valeurs)# on calcul le maximum des valeurs mesurees
    minimum=min(valeurs)# on calcul le minimum des valeurs mesurees

    # if inter_exter=="e":
    #     pass #moyennes de saisons

############################### eregristrement #################################

def enregistrement_texte():# on creefonction qui permet d'enregistrer les mesures dans un fichier texte
    global enregistrement# definition des variable suivante en variable globales
    enregistrement=1
    if len(liste_des_humiditees)==0:#si l'utilisateur n'a effectuer aucune mesure, alors on afficheune alerte pour lui dire qu'il ne peut pas enregisre
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectue de mesures")#affichage de l'alerte
    else:
        popup_enregistrement("txt")#demarre la fonction "popup_enregistrement" avec l'extension en argument
        if os.path.isfile(emplacement):#si le fichier existe deja a cet emplacement
            os.remove(emplacement)# alors on le remplace par le nouveau
        with open(emplacement, "x") as fichier_texte:# on ouvre le fichier en tant que fichoer_texte
          date = datetime.datetime.now()# on ajoute a la variable "date" la date actuelle
          fichier_texte.write(f"date: {date.day}/{date.month}/{date.year}\n")# on ecrit dans le fichier la date en jour, en mois et en annee
          for i in range(len(liste_des_humiditees)):#on parcours la liste des humiditees
              fichier_texte.write(f"{liste_des_dates_de_mesures[i]} >>> humidite: {liste_des_humiditees[i]}%   Temperature: {liste_des_temperature[i]}C\n")#on ecrit dans le fichier texte les valeurs mesurees
          if len(liste_des_dates_de_mesures)>1:# si la liste des dates de mesures comporte au minimum 2 valeurs
              fichier_texte.write(f"Humidite>>> moyenne:{moy_humidite}% minimum:{min_humidite}% maximum:{max_humidite}%\n")# alors on ecrit dans le fichier texte la moyenne, le minimum et le maximum du taux d'humidites
              fichier_texte.write(f"Temperature>>> moyenne:{moy_temperature}C minimum:{min_temperature}C maximum:{max_temperature}C\n")#meme fonctionnement que precedement avec la temperature
def enregistrement_CSV():
    global enregistrement# definition des variable suivante en variable globales
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectue de mesures")
    else:
        popup_enregistrement("csv") #demarre la fonction "popup_enregistrement" avec l'extension en argument
        if os.path.isfile(emplacement):
            os.remove(emplacement)
        with open(emplacement, "a", newline="") as ficher_csv:#"newline" permet de ne pas sauter de ligne entre chaque nouvelle ligne
            ecrire = csv.writer(ficher_csv, delimiter=" ") #on definit la variable "ecrire" qui sert a editer le fichier csv
            ecrire.writerow("Heure,Taux_d'humidite,Temperature")#on ecrit dans une nouvelle ligne du fichier
            for i in range(len(liste_des_humiditees)):
                ecrire.writerow(f"{liste_des_dates_de_mesures[i]},{liste_des_humiditees[i]}%,{liste_des_temperature[i]}C")
            if len(liste_des_dates_de_mesures)>1:
                ecrire.writerow(f"Humidite>>>,moyenne:{moy_humidite}%,minimum:{min_humidite}%,maximum:{max_humidite}%")
                ecrire.writerow(f"Temperature>>>,moyenne:{moy_temperature}C,minimum:{min_temperature}C,maximum:{max_temperature}C")

def enregistrement_reg():
    global enregistrement# definition des variable suivante en variable globales
    enregistrement=1
    if len(liste_des_humiditees)==0:
        showinfo("Aucunes valeurs", "Vous ne pouvez pas enregistrer car vous n'avez pas effectue de mesures")
    else:
        date = datetime.datetime.now()
        pressepapier="mesure(numero) temperature(c) humidite(taux)\n" #on definit une variable qui garde en memoire les noms et les unites des valeurs
        for i in range(len(liste_des_humiditees)):#on repete l'operation autant qu'il y a de mesures
            pressepapier=pressepapier + f"{i}  {liste_des_temperature[i]}  {liste_des_humiditees[i]}\n" # on ajoute a chaque fois le numero de la mesure, la temperature et le taux d'humidite
        pyperclip.copy(pressepapier) #on copie tout cela dans le presse-papier

##################################demarrage mesure et analyse ##################

def demarrage():#fonction qui s'execute l'orsque l'on appuie sur le bouton "Demarrer la mesure"
    enregistrement=0 #on remet a zero enregistrement car on effectue une nouvelle mesure
    global liste_des_humiditees, liste_des_temperature, liste_des_dates_de_mesures# definition des variable suivante en variable globales
    global min_humidite, max_humidite, moy_humidite, min_temperature, max_temperature, moy_temperature
    global simu
    liste_des_humiditees = []#on remet ces liste a zero
    liste_des_temperature = []
    liste_des_dates_de_mesures = []
    recuperation_valeurs()#on demarre la recuperation des valeurs
    if simu==1:# si l'utilisateur a demande une simulation
        simulation_reception()#alors on lance la fonction
    else:#sinon
        reception()#alors on lance la fonction
    simu = 0 #on remet la variable qui gère la simulation a zero
    temperature_actuelle=liste_des_temperature[len(liste_des_temperature)-1] #temperature_actuelle prend la derniere valeur mesuree
    humidite_actuelle=liste_des_humiditees[len(liste_des_humiditees)-1]
    valeur_temperature.config( text =  temperature_actuelle)#on mets a jour l'interface graphique principale avec les valeurs de temperature actuel
    valeur_humidite.config( text =  humidite_actuelle)

    if nombre_de_mesures!=1:  # si il y a plus d'une valeur dans la mesure
        analyse_donnees(liste_des_temperature) #on lance la fonction pour étudier les temperatures mesuree
        valeur_min_temperature.config(text = minimum)#on mets a jour l'interface graphique
        min_temperature = minimum #on assigne des noms de variable plus précis pour les fonction d'exportation
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
    sauvergarde_historique()#on sauvegarde la mesure dans l'historique
    showinfo("Mesures terminees", "vos mesures ont ete effectuees")

######################################debut ####################################
affichage_tkinter()
