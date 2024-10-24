from difflib import get_close_matches
import re

def extraer_campos_de_query(query):
    # Buscar las palabras clave en el 'project' de la query y extraer los campos
    # Se asume que la query tiene una estructura tipo 'project campo1, campo2, ...'
    match = re.search(r'project\s+([\w\s,.-]+)', query, re.IGNORECASE)
    if match:
        # Extraer los campos y convertirlos en una lista
        campos = [campo.strip() for campo in match.group(1).split(',')]
        return campos
    else:
        print("No se encontraron campos en la query.")
        return []

def comprobar_campos(campos_estandar, query):
    # Convertir la lista de campos estandarizados a minúsculas para comparación insensible a mayúsculas
    campos_estandar_lower = [campo.lower() for campo in campos_estandar]
    resultados = []

    # Extraer campos de la query
    campos_en_query = extraer_campos_de_query(query)

    # Comprobación de cada campo en la query
    for campo in campos_en_query:
        campo_lower = campo.lower()

        # Si el campo está en la lista estandarizada, está correcto
        if campo_lower in campos_estandar_lower:
            resultados.append((campo, "Sí", "Campo estandarizado"))
        else:
            # Si no está, buscar sugerencias basadas en coincidencias parciales
            sugerencias = get_close_matches(campo_lower, campos_estandar_lower, n=3, cutoff=0.5)

            # También buscar coincidencias de subcadenas en los campos estandarizados
            subcadena_sugerencias = [c for c in campos_estandar if campo_lower in c.lower()]

            # Si se encuentran coincidencias, añadirlas a las sugerencias
            if sugerencias or subcadena_sugerencias:
                todas_sugerencias = list(set(sugerencias + subcadena_sugerencias))
                resultados.append((campo, "No", ", ".join(todas_sugerencias)))
            else:
                resultados.append((campo, "No", "Sin sugerencias"))

    # Imprimir los resultados
    for campo, estandarizado, sugerencia in resultados:
        print(f"Campo: {campo}, Estandarizado: {estandarizado}, Sugerencias: {sugerencia}")

# Lista de campos estandarizados
campos_estandar = ["activity", "user", "timestamp", "status"]


query = """
datatable(Activity: string, User: string, Timestamp: string, Status: string)
| project Activity, usuario, Time-stamp, Status
"""


comprobar_campos(campos_estandar, query)
