# Morele Price Tracker & PC Builder 🖥️📈

A sophisticated Python-based tool designed to monitor component prices from Morele.net and manage your PC build budget effectively. 

## 💡 Motivation
This project was born out of a real need while building a new PC in early 2026. At the time, component prices (especially RAM and CPUs) were highly volatile and expensive. This scraper allowed me to automate the process of checking prices, helping me identify "price drops" and purchase parts at the best possible moment to save money.

## 🚀 Key Features
* **Smart Web Scraping:** Automatically fetches real-time prices from Morele.net using `BeautifulSoup`.
* **PC Builder & Manager:** Create custom PC configurations and track the total cost of your dream setup in one place.
* **Advanced Data Visualization:**
    * **Line Charts:** Visualize price trends for individual products and entire PC sets over time.
    * **Pie Charts:** Analyze the cost distribution of your build to see which components take up most of your budget.
* **Real-time Price Alerts:** Instant console feedback on whether prices went down (✔️), up (❌), or stayed the same (🟡) during updates.
* **Persistent Storage:** All data and history are automatically saved to a `products.json` file.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Libraries:** `requests`, `beautifulsoup4`, `matplotlib`

## 📥 Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Dzajcek/Morele-Price-Tracker.git](https://github.com/Dzajcek/Morele-Price-Tracker.git)
