import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración global para gráficos en fondo oscuro
plt.style.use('dark_background')
sns.set_palette("pastel")

# 1. Distribución de Goles por Equipo
def plot_goals_by_team(data_fut):
    team_goals = data_fut.groupby('home_team')['home_score'].sum().add(
        data_fut.groupby('away_team')['away_score'].sum(), fill_value=0
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    team_goals.sort_values().plot(kind='barh', ax=ax, color=sns.color_palette("coolwarm", len(team_goals)))
    ax.set_xlabel("Goles", fontsize=12, color='white')
    ax.set_ylabel("Equipos", fontsize=12, color='white')
    ax.tick_params(colors='white')
    st.pyplot(fig)

# 2. Resultados por Jornada
def plot_results_by_week(data_fut):
    match_week_avg = data_fut.groupby('match_week')[['home_score', 'away_score']].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    match_week_avg.plot(ax=ax, marker='o', linestyle='-', linewidth=2,
                        color=sns.color_palette("viridis", len(match_week_avg.columns)))
    ax.set_xlabel("Jornada", fontsize=12, color='white')
    ax.set_ylabel("Promedio de Goles", fontsize=12, color='white')
    ax.legend(["Goles Local", "Goles Visitante"], fontsize=10, facecolor='black', edgecolor='white')
    ax.tick_params(colors='white')
    st.pyplot(fig)

# 3. Frecuencia de Estadios
def plot_stadium_frequency(data_fut):
    stadium_counts = data_fut['stadium'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    stadium_counts.plot(kind='bar', ax=ax, color=sns.color_palette("plasma", len(stadium_counts)))
    ax.set_xlabel("Estadio", fontsize=12, color='white')
    ax.set_ylabel("Cantidad de Partidos", fontsize=12, color='white')
    ax.tick_params(colors='white')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
