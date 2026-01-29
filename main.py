import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import datetime
import json
import os
from time import sleep

class MoreleScraper:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
        }
 
        folder = os.path.dirname(__file__)
        self.file_name = os.path.join(folder, "products.json")

        self.products = {}

        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as file:
                    self.products = json.load(file)
                print(f"Zaladowano dane dla {len(self.products)} produktow.")
            except Exception as e:
                print(f"Blad podczas wczytywania pliku: {e}")

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self.products, file, indent=4, ensure_ascii=False)

    def add_product(self):
        print("Podaj poprawny link produktu ze strony morele.net")
        try:
            url = input("> ")
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                name = soup.find("h1", class_="prod-name").get_text().strip()
                price_elements = soup.find("div", id="product_price")

                if price_elements:
                    price = price_elements["data-price"]
                
                time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                
                if name not in self.products:
                    self.products[name] = []

                self.products[name].append({"price": float(price), "time": time, "url": url})
                
                self.save_data()
                print(f"SUKCES. Dodano do listy: {name}")
                input("Wcisnij enter, aby kontynuowac")
        except:
            print("Blad. Link nie dziala lub jest niepoprawny")
            input("Wcisnij enter, aby kontynuowac")


    def remove_product(self):
        if not self.products:
            print("Twoja lista produktow jest pusta.")
            return
        self.display_products()
        try:
            user_choice = int(input(f"Podaj numer produktu (1-{len(self.products)}) ktory chcesz usunac: "))

            products_name = list(self.products.keys())

            if 1 <= user_choice <= len(products_name):
                delete_product_name = products_name[user_choice-1]
                self.products.pop(delete_product_name)

                self.save_data()  
                print(f"SUKCES. Usunięto z listy: {delete_product_name}.")
                input("Wcisnij enter, aby kontynuowac")
            else:
                print("Blad. Numer poza zakresem")
                input("Wcisnij enter, aby kontynuowac")

        except ValueError:
            print("Blad. Musisz podać liczbe.")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")
            input("Wcisnij enter, aby kontynuowac")


    def display_products(self):
        if not self.products:
            print("Twoja lista produktow jest pusta.")
            input("Wcisnij enter, aby kontynuowac")
            return
        
        for i, (name, history) in enumerate(self.products.items(), start=1):
            last_measurement = history[-1]
            price = last_measurement["price"]
            time = last_measurement["time"]
            print(f"{i}. nazwa: {name} | Aktualna cena: {price} zł (z dnia: {time})")

    def update_all_prices(self):
        if not self.products:
            print("Brak produktów do aktualizacji.")
            return
        
        print(f"Aktualizacja {len(self.products)} produktow...")

        for name, history in self.products.items():
            url = history[-1].get("url")
            if not url:
                print(f"Pominieto {name} (brak zapisanego linku).")
                continue

            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    price_element = soup.find("div", id="product_price")
                    
                    if price_element:
                        price = float(price_element["data-price"])
                        time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                        
                        self.products[name].append({"price": price, "time": time, "url": url})
                        print(f"Zaktualizowano: {name} -> {price} zł")
                
                sleep(1)

            except Exception as e:
                print(f"Blad przy aktualizacji {name}: {e}")

        self.save_data()
        print("Aktualizacja zakonczona.")
        input("Wcisnij enter, aby kontynuowac")


    def draw_plot(self):
        if not self.products:
            print("Twoja lista produktow jest pusta.")
            input("Wcisnij enter, aby kontynuowac")
            return
        self.display_products()
        try:
            user_input = int(input(f"Podaj produkt 1-{len(self.products)}: ")) - 1
            product_name = list(self.products.keys())[user_input]
        except:
            print("Blad. Podano niepoprawna wartosc.")
            input("Wcisnij enter, aby kontynuowac")
            return
        history = self.products[product_name]
        
        dates = [m["time"] for m in history]
        prices = [m["price"] for m in history]

        plt.plot(dates, prices, marker="o", linestyle="-")
        plt.title(f"Zmiana ceny: {product_name}")
        plt.xlabel("Data")
        plt.ylabel("Cena (zł)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    scraper = MoreleScraper()
    is_running = True

    while(is_running):
        print("\n=== MORELE SCRAPER ===")
        print("1 - Dodaj produkt")
        print("2 - Usun produkt")
        print("3 - Wyswietl produkty")
        print("4 - Utworz wykres")
        print("5 - Aktualizuj wszystkie ceny")
        print("6 - Opusc program")
        
        user_choice = input("> ")
        if user_choice == "1":
            scraper.add_product()
        elif user_choice == "2":
            scraper.remove_product()
        elif user_choice == "3":
            scraper.display_products()
        elif user_choice == "4":
            scraper.draw_plot()
        elif user_choice == "5":
            scraper.update_all_prices()
        elif user_choice == "6":
            print("Dziekujemy za korzystanie z programu")
            is_running = False
        else:
            print("Blad. Niepoprawna opcja")