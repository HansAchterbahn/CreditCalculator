import matplotlib.pyplot as plt

if __name__ == '__main__':
    kredit_summe = 475000   # Euro
    zins = 0.0361             # Prozent
    tilgung = 1668          # Euro

    monate = ["Jan.", "Feb.", "Mär.", "Apr.", "Mai", "Jun.", "Jul.", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]

    restschuld = kredit_summe
    jahr = 0
    monat_letzter = 0
    tilgung_letzte = 0
    jahre = []
    restschulden = []

    while restschuld > 0:
        jahre.append(jahr)
        restschulden.append(restschuld)

        if restschuld == 0:
            break

        for i in range(12):
            restschuld = restschuld - tilgung
            if restschuld < 0:
                tilgung_letzte = tilgung - restschuld
                restschuld = 0
                monat_letzter = int(i)
                break

        restschuld = restschuld * (1+zins)
        jahr = jahr + 1

        print("Jahr", jahr, "Restschuld:", round(restschuld))



        if jahr > 100:
            break


print()
print("Letztes Jahr:", jahr)
print("Letzter Monat:", str(monat_letzter))

gesamt_summe = ((jahr-1) * 12 + monat_letzter) * tilgung + tilgung_letzte
print("Summe Gesamt:", round(gesamt_summe))
print("Zurückgezahlt:", round(gesamt_summe/kredit_summe*100), "%")


plt.plot(jahre,restschulden)
plt.show()



