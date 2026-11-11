import time
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
URL_PRODUIT = "https://www.amazon.fr/dp/B0XXXXXXXX"
PRIX_CIBLE = 1750.0

# Tes identifiants intégrés
TELEGRAM_TOKEN = "9195484257:AAHXX2Fx69ZMjEtOcCGXrCuba8EBZ6Mtf58"
TELEGRAM_CHAT_ID = "7961077547"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
}

def envoyer_alerte_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erreur lors de l'envoi du message Telegram : {e}")

def verifier_prix():
    try:
        response = requests.get(URL_PRODUIT, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erreur d'accès à la page ({response.status_code})")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        prix_element = soup.find("span", {"class": "a-offscreen"})
        
        if prix_element:
            prix_texte = prix_element.get_text().replace("€", "").replace("\xa0", "").replace(" ", "").replace(",", ".").strip()
            prix_actuel = float(prix_texte)
            
            print(f"Prix actuel détecté : {prix_actuel} €")

            if prix_actuel <= PRIX_CIBLE:
                message = f"🚨 ALERTE PROMO LENOVO LEGION PRO !\n\nLe prix est tombé à {prix_actuel} € (Objectif : {PRIX_CIBLE} €).\n\nLien : {URL_PRODUIT}"
                envoyer_alerte_telegram(message)
                print("Alerte envoyée sur Telegram !")
            else:
                print(f"Pas encore au prix cible ({PRIX_CIBLE} €).")
        else:
            print("Impossible de trouver la balise de prix sur la page.")

    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")

if __name__ == "__main__":
    print("Démarrage du suivi de prix Amazon...")
    verifier_prix()
