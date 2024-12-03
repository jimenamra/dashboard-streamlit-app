import streamlit as st
from app.dynamodb import fetch_data
from app.data_processing import process_competitions, process_matches, process_lineups
from app.visualization import plot_team_results, plot_goal_comparison, plot_position_distribution
from app.utils import extract_parsed_data, expand_positions

st.set_page_config(layout="wide")
st.title("Football Analytics Dashboard ⚽🏆")

# Obtener datos de DynamoDB
competitions_data = fetch_data("competitions")
matches_data = fetch_data("matches")
lineups_data = fetch_data("lineups")

# Procesar datos
competitions_df = process_competitions(competitions_data)
matches_df = process_matches(matches_data)
lineups_df = process_lineups(lineups_data)

# Extraer datos relevantes
competitions_df = extract_parsed_data(competitions_df, column_name='data', key_to_extract='competition_name')
competitions_df = extract_parsed_data(competitions_df, column_name='data', key_to_extract='season_name')
lineups_df = extract_parsed_data(lineups_df, column_name='data', key_to_extract='team_name')
lineups_df = expand_positions(lineups_df)

matches_df["competition"] = matches_df["competition"].str.split(" - ").str[1]

# Filtro principal: Competición
competition_name = st.selectbox(
    "Seleccione una Competición",
    sorted(competitions_df["competition_name"].unique())
)

if competition_name:
    # Filtrar temporadas por competición
    seasons = competitions_df[competitions_df["competition_name"] == competition_name]["season_name"].unique()
    season = st.selectbox("Seleccione una Temporada", sorted(seasons))

    if season:
        # Filtrar equipos por competición y temporada
        filtered_matches = matches_df[(matches_df["competition"] == competition_name) &
                                      (matches_df["season"] == season)]
        teams = set(filtered_matches["home_team"]).union(filtered_matches["away_team"])
        team_name = st.selectbox("Seleccione un Equipo", sorted(teams))

        if team_name:
            # Visualización de equipo
            st.subheader(f"Análisis del Equipo: {team_name}")
            
            # Datos del equipo
            team_matches = filtered_matches[
                (filtered_matches["home_team"] == team_name) | (filtered_matches["away_team"] == team_name)
            ]
            
            # Mostrar tabla de partidos del equipo
            st.write(f"Partidos de {team_name}")
            st.dataframe(team_matches)

            # Visualización de resultados del equipo
            plot_team_results(team_matches)

            # Distribución de posiciones de jugadores
            st.subheader("Distribución de Posiciones")
            team_lineups = lineups_df[lineups_df["team_name"] == team_name]
            if not team_lineups.empty:
                plot_position_distribution(team_lineups)
            else:
                st.warning("No hay datos de alineaciones disponibles para este equipo.")

            # Comparación de goles
            st.subheader("Comparación de Goles")
            plot_goal_comparison(team_matches)
