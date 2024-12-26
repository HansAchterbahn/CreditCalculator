from unittest.mock import inplace

import matplotlib.pyplot as plt
import numpy as np
from itertools import zip_longest
import pandas as pd
from tabulate import tabulate
import yaml
from pprint import pprint
import subprocess

def add_list(a_list:list, b_list:list):
    # method to add two lists together and return the result
    return [a + b for a, b in zip_longest(a_list, b_list, fillvalue=0)]

def eingangswerte(*kredit_pakete:str):
    # YAML Datei mit Kreditdaten lesen
    with open("loan.yaml", mode="rb") as file:
        result = yaml.safe_load(file)
    kreditgeberkonditionen = {}
    for paket in kredit_pakete:
        kreditgeberkonditionen.update(result[paket])

    print("Kreditgeberkonditionen")
    pprint(kreditgeberkonditionen)
    print()

    return kreditgeberkonditionen

def berrechnung_der_kredite(kreditgeber_konditionen):
    # Berechnung der Kredite über die Jahre und summierung der Kredite

    # Leeres Dict für Kredit Ausgangsdaten im Jahresverlauf
    kredite_out = dict()

    # Durchlauf der einzelnen Kredite mit ihren jeweiligen Konditionen pro Jahr
    print('Berechne:')
    for kreditgeber, konditionen in kreditgeber_konditionen.items():
        print('-', kreditgeber)

        # Init der Variablen
        jahr = 1
        restschuld = 0

        # Ausgangs Dict anlegen/zurücksetzen
        kredit_out = dict({
            'Jahre': [],
            'Restschulden': [],
            'Zinsen': [],
            'Tilgungen': [],
            'Jährliche Rate': [],
            'Sondertilgungen': [],
            'Aufgenommene Summen': []
        })

        kondition = dict({
            'Zinssatz': 0,
            'Monatliche Rate': 0,
            'Sondertilgung': 0,
            'Aufgenommene Summe': 0
        })

        # Durchlaufe für den aktuellen Kredit die Jahre bis die Restschuld beglichen ist
        while True:
            # Einmalige Änderungen zurücksetzen
            #kondition['Sondertilgung'] = 0
            kondition['Aufgenommene Summe'] = 0

            # Prüfen, ob sich für das aktuelle Jahr Änderungen ergeben haben
            if jahr in konditionen:
                for k in konditionen[jahr]:
                    kondition[k] = konditionen[jahr][k]

            # Neue Kreditsumme zu Restschulden addieren (Initial + Nachschuss)
            restschuld += kondition['Aufgenommene Summe']
            kredit_out['Restschulden'].append(round(restschuld, 2))         # Restschuld in Euro über die Laufzeit in Jahren

            # Jahreszinsen berechnen
            zinsen_jahr   = round(restschuld * kondition['Zinssatz'], 2)
            kredit_out['Zinsen'].append(zinsen_jahr)
            restschuld      = restschuld + zinsen_jahr

            # Monatsweise Abrechnung der Rate, um den letzten Monat exakt bestimmen zu können
            raten_monatlich = []
            for i in range(12):
                restschuld = restschuld - kondition['Monatliche Rate']
                # Wenn die Restschuld kleiner als Null ist, wird die letzte Rate und der letzte Monat berechnet
                if restschuld <= 0:
                    monatliche_rate_letzte = kondition['Monatliche Rate'] + restschuld
                    restschuld = 0
                    raten_monatlich.append(monatliche_rate_letzte)
                    break
                raten_monatlich.append(kondition['Monatliche Rate'])

            # Sondertilgung von der Restschuld abziehen
            if restschuld > 0:
                restschuld -= kondition['Sondertilgung']
                if restschuld <= 0:
                    kondition['Sondertilgung'] = kondition['Sondertilgung'] + restschuld
            else:
                kondition['Sondertilgung'] = 0

            # Berechnung der Restschuld und Jahreszahl erhöhen
            rate_jahr     = round(sum(raten_monatlich),2)
            tilgung_jahr  = round(rate_jahr - zinsen_jahr,2)

            # Daten für Graphen aufnehmen
            kredit_out['Jahre'].append(jahr)                      # aktuelles Laufzeitjahr
            kredit_out['Tilgungen'].append(tilgung_jahr)               # aktuell zu zahlende Jahrestilgung
            kredit_out['Sondertilgungen'].append(kondition['Sondertilgung'])   # aktuell zu zahlende Sondertilgung
            kredit_out['Jährliche Rate'].append(tilgung_jahr + zinsen_jahr)
            kredit_out['Aufgenommene Summen'].append(kondition['Aufgenommene Summe'])

            # Falls die Laufzeit größer als 100 Jahre ist, wird die Schleife verlassen
            if jahr > 100:
                break

            if restschuld <= 0.004:
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
        'Jährliche Rate':      [],
        'Sondertilgungen':      [],
        'Aufgenommene Summen':  [],
    })

    # Durchlaufen der Kredite → jeder Kredit wird einzeln aufsummiert
    for kredit in kredite_out.values():
        # Aufsummieren der einzelnen Elemente jedes Kredits (Jahre ausgenommen)
        for key in list(kredit.keys())[1:]:
            kredite_kumuliert[key] = add_list(kredite_kumuliert[key], kredit[key])

        # Die Jahre werden nicht summiert, sondern der längste Datensatz wird übernommen
        if len(kredite_kumuliert['Jahre']) < len(kredit['Jahre']):
            kredite_kumuliert['Jahre'] = kredit['Jahre']

    # Summierter Kredit wird zum Kedite Output Dict hinzugefügt → einfachere Verarbeitung in der Ausgabe (Table + Plot)
    kredite_out["Kredite Kumuliert"] = kredite_kumuliert

    return kredite_out

