from datetime import datetime

def validate_fields(label, amount, date_str):
    errors = []
    
    if not label.strip():
        errors.append("Étiquette ne peut pas être vide")
    
    try:
        amount = float(amount)
        if amount <= 0:
            errors.append("Le montant doit être positif")
    except ValueError:
        errors.append("Le montant doit être un nombre valide")
        
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        errors.append("Format de date invalide (attendu YYYY-MM-DD)")
        
    return errors