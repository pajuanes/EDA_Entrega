import pandas as pd
import os

def pedir_objetivo_equipos(equipos, output_file):
    """
    Pregunta al usuario el objetivo de cada equipo y lo almacena en un DataFrame.

    Args:
        equipos (list): Lista de equipos a los que se les asignará un objetivo.

    Returns:
        pd.DataFrame: DataFrame con los equipos y sus objetivos.
    """
    # Opciones explicativas para mostrar al usuario
    opciones_completas = {
        "1": "Ganar la Liga",
        "2": "Quedar en puestos de la Champions League (1st-4th)",
        "3": "Quedar en puestos de la Europa League (5th)",
        "4": "Quedar en puestos de la Conference League (6th)",
        "5": "Permanencia en la categoría (Hasta 16 posiciones)"
    }

    # Opciones simplificadas que se guardarán en el DataFrame
    objetivos_guardados = {
        "1": "Liga",
        "2": "Champions League",
        "3": "Europa League",
        "4": "Conference League",
        "5": "Permanencia"
    }

    # Crear una lista vacía para almacenar los resultados
    objetivos = []

    print("\nIntroduce el objetivo de cada equipo al comienzo de la temporada:")
    print("Escribe 'q' o 'exit' para salir del programa en cualquier momento.")
    print("Opciones:")
    for key, value in opciones_completas.items():
        print(f"{key}. {value}")
    if os.path.exists(output_file):
        print("6. Visualizar el contenido actual del archivo CSV")
    
    # Preguntar objetivo para cada equipo
    for equipo in equipos:
        while True:  # Validar la entrada
            print(f"\nEquipo: {equipo}")
            print("Elige una opción del 1 al 5:")
            opcion = input("Opción: ").strip()
            # Salir si el usuario escribe 'q' o 'exit'
            if opcion in ["q", "exit"]:
                print("\nHas salido del programa.")
                exit()
            if opcion == "6" and os.path.exists(output_file):
                print("\nContenido del archivo existente:")
                df_existente = pd.read_csv(output_file)
                print(df_existente)
            elif opcion in objetivos_guardados:
                objetivos.append(objetivos_guardados[opcion])
                break
            else:
                print("Opción inválida. Por favor, selecciona un número entre 1 y 5.")

    # Crear el DataFrame final
    df_objetivos = pd.DataFrame({
        "Equipo": equipos,
        "Objetivo": objetivos
    })

    return df_objetivos

def main():
    file_path = '../data/LigaEspanola2023-2024-Resultados.xlsx'
    df = pd.read_excel(file_path, sheet_name=0)
    # Obtener equipos únicos combinando "Home Team" y "Away Team"
    equipos = pd.concat([df["Home Team"], df["Away Team"]]).unique()

    # Ordenar los equipos alfabéticamente
    equipos_ordenados = sorted(equipos)

    # Archivo de salida
    file_csv = "../data/objetivos_equipos.csv"

    # Llamar a la función para pedir objetivos
    df_objetivos = pedir_objetivo_equipos(equipos_ordenados, file_csv)

    # Mostrar el resultado
    print("\nResultados Finales:")
    print(df_objetivos)

    # Guardar en CSV
    df_objetivos.to_csv(file_csv, index=False)
    print(f"\nLos objetivos se han guardado en '{file_csv}'.")

if __name__ == "__main__":
    main()
