import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # Eingangsgrößen

    preis_haus                = 399000
    preis_sanierung_haupthaus = 50000 #200000 # nur die Außendämmung, Wände und Bäder #300000 # über den Daumen gepeilt mit Internet Tool
    preis_moebel_haupthaus    = 0
    preis_sanierung_saal      = 250000  # über den Daumen gepeilt mit Internet Tool
    preis_moebel_saal         = 0
    preis_acker               = 20000
    preis_wiese               = 5000

    einzelposten = [
        preis_haus,
        preis_sanierung_haupthaus,
        #preis_moebel_haupthaus,
        #preis_sanierung_saal,
        #preis_moebel_saal,
        #preis_wiese,
        #preis_acker
    ]

    kredit_summe = sum(einzelposten)

    jahres_modalitaeten = {
        0:  {'zinssatz': 0.04, 'monatliche_rate': 2200, 'sondertilgung': 0},
#        0: {'zinssatz': 0.0219, 'monatliche_rate': 1800, 'sondertilgung': 0},
#        5:  {'zinssatz': 0.04, 'monatliche_rate': 6000, 'sondertilgung': 30000},
#        6:  {'zinssatz': 0.04, 'monatliche_rate': 6000, 'sondertilgung': 0},
#        10: {'zinssatz': 0.03, 'monatliche_rate': 6000, 'sondertilgung': 0}
    }

    zinssatz        = jahres_modalitaeten[0]['zinssatz']
    monatliche_rate = jahres_modalitaeten[0]['monatliche_rate']
    sondertilgung   = jahres_modalitaeten[0]['sondertilgung']

    # Init der Variablen
    monate = ["Jan.", "Feb.", "Mär.", "Apr.", "Mai", "Jun.", "Jul.", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]

    jahr = 0
    monat_letzter = 0
    monatliche_rate_letzte = 0
    jahre = []
    restschulden = []
    zinsen = []
    tilgungen = []
    sondertilgungen = []

    # Restschuld wird auf die Kreditsumme gesetzt
    jahres_zins = kredit_summe * zinssatz
    tilgung = monatliche_rate*12 - jahres_zins
    restschuld = kredit_summe + jahres_zins

    # Durchlaufe das nächste Jahr bis die Restschuld beglichen ist
    while restschuld > 0:
        # Prüfen, ob sich für das aktuelle Jahr Änderungen ergeben haben
        if jahr in jahres_modalitaeten:
            zinssatz        = jahres_modalitaeten[jahr]['zinssatz']
            monatliche_rate = jahres_modalitaeten[jahr]['monatliche_rate']
            sondertilgung   = jahres_modalitaeten[jahr]['sondertilgung']

        # Sondertilgung von der Restschuld abziehen
        restschuld = restschuld - sondertilgung
        sondertilgungen.append(sondertilgung)

        # Daten für Graphen aufnehemen
        jahre.append(jahr)                  # aktuelles Laufzeitjahr
        restschulden.append(restschuld)     # Restschuld in Euro über die Laufzeit in Jahren
        zinsen.append(jahres_zins)          # aktuell zu zahlende Jahreszinsen
        tilgungen.append(tilgung)           # aktuell zu zahlende Jahrestilgung

        # Monateweise abrechnung der Tilgung, um den letzten Monat exakt bestimmen zu können
        for i in range(12):
            restschuld = restschuld - monatliche_rate
            # Wenn die Restschuld kleiner als Null ist, wird die Letzte Rate und der letzte Monat berechnet
            if restschuld < 0:
                monatliche_rate_letzte = monatliche_rate + restschuld
                restschuld = 0
                monat_letzter = int(i+1)
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
sondertilgungen_summe = sum(sondertilgungen)
rueckzahlung_vollstaendig = ((jahr - 1) * 12 + monat_letzter) * monatliche_rate + monatliche_rate_letzte + sondertilgungen_summe
print()
print("     Kredit:", kredit_summe, "€")
print("Rückzahlung:", round(rueckzahlung_vollstaendig), "€")
print("Gewinn Bank:", round(rueckzahlung_vollstaendig-kredit_summe), "€")
print()
print("Rück.  Rel.:", round(rueckzahlung_vollstaendig / kredit_summe * 100), "%")

plt.figure(1)
plt.subplot(1,2,1)
plt.plot(jahre,np.array(restschulden)/1000, label='Restschulden')
plt.legend()
plt.xlabel("Jahre")
plt.ylabel("Tausend Euro")
plt.grid(True)

plt.subplot(1,2,2)
plt.plot(jahre,np.array(tilgungen)/1000, label='Tilgung')
plt.plot(jahre,np.array(zinsen)/1000, label='Zinsen')
plt.legend()
plt.xlabel("Jahre")
#plt.ylabel("Tausend Euro")
plt.grid(True)

plt.show()



