from IPython.display import display, Image, HTML
import os
import base64

### Definición de Funciones ###

# Función para visualizar la diferencia de goles acumulada
def diferencia_goles_acumulada(dataframe, plt, teams=None):
    """
    Visualiza la diferencia de goles acumulada en casa y fuera de casa para los equipos seleccionados.

    Parámetros:
        dataframe (DataFrame): Datos de los partidos.
        teams (list): Lista con los nombres de los equipos a visualizar.
                      Si es None, se seleccionarán todos los equipos.
    """
    # Calcular la diferencia de goles
    dataframe["Home_GD"] = dataframe["Home Score"] - dataframe["Away Score"]
    dataframe["Away_GD"] = dataframe["Away Score"] - dataframe["Home Score"]

    # Crear DataFrames separados para Casa y Fuera
    home_df = dataframe[["Round", "Home Team", "Home_GD"]].rename(columns={"Home Team": "Team", "Home_GD": "Goal_Difference"})
    away_df = dataframe[["Round", "Away Team", "Away_GD"]].rename(columns={"Away Team": "Team", "Away_GD": "Goal_Difference"})

    # Calcular la diferencia acumulada
    home_df["Goal_Difference_Cum"] = home_df.groupby("Team")["Goal_Difference"].cumsum()
    away_df["Goal_Difference_Cum"] = away_df.groupby("Team")["Goal_Difference"].cumsum()

    # Filtrar equipos si se proporciona una lista
    if teams:
        home_df = home_df[home_df["Team"].isin(teams)]
        away_df = away_df[away_df["Team"].isin(teams)]

    # Crear gráficos separados
    fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    # Gráfico de Casa
    for team in home_df["Team"].unique():
        team_data = home_df[home_df["Team"] == team]
        ax[0].plot(team_data["Round"], team_data["Goal_Difference_Cum"], marker="o", label=team)

    ax[0].set_title("Diferencia de Goles Acumulada - En Casa")
    ax[0].set_xlabel("Jornada")
    ax[0].set_ylabel("Diferencia de Goles")
    ax[0].legend(fontsize="small")
    ax[0].grid()

    # Gráfico de Fuera
    for team in away_df["Team"].unique():
        team_data = away_df[away_df["Team"] == team]
        ax[1].plot(team_data["Round"], team_data["Goal_Difference_Cum"], marker="o", label=team)

    ax[1].set_title("Diferencia de Goles Acumulada - Fuera de Casa")
    ax[1].set_xlabel("Jornada")
    ax[1].legend(fontsize="small")
    ax[1].grid()

    # Ajustar diseño
    plt.tight_layout()
    plt.show()

# Función para visualizar la cantidad de victorias y derrotas de todos los equipos
def plot_victorias_derrotas(df_home_wins, df_away_wins, df_home_losses, df_away_losses, plt):
    """
    Visualiza las victorias y derrotas de los equipos seleccionados.

    Parámetros:
        df_home_wins (Dataframe): Datos de las victorias en casa.
        df_away_wins (Dataframe): Datos de las victorias fuera de casa.
        df_home_losses (Dataframe): Datos de las derrotas en casa.
        df_away_losses (Dataframe): Datos de las derrotas fuera de casa.
    """
    # Crear una figura con 2 filas y 2 columnas de subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid de subplots

    # Graficar en cada subplot
    df_home_wins.plot(
        kind="bar", color="green", ax=axes[0, 0], title="Victorias en Casa"
    )
    axes[0, 0].set_xlabel("Equipos")
    axes[0, 0].set_ylabel("Cantidad")
    axes[0, 0].tick_params(axis="x", rotation=45)
    axes[0, 0].grid()

    df_away_wins.plot(
        kind="bar", color="blue", ax=axes[0, 1], title="Victorias Fuera"
    )
    axes[0, 1].set_xlabel("Equipos")
    axes[0, 1].set_ylabel("Cantidad")
    axes[0, 1].tick_params(axis="x", rotation=45)
    axes[0, 1].grid()

    df_home_losses.plot(
        kind="bar", color="red", ax=axes[1, 0], title="Derrotas en Casa"
    )
    axes[1, 0].set_xlabel("Equipos")
    axes[1, 0].set_ylabel("Cantidad")
    axes[1, 0].tick_params(axis="x", rotation=45)
    axes[1, 0].grid()

    df_away_losses.plot(
        kind="bar", color="orange", ax=axes[1, 1], title="Derrotas Fuera"
    )
    axes[1, 1].set_xlabel("Equipos")
    axes[1, 1].set_ylabel("Cantidad")
    axes[1, 1].tick_params(axis="x", rotation=45)
    axes[1, 1].grid()

    # Ajustar diseño
    plt.tight_layout()

    # Mostrar todos los subplots
    plt.show()

# Definimos la función para mostrar los logos
def show_team_logos(folder_path, max_images=10):
    """
    Muestra las imágenes de los logos de los equipos en HTML.
    
    Parámetros:
        folder_path (str): Ruta de la carpeta donde están los logos.
        max_images (int): Número máximo de imágenes a mostrar.
    """
    # Obtener todas las imágenes de la carpeta
    image_files = [file for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
    image_files = image_files[:max_images]  # Mostrar solo hasta max_images

    # Leer y codificar la imagen en Base64
    try:
        html_content = '<div style="display: flex; flex-wrap: wrap; gap: 20px;">'
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            with open(image_path, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode("utf-8")

            # HTML con la imagen incrustada en Base64
            html_content += f'''
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{base64_image}" style="width: 20px; height: auto;" />
                    <p style="font-size: 12px;">{image_file.replace("_", " ").split(".")[0]}</p>
                </div>
            '''
        # Mostrar el HTML
        display(HTML(html_content))
    except FileNotFoundError:
        print(f"Error: No se encuentra la imagen '{image_path}'.")

    