def erstelle_kredit_zusammenfassung(kredite_out):
    # Berechnung und Ausgabe der insgesamt für den Kredit gezahlten Summe + Relation zur Kreditsumme
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
    # Erstellen der Kreditverlauf-Tabelle
    for kreditgeber, kredit in kredite_out.items():
        table_mixed_outline = tabulate(kredit, headers='keys', tablefmt='mixed_outline', floatfmt='.2f')
        kredit_reduced_cols = kredit.copy()
        kredit_reduced_cols.popitem()
        kredit_reduced_cols.popitem()
        table_markdown = tabulate(kredit_reduced_cols, headers='keys', tablefmt='pipe', floatfmt='.2f')

        print()
        print(kreditgeber)
        print(table_mixed_outline)

        pd.DataFrame(kredit).to_excel('export/' + kreditgeber + '.xlsx')

        with open('export/'+kreditgeber+'.table', 'w') as table_file:
            table_file.write(table_markdown)

def erstelle_kredit_plot(kredite_out, interval):
    # Plot der Ergebnisse
    # interval: monthly / yearly
    if interval == "monthly":
        year_divider = 12
    else:
        year_divider = 1


    kredit_anzahl = len(kredite_out)
    fig, axs = plt.subplots(nrows=2, ncols=kredit_anzahl, figsize=(4*kredit_anzahl,7), layout="constrained")
    fig.supxlabel("Jahre")
    #fig.supylabel("Tausend Euro")

    for i, (kreditgeber, kredit)in enumerate(kredite_out.items()):
        # Aktuellen Plot für Restschulden festlegen (obere Zeile)
        ax = axs[0][i]

        # Plot Titel erstellen (Kreditgeber, Zinsen, Monatliche Rate)
        aufgenommene_summe = round(sum(kredit["Aufgenommene Summen"])/1000) # in tausend €
        zins = round(kredit["Zinsen"][0]/kredit["Aufgenommene Summen"][0]*100, 2)
        rate = round(kredit["Jährliche Rate"][0]/year_divider, 2)
        ax.set_title(kreditgeber+"\n\n", weight='bold', fontsize=16)
        ax.set_title(
            "Summe: "+str(aufgenommene_summe)+" t€\n"+\
            "Zins:  "+str(zins)+" %", loc = "left"
        )
        ax.set_title("Rate: "+str(rate)+" €", loc = "right")


        # Restschulden plotten
        ax.plot(kredit['Jahre'], np.array(kredit['Restschulden']) / 1000, "-*", label='Restschulden')
        ax.legend()
        #ax.xlabel("Jahre")
        if i == 0:
            ax.set_ylabel("Tausend Euro")
        ax.grid(True)

        # Aktuellen Plot für Tilgung, Zinsen, Rate und Sondertilgung festlegen & plotten
        ax = axs[1][i]
        ax.plot(kredit['Jahre'], np.array(kredit['Tilgungen']) / year_divider, "-*", label='Tilgung')
        ax.plot(kredit['Jahre'], np.array(kredit['Zinsen']) / year_divider, "-*", label='Zinsen')
        ax.plot(kredit['Jahre'], np.array(kredit['Jährliche Rate']) / year_divider, "-*", label='Rate')
        ax.plot(kredit['Jahre'], np.array(kredit['Sondertilgungen']) / year_divider, "*", label='Sondertilgungen')
        ax.legend()
        #ax.set_xlabel("Jahre")
        if i == 0:
            ax.set_ylabel("Euro")
        ax.grid(True)

    # speichern und anzeigen des Plots
    plt.savefig('export/Kredit_Kennlinien.jpg')
    plt.show()

