import matplotlib.pyplot as plt

if __name__ == '__main__':
    kredit_summe = 475000   # Euro
    zins = 0.05             # Prozent
    tilgung = 2800          # Euro

    restschuld = kredit_summe
    jahr = 0

    jahre = []
    restschulden = []

    while restschuld > 0:
        jahre.append(jahr)
        restschulden.append(restschuld)

        restschuld = (restschuld - 12 * tilgung) * (1+zins)
        jahr = jahr + 1

        print("Jahr", jahr, "Restschuld:", restschuld)

        if jahr > 100:
            break

plt.plot(jahre,restschulden)
plt.show()



