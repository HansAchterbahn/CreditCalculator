import matplotlib.pyplot as plt
import numpy as np
from itertools import zip_longest
import pandas as pd
from tabulate import tabulate

def add_list(a_list:list, b_list:list):
    return [a + b for a, b in zip_longest(a_list, b_list, fillvalue=0)]

def eingangswerte():
    ####################################################################################################################
    # Eingangsgrößen
    ####################################################################################################################

    # Initile Kostenaufstellung
    einzel_kosten = {
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
    gesamt_kosten = sum(einzel_kosten.values())
    grundstuecks_kosten = (
        einzel_kosten['Haus+Grund Kaufpreis'] +
        einzel_kosten['Wiese 1+2 Kaufpreis'] +
        einzel_kosten['Acker Kaufpreis']
    )

    # Kreditsummen, die sich aus den Initialen Kosten ergeben
    kfw_124 = 100000            # es gibt 100.000 € für den Erwerb von Eigenheimen mit 3.71% Zinsen von der KfW (124)
    hauskredit_bank = gesamt_kosten - kfw_124   # Von den initialen Kosten wird KfW Kredit abgezogen
    kaufnebenkosten = grundstuecks_kosten * 0.1     # die Kaufnebenkosten betragen in der Regel 10% den Kaufpreises

    # Kreditgeber und deren Konditionen mit allen Änderungen über die Jahre
    kreditgeber_konditionen = {
        'Bank (Haus+Sanierung)': {
            # Hauptkredit Sparkasse / VR-Bank / etc.
            0: {'Zinssatz': 0.04, 'Monatliche Rate': 1700, 'Sondertilgung': 0, 'Aufgenommene Summe': hauskredit_bank},
            3: {'Zinssatz': 0.04, 'Monatliche Rate': 1700, 'Sondertilgung': 12000, 'Aufgenommene Summe': 0},
        },
        'KfW 124 (Haus)': {
            # KfW Kredit 124 - Eigentumserwerb
            0: {'Zinssatz': 0.0371, 'Monatliche Rate': 500, 'Sondertilgung': 0, 'Aufgenommene Summe': kfw_124},
        },
        'Kauf-Nk. (Haus)': {
            # Kaufnebenkosten - Privatkredit
            0: {'Zinssatz': 0.03, 'Monatliche Rate': 1200, 'Sondertilgung': 0, 'Aufgenommene Summe': kaufnebenkosten},
        }
    }

    return kreditgeber_konditionen

def berrechnung_der_kredite(kreditgeber_konditionen):
    ####################################################################################################################
    # Berechnung der Kredite über die Jahre und summierung der Kredite
    ####################################################################################################################

    # Leeres Dict für Kredit Ausgangsdaten im Jahresverlauf
    kredite_out = dict()

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
        kredit_out = dict({
            'Jahre': [],
            'Restschulden': [],
            'Zinsen': [],
            'Tilgungen': [],
            'Monatliche Rate': [],
            'Sondertilgungen': [],
            'Aufgenommene Summen': []
        })

        # Durchlaufe für den aktuellen Kredit die Jahre bis die Restschuld beglichen ist
        while True:
            # Einmalige Änderungen zurücksetzen
            #sondertilgung = 0
            aufgenommene_summe = 0

            # Prüfen, ob sich für das aktuelle Jahr Änderungen ergeben haben
            if jahr in konditionen:
                zinssatz            = konditionen[jahr]['Zinssatz']
                rate_monatlich      = konditionen[jahr]['Monatliche Rate']
                sondertilgung       = konditionen[jahr]['Sondertilgung']
                aufgenommene_summe  = konditionen[jahr]['Aufgenommene Summe']

            # Neue Kreditsumme zu Restschulden addieren (Initial + Nachschuss)
            restschuld += aufgenommene_summe
            kredit_out['Aufgenommene Summen'].append(aufgenommene_summe)

            # Jahreszinsen berechnen
            jahres_zinsen   = restschuld * zinssatz
            kredit_out['Zinsen'].append(jahres_zinsen)
            restschuld      = restschuld + jahres_zinsen
            kredit_out['Restschulden'].append(restschuld)         # Restschuld in Euro über die Laufzeit in Jahren

            # Ausgabe von Jahr und Restschuld
            #print("Jahr", jahr, "Restschuld:", round(restschuld))

            # Sondertilgung von der Restschuld abziehen
            restschuld -= sondertilgung

            # Monatsweise Abrechnung der Rate, um den letzten Monat exakt bestimmen zu können
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
            kredit_out['Jahre'].append(jahr)                      # aktuelles Laufzeitjahr
            kredit_out['Tilgungen'].append(tilgung)               # aktuell zu zahlende Jahrestilgung
            kredit_out['Sondertilgungen'].append(sondertilgung)   # aktuell zu zahlende Sondertilgung
            kredit_out['Monatliche Rate'].append(tilgung + jahres_zinsen)

            # Falls die Laufzeit größer als 100 Jahre ist, wird die Schleife verlassen
            if jahr > 100:
                break

            if restschuld <= 0:
                break

            # Jahr
            jahr += 1

        # Fertig berechneter Kredit wir im Kredite Dict gespeichert
        kredite_out[kreditgeber] = kredit_out

    # Kredite in einem Dict summieren
    kredite_kumuliert = dict({
        'Jahre':                [],
        'Restschulden':         [],
        'Zinsen':               [],
        'Tilgungen':            [],
        'Monatliche Rate':      [],
        'Sondertilgungen':      [],
        'Aufgenommene Summen':  [],
    })

    # Durchlaufen der Kredite → jeder Kredit wird einzeln aufsummiert
    for kredit in kredite_out.values():
        # Aufsummieren der einzelnen Elemente jedes Kredits (Jahre ausgenommen)
        for key in list(kredit.keys())[1:]:
            print(key)
            kredite_kumuliert[key] = add_list(kredite_kumuliert[key], kredit[key])

        # Die Jahre werden nicht summiert, sondern der längste Datensatz wird übernommen
        if len(kredite_kumuliert['Jahre']) < len(kredit['Jahre']):
            kredite_kumuliert['Jahre'] = kredit['Jahre']

    # Summierter Kredit wird zum Kedite Output Dict hinzugefügt → einfachere Verarbeitung in der Ausgabe (Table + Plot)
    kredite_out["Kredite Kumuliert"] = kredite_kumuliert

    return kredite_out

def erstelle_kredit_zusammenfassung(kredite_out):
    ####################################################################################################################
    # Berechnung und Ausgabe der insgesamt für den Kredit gezahlten Summe + Relation zur Kreditsumme
    ####################################################################################################################
    rueckzahlung_vollstaendig = (
        sum(kredite_out['Kredite Kumuliert']['Zinsen']) +
        sum(kredite_out['Kredite Kumuliert']['Tilgungen']) +
        sum(kredite_out['Kredite Kumuliert']['Sondertilgungen'])
        )
    augenommene_summe = sum(kredite_out['Kredite Kumuliert']['Aufgenommene Summen'])

    print()
    print("     Kredit:", augenommene_summe, "€")
    print("Rückzahlung:", round(rueckzahlung_vollstaendig), "€")
    print("Gewinn Bank:", round(rueckzahlung_vollstaendig - augenommene_summe), "€")
    print()
    print("Rück.  Rel.:", round(rueckzahlung_vollstaendig / augenommene_summe * 100), "%")

def erstelle_kredit_tabellen(kredite_out):
    ####################################################################################################################
    # Erstellen der Kreditverlauf-Tabelle
    ####################################################################################################################
    for kreditgeber, kredit in kredite_out.items():
        print()
        print(kreditgeber)
        print(tabulate(kredit, headers='keys', tablefmt='mixed_outline'))
        df = pd.DataFrame(kredit).to_excel('export/' + kreditgeber + '.xlsx')

def erstelle_kredit_plot(kredite_out):
    ####################################################################################################################
    # Plot der Ergebnisse
    ####################################################################################################################
    kredit_anzahl = len(kredite_out)
    fig, axs = plt.subplots(nrows=2, ncols=kredit_anzahl, figsize=(4*kredit_anzahl,7), layout="constrained")
    fig.supxlabel("Jahre")
    fig.supylabel("Tausend Euro")

    for i, (kreditgeber, kredit)in enumerate(kredite_out.items()):
        ax = axs[0][i]
        ax.set_title(kreditgeber, weight='bold')
        ax.plot(kredit['Jahre'], np.array(kredit['Restschulden']) / 1000, "-*", label='Restschulden')
        ax.legend()
        #ax.xlabel("Jahre")
        #ax.set_ylabel("Tausend Euro")
        ax.grid(True)

        ax = axs[1][i]
        ax.plot(kredit['Jahre'], np.array(kredit['Tilgungen']) / 1000, "-*", label='Tilgung')
        ax.plot(kredit['Jahre'], np.array(kredit['Zinsen']) / 1000, "-*", label='Zinsen')
        ax.plot(kredit['Jahre'], np.array(kredit['Monatliche Rate']) / 1000, "-*", label='Monatliche Rate')
        ax.plot(kredit['Jahre'], np.array(kredit['Sondertilgungen']) / 1000, "*", label='Sondertilgungen')
        ax.legend()
        #ax.set_xlabel("Jahre")
        #ax.set_ylabel("Tausend Euro")
        ax.grid(True)

    # speichern und anzeigen des Plots
    plt.savefig('export/Kredit_Kennlinien.jpg')
    plt.show()

if __name__ == '__main__':
    konditionen = eingangswerte()
    output = berrechnung_der_kredite(konditionen)
    
    erstelle_kredit_zusammenfassung(output)
    erstelle_kredit_tabellen(output)
    erstelle_kredit_plot(output)





