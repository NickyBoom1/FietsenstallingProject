import csv
import random
import datetime


def csvread(bestandsnaam):
    with open("database/" + bestandsnaam, "r") as ReadMyCsv:
        reader = csv.DictReader(ReadMyCsv, delimiter=";")

        gegevens = []
        for gegeven in reader:
            gegevens.append(gegeven)

    return gegevens


def registreren():
    """Functie voor het registreren van de gebruiker. Slaat de gegevens op in gebruikers.csv"""
    gegevens = csvread("gebruikers.csv")

    mail = input("E-mail adres: ")
    mail_lijst = []
    for gegeven in gegevens:
        mail_lijst.append(gegeven['mail'])

    while mail in mail_lijst:
        print("Dit e-mail adress is al geregistreerd")
        mail = input("E-mail adres: ")

    naam = input("Voornaam: ")
    tussenvoegsel = input("Tussenvoegsel: ")
    achternaam = input("Achternaam: ")

    while True:
        try:
            telefoonnummer = int(input("Telefoon nummer: "))
            break
        except:
            print("Telefoonnummer klopt niet..")

    wachtwoord = input("Wachtwoord: ")

    while len(wachtwoord) <= 6:
        print("Wachtwoord moet ten minste 6 tekens lang zijn.. ")
        wachtwoord = input("Wachtwoord: ")

    fietsnummer = int(random.randint(1000, 9999))

    fietsnummer_lijst = []
    for gegeven in gegevens:
        fietsnummer_lijst.append(gegeven['fietsnummer'])

    while str(fietsnummer) in fietsnummer_lijst:
        fietsnummer = int(random.randint(1000, 9999))

    nieuwe_gegevens = str(fietsnummer) + ';' + naam + ';' + tussenvoegsel + ';' + achternaam + ';' + mail + ';' + wachtwoord + ';' + str(telefoonnummer)

    bestand = open('database/gebruikers.csv', 'a') #nog in een fucntie zetten?
    bestand.write(nieuwe_gegevens + '\n')
    bestand.close()


def persoonlijke_informatie_opvragen():
    print("U moet eerst inloggen om deze gegevens te mogen bekijken.")
    correctLogin = 0

    while correctLogin == 0:
        correctLogin = inloggen()

    gegevens = csvread("gebruikers.csv")
    stalling_gegevens = csvread("gestald.csv")

    for gegeven in gegevens:
        if mail == gegeven["mail"]:
            if gegeven["tussenvoegsel"] == "":
                print("Uw volledige naam: " + gegeven["voornaam"] + " " + gegeven["achternaam"])
            else:
                print("Uw volledige naam: " + gegeven["voornaam"] + " " + gegeven["tussenvoegsel"] + " " + gegeven[
                    "achternaam"])
            print("Uw unieke fietsnummer is: " + gegeven["fietsnummer"])
            print("Uw e-mail adres is: " + gegeven["mail"])
            print("Uw telefoonnummer is: " + gegeven["telefoonnummer"])

        for fietsdata in stalling_gegevens:
            if gegeven["fietsnummer"] == fietsdata["fietsnummer"]:
                data = fietsdata["staldata"]

    print("En dan nog iets doen met -> " + data)


def algemene_informatie_aanvragen():
    gegevens = csvread("gestald.csv")

    vrije_plekken = 1000 - (len(gegevens) + 1)

    print("Er zijn nog " + str(vrije_plekken) + " van de 1000 plekken over.")
    print("De kosten voor het bergen van uw fiets zijn 0.10 euro per uur.")


def inloggen():
    global mail             # voor in de functies informatie opvragen
    gegevens_gebruiker = csvread("gebruikers.csv")
    mail = str(input("Geef je e-mailadres: "))
    wachtwoord = str(input("Geef je wachtwoord: "))
    counter = 3

    while counter > 0:
        for item in gegevens_gebruiker:
            if str(item['wachtwoord']) == wachtwoord and str(item['mail']) == mail:
                return (str(item['fietsnummer']))
        else:
            print("Combinatie is niet correct.. " + "Je hebt nog " + str(counter) + "inlogpogingen over..")
            mail = str(input("Geef je e-mailadres: "))
            wachtwoord = str(input("Geef je wachtwoord: "))
            counter -= 1

    print("Inlogpogingen overschreden..")
    return 0


def stallen():
    vandaag = datetime.datetime.today()
    datum = vandaag.strftime('/%d/%m/%Y')
    tijd = vandaag.strftime('%H/%M')
    gegevens = csvread('gestald.csv')
    response_inloggen = inloggen()

    if response_inloggen != 0:

        fietsnummer = input("Fietsnummer: ")

        pogingen_fietsnummer = 0
        while str(fietsnummer) != response_inloggen and pogingen_fietsnummer < 5:
            print(str(fietsnummer) + " is niet geregistreerd.. Probeer opnieuw..")
            fietsnummer = input("Fietsnummer: ")
            pogingen_fietsnummer += 1

        fietsnummer_lijst = []
        for gegeven in gegevens:
            fietsnummer_lijst.append(gegeven['fietsnummer'])

        if fietsnummer in fietsnummer_lijst:
            print("Fiets staat al in stalling..")

        else:
            print("Fiets kan gestald worden..")
            gegevens_stalling = str(fietsnummer) + ";" + tijd + datum

            bestand = open('database/gestald.csv', 'a')  # nog in een fucntie zetten?
            bestand.write(gegevens_stalling + '\n')
            bestand.close()

    else:
        print("Fiets kan niet gestald worden..")