import os
from difflib import get_close_matches
import re
import yaml

def compare_title_with_rule():
    # Especifica la ruta de la carpeta donde están tus archivos
    folder_path = 'ruta/a/tu/carpeta'  # Reemplaza esto con la ruta real

    # Construye las rutas completas a los archivos
    rule_file_path = os.path.join(folder_path, 'rule.yml')
    code_file_path = os.path.join(folder_path, 'code.yml')

    # Cargar datos desde rule.yml
    with open(rule_file_path, 'r') as rule_file:
        rule_data = yaml.safe_load(rule_file)
        title = rule_data.get('title')

    # Cargar datos desde code.yml
    with open(code_file_path, 'r') as code_file:
        code_data = yaml.safe_load(code_file)
        rule_string = code_data.get('rule')
        query = code_data.get('code')

    # Verificar si los campos necesarios están presentes
    if title is None:
        print("El campo 'title' falta en rule.yml.")
        return
    if rule_string is None:
        print("El campo 'rule' falta en code.yml.")
        return
    if query is None:
        print("El campo 'code' falta en code.yml.")
        return

    # Extraer el nombre después del último guión bajo '_'
    name_after_last_underscore = rule_string.split('_')[-1]

    # Comparar el nombre extraído con el título
    if title == name_after_last_underscore:
        print("Éxito: El título en rule.yml coincide con el nombre extraído del 'rule' en code.yml.")
    else:
        print("Se detectó una discrepancia:")
        print(f"Título en rule.yml: {title}")
        print(f"Nombre extraído del 'rule' en code.yml: {name_after_last_underscore}")

    # Proceder a extraer el último project en la query y normalizar campos
    extract_and_normalize_fields(query)

def extract_and_normalize_fields(query):
    # Extraer todas las declaraciones 'project'
    projects = re.findall(r'\|\s*project\s+([^\|]+)', query, re.IGNORECASE)
    if not projects:
        print("No se encontraron declaraciones 'project' en la query.")
        return

    # Tomar la última declaración 'project'
    last_project = projects[-1]
    print("\nÚltima declaración 'project':")
    print(f"| project {last_project.strip()}")

    # Extraer campos de la última declaración 'project'
    campos_en_query = [campo.strip() for campo in last_project.strip().split(',')]

    # Campos estándar (puedes modificar esta lista según sea necesario)
    campos_estandar = ["Atun", "Paco", "Mama"]

    # Ahora utiliza el código de normalización de campos
    comprobar_campos(campos_estandar, campos_en_query)

def comprobar_campos(campos_estandar, campos_en_query):
    # Mantener los nombres originales de los campos para las sugerencias
    campos_estandar_dict = {campo.lower(): campo for campo in campos_estandar}
    resultados = []

    # Verificar cada campo en la query
    for campo in campos_en_query:
        campo_lower = campo.lower()

        # Verificador básico
        if campo_lower in campos_estandar_dict:
            resultados.append((campo, "Sí", "Campo estandarizado"))
        else:
            # Coincidencias parciales
            sugerencias_lower = get_close_matches(campo_lower, campos_estandar_dict.keys(), n=3, cutoff=0.5)

            # Convertir sugerencias de nuevo a mayúsculas/minúsculas originales
            sugerencias = [campos_estandar_dict[sug] for sug in sugerencias_lower]

            # Sugerencias de subcadenas
            subcadena_sugerencias = [c for c in campos_estandar if campo_lower in c.lower()]

            # Si se encuentra coincidencia, añadir a sugerencias
            if sugerencias or subcadena_sugerencias:
                todas_sugerencias = list(set(sugerencias + subcadena_sugerencias))
                resultados.append((campo, "No", ", ".join(todas_sugerencias)))
            else:
                resultados.append((campo, "No", "Sin sugerencias"))

    # Verificar si el orden de los campos coincide con el estándar
    orden_correcto = [campo.lower() for campo in campos_estandar] == [campo.lower() for campo in campos_en_query]

    # Imprimir resultados
    for campo, estandarizado, sugerencia in resultados:
        print(f"Campo: {campo}, Estandarizado: {estandarizado}, Sugerencias: {sugerencia}")

    # Informar sobre el orden
    if orden_correcto:
        print("El orden de los campos es correcto.")
    else:
        print("El orden de los campos es incorrecto.")

    # Mostrar los campos ordenados alfabéticamente
    campos_ordenados = sorted(campos_en_query, key=lambda s: s.lower())
    print("\nCampos ordenados alfabéticamente:")
    print(", ".join(campos_ordenados))

    # Mostrar la declaración 'project' original con comas separadas por espacio
    project_original = ", ".join(campos_en_query)
    print("\nProject original con comas separadas por espacio:")
    print(f"project {project_original}")

# Ejecutar la comparación y normalización de campos
compare_title_with_rule()
