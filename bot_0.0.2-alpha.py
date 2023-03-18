
from bs4 import BeautifulSoup
import string
import random
import time
import requests
from datetime import datetime
import config
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

timer = (8, 19)

apiToken = os.getenv("API_TOKEN")
chatID = os.getenv("CHAT_ID")
refferal = "%26tag=" + os.getenv("REFFERAL_CODE")


fun = random.randint(900, 1600)
lista = []
lista2 = []
cont = 0

headers = config.headers


def orologio(timer):
    block = False

    while block == False:
        ore = datetime.now().strftime('%H:%M').split(":")

        if (int(ore[0]) < int(timer[0])) or (int(ore[0]) > int(timer[1])):
            time.sleep(5)
            pass
        else:
            block = True
            return "FALSE"


def controllo(url):
    if (len(url) <= 80):
        return 0
    else:
        return True


def send_to_telegram(message):

    link = message["URL"]
    discounted_price = message["discounted_price"]
    original_price = message["original_price"]
    discounted_percentage = message["discount_percentage"]
    product_title = message["product_title"]
    code = codegen()

    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage?chat_id=@{chatID}&parse_mode=HTML&text=⌛️OFFERTA A TEMPO⌛️\n\n<b>{product_title[:90]}</b>\n\nPrezzo: <b>{discounted_price}</b> <s>{original_price}</s>\nSconto: <b>{discounted_percentage}</b>\nLink: <a href="{link}">https://amzn.to/{code}</a>\n'

    # api = {"URL": url, "discounted_price": discounted_price, "original_price": original_price, "discount_percentage": discount_percentage}

    try:
        if (message == None):
            print("ora (" + datetime.now().strftime('%H:%M') + "): Errore di Codifica")
            pass
        else:
            response = requests.post(apiURL).json
            if str(response) == "<bound method Response.json of <Response [200]>>":
                adesso = datetime.now().strftime('%H:%M')
                print("\n_____________________________\n")
                print("Ora: " + adesso)
                print("Titolo: " + data["product_title"])
                print("Prezzo: " + data["discounted_price"])
                print("prezzo vecchio: " + data["original_price"])
                print("Percentuale di sconto: " +
                      data["discount_percentage"])
                time.sleep(fun)
            cw = 1
            while str(response) != "<bound method Response.json of <Response [200]>>":
                if cw == 3:
                    print(
                        "ora (" + datetime.now().strftime('%H:%M') + "): Errore link...")
                    print(response)
                    break
                else:
                    response = requests.post(apiURL).json
                    print("ora (" + datetime.now().strftime('%H:%M') +
                          "): Tentatico n°: " + str(cw))
                    cw = cw + 1

    except Exception as e:
        print(e)
        pass


def codegen():

    x = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
        string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    return x


def trova(url, lista=lista):
    response = requests.get(url, headers=headers, timeout=5)


# Analizza l'HTML della pagina con Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

# Trova tutti i tag <a> che contengono l'attributo "href"
    links = soup.find_all("a", {"class": "a-link-normal"}, href=True)

# Stampa tutti i link trovati

    for link in links:
        if (link["href"] == "#"):
            pass
        else:
            lista.append(link["href"])
            # print("https://www.amazon.it" + link["href"])


def trova_prezzo_e_sconto(url):

    try:
        response = requests.get(url, headers=headers, timeout=5)
        # Analizza l'HTML della pagina con Beautiful Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Cerca il prezzo scontato
        prices = soup.find_all("span", {"class": "a-offscreen"})
        discounted_price = prices[0].text
        original_price = soup.find_all(
            "span", {"class": "a-price a-text-price"})
        original_price = original_price[0].find(
            "span", {"class": "a-offscreen"}).text
        discount_percentage = soup.find('span', {'class': 'savingsPercentage'})
        discount_percentage = discount_percentage.text.strip()

        product_title = soup.find_all('span', {'id': 'productTitle'})
        product_title = soup.find('span', {'id': 'productTitle'})
        product_title = product_title.text.strip()

    except:
        discounted_price = "0"
        original_price = "0"
        discount_percentage = "0"
        product_title = ""

    # Restituisci un dizionario con tutte le informazioni utili
    if (discounted_price == "0"):
        return None
    else:
        return {"URL": url, "discounted_price": discounted_price, "original_price": original_price, "discount_percentage": discount_percentage, "product_title": product_title}


if __name__ == "__main__":
    print("ora (" + datetime.now().strftime('%H:%M') + "): Bot Inizializzato....")

    try:
        f = open(".backupList.csv", "r")
        lista2 = list(f.split(","))
        f.close()
    except:
        pass

    while cont <= 1:

        for x in config.url:
            trova(x)
        lista = list(dict.fromkeys(lista))
        lista = random.sample(lista, len(lista))

        for i in lista:
            orologio(timer)
            if "https://www.amazon.it" + i in lista2:
                print("(IN LISTA) -> " + "https://www.amazon.it"+i)
                pass
            elif (i.startswith("/sspa/click?")):
                pass
            elif (i.startswith("/product-reviews/")):
                pass
            elif (i.startswith("/hz/")):
                pass
            elif (i.startswith("/dp/")):
                pass
            elif (i.startswith("/gp/")):
                pass
            elif (i.startswith("/b/")):
                pass
            elif (i.startswith("h")):
                pass
            elif (i.startswith("/promotion/")):
                pass
            elif (i.startswith("/stores/")):
                pass
            elif (i.startswith("/computer/")):
                pass
            else:
                # print("non in lista")
                # print("https://www.amazon.it" + i)
                check = controllo("https://www.amazon.it" + i)

                lista2.append("https://www.amazon.it" + i)

                f = open(".backupList.csv", "a")
                lista_file = ','.join(lista2)
                f.write(lista_file)
                f.close()
                n = "https://www.amazon.it" + i + "%26" + "linkCode=ll1" + refferal
                check = controllo(n)

                if check == True:
                    data = trova_prezzo_e_sconto(n)
                    try:
                        send_to_telegram(data)
                    except:
                        pass
                else:
                    pass
