"""
Pruebas unitarias para el módulo de validadores usando pytest.
"""
from utils.validadores import validar_isbn13, validar_email

# Pytest busca automáticamente todas las funciones que empiecen con "test_"

def test_validar_isbn13_correcto():
    # Arrange & Act: Preparamos un ISBN real (El Principito) y lo validamos
    resultado = validar_isbn13("9788498381498")
    # Assert: Afirmamos que el resultado DEBE ser True
    assert resultado == True

def test_validar_isbn13_incorrecto():
    # Un ISBN que claramente es falso
    resultado = validar_isbn13("1111111111111")
    assert resultado == False

def test_validar_isbn13_letras():
    # Un ISBN que contiene letras no debería pasar
    resultado = validar_isbn13("978849838149A")
    assert resultado == False

def test_validar_email_correcto():
    resultado = validar_email("alumno.ejemplo@universidad.edu.mx")
    assert resultado == True

def test_validar_email_sin_arroba():
    resultado = validar_email("alumnouniversidad.com")
    assert resultado == False