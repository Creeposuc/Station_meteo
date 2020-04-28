import csv
import datetime
import time
# with open("valeurtest.csv", "a") as csvfile:
#     ecrire = csv.writer(csvfile, delimiter=" ")
#     for i in range(10):
#         ecrire = csv.writer(csvfile, delimiter=" ")
#         ecrire.writerow(f"{i},°C")

# def enregistrement_CSV(temperature, humidite):
#     with open("valeursmesure.csv", "a") as csvfile:
#         ecrire = csv.writer(csvfile, delimiter=" ")
#         date = datetime.datetime.now()
#         ecrire.writerow(f"Date:,{date.day}/{date.month}/{date.year}")
#         ecrire.writerow("Heure,Temperature,Taux d'humidité")
#         for i in range(len(temperature)):
#             date = datetime.datetime.now()
#             ecrire.writerow(f"{date.hour}:{date.minute}:{date.second},{temperature[i]}C,{humidite[i]}%")
#
# enregistrement_CSV([1,2,3,4], [1,2,3,4])

ti = datetime.datetime.now()
with open(f"valeurtest.csv", "a") as csvfile:
    temp_writer = csv.writer(csvfile, delimiter= ' ')
    temp_writer.writerow(f"{ti.hour}:{ti.minute},°C")
    temp_writer.writerow(f"{ti.hour}:{ti.minute},°C")
    temp_writer.writerow(f"{ti.hour}:{ti.minute},°C")
    temp_writer.writerow(f"{ti.hour}:{ti.minute},°C")
