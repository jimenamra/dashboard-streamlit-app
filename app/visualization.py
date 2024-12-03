import matplotlib.pyplot as plt
import streamlit as st

def plot_team_results(matches_df):
    """
    Grafica los resultados de los partidos por equipo como barras apiladas.
    """
    if matches_df.empty:
        st.warning("No hay datos de partidos para mostrar.")
        return

    # Agrupar y pivotar para preparar los datos
    try:
        team_results = matches_df.groupby(['home_team', 'result']).size().reset_index(name='counts')
        pivot_data = team_results.pivot(index='home_team', columns='result', values='counts').fillna(0)
        
        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(10, 6))
        pivot_data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_ylabel("Cantidad de Resultados")
        ax.set_title("Resultados de Partidos por Equipo")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al generar la gráfica: {e}")

def plot_goal_comparison(matches_df):
    """
    Grafica la comparación de goles anotados y recibidos por equipo.
    """
    if matches_df.empty:
        st.warning("No hay datos de goles para mostrar.")
        return

    try:
        # Agrupar y sumar los goles
        goals_competition = matches_df.groupby('home_team').agg({'home_score': 'sum', 'away_score': 'sum'}).reset_index()
        
        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(10, 6))
        goals_competition.plot(x='home_team', y=['home_score', 'away_score'], kind='bar', ax=ax)
        ax.set_ylabel("Total de Goles")
        ax.set_title("Comparación de Goles Anotados y Recibidos por Equipo")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al generar la gráfica: {e}")

def plot_position_distribution(expanded_lineups_df):
    """
    Grafica la distribución de posiciones de jugadores.
    """
    if expanded_lineups_df.empty:
        st.warning("No hay datos de alineaciones para mostrar.")
        return

    try:
        # Contar las posiciones de los jugadores
        position_counts = expanded_lineups_df['position'].value_counts()

        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(8, 6))
        position_counts.plot(kind='barh', ax=ax)
        ax.set_xlabel("Cantidad de Jugadores")
        ax.set_ylabel("Posiciones")
        ax.set_title("Distribución de Posiciones")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al generar la gráfica: {e}")

def plot_weekly_matches(matches_df):
    """
    Grafica el número de partidos jugados por semana.
    """
    if matches_df.empty:
        st.warning("No hay datos de partidos semanales para mostrar.")
        return

    try:
        # Contar partidos por semana
        weekly_matches = matches_df.groupby('match_week').size().reset_index(name='counts')
        
        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(weekly_matches['match_week'], weekly_matches['counts'], marker='o', linestyle='-')
        ax.set_xlabel("Semana")
        ax.set_ylabel("Número de Partidos")
        ax.set_title("Número de Partidos por Semana")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al generar la gráfica: {e}")
