# messages.py
import os
import random

def load_messages(directory="messages"):
    """Charge tous les messages depuis des fichiers texte situés dans le dossier 'directory'."""
    messages = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                    messages.append(file.read())
    except FileNotFoundError:
        print(f"Le dossier {directory} n'existe pas.")
    return messages

def get_rotating_message(title, messages):
    """
    Retourne un message tournant en remplaçant la variable '$title'
    par le titre du projet.
    """
    if not messages:
        return f"Bonjour,\n\nNous pouvons intervenir immédiatement sur votre projet {title}.\nCordialement,\nVotre équipe"
    message_template = random.choice(messages)
    return message_template.replace("$title", title)
