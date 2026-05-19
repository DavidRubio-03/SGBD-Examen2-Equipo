"""
Módulo para el manejo y formateo de cadenas de texto (strings).
"""
import re
import unicodedata

def normalizar_titulo(titulo: str) -> str:
    """
    Limpia el título: elimina espacios extra, capitaliza y remueve caracteres no permitidos.
    """
    # 1. Eliminar caracteres extraños usando expresiones regulares (dejamos letras, números y espacios)
    titulo_limpio = re.sub(r'[^a-zA-Z0-9\s,áéíóúÁÉÍÓÚñÑ]', '', titulo)
    
    # 2. Eliminar espacios múltiples usando split() y join()
    titulo_limpio = " ".join(titulo_limpio.split())
    
    # 3. Capitalizar cada palabra (Title Case)
    return titulo_limpio.title()


def generar_slug(texto: str) -> str:
    """
    Convierte texto a formato URL (minúsculas, guiones, sin acentos).
    """
    # 1. Quitar acentos usando la librería unicodedata
    texto_limpio = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    
    # 2. Convertir a minúsculas y quitar espacios en los extremos con strip()
    slug = texto_limpio.lower().strip()
    
    # 3. Reemplazar los espacios internos por guiones
    slug = "-".join(slug.split())
    
    # 4. Asegurarnos de que solo queden letras, números y guiones
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    return slug


def formatear_reporte_libro(libro_dict: dict) -> str:
    """
    Genera una cadena multilinea formateada con f-strings.
    """
    # Usamos f-strings y alineación: el "<20" significa "alinear a la izquierda usando 20 espacios"
    reporte = f"""
    {'-'*40}
    FICHA DEL LIBRO
    {'-'*40}
    Título:      {libro_dict.get('titulo', 'N/A'):<20}
    Autor:       {libro_dict.get('autor', 'N/A'):<20}
    ISBN:        {libro_dict.get('isbn', 'N/A'):<20}
    {'-'*40}
    """
    return reporte


def buscar_en_texto(haystack: str, needle: str) -> bool:
    """
    Búsqueda case-insensitive (no le importan mayúsculas/minúsculas).
    """
    # Convertimos ambos textos a minúsculas (lower) y buscamos si la "aguja" (needle) está en el "pajar" (haystack)
    return needle.lower() in haystack.lower()


# Pruebas rápidas para verificar que funciona
if __name__ == "__main__":
    print("Normalizar: ", normalizar_titulo("   el   señor de los   anillos!!!  "))
    print("Generar Slug:", generar_slug("Cien Años de Soledad"))
    print("Búsqueda:   ", buscar_en_texto("Harry Potter y la Piedra", "POTTER"))