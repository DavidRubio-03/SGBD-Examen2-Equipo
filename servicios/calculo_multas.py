"""
Módulo para el cálculo de multas por retraso en devoluciones.
"""
from utils.constantes import MULTA_DIARIA_MXN_ALUMNO, MULTA_DIARIA_MXN_PROFESOR

def calcular_multa_if(dias_retraso: int, tipo_usuario: str) -> float:
    """
    Calcula la multa usando sentencias if/elif/else.
    """
    # Si no hay retraso o es administrador, no hay multa
    if dias_retraso <= 0 or tipo_usuario.lower() == 'admin':
        return 0.0
        
    multa_base = 0.0
    
    # Operadores relacionales (==) y lógicos
    if tipo_usuario.lower() == 'alumno':
        multa_base = dias_retraso * MULTA_DIARIA_MXN_ALUMNO
    elif tipo_usuario.lower() == 'profesor':
        multa_base = dias_retraso * MULTA_DIARIA_MXN_PROFESOR
    else:
        return 0.0 # Caso donde el usuario no existe
        
    # Penalización del 20% si el retraso es mayor a 30 días (> 30)
    if dias_retraso > 30:
        multa_base += (multa_base * 0.20)
        
    return multa_base


def calcular_multa_match(dias_retraso: int, tipo_usuario: str) -> float:
    """
    Calcula la multa usando la sentencia match/case (Python 3.10+).
    """
    if dias_retraso <= 0:
        return 0.0
        
    multa_base = 0.0
    
    # match/case es como un "interruptor" que evalúa el valor de una variable
    match tipo_usuario.lower():
        case 'alumno':
            multa_base = dias_retraso * MULTA_DIARIA_MXN_ALUMNO
        case 'profesor':
            multa_base = dias_retraso * MULTA_DIARIA_MXN_PROFESOR
        case 'admin':
            return 0.0
        case _:
            return 0.0 # El guión bajo (_) significa "cualquier otro caso"
            
    if dias_retraso > 30:
        multa_base *= 1.20 # Multiplicar por 1.20 es otra forma matemática de sumar el 20%
        
    return multa_base


# 6 Llamadas de prueba solicitadas por el profesor
if __name__ == "__main__":
    print("--- Pruebas con if/elif/else ---")
    print(f"1. Alumno, 0 días: ${calcular_multa_if(0, 'alumno')}")
    print(f"2. Alumno, 10 días: ${calcular_multa_if(10, 'alumno')}")
    print(f"3. Alumno, 40 días (penalización): ${calcular_multa_if(40, 'alumno')}")
    
    print("\n--- Pruebas con match/case ---")
    print(f"4. Profesor, 5 días: ${calcular_multa_match(5, 'profesor')}")
    print(f"5. Profesor, 35 días (penalización): ${calcular_multa_match(35, 'profesor')}")
    print(f"6. Admin, 50 días: ${calcular_multa_match(50, 'admin')}")