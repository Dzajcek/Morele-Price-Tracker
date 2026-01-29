# Morele Price Tracker 📈

Prosty monitor cen produktów ze sklepu Morele.net napisany w Pythonie. 
Program pozwala śledzić zmiany cen w czasie i wizualizować je na wykresach.

## Motivation
This project was born out of a real need while building a new PC. At the time, component prices (especially RAM) were highly volatile and expensive. This scraper allowed me to monitor price trends automatically without checking the store manually every day, helping me buy parts at the best possible price.

## Funkcje
* Dodawanie produktów za pomocą linku.
* Automatyczna aktualizacja cen wszystkich śledzonych przedmiotów.
* Zapisywanie historii cen do pliku JSON.
* Generowanie wykresów zmian cen (Matplotlib).

## Instalacja
1. Sklonuj repozytorium.
2. Zainstaluj wymagane biblioteki: `pip install -r requirements.txt`.
3. Uruchom program: `python main.py`.
