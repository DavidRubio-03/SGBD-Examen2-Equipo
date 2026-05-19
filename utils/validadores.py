"""
Módulo de validaciones generales para los datos del sistema.
"""

def validar_isbn13(isbn: str) -> bool:
    """
    Verifica que un ISBN-13 tenga 13 dígitos y cumpla el algoritmo de verificación.
    """
    if not isinstance(isbn, str):
        return False
        
    # Limpiamos el texto por si el usuario le puso guiones o espacios
    isbn_limpio = isbn.replace("-", "").replace(" ", "")
    
    # Verificamos que sean exactamente 13 caracteres numéricos
    if len(isbn_limpio) != 13 or not isbn_limpio.isdigit():
        return False
        
    # Algoritmo matemático para verificar un ISBN real
    suma = 0
    for i in range(12):
        multiplicador = 1 if i % 2 == 0 else 3
        suma += int(isbn_limpio[i]) * multiplicador
        
    digito_verificador = (10 - (suma % 10)) % 10
    
    # Comprobamos si el último dígito coincide con el cálculo
    return int(isbn_limpio[12]) == digito_verificador


def validar_email(email: str) -> bool:
    """
    Valida de forma básica que el string contenga '@' y un dominio con punto.
    """
    if not isinstance(email, str):
        return False
        
    # Verificamos que tenga arroba
    if "@" in email:
        partes = email.split("@")
        # Aseguramos que haya algo antes del arroba y un punto después
        if len(partes) == 2 and "." in partes[1]:
            return True
            
    return False