import csv
import datetime
import time
with open("valeurtest.csv", "a") as csvfile:
    ecrire = csv.writer(csvfile, delimiter=" ")
    for i in range(10):
        heure = datetime.datetime.now()
        print(f"{heure.hour}:{heure.minute}:{heure.second}")
        time.sleep(2)
        ecrire.writerow(f"{i},°C")
