import matplotlib.pyplot as plt
import numpy as np
from itertools import zip_longest

def add_list(a_list:list, b_list:list):
    return [a + b for a, b in zip_longest(a_list, b_list, fillvalue=0)]

if __name__ == '__main__':
    # Eingangsgrößen

    preis_haus                = 350000
    preis_sanierung_haupthaus =  60000 #200000 # nur die Außendämmung, Wände und Bäder #300000 # über den Daumen gepeilt mit Internet Tool
    preis_sanierung_saal      = 250000  # über den Daumen gepeilt mit Internet Tool
    preis_acker               = 25000
    preis_wiese               = 0

    einzelposten = [
        preis_haus,
        preis_sanierung_haupthaus,
        #preis_sanierung_saal,
        #preis_wiese,
        #preis_acker
    ]


    kredite_konditionen = [
        {
            # Hauptkredit Sparkasse / VR-Bank / etc.
            0: {'zinssatz': 0.03, 'monatliche_rate': 500, 'sondertilgung': 0, 'kredit': 18000},
            #1: {'zinssatz': 0.03, 'monatliche_rate': 500, 'sondertilgung': 0, 'kredit': 0},
            #  5:  {'zinssatz': 0.04, 'monatliche_rate': 6000, 'sondertilgung': 30000},
            #  6:  {'zinssatz': 0.04, 'monatliche_rate': 6000, 'sondertilgung': 0},
            #  10: {'zinssatz': 0.03, 'monatliche_rate': 6000, 'sondertilgung': 0}
        },
        {
            # KfW Kredit 124 - Eigentumserwerb
            0: {'zinssatz': 0.03, 'monatliche_rate': 500, 'sondertilgung': 0, 'kredit': 18000},
            #1: {'zinssatz': 0.03, 'monatliche_rate': 500, 'sondertilgung': 0, 'kredit': 0},
            #0: {'zinssatz': 0.037, 'monatliche_rate': 500, 'sondertilgung': 0, 'kredit': 50000},
            #0: {'zinssatz': 0.0219, 'monatliche_rate': 1800, 'sondertilgung': 0},
            #2:  {'zinssatz': 0.037, 'monatliche_rate': 500, 'sondertilgung': 10000},
            #3:  {'zinssatz': 0.037, 'monatliche_rate': 500, 'sondertilgung': 0},
            #10: {'zinssatz': 0.03, 'monatliche_rate': 6000, 'sondertilgung': 0}
        },
        # {
        #     # Sonderkredit Kaufnebenkosten
        #     0: {'zinssatz': 0.05, 'monatliche_rate': 200, 'sondertilgung': 0, 'kredit': 35000}
        # }
    ]

    # Output Container
    jahre_output = []
    zinsen_output = []
    restschulden_output = []
    tilgungen_output = []
    sondertilgungen_output = []
    kredite_output = []

    for k, kondition in enumerate(kredite_konditionen):
        print()
        print("Kredit",k)
        print("--------")




        # Init der Variablen
        jahr = 0
        monat_letzter = 0
        monatliche_rate_letzte = 0
        restschuld = 0

        # Listen für die Auszuwertenden Daten vorbereiten
        jahre = []
        restschulden = []
        zinsen = []
        tilgungen = []
        sondertilgungen = []
        kredite = []

        # Durchlaufe die Jahre bis die Restschuld beglichen ist
        while True:
            # Einmalige Änderungen zurücksetzen
            sondertilgung = 0
            kredit = 0

            # Prüfen, ob sich für das aktuelle Jahr Änderungen ergeben haben
            if jahr in kondition:
                zinssatz        = kondition[jahr]['zinssatz']
                rate_monatlich  = kondition[jahr]['monatliche_rate']
                sondertilgung   = kondition[jahr]['sondertilgung']
                kredit          = kondition[jahr]['kredit']

            # Neue Kreditsumme zu Restschulden addieren (Initial + Nachschuss)
            restschuld += kredit
            kredite.append(kredit)

            # Jahreszinsen berechnen
            jahres_zinsen   = restschuld * zinssatz
            zinsen.append(jahres_zinsen)
            restschuld      = restschuld + jahres_zinsen
            restschulden.append(restschuld)         # Restschuld in Euro über die Laufzeit in Jahren


            # Sondertilgung von der Restschuld abziehen
            restschuld -= sondertilgung

            # Ausgabe von Jahr und Restschuld
            print("Jahr", jahr, "Restschuld:", round(restschuld))

            # Monateweise abrechnung der Rate, um den letzten Monat exakt bestimmen zu können
            raten_monatlich = []
            for i in range(12):
                restschuld = restschuld - rate_monatlich
                #print("  -", restschuld)
                # Wenn die Restschuld kleiner als Null ist, wird die letzte Rate und der letzte Monat berechnet
                if restschuld <= 0:
                    monatliche_rate_letzte = rate_monatlich + restschuld
                    restschuld = 0
                    monat_letzter = int(i)
                    raten_monatlich.append(monatliche_rate_letzte)
                    break
                raten_monatlich.append(rate_monatlich)
            # Berechnung der Restschuld und Jahreszahl erhöhen
            rate_jahr     = sum(raten_monatlich)
            tilgung         = rate_jahr - jahres_zinsen

            # Daten für Graphen aufnehmen
            jahre.append(jahr)                      # aktuelles Laufzeitjahr
            tilgungen.append(tilgung)               # aktuell zu zahlende Jahrestilgung
            sondertilgungen.append(sondertilgung)   # aktuell zu zahlende Sondertilgung

            # Falls die Laufzeit größer als 100 Jahre ist, wird die Schleife verlassen
            if jahr > 100:
                break

            if restschuld <= 0:
                break

            # Jahr
            jahr += 1

        jahre_output.append(jahre)
        zinsen_output.append(zinsen)
        restschulden_output.append(restschulden)
        tilgungen_output.append(tilgungen)
        sondertilgungen_output.append(sondertilgungen)
        kredite_output.append(kredite)

    jahre_sum               = []
    zinsen_sum              = []
    restschulden_sum        = []
    tilgungen_sum           = []
    sondertilgungen_sum     = []
    monatliche_rate_sum     = []
    kredite_sum             = []

    for i in range(len(jahre_output)):
        if len(jahre_sum) < len(jahre_output[i]):
            jahre_sum = jahre_output[i]

        zinsen_sum              = add_list(zinsen_sum, zinsen_output[i])
        restschulden_sum        = add_list(restschulden_sum, restschulden_output[i])
        tilgungen_sum           = add_list(tilgungen_sum, tilgungen_output[i])
        sondertilgungen_sum     = add_list(sondertilgungen_sum, sondertilgungen_output[i])
        monatliche_rate_sum     = add_list(tilgungen_sum, zinsen_sum)
        kredite_sum             = add_list(kredite_sum, kredite_output[i])


    # Berechnung und Ausgabe der insgesamt für den Kredit gezahlten Summe + Relation zur Kreditsumme
    sondertilgungen_summe = sum(sondertilgungen_sum)
    rueckzahlung_vollstaendig = sum(zinsen_sum) + sum(tilgungen_sum) + sum(sondertilgungen_sum)
    kredit_vollständig = sum(kredite_sum)
    print()
    print("     Kredit:", kredit_vollständig, "€")
    print("Rückzahlung:", round(rueckzahlung_vollstaendig), "€")
    print("Gewinn Bank:", round(rueckzahlung_vollstaendig-kredit_vollständig), "€")
    print()
    print("Rück.  Rel.:", round(rueckzahlung_vollstaendig / kredit_vollständig * 100), "%")

    plt.figure(1)
    plt.subplot(1,2,1)
    plt.plot(jahre_sum,np.array(restschulden_sum)/1000, "-*", label='Restschulden')
    plt.legend()
    plt.xlabel("Jahre")
    plt.ylabel("Tausend Euro")
    plt.grid(True)

    plt.subplot(1,2,2)
    plt.plot(jahre_sum,np.array(tilgungen_sum)/1000, "-*", label='Tilgung')
    plt.plot(jahre_sum,np.array(zinsen_sum)/1000, "-*", label='Zinsen')
    plt.plot(jahre_sum, np.array(monatliche_rate_sum)/1000, "-*", label='Monatliche Rate')
    plt.plot(jahre_sum, np.array(sondertilgungen_sum) / 1000, "*", label='Sondertilgungen')
    plt.legend()
    plt.xlabel("Jahre")
    #plt.ylabel("Tausend Euro")
    plt.grid(True)


    plt.show()



