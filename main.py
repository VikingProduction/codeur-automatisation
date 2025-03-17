# main.py
import feedparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from exceptions import BudgetNotRecognizedException, ElementNotFoundException
from messages import load_messages, get_rotating_message
from datetime import datetime, timedelta
import os

LOG_FILE = "posted_offers.txt"

def load_posted_offers():
    """Charge les identifiants (GUID) des offres déjà postées."""
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}

def log_posted_offer(guid):
    """Enregistre l'identifiant d'une offre postée."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{guid}\n")

def determiner_offre(budget_str):
    """
    Détermine le montant et la durée de l'offre en fonction du budget.
    Renvoie (offer_amount, offer_duration) ou lève une exception si non reconnu.
    """
    if "Moins de 500" in budget_str:
        return 390, 2
    elif "500" in budget_str and "1000" in budget_str:
        return 750, 7
    elif "1000" in budget_str and "10000" in budget_str:
        return 3500, 21
    elif "10000" in budget_str:
        return 7500, 90
    else:
        raise BudgetNotRecognizedException(f"Budget non reconnu: {budget_str}")

def extract_budget(description):
    """
    Extrait le texte du budget depuis la description.
    Par exemple, à partir de "Budget : Moins de 500 € - Catégories : ..." retourne "Moins de 500".
    """
    try:
        if "Budget :" in description:
            part = description.split("Budget :")[1]
            budget_part = part.split("€")[0]
            return budget_part.strip()
    except Exception as e:
        print("Erreur d'extraction du budget:", e)
    return ""

def is_recent(pub_date_str, max_minutes=30):
    """
    Vérifie que la date de publication est celle du jour et qu'elle date de moins de max_minutes.
    """
    try:
        pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
    except Exception as e:
        print(f"Erreur lors du parsing de la date '{pub_date_str}' : {e}")
        return False
    now = datetime.now(pub_date.tzinfo)
    return (pub_date.date() == now.date()) and ((now - pub_date) <= timedelta(minutes=max_minutes))

def init_driver():
    """Initialise le driver Selenium (ici avec Chrome)."""
    driver = webdriver.Chrome()
    return driver

def login(driver):
    """
    Automatisation de la connexion sur Codeur.
    La page de connexion est : https://www.codeur.com/users/sign_in
    Les champs à remplir sont : id="user_email" et id="user_password".
    """
    driver.get("https://www.codeur.com/users/sign_in")
    # Attendre que la page de connexion se charge
    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_email")))
    password_input = driver.find_element(By.ID, "user_password")
    
    # Saisie des identifiants (vous pouvez également les stocker dans des variables d'environnement)
    email = input("Entrez votre email : ")
    password = input("Entrez votre mot de passe : ")
    
    email_input.clear()
    email_input.send_keys(email)
    password_input.clear()
    password_input.send_keys(password)
    
    # Cliquer sur le bouton de connexion
    submit_btn = driver.find_element(By.NAME, "commit")
    submit_btn.click()
    
    # Optionnel : attendre qu'un élément caractéristique apparaisse pour confirmer la connexion
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "some_element_after_login")))

def submit_offer(driver, link, title, offer_amount, offer_duration, message):
    """
    Navigue sur la page du projet et soumet l'offre en remplissant le formulaire.
    """
    driver.get(link)
    try:
        btn_offre = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "project-actions"))
        )
        btn_offre.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "offer_amount"))
        )
        
        montant_input = driver.find_element(By.ID, "offer_amount")
        montant_input.clear()
        montant_input.send_keys(str(offer_amount))
        
        duree_input = driver.find_element(By.ID, "offer_duration")
        duree_input.clear()
        duree_input.send_keys(str(offer_duration))
        
        commentaire = driver.find_element(By.ID, "offer_comments_attributes_0_content")
        commentaire.clear()
        commentaire.send_keys(message)
        
        submit_btn = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'Publier mon offre')]")
        submit_btn.click()
        
        print(f"Offre soumise pour : {title}")
    except Exception as e:
        raise ElementNotFoundException(f"Erreur lors de la soumission de l'offre pour {title}: {e}")

def main():
    # Charger les messages tournants depuis le dossier 'messages'
    messages = load_messages("messages")
    
    # Liste des mots-clés d'exclusion (à personnaliser)
    mots_exclusion = ['motclé1', 'motclé2']
    
    # Charger la liste des offres déjà postées (GUID)
    posted_offers = load_posted_offers()
    
    # Récupérer et parser le flux RSS depuis Codeur
    rss_url = "https://www.codeur.com/projects?format=rss"
    feed = feedparser.parse(rss_url)
    
    driver = init_driver()
    login(driver)
    
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = entry.description
        guid = entry.get("guid", "")
        pub_date_str = entry.get("pubDate") or entry.get("published")
        
        # Vérifier la date (doit être aujourd'hui et datant de moins de 30 minutes)
        if not pub_date_str or not is_recent(pub_date_str):
            print(f"Projet ignoré (date non récente) : {title}")
            continue
        
        # Vérifier si l'offre a déjà été postée
        if guid in posted_offers:
            print(f"Offre déjà postée pour : {title} (GUID : {guid})")
            continue
        
        # Vérifier les mots-clés d'exclusion
        if any(mot in title or mot in description for mot in mots_exclusion):
            print(f"Exclusion du projet : {title}")
            continue
        
        # Extraction du budget et détermination de l'offre
        budget_str = extract_budget(description)
        try:
            offer_amount, offer_duration = determiner_offre(budget_str)
        except BudgetNotRecognizedException as e:
            print(f"Budget non reconnu pour {title}: {e}")
            continue
        
        # Obtenir un message tournant personnalisé
        message = get_rotating_message(title, messages)
        
        try:
            submit_offer(driver, link, title, offer_amount, offer_duration, message)
            log_posted_offer(guid)
        except ElementNotFoundException as e:
            print(e)
            continue
    
    driver.quit()

if __name__ == "__main__":
    main()
