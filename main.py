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

    # Kreditsummen
    hauskredit_kfw = 100000
    hauskredit_bank = sum(initiale_kosten.values()) - hauskredit_kfw
    kaufnebenkosten = 35000

    # Kreditgeber und deren Konditionen mit allen Änderungen über die Jahre
    kreditgeber_konditionen = {
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

    # Leere Liste für Kredit Ausgangsdaten im Jahresverlauf
    kredite_output = []

    # Durchlauf der einzelnen Kredite mit ihren jeweiligen Konditionen pro Jahr
    for kreditgeber, konditionen in kreditgeber_konditionen.items():
        print()
        print(kreditgeber)
        print("-"*len(kreditgeber))

        # Init der Variablen
        jahr = 0
        monat_letzter = 0
        monatliche_rate_letzte = 0
        restschuld = 0

        # Ausgangs Dict anlegen/zurücksetzen
        kredit_output = dict({
            'Jahre': [],
            'Restschulden': [],
            'Zinsen': [],
            'Tilgungen': [],
            'Sondertilgungen': [],
            'Kredite': []
        })

        # Durchlaufe für den aktuellen Kredit die Jahre bis die Restschuld beglichen ist
        while True:
            # Einmalige Änderungen zurücksetzen
            sondertilgung = 0
            kredit = 0

            # Prüfen, ob sich für das aktuelle Jahr Änderungen ergeben haben
            if jahr in konditionen:
                zinssatz        = konditionen[jahr]['zinssatz']
                rate_monatlich  = konditionen[jahr]['monatliche_rate']
                sondertilgung   = konditionen[jahr]['sondertilgung']
                kredit          = konditionen[jahr]['kredit']

            # Neue Kreditsumme zu Restschulden addieren (Initial + Nachschuss)
            restschuld += kredit
            kredit_output['Kredite'].append(kredit)

            # Jahreszinsen berechnen
            jahres_zinsen   = restschuld * zinssatz
            kredit_output['Zinsen'].append(jahres_zinsen)
            restschuld      = restschuld + jahres_zinsen
            kredit_output['Restschulden'].append(restschuld)         # Restschuld in Euro über die Laufzeit in Jahren


            # Sondertilgung von der Restschuld abziehen
            restschuld -= sondertilgung

            # Ausgabe von Jahr und Restschuld
            #print("Jahr", jahr, "Restschuld:", round(restschuld))

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
            kredit_output['Jahre'].append(jahr)                      # aktuelles Laufzeitjahr
            kredit_output['Tilgungen'].append(tilgung)               # aktuell zu zahlende Jahrestilgung
            kredit_output['Sondertilgungen'].append(sondertilgung)   # aktuell zu zahlende Sondertilgung

            # Falls die Laufzeit größer als 100 Jahre ist, wird die Schleife verlassen
            if jahr > 100:
                break

            if restschuld <= 0:
                break

            # Jahr
            jahr += 1

        kredite_output.append(kredit_output)

    # Dict in dem alle Kredite zusammensummiert werden
    kredite_kumuliert = dict({
        'Jahre':            [],
        'Zinsen':           [],
        'Restschulden':     [],
        'Tilgungen':        [],
        'Sondertilgungen':  [],
        'Monatliche Rate':  [],
        'Kredite':          [],
    })

    for i in range(len(kredite_output)):
        if len(kredite_kumuliert['Jahre']) < len(kredite_output[i]['Jahre']):
            kredite_kumuliert['Jahre'] = kredite_output[i]['Jahre']

        kredite_kumuliert['Zinsen']          = add_list(kredite_kumuliert['Zinsen'], kredite_output[i]['Zinsen'])
        kredite_kumuliert['Restschulden']    = add_list(kredite_kumuliert['Restschulden'], kredite_output[i]['Restschulden'])
        kredite_kumuliert['Tilgungen']       = add_list(kredite_kumuliert['Tilgungen'], kredite_output[i]['Tilgungen'])
        kredite_kumuliert['Sondertilgungen'] = add_list(kredite_kumuliert['Sondertilgungen'], kredite_output[i]['Sondertilgungen'])
        kredite_kumuliert['Monatliche Rate'] = add_list(kredite_kumuliert['Tilgungen'], kredite_kumuliert['Zinsen'])
        kredite_kumuliert['Kredite']         = add_list(kredite_kumuliert['Kredite'], kredite_output[i]['Kredite'])


    # Berechnung und Ausgabe der insgesamt für den Kredit gezahlten Summe + Relation zur Kreditsumme
    sondertilgungen_vollstaendig = sum(kredite_kumuliert['Sondertilgungen'])
    rueckzahlung_vollstaendig = sum(kredite_kumuliert['Zinsen']) + sum(kredite_kumuliert['Tilgungen']) + sum(kredite_kumuliert['Sondertilgungen'])
    kredit_vollstaendig = sum(kredite_kumuliert['Kredite'])
    print()
    print("     Kredit:", kredit_vollstaendig, "€")
    print("Rückzahlung:", round(rueckzahlung_vollstaendig), "€")
    print("Gewinn Bank:", round(rueckzahlung_vollstaendig - kredit_vollstaendig), "€")
    print()
    print("Rück.  Rel.:", round(rueckzahlung_vollstaendig / kredit_vollstaendig * 100), "%")


    # Plot
    kredit_anzahl = len(kreditgeber_konditionen)
    fig, axs = plt.subplots(nrows=2, ncols=1+kredit_anzahl, figsize=(4+4*kredit_anzahl,7), layout="constrained")
    fig.supxlabel("Jahre")
    fig.supylabel("Tausend Euro")

    ax = axs[0][0]
    ax.set_title("Kredite Kumuliert", weight="bold")
    ax.plot(kredite_kumuliert['Jahre'],np.array(kredite_kumuliert['Restschulden'])/1000, "-*", label='Restschulden')
    ax.legend()
    #ax.set_xlabel("Jahre")
    #ax.set_ylabel("Tausend Euro")
    ax.grid(True)

    ax = axs[1][0]
    ax.plot(kredite_kumuliert['Jahre'],np.array(kredite_kumuliert['Tilgungen'])/1000, "-*", label='Tilgung')
    ax.plot(kredite_kumuliert['Jahre'],np.array(kredite_kumuliert['Zinsen'])/1000, "-*", label='Zinsen')
    ax.plot(kredite_kumuliert['Jahre'], np.array(kredite_kumuliert['Monatliche Rate'])/1000, "-*", label='Monatliche Rate')
    ax.plot(kredite_kumuliert['Jahre'], np.array(kredite_kumuliert['Sondertilgungen']) / 1000, "*", label='Sondertilgungen')
    ax.legend()
    #ax.set_xlabel("Jahre")
    #ax.set_ylabel("Tausend Euro")
    ax.grid(True)

    for i, ax in enumerate(axs[0][1:]):
        #plt.subplot(int(plot_amount),2,i*2+1)
        ax.set_title((list(kreditgeber_konditionen.keys()))[i], weight='bold')
        ax.plot(kredite_output[i]['Jahre'], np.array(kredite_output[i]['Restschulden']) / 1000, "-*", label='Restschulden')
        ax.legend()
        #ax.xlabel("Jahre")
        #ax.set_ylabel("Tausend Euro")
        ax.grid(True)

    for i, ax in enumerate(axs[1][1:]):
        ax.plot(kredite_output[i]['Jahre'], np.array(kredite_output[i]['Tilgungen']) / 1000, "-*", label='Tilgung')
        ax.plot(kredite_output[i]['Jahre'], np.array(kredite_output[i]['Zinsen']) / 1000, "-*", label='Zinsen')
        ax.plot(kredite_output[i]['Jahre'], np.array(add_list(kredite_output[i]['Tilgungen'], kredite_output[i]['Zinsen'])) / 1000, "-*", label='Monatliche Rate')
        ax.plot(kredite_output[i]['Jahre'], np.array(kredite_output[i]['Sondertilgungen']) / 1000, "*", label='Sondertilgungen')
        ax.legend()
        #ax.set_xlabel("Jahre")
        #ax.set_ylabel("Tausend Euro")
        ax.grid(True)





    plt.show()



