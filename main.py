import matplotlib.pyplot as plt
import numpy as np
from itertools import zip_longest

def add_list(a_list:list, b_list:list):
    return [a + b for a, b in zip_longest(a_list, b_list, fillvalue=0)]

if __name__ == '__main__':
    # Eingangsgrößen
    initiale_kosten = {
        'Haus+Grund Kaufpreis':             350000,  # Fix
        'Acker Kaufpreis':                   25000,  # Fix
        'Wiese 1+2 Kaufpreis':                   0,  # Fix
        'Haupthaus Dämmung Fassade':         50000,  # geschätzt
        'Haupthaus Dämmung Dach':            10000,  # geschätzt - in Eigenleistung
#        'Saal Dämmung Fassade':              50000,  # geschätzt
#        'Saal Dämmung Dach':                 10000,
#        'Saal Ausbau EG':                   100000,  # geschätzt
#        'Saal Ausbau 1.OG':                 100000,  # geschätzt
    }

    hauskredit_kfw = 100000
    hauskredit_bank = sum(initiale_kosten.values()) - hauskredit_kfw
    kaufnebenkosten = 35000


    kredite_konditionen = {
        'Bank (Haus+Sanierung)': {
            # Hauptkredit Sparkasse / VR-Bank / etc.
            0: {'zinssatz': 0.04, 'monatliche_rate': 1700, 'sondertilgung': 0, 'kredit': hauskredit_bank},
        },
        'KfW 124 (Haus)': {
            # KfW Kredit 124 - Eigentumserwerb
            0: {'zinssatz': 0.0371, 'monatliche_rate': 500, 'sondertilgung': 0, 'kredit': hauskredit_kfw},
        },
        'Kauf-Nk. (Haus)': {
            # Kaufnebenkosten - Privatkredit
            0: {'zinssatz': 0.03, 'monatliche_rate': 1200, 'sondertilgung': 0, 'kredit': kaufnebenkosten},
        }
    }

    # Output Container
    jahre_pro_kredit = []
    zinsen_pro_kredit = []
    restschulden_pro_kredit = []
    tilgungen_pro_kredit = []
    sondertilgungen_pro_kredit = []
    kredite_pro_kredit = []

    for kreditgeber, kondition in kredite_konditionen.items():
        print()
        print(kreditgeber)
        print("-"*len(kreditgeber))




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

        jahre_pro_kredit.append(jahre)
        zinsen_pro_kredit.append(zinsen)
        restschulden_pro_kredit.append(restschulden)
        tilgungen_pro_kredit.append(tilgungen)
        sondertilgungen_pro_kredit.append(sondertilgungen)
        kredite_pro_kredit.append(kredite)

    jahre_sum               = []
    zinsen_sum              = []
    restschulden_sum        = []
    tilgungen_sum           = []
    sondertilgungen_sum     = []
    monatliche_rate_sum     = []
    kredite_sum             = []

    for i in range(len(jahre_pro_kredit)):
        if len(jahre_sum) < len(jahre_pro_kredit[i]):
            jahre_sum = jahre_pro_kredit[i]

        zinsen_sum              = add_list(zinsen_sum, zinsen_pro_kredit[i])
        restschulden_sum        = add_list(restschulden_sum, restschulden_pro_kredit[i])
        tilgungen_sum           = add_list(tilgungen_sum, tilgungen_pro_kredit[i])
        sondertilgungen_sum     = add_list(sondertilgungen_sum, sondertilgungen_pro_kredit[i])
        monatliche_rate_sum     = add_list(tilgungen_sum, zinsen_sum)
        kredite_sum             = add_list(kredite_sum, kredite_pro_kredit[i])


    # Berechnung und Ausgabe der insgesamt für den Kredit gezahlten Summe + Relation zur Kreditsumme
    sondertilgungen_summe = sum(sondertilgungen_sum)
    rueckzahlung_vollstaendig = sum(zinsen_sum) + sum(tilgungen_sum) + sum(sondertilgungen_sum)
    kredit_vollstaendig = sum(kredite_sum)
    print()
    print("     Kredit:", kredit_vollstaendig, "€")
    print("Rückzahlung:", round(rueckzahlung_vollstaendig), "€")
    print("Gewinn Bank:", round(rueckzahlung_vollstaendig - kredit_vollstaendig), "€")
    print()
    print("Rück.  Rel.:", round(rueckzahlung_vollstaendig / kredit_vollstaendig * 100), "%")


    # Plot
    kredit_anzahl = len(kredite_konditionen)
    fig, axs = plt.subplots(nrows=2, ncols=1+kredit_anzahl, figsize=(4+4*kredit_anzahl,7), layout="constrained")
    fig.supxlabel("Jahre")
    fig.supylabel("Tausend Euro")

    ax = axs[0][0]
    ax.set_title("Kredite Kumuliert", weight="bold")
    ax.plot(jahre_sum,np.array(restschulden_sum)/1000, "-*", label='Restschulden')
    ax.legend()
    #ax.set_xlabel("Jahre")
    #ax.set_ylabel("Tausend Euro")
    ax.grid(True)

    ax = axs[1][0]
    ax.plot(jahre_sum,np.array(tilgungen_sum)/1000, "-*", label='Tilgung')
    ax.plot(jahre_sum,np.array(zinsen_sum)/1000, "-*", label='Zinsen')
    ax.plot(jahre_sum, np.array(monatliche_rate_sum)/1000, "-*", label='Monatliche Rate')
    ax.plot(jahre_sum, np.array(sondertilgungen_sum) / 1000, "*", label='Sondertilgungen')
    ax.legend()
    #ax.set_xlabel("Jahre")
    #ax.set_ylabel("Tausend Euro")
    ax.grid(True)

    for i, ax in enumerate(axs[0][1:]):
        #plt.subplot(int(plot_amount),2,i*2+1)
        ax.set_title((list(kredite_konditionen.keys()))[i], weight='bold')
        ax.plot(jahre_pro_kredit[i], np.array(restschulden_pro_kredit[i]) / 1000, "-*", label='Restschulden')
        ax.legend()
        #ax.xlabel("Jahre")
        #ax.set_ylabel("Tausend Euro")
        ax.grid(True)

    for i, ax in enumerate(axs[1][1:]):
        ax.plot(jahre_pro_kredit[i], np.array(tilgungen_pro_kredit[i]) / 1000, "-*", label='Tilgung')
        ax.plot(jahre_pro_kredit[i], np.array(zinsen_pro_kredit[i]) / 1000, "-*", label='Zinsen')
        ax.plot(jahre_pro_kredit[i], np.array(add_list(tilgungen_pro_kredit[i], zinsen_pro_kredit[i])) / 1000, "-*", label='Monatliche Rate')
        ax.plot(jahre_pro_kredit[i], np.array(sondertilgungen_pro_kredit[i]) / 1000, "*", label='Sondertilgungen')
        ax.legend()
        #ax.set_xlabel("Jahre")
        #ax.set_ylabel("Tausend Euro")
        ax.grid(True)





    plt.show()



