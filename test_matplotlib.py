import datetime
import matplotlib.pyplot as plt
import time
liste_des_dates = []
for i in range(4):
    date = datetime.datetime.now()
    liste_des_dates.append(f"{date.minute}m{date.second}s")
    time.sleep(1)

plt.title("Danger de la vitesse")
plt.plot(liste_des_dates, [1,0,4,3])
plt.xlabel('Vitesse')
plt.ylabel('Temps')
plt.show()
