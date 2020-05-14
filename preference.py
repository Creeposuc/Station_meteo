from tkinter import *
import os
def preference():
    global couleur_boutton #couleur_courbe_temperature #couleur_courbe_humidite
    preference=Tk()
    titre_preference = Label(preference, text="Préférence de l'affichage",font=("bold",16)).grid(row=0, column=0)

    cadre_preference_principal = Frame(preference, borderwidth=5, relief=GROOVE)
    cadre_preference_principal.grid(row=1, column=0)
    titre_interface_principal = Label(cadre_preference_principal, text="Interface principal", font=(14)).grid(row=0, column=0)

    titre_couleur_boutton = Label(cadre_preference_principal, text="Couleur des bouttons :").grid(row=1, column=0)
    boutton_couleur_boutton = Button(cadre_preference_principal, text="Choix de la couleur des bouttons", command=choix_couleur_boutton, bg="red").grid(row=2, column=0)

    cadre_preference_graphique = Frame(preference, borderwidth=5, relief=GROOVE)
    cadre_preference_graphique.grid(row=2, column=0)
    titre_interface_graphique = Label(cadre_preference_graphique, text="Interface graphique", font=(14)).grid(row=0, column=0, columnspan=2)

    cadre_preference_courbe_temperature =Frame(cadre_preference_graphique, borderwidth=5, relief=GROOVE)
    cadre_preference_courbe_temperature.grid(row=1, column=0)

    titre_aspect_courbe_temperature = Label(cadre_preference_courbe_temperature, text="Aspect de la courbe de la température").grid(row=0, column=0)


    titre_couleur_courbe_temperature = Label(cadre_preference_courbe_temperature, text="Couleur de la courbe de la température :").grid(row=0, column=0)
    boutton_courbe_temperature = Button(cadre_preference_courbe_temperature, text="Choix de la couleur de la courbe", command=choix_couleur_courbe_temperature, bg="red").grid(row=1, column=0)

    cadre_preference_courbe_humidite = Frame(cadre_preference_graphique, borderwidth=5, relief=GROOVE)
    cadre_preference_courbe_humidite.grid(row=1, column=1)

    titre_aspect_courbe_humidite = Label(cadre_preference_courbe_humidite, text="Aspect de la courbe du taux d'humidité")

    boutton_appliquer = Button(preference, text="Appliquer", command=appliquer_preference, bg="red").grid(row=2, column=0)
    preference.mainloop()

def choix_couleur_boutton():
    global couleur_boutton
    couleur_boutton = askcolor(title="Couleur des bouttons", parent=preference)
def choix_couleur_courbe_temperature():
    global couleur_courbe_temperature
    couleur_courbe_temperature = askcolor(title="Couleur de la courbe de la température", parent=preference)
def choix_couleur_courbe_humidite():
    global couleur_courbe_humidite
    couleur_courbe_humidite = askcolor(title="Couleur de la courbe du taux d'humidité", parent=preference)

def appliquer_preference():
    os.remove("savegarde_des_preference.py")
    with open("savegarde_des_preference.txt","x") as save_pref:
        save_pref.write(couleur_boutton)
        #save_pref.write(couleur_courbe_temperature)
        # save_pref.write(couleur_courbe_humidite)
preference()