def erstelle_kredit_plot_singles(kredite_out, interval):
    # Plot der Ergebnisse
    # interval: monthly / yearly
    if interval == "monthly":
        year_divider = 12
    else:
        year_divider = 1


    kredit_anzahl = len(kredite_out)
    for i, (kreditgeber, kredit)in enumerate(kredite_out.items()):

        # figure definieren
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9,4), layout="constrained")

        # Restschulden festlegen & plotten
        ax = axs[0]
        ax.plot(kredit['Jahre'], np.array(kredit['Restschulden']) / 1000, "-*", label='Restschulden')
        ax.legend()
        ax.set_xlabel("Jahre")
        ax.set_ylabel("Tausend Euro")
        ax.grid(True)

        # Plot für Tilgung, Zinsen, Rate und Sondertilgung festlegen & plotten
        ax = axs[1]
        ax.plot(kredit['Jahre'], np.array(kredit['Tilgungen']) / year_divider, "-*", label='Tilgung')
        ax.plot(kredit['Jahre'], np.array(kredit['Zinsen']) / year_divider, "-*", label='Zinsen')
        ax.plot(kredit['Jahre'], np.array(kredit['Jährliche Rate']) / year_divider, "-*", label='Rate')
        ax.plot(kredit['Jahre'], np.array(kredit['Sondertilgungen']) / year_divider, "*", label='Sondertilgungen')
        ax.legend()
        ax.set_xlabel("Jahre")
        ax.set_ylabel("Euro")
        ax.grid(True)

        # speichern und anzeigen des Plots
        save_path = 'export/' + kreditgeber + '.jpg'
        save_path = save_path.replace(' ', '_')
        plt.savefig(save_path)
        #plt.show()

def erstelle_tilgungsplaene(kredit_output):
    with open('template.md', 'r') as template:
        md_text_template = template.read()

    for i, (kreditgeber, kredit) in enumerate(kredit_output.items()):
        print(kreditgeber)

        aufgenommene_summe = round(sum(kredit["Aufgenommene Summen"])) # in tausend €
        zins = round(kredit["Zinsen"][0]/kredit["Aufgenommene Summen"][0]*100, 2)
        rate = round(kredit["Jährliche Rate"][0], 2)

        md_text = md_text_template

        with open('export/'+kreditgeber+'.table', 'r') as table:
            md_table = table.read()

        md_text = md_text.replace('{{kreditgeber}}', kreditgeber)
        md_text = md_text.replace('{{aufgenommene_summe}}', str(aufgenommene_summe))
        md_text = md_text.replace('{{zinssatz}}', str(zins))
        md_text = md_text.replace('{{jaehrliche_rate}}', str(rate))
        md_text = md_text.replace('{{tilgung_tabelle}}', md_table)
        md_text = md_text.replace('{{tilgung_grafik}}', kreditgeber.replace(' ', '_')+'.jpg')

        with open('export/'+kreditgeber+'.md', 'w') as md_file:
            md_file.write(md_text)
        try:
            subprocess.run(['pandoc', 'export/'+kreditgeber+'.md', '-o', 'export/'+kreditgeber+'.pdf', '--variable=geometry:' + 'a4paper'])
        except:
            print('Was not able to create "' + kreditgeber+'.pdf".')



if __name__ == '__main__':
    # Kreditdaten einlesen und berechnen
    konditionen = eingangswerte(
        "01-Bank-innen-minimal-im-ersten-jahr",
        "21-Privatkredite"
    )
    output = berrechnung_der_kredite(konditionen)

    # Kredit übersicht erstellen
    erstelle_kredit_zusammenfassung(output)
    erstelle_kredit_tabellen(output)
    erstelle_kredit_plot(output, "monthly")

    # Tilgungspläne erstellen
    erstelle_kredit_plot_singles(output, "yearly")
    erstelle_tilgungsplaene(output)



