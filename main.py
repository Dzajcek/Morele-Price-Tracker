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
            if name == "pc_sets":
                continue
            
            last_measurement = history[-1]
            price = last_measurement["price"]
            time = last_measurement["time"]
            print(f"{i}. nazwa: {name} | Aktualna cena: {price} zł (z dnia: {time})")

    def manage_pc_builder(self):
        if "pc_sets" not in self.products:
            self.products["pc_sets"] = {}
        
        set_name = "Moja Konfiguracja"
        
        if set_name not in self.products["pc_sets"]:
            self.products["pc_sets"][set_name] = []

        while True:
            current_set = self.products["pc_sets"][set_name]
            
            print(f"\n=== ZESTAW: {set_name} ===")
            if not current_set:
                print("Twój zestaw jest pusty.")
            else:
                total_price = 0
                for item_name in current_set:
                    if item_name in self.products:
                        last_price = self.products[item_name][-1]["price"]
                        total_price += last_price
                        print(f"- {item_name}: {last_price} zł")
                print(f"--- ŁĄCZNA CENA: {total_price:.2f} zł ---")

            print("\nOpcje:")
            print("1 - Dodaj produkt do zestawu")
            print("2 - Usuń produkt z zestawu")
            print("3 - Wykres ceny całego zestawu")
            print("4 - Udzial procentowy podzespolow")
            print("5 - Powrót")
            
            choice = input("> ")

            if choice == "1":
                available_prods = {k: v for k, v in self.products.items() if k != "pc_sets"}
                
                if not available_prods:
                    print("Brak produktów na głównej liście!")
                    continue

                for i, name in enumerate(available_prods.keys(), start=1):
                    print(f"{i}. {name}")

                try:
                    idx = int(input("Podaj numer produktu do dodania: ")) - 1
                    prod_name = list(available_prods.keys())[idx]
                    
                    if prod_name not in current_set:
                        self.products["pc_sets"][set_name].append(prod_name)
                        self.save_data()
                        print(f"Dodano {prod_name} do zestawu!")
                    else:
                        print("Ten produkt jest już w zestawie.")
                except:
                    print("Błąd wyboru.")

            elif choice == "2":
                for i, name in enumerate(current_set, 1):
                    print(f"{i}. {name}")
                try:
                    idx = int(input("Numer do usunięcia: ")) - 1
                    removed = self.products["pc_sets"][set_name].pop(idx)
                    self.save_data()
                    print(f"Usunięto {removed}")
                except:
                    print("Błąd.")

            elif choice == "3":
                self.draw_set_plot(set_name)

            elif choice == "4":
                self.draw_pc_pie_chart(set_name)

            elif choice == "5":
                break

    def draw_pc_pie_chart(self, set_name):
        current_set = self.products.get("pc_sets", {}).get(set_name, [])
        if not current_set:
            print("Zestaw jest pusty!")
            return

        labels = []
        sizes = []

        for prod_name in current_set:
            if prod_name in self.products:
                labels.append(prod_name)
                sizes.append(self.products[prod_name][-1]["price"])

        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, shadow=True)
        plt.title(f"Struktura kosztów zestawu: {set_name}")
        plt.axis('equal') 
        plt.tight_layout()
        plt.show()

    def update_all_prices(self):
        if not self.products:
            print("Brak produktów do aktualizacji.")
            return
        
        print(f"Aktualizacja {len(self.products)} produktow...")

        for name, history in self.products.items():
            if name == "pc_sets":
                continue
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

                        if history[-1].get("price") > price:
                            roznica = history[-1].get("price") - price
                            print(f"✔️ CENA SPADLA O {roznica:.2f} zł!")
                        elif history[-1].get("price") < price:
                            roznica = price - history[-1].get("price")
                            print(f"❌ CENA WZROSLA O {roznica:.2f} zł!!")
                        else:
                            print("🟡 CENA NIE ULEGLA ZMIANIE!")
                        
                        self.products[name].append({"price": price, "time": time, "url": url})
                        print(f"Zaktualizowano: {name} -> {price} zł")
                
                sleep(0.5)

            except Exception as e:
                print(f"Blad przy aktualizacji {name}: {e}")

        self.save_data()
        print("Aktualizacja zakonczona.")
        input("Wcisnij enter, aby kontynuowac")


    def draw_set_plot(self, set_name):
        current_set = self.products["pc_sets"][set_name]
        if not current_set: 
            return
        
        reference_product = current_set[0]
        if reference_product not in self.products:
            return
            
        dates = [entry["time"] for entry in self.products[reference_product]]
        total_prices_history = []

        for date in dates:
            daily_sum = 0
            for prod in current_set:
                price_on_date = 0
                for entry in self.products[prod]:
                    if entry["time"] <= date:
                        price_on_date = entry["price"]
                daily_sum += price_on_date
            total_prices_history.append(daily_sum)

        plt.figure(figsize=(12, 6))
        plt.plot(dates, total_prices_history, marker="o", markersize=4, color="green", linewidth=2, label="Cena zestawu")
        plt.title(f"Historia wartości zestawu: {set_name}")
        
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10)) 
        
        plt.xticks(rotation=45)
        plt.ylabel("Suma (zł)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def draw_plot(self):
            available_products = {k: v for k, v in self.products.items() if k != "pc_sets"}
            
            if not available_products:
                print("Brak danych do stworzenia wykresu.")
                input("Wcisnij enter, aby kontynuowac")
                return

            for i, name in enumerate(available_products.keys(), start=1):
                print(f"{i}. {name}")
            
            try:
                choice = int(input(f"Wybierz produkt (1-{len(available_products)}): ")) - 1
                product_name = list(available_products.keys())[choice]
                history = available_products[product_name]
                
                dates = [m["time"] for m in history]
                prices = [m["price"] for m in history]

                plt.figure(figsize=(10, 6))
                plt.plot(dates, prices, marker="o", linestyle="-", color="b")
                plt.title(f"Historia ceny: {product_name}")
                plt.xlabel("Data")
                plt.ylabel("Cena (zł)")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            except (ValueError, IndexError):
                print("Blad. Podano niepoprawny numer.")
                input("Wcisnij enter, aby kontynuowac")

def main():
    scraper = MoreleScraper()
    is_running = True
    while(is_running):
        print("\n=== MORELE SCRAPER ===")
        print("1 - Dodaj produkt")
        print("2 - Usun produkt")
        print("3 - Wyswietl produkty")
        print("4 - Utworz wykres produktu")
        print("5 - Aktualizuj wszystkie ceny")
        print("6 - Menedzer komputera")
        print("7 - Opusc program")
        
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
            scraper.manage_pc_builder()
        elif user_choice == "7":
            print("Dziekujemy za korzystanie z programu")
            is_running = False
        else:
            print("Blad. Niepoprawna opcja")


if __name__ == "__main__":
    main()