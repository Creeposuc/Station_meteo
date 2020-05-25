from tkinter import *#importation du module Tkinter
import os#module qui nous permet dans notre cas de verifier la presence d'un fichier
def historique(): #fonction qui demarre l'interface graphique de l'historique
    global date_recherche_selectionne, boutton_recherche, affichage_resultat
    historique=Tk()

    bar_de_menu = Menu(historique)# création d'une barre de menu dans la fenêtre
    Menu_fichier = Menu(bar_de_menu, tearoff=0) # on créer une variable qui gère la barre de menu
    Menu_fichier.add_command(label = "quitter", command=exit)# création d'un boutton dans le menu déroulant qui a un nom (Label) et une commande (une fonction)
    bar_de_menu.add_cascade(label="Fichier", menu=Menu_fichier) #on donne le nom de "Fichier" au menu déroulant définit par Menu_fichier
    historique.config(menu=bar_de_menu)#on donne le menu précédent a la fenêtre de nom "fenetre"

    #la plupart des widgets ci dessous ont le meme fonctionnement, au moins un widget de chaque type est commente
    #Tout les widgets ci dessous sont places avec la methode de placement "grid"
    titre_historique = Label(historique, text="Historique", font=("bold",16)).grid(row=0, column=0)# creation d'un label qui a pour texte "Historique"

    cadre_recherche = Frame(historique, borderwidth=5, relief=GROOVE)# creation d'un cadre qui est place dans historique et qui contiendra la zone de recherche
    cadre_recherche.grid(row=1, column=0)
    titre_recherche = Label(cadre_recherche, text="Rechercher dans l'historique par date:").grid(row=0, column=0, columnspan=2)

    date_recherche_selectionne=StringVar()
    zone_de_recherche =  Entry(cadre_recherche, textvariable=date_recherche_selectionne ,width=40)# creation d'une zone de recherche contenu dans cadre_recherche
    zone_de_recherche.grid(row=1, column=0)
    date_recherche_selectionne.set("jour/mois/années heure:minute:seconde")

    boutton_recherche = Button(cadre_recherche, text="Rechercher", command=recherche_historique, bg="red").grid(row=1, column=1)# creation d'un boutton qui a pour texte "Rechercher", et pour commande recherche_historique

    cadre_historique = Frame(historique, borderwidth=5, relief=GROOVE)
    cadre_historique.grid(row=2, column=0)
    affichage_resultat = Text(cadre_historique, width=70, height=30)
    affichage_resultat.grid(row=0, column=0)

    historique.mainloop()

def recherche_historique():#recherche des mesures dans l'historique à partie de dates iscrite par l'utilisateur
    date_recherche=date_recherche_selectionne.get()#on récupère la date entrée dans le champ de saisie
    datetrouve=0
    with open("Historiques_des_valeurs_mesurées", "r") as fichier_texte: #on lis le ficier qui contient l'historique
        for ligne in fichier_texte:#on parcours les lignes du fichier
            if date_recherche in ligne:#si on trouve la date alors
                affichage_resultat.insert(END, ">>>>")#on ajoute dans ces carractere la fenetre de l'affiche de l'historique
                affichage_resultat.insert(END, ligne)#on ajoute la ligne dans la fenetre de l'affiche de l'historique
                datetrouve=1#on mets la variable datetrouve a 1
            elif datetrouve==1 and (">>>" in ligne):#si la ligne se touve derniere la date recherche et est une mesure
                affichage_resultat.insert(END, ligne)#alors on écrit la mesure
            else:#sinon
                datetrouve=0

historique()#on lance l'historique
