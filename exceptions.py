# exceptions.py

class BudgetNotRecognizedException(Exception):
    """Exception levée lorsque le format du budget est introuvable ou non reconnu."""
    pass

class ElementNotFoundException(Exception):
    """Exception levée lorsqu'un élément attendu sur la page n'est pas trouvé."""
    pass
