from tkinter import *
from tkinter.colorchooser import *#gère les fenêtre popup
import os
couleur_boutton = "#FF0D39"
couleur_courbe_humidite = "#0502E8"
couleur_courbe_temperature = "#FF4A08"
def preference():
    global aspect_courbe_humidite, aspect_courbe_temperature
    preference=Tk()
    titre_preference = Label(preference, text="Préférence de l'affichage",font=("bold",16)).grid(row=0, column=0)

    cadre_preference_principal = Frame(preference, borderwidth=5, relief=GROOVE)
    cadre_preference_principal.grid(row=1, column=0)
    titre_interface_principal = Label(cadre_preference_principal, text="Interface principal", font=(14)).grid(row=0, column=0)

    titre_couleur_boutton = Label(cadre_preference_principal, text="Couleur des bouttons :").grid(row=1, column=0)
    boutton_couleur_boutton = Button(cadre_preference_principal, text="Choix de la couleur des bouttons", command=choix_couleur_boutton, bg="orange").grid(row=2, column=0)


    cadre_preference_graphique = Frame(preference, borderwidth=5, relief=GROOVE)
    cadre_preference_graphique.grid(row=2, column=0)
    titre_interface_graphique = Label(cadre_preference_graphique, text="Interface graphique", font=(14)).grid(row=0, column=0, columnspan=2)


    cadre_preference_courbe_temperature =Frame(cadre_preference_graphique, borderwidth=5, relief=GROOVE)
    cadre_preference_courbe_temperature.grid(row=1, column=0)

    titre_aspect_courbe_temperature = Label(cadre_preference_courbe_temperature, text="Aspect de la courbe de la température :", font=(12)).grid(row=0, column=0)
    aspect_courbe_temperature=StringVar()
    aspect_courbe_temperature.set("tp")
    courbe_temperature_trait_plein = Radiobutton(cadre_preference_courbe_temperature, text="Trait plein", variable=aspect_courbe_temperature, value="tp")
    courbe_temperature_trait_plein.grid(row=1, column=0)
    courbe_temperature_pointille = Radiobutton(cadre_preference_courbe_temperature, text="Pointillés", variable=aspect_courbe_temperature, value="pt")
    courbe_temperature_pointille.grid(row=2, column=0)
    # courbe_temperature_point_mesure = Radiobutton(cadre_preference_courbe_temperature, text="Points de mesures uniquement", variable=aspect_courbe_temperature, value="pm")
    # courbe_temperature_point_mesure.grid(row=3, column=0)

    titre_couleur_courbe_temperature = Label(cadre_preference_courbe_temperature, text="Couleur de la courbe de la température :", font=(12)).grid(row=4, column=0)
    boutton_couleur_courbe_temperature = Button(cadre_preference_courbe_temperature, text="Choix de la couleur de la courbe", command=choix_couleur_courbe_temperature, bg="orange").grid(row=5, column=0)


    cadre_preference_courbe_humidite = Frame(cadre_preference_graphique, borderwidth=5, relief=GROOVE)
    cadre_preference_courbe_humidite.grid(row=1, column=1)

    titre_aspect_courbe_humidite = Label(cadre_preference_courbe_humidite, text="Aspect de la courbe du taux d'humidité :", font=(12)).grid(row=0, column=0)
    aspect_courbe_humidite=StringVar()
    aspect_courbe_humidite.set("tp")
    courbe_humidite_trait_plein = Radiobutton(cadre_preference_courbe_humidite, text="Trait plein", variable=aspect_courbe_humidite, value="tp")
    courbe_humidite_trait_plein.grid(row=1, column=0)
    courbe_humidite_pointille = Radiobutton(cadre_preference_courbe_humidite, text="Pointillés", variable=aspect_courbe_humidite, value="pt")
    courbe_humidite_pointille.grid(row=2, column=0)
    # courbe_humidite_point_mesure = Radiobutton(cadre_preference_courbe_humidite, text="Points de mesures uniquement", variable=aspect_courbe_humidite, value="pm")
    # courbe_humidite_point_mesure.grid(row=3, column=0)

    titre_couleur_courbe_humidite = Label(cadre_preference_courbe_humidite, text="Couleur de la courbe du taux d'humidité :", font=(12)).grid(row=4, column=0)
    boutton_couleur_courbe_humidite = Button(cadre_preference_courbe_humidite, text="Choix de la couleur de la courbe", command=choix_couleur_courbe_humidite, bg="orange").grid(row=5, column=0)

    boutton_appliquer = Button(preference, text="Appliquer", command=appliquer_preference, bg="red").grid(row=3, column=0)
    preference.mainloop()

def choix_couleur_boutton():
    global couleur_boutton
    couleur_boutton = askcolor(title="Couleur des bouttons")[1]
    print(couleur_boutton)
def choix_couleur_courbe_temperature():
    global couleur_courbe_temperature
    couleur_courbe_temperature = askcolor(title="Couleur de la courbe de la température")[1]
def choix_couleur_courbe_humidite():
    global couleur_courbe_humidite
    couleur_courbe_humidite = askcolor(title="Couleur de la courbe du taux d'humidité")[1]

def appliquer_preference():
    if os.path.isfile("savegarde_des_preference.txt"):
        os.remove("savegarde_des_preference.txt")
    with open("savegarde_des_preference.txt","x") as save_pref:
        save_pref.write(f"{couleur_boutton}\n")
        save_pref.write(f"{couleur_courbe_temperature}\n")
        save_pref.write(f"{couleur_courbe_humidite}\n")
        save_pref.write(f"{aspect_courbe_humidite.get()}\n")
        save_pref.write(f"{aspect_courbe_temperature.get()}\n")
preference()
