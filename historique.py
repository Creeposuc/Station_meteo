from tkinter import *
import os
print(">>>lancement_historique")
def historique():
    global date_recherche_selectionne, boutton_recherche, affichage_resultat

    historique=Tk()
    titre_historique = Label(historique, text="Historique", font=("bold",16)).grid(row=0, column=0)

    cadre_recherche = Frame(historique, borderwidth=5, relief=GROOVE)
    cadre_recherche.grid(row=1, column=0)
    titre_recherche = Label(cadre_recherche, text="Rechercher dans l'historique par date:").grid(row=0, column=0, columnspan=2)

    date_recherche_selectionne=StringVar()
    zone_de_recherche =  Entry(cadre_recherche, textvariable=date_recherche_selectionne ,width=19)
    zone_de_recherche.grid(row=1, column=0)
    date_recherche_selectionne.set("jour/mois/années")

    boutton_recherche = Button(cadre_recherche, text="Rechercher", command=recherche_historique, bg="red").grid(row=1, column=1)

    cadre_historique = Frame(historique, borderwidth=5, relief=GROOVE)
    cadre_historique.grid(row=2, column=0)
    affichage_resultat = Text(cadre_historique, width=50, height=30)
    affichage_resultat.grid(row=0, column=0)

    historique.mainloop()

def recherche_historique():
    date_recherche=date_recherche_selectionne.get()
    print("recherche de >", date_recherche)

    with open("Historiques_des_valeurs_mesurées", "r") as fichier_texte:
        for ligne in fichier_texte:
            if date_recherche in ligne:
                print("date trouvé")
                affichage_resultat.insert(END, (ligne))
            elif ">>>" in ligne:
                affichage_resultat.insert(END, (ligne))
            else:
                break
        fichier_texte.close()
    print("fin de la recherche")
historique()
os.system("pause")
