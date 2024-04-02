import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Eingangsgrößen
    kredit_summe = 475000   # Euro
    zins = 0.0361           # Prozent
    tilgung = 1668          # Euro

    # Init der Variablen
    monate = ["Jan.", "Feb.", "Mär.", "Apr.", "Mai", "Jun.", "Jul.", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]

    jahr = 0
    monat_letzter = 0
    tilgung_letzte = 0
    jahre = []
    restschulden = []

    # Restschuld wird auf die Kreditsumme gesetzt
    restschuld = kredit_summe

    # Durchlaufe das nächste Jahr bis die Restschuld beglichen ist
    while restschuld > 0:
        # Listen für Grafische darstellung befüllen → Restschuld in Euro über die Laufzeit in Jahren
        jahre.append(jahr)
        restschulden.append(restschuld)

        # Falls die Restschuld gleich Null ist wird die Schleife verlassen
        if restschuld == 0:
            break

        # Monateweise abrechnung der Tilgung, um den letzten Monat exakt bestimmen zu können
        for i in range(12):
            restschuld = restschuld - tilgung
            # Wenn die Restschuld kleiner als Null ist, wird die Letzte Rate und der letzte Monat berechnet
            if restschuld < 0:
                tilgung_letzte = tilgung + restschuld
                restschuld = 0
                monat_letzter = int(i)
                break

        # Berechnung der Restschuld für das Folgejahr und Jahreszahl erhöhen
        restschuld = restschuld * (1+zins)
        jahr = jahr + 1

        # Ausgabe von Jahr und Restschuld
        print("Jahr", jahr, "Restschuld:", round(restschuld))


        # Falls die Laufzeit größer als 100 Jahre ist, wird die Schleife verlassen
        if jahr > 100:
            break

# Ausgabe des letzten Monats im letzten Jahr
print()
print("Letztes Jahr:", jahr)
print("Letzter Monat:", str(monat_letzter))

# Berechnung und Ausgabe der insgesamt für den Kredit gezahlten Summe + Relation zur Kreditsumme
rueckzahlung_vollstaendig = ((jahr - 1) * 12 + monat_letzter) * tilgung + tilgung_letzte
print()
print("     Kredit:", kredit_summe, "€")
print("Rückzahlung:", round(rueckzahlung_vollstaendig), "€")
print()
print("Rück.  Rel.:", round(rueckzahlung_vollstaendig / kredit_summe * 100), "%")


plt.plot(jahre,restschulden)
plt.show()



