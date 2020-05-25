from tkinter import * #importation du module Tkinter
from tkinter.colorchooser import *#gère les fenêtre popup
from tkinter.messagebox import * #module qui permet de d'afficher ici le selecteur de couleur
import os#module qui nous permet dans notre cas de verifier la presence d'un fichier
#les différentes variable ci dessous on des valeurs de base des préférence (si on applique sans modification)
couleur_boutton = "#FF0D39"
couleur_courbe_humidite = "#0502E8"
couleur_courbe_temperature = "#FF4A08"
aspect_courbe_humidite = "tp"
aspect_courbe_temperature = "tp"

def preference():
    global aspect_courbe_humidite, aspect_courbe_temperature
    preference=Tk()
    #la plupart des widgets ci dessous ont le meme fonctionnement, au moins un widget de chaque type est commente
    #Tout les widgets ci dessous sont places avec la methode de placement "grid"
    titre_preference = Label(preference, text="Préférence de l'affichage",font=("bold",16)).grid(row=0, column=0)# creation d'un label qui a pour texte "Preference de l'affichage"

    cadre_preference_principal = Frame(preference, borderwidth=5, relief=GROOVE)# creation d'un cadre qui est place dans preference et qui contiendra les preferences principales
    cadre_preference_principal.grid(row=1, column=0)
    titre_interface_principal = Label(cadre_preference_principal, text="Interface principal", font=(14)).grid(row=0, column=0)

    titre_couleur_boutton = Label(cadre_preference_principal, text="Couleur des bouttons :").grid(row=1, column=0)
    boutton_couleur_boutton = Button(cadre_preference_principal, text="Choix de la couleur des bouttons", command=choix_couleur_boutton, bg="orange").grid(row=2, column=0)# creation d'un boutton qui a pour texte "Choix de la couleur des bouttons", et pour commande choix_couleur_boutton


    cadre_preference_graphique = Frame(preference, borderwidth=5, relief=GROOVE)
    cadre_preference_graphique.grid(row=2, column=0)
    titre_interface_graphique = Label(cadre_preference_graphique, text="Interface graphique", font=(14)).grid(row=0, column=0, columnspan=2)


    cadre_preference_courbe_temperature =Frame(cadre_preference_graphique, borderwidth=5, relief=GROOVE)
    cadre_preference_courbe_temperature.grid(row=1, column=0)

    titre_aspect_courbe_temperature = Label(cadre_preference_courbe_temperature, text="Aspect de la courbe de la température :", font=(12)).grid(row=0, column=0)
    aspect_courbe_temperature=StringVar()# creation de la variable aspect_courbe_temperature
    aspect_courbe_temperature.set("tp")#on defini la variable sur la valeur "tp"
    courbe_temperature_trait_plein = Radiobutton(cadre_preference_courbe_temperature, text="Trait plein", variable=aspect_courbe_temperature, value="tp")#on cree un boutton radio qui a pour variable aspect_courbe_temperature et pour valeur "tp"
    courbe_temperature_trait_plein.grid(row=1, column=0)
    courbe_temperature_pointille = Radiobutton(cadre_preference_courbe_temperature, text="Pointillés", variable=aspect_courbe_temperature, value="pt")#on cree un boutton radio qui a pour variable aspect_courbe_temperature et pour valeur "pt"
    courbe_temperature_pointille.grid(row=2, column=0)

    titre_couleur_courbe_temperature = Label(cadre_preference_courbe_temperature, text="Couleur de la courbe de la température :", font=(12)).grid(row=4, column=0)
    boutton_couleur_courbe_temperature = Button(cadre_preference_courbe_temperature, text="Choix de la couleur de la courbe", command=choix_couleur_courbe_temperature, bg="orange").grid(row=5, column=0)


    cadre_preference_courbe_humidite = Frame(cadre_preference_graphique, borderwidth=5, relief=GROOVE)
    cadre_preference_courbe_humidite.grid(row=1, column=1)

    titre_aspect_courbe_humidite = Label(cadre_preference_courbe_humidite, text="Aspect de la courbe du taux d'humidité :", font=(12)).grid(row=0, column=0)
    aspect_courbe_humidite=StringVar()# creation de la variable aspect_courbe_humidite
    aspect_courbe_humidite.set("tp")#on defini la variable sur la valeur "tp"
    courbe_humidite_trait_plein = Radiobutton(cadre_preference_courbe_humidite, text="Trait plein", variable=aspect_courbe_humidite, value="tp")#on cree un boutton radio qui a pour variable aspect_courbe_humidite et pour valeur "tp"
    courbe_humidite_trait_plein.grid(row=1, column=0)
    courbe_humidite_pointille = Radiobutton(cadre_preference_courbe_humidite, text="Pointillés", variable=aspect_courbe_humidite, value="pt")#on cree un boutton radio qui a pour variable aspect_courbe_humidite et pour valeur "pt"
    courbe_humidite_pointille.grid(row=2, column=0)

    titre_couleur_courbe_humidite = Label(cadre_preference_courbe_humidite, text="Couleur de la courbe du taux d'humidité :", font=(12)).grid(row=4, column=0)
    boutton_couleur_courbe_humidite = Button(cadre_preference_courbe_humidite, text="Choix de la couleur de la courbe", command=choix_couleur_courbe_humidite, bg="orange").grid(row=5, column=0)

    boutton_appliquer = Button(preference, text="Appliquer", command=appliquer_preference, bg="red").grid(row=3, column=0)
    preference.mainloop()#lancement et ouverture des preferences

#les trois fonctions suivantes permettent de lancer des selecteur de couleurs, ces couleurs sont gardées en mémoire dans une variable définit en variable globale
def choix_couleur_boutton():
    global couleur_boutton
    couleur_boutton = askcolor(title="Couleur des bouttons")[1]
def choix_couleur_courbe_temperature():
    global couleur_courbe_temperature
    couleur_courbe_temperature = askcolor(title="Couleur de la courbe de la température")[1]
def choix_couleur_courbe_humidite():
    global couleur_courbe_humidite
    couleur_courbe_humidite = askcolor(title="Couleur de la courbe du taux d'humidité")[1]

def appliquer_preference():#fonction qui se lance quand l'utilisateur appuie sur appliquer, cette fonction enregistre dans un fichier les préférence de l'utlisateur selectionnées
    if os.path.isfile("savegarde_des_preference.txt"):#on supprime le fichier si il existe déjà
        os.remove("savegarde_des_preference.txt")
    with open("savegarde_des_preference.txt","x") as save_pref: #on ouvre le fichier en tant que save_pref
        save_pref.write(f"{couleur_boutton}\n") #on ecrit les differentes valeurs choisit par l'utilisateur
        save_pref.write(f"{couleur_courbe_temperature}\n")
        save_pref.write(f"{couleur_courbe_humidite}\n")
        save_pref.write(f"{aspect_courbe_humidite.get()}\n")
        save_pref.write(f"{aspect_courbe_temperature.get()}\n")
    showinfo("Redémmarage Recquis", "Un redémmarage de l'application est requis pour que les changements s'applique") #fenetre popup
preference()#on demarre la fonction preference
