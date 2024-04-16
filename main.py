import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Eingangsgrößen

    preis_haus                = 399000
    preis_sanierung_haupthaus = 300000  # über den Daumen gepeilt mit Internet Tool
    preis_moebel_haupthaus    =  50000
    preis_sanierung_saal      = 500000  # über den Daumen gepeilt mit Internet Tool
    preis_moebel_saal         = 0
    preis_acker               = 0
    preis_wiese               = 0

    kredit_summe    = preis_haus + \
        preis_sanierung_haupthaus + \
        preis_moebel_haupthaus + \
        preis_sanierung_saal + \
        preis_moebel_saal + \
        preis_wiese + \
        preis_acker

    zinssatz        = 0.04 #0.0371        # Prozent
    monatliche_rate = 6000          # Euro

    # Init der Variablen
    monate = ["Jan.", "Feb.", "Mär.", "Apr.", "Mai", "Jun.", "Jul.", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]

    jahr = 0
    monat_letzter = 0
    monatliche_rate_letzte = 0
    jahre = []
    restschulden = []
    zinsen = []
    tilgungen = []

    # Restschuld wird auf die Kreditsumme gesetzt
    jahres_zins = kredit_summe * zinssatz
    tilgung = monatliche_rate*12 - jahres_zins
    restschuld = kredit_summe + jahres_zins

    # Durchlaufe das nächste Jahr bis die Restschuld beglichen ist
    while restschuld > 0:
        # Listen für Grafische darstellung befüllen → Restschuld in Euro über die Laufzeit in Jahren
        jahre.append(jahr)
        restschulden.append(restschuld)
        zinsen.append(jahres_zins)
        tilgungen.append(tilgung)

        # Monateweise abrechnung der Tilgung, um den letzten Monat exakt bestimmen zu können
        for i in range(12):
            restschuld = restschuld - monatliche_rate
            # Wenn die Restschuld kleiner als Null ist, wird die Letzte Rate und der letzte Monat berechnet
            if restschuld < 0:
                monatliche_rate_letzte = monatliche_rate + restschuld
                restschuld = 0
                monat_letzter = int(i)
                break

        # Berechnung der Restschuld für das Folgejahr und Jahreszahl erhöhen
        jahres_zins = restschuld * zinssatz
        tilgung = monatliche_rate*12 - jahres_zins
        restschuld = restschuld + jahres_zins
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
rueckzahlung_vollstaendig = ((jahr - 1) * 12 + monat_letzter) * monatliche_rate + monatliche_rate_letzte
print()
print("     Kredit:", kredit_summe, "€")
print("Rückzahlung:", round(rueckzahlung_vollstaendig), "€")
print("Gewinn Bank:", round(rueckzahlung_vollstaendig-kredit_summe), "€")
print()
print("Rück.  Rel.:", round(rueckzahlung_vollstaendig / kredit_summe * 100), "%")

plt.figure(1)
plt.subplot(1,2,1)
plt.plot(jahre,restschulden, label='Restschulden')
plt.legend()
plt.xlabel("Jahre")
plt.ylabel("Euro")
plt.grid(True)

plt.subplot(1,2,2)
plt.plot(jahre,tilgungen, label='Tilgung')
plt.plot(jahre,zinsen, label='Zinsen')
plt.legend()
plt.xlabel("Jahre")
plt.ylabel("Euro")
plt.grid(True)

plt.show()



