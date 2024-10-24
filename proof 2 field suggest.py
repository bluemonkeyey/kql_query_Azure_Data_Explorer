from difflib import get_close_matches
import re

def extraer_campos_de_query(query):
    # search in project
    # you need to put your final projection under a project, other methods like summarize are not valid
    match = re.search(r'project\s+([\w\s,.-]+)', query, re.IGNORECASE)
    if match:
        # extract and convert to list
        campos = [campo.strip() for campo in match.group(1).split(',')]
        return campos
    else:
        print("No se encontraron campos en la query.")
        return []

def comprobar_campos(campos_estandar, query):
    # Keep original field names for suggestions
    campos_estandar_dict = {campo.lower(): campo for campo in campos_estandar}
    resultados = []

    # extract query fields
    campos_en_query = extraer_campos_de_query(query)

    # check every field in query
    for campo in campos_en_query:
        campo_lower = campo.lower()

        # basic correct checker
        if campo_lower in campos_estandar_dict:
            resultados.append((campo, "Sí", "Campo estandarizado"))
        else:
            # partial matches
            sugerencias_lower = get_close_matches(campo_lower, campos_estandar_dict.keys(), n=3, cutoff=0.5)

            # Convert suggestions back to original case
            sugerencias = [campos_estandar_dict[sug] for sug in sugerencias_lower]

            # substring suggestions
            subcadena_sugerencias = [c for c in campos_estandar if campo_lower in c.lower()]

            # if found match add to suggestions
            if sugerencias or subcadena_sugerencias:
                todas_sugerencias = list(set(sugerencias + subcadena_sugerencias))
                resultados.append((campo, "No", ", ".join(todas_sugerencias)))
            else:
                resultados.append((campo, "No", "Sin sugerencias"))

    # Check if the order of the fields matches the standard
    orden_correcto = [campo.lower() for campo in campos_estandar] == [campo.lower() for campo in campos_en_query]

    # print results
    for campo, estandarizado, sugerencia in resultados:
        print(f"Campo: {campo}, Estandarizado: {estandarizado}, Sugerencias: {sugerencia}")

    # Inform about the order
    if orden_correcto:
        print("El orden de los campos es correcto.")
    else:
        print("El orden de los campos es incorrecto.")

# standard fields
campos_estandar = ["Atun", "Paco", "Mama"]

query = """
| project Atun, Mama, Paco
"""

comprobar_campos(campos_estandar, query)
