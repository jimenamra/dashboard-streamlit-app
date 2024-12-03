import streamlit as st
from app.dynamodb import fetch_data
from app.data_processing import process_competitions, process_matches, process_lineups
from app.visualization import plot_goals_by_team,plot_results_by_week,plot_stadium_frequency
from app.utils import extract_parsed_data, expand_positions
import pandas as pd

st.set_page_config(
    page_title="Football Dashboard",  
    page_icon="⚽",  
    layout="centered",  
)
st.title("Football Analytics Dashboard ⚽🏆")

competitions_data = fetch_data("competitions")
matches_data = fetch_data("matches")
lineups_data = fetch_data("lineups")

competitions_df = process_competitions(competitions_data)
matches_df = process_matches(matches_data)
lineups_df = process_lineups(lineups_data)

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
            # Visualización 
            st.subheader(f"Análisis del Equipo: {team_name}")
            
            team_matches = filtered_matches[
                (filtered_matches["home_team"] == team_name) | (filtered_matches["away_team"] == team_name)
            ]
            team_matches['home_score'] = pd.to_numeric(team_matches['home_score'], errors='coerce')
            team_matches['away_score'] = pd.to_numeric(team_matches['away_score'], errors='coerce')

            st.write(f"Partidos de {team_name}")
            st.dataframe(team_matches)

            st.subheader("Distribución de Goles del Equipo")
            plot_goals_by_team(team_matches)  

            st.subheader("Comparación de Goles por Partido")
            plot_results_by_week(team_matches) 

            st.subheader("Frecuencia de Estadios Jugados")
            plot_stadium_frequency(team_matches) 
