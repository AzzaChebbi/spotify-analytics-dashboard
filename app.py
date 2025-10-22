import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from datasets import load_dataset  # pip install datasets

st.set_page_config(page_title="Spotify Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- LOAD DATASET ----
@st.cache_data
def load_data():
    dataset = load_dataset("maharshipandya/spotify-tracks-dataset")
    df = pd.DataFrame(dataset["train"])
    return df

df = load_data()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
top_n_artists = 50
top_n_genres = 20

top_artists = df['artists'].value_counts().head(top_n_artists).index.tolist()
top_genres = df['track_genre'].value_counts().head(top_n_genres).index.tolist()

artists = st.sidebar.multiselect("Select Artists:", options=top_artists, default=top_artists)
genres = st.sidebar.multiselect("Select Genres:", options=top_genres, default=top_genres)

df_selection = df[(df["artists"].isin(artists)) & (df["track_genre"].isin(genres))]

if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

# ---- MAINPAGE ----
st.title(":bar_chart: Spotify Dashboard")
st.markdown("##")

# TOP KPIs
total_tracks = len(df_selection)
average_duration = round(df_selection["duration_ms"].mean() / 1000, 2)
average_popularity = round(df_selection["popularity"].mean(), 1)
average_danceability = round(df_selection["danceability"].mean(), 2)
average_energy = round(df_selection["energy"].mean(), 2)

kpi_columns = st.columns(5)
kpi_columns[0].metric("Total Tracks", total_tracks)
kpi_columns[1].metric("Avg. Duration (s)", average_duration)
kpi_columns[2].metric("Avg. Popularity", average_popularity)
kpi_columns[3].metric("Avg. Danceability", average_danceability)
kpi_columns[4].metric("Avg. Energy", average_energy)

st.markdown("---")

# ---- VISUALIZATIONS ----

# 1. Popularity by Genre
popularity_by_genre = df_selection.groupby("track_genre")["popularity"].mean().sort_values()
fig_genre_popularity = px.bar(popularity_by_genre, x=popularity_by_genre.index, y="popularity", title="<b>Popularity by Genre</b>", color=popularity_by_genre.index, template="plotly_white")

# 2. Duration by Genre
duration_by_genre = df_selection.groupby("track_genre")["duration_ms"].mean() / 1000  # Convert ms to seconds
fig_duration = px.bar(duration_by_genre, x=duration_by_genre.index, y="duration_ms", title="<b>Average Duration by Genre (in seconds)</b>", color=duration_by_genre.index, template="plotly_white")

# 3. Danceability vs Energy (Best Selling Factors)
fig_dance_vs_energy = px.scatter(df_selection, x="danceability", y="energy", color="track_genre", size="popularity", title="<b>Danceability vs Energy</b>", template="plotly_white", hover_name="track_name", size_max=10)

# 4. Track Popularity Distribution
fig_popularity_distribution = px.histogram(df_selection, x="popularity", nbins=30, title="<b>Popularity Distribution</b>", template="plotly_white")

# 5. Danceability Distribution
fig_danceability_distribution = px.histogram(df_selection, x="danceability", nbins=30, title="<b>Danceability Distribution</b>", template="plotly_white")

# 6. Energy vs Danceability by Genre
fig_energy_vs_danceability = px.scatter(df_selection, x="danceability", y="energy", color="track_genre", title="<b>Energy vs Danceability by Genre</b>", template="plotly_white", hover_name="track_name")

# 7. Correlation between Danceability and Popularity
fig_dance_popularity_corr = px.scatter(df_selection, x="danceability", y="popularity", color="track_genre", title="<b>Danceability vs Popularity</b>", template="plotly_white", hover_name="track_name")

# 8. Loudness vs Energy
fig_loudness_vs_energy = px.scatter(df_selection, x="loudness", y="energy", color="track_genre", title="<b>Loudness vs Energy</b>", template="plotly_white", hover_name="track_name")

# 9. Track Count by Genre
track_count_by_genre = df_selection['track_genre'].value_counts()
fig_genre_count = px.bar(track_count_by_genre, x=track_count_by_genre.index, y=track_count_by_genre.values, title="<b>Track Count by Genre</b>", color=track_count_by_genre.index, template="plotly_white")

# 10. Average Popularity by Artist
popularity_by_artist = df_selection.groupby("artists")["popularity"].mean().sort_values(ascending=False).head(10)
fig_artist_popularity = px.bar(popularity_by_artist, x=popularity_by_artist.index, y="popularity", title="<b>Top 10 Artists by Average Popularity</b>", color=popularity_by_artist.index, template="plotly_white")

# 11. TRACK COUNT BY EXPLICITNESS (Pie Chart)
fig_explicit_count = px.pie(df_selection, names="explicit", title="<b>Track Count by Explicitness</b>", template="plotly_white")

# DISPLAY PLOTS
plot_columns = st.columns(2)
plot_columns[0].plotly_chart(fig_genre_popularity, use_container_width=True)
plot_columns[1].plotly_chart(fig_duration, use_container_width=True)

st.markdown("---")

plot_columns2 = st.columns(2)
plot_columns2[0].plotly_chart(fig_dance_vs_energy, use_container_width=True)
plot_columns2[1].plotly_chart(fig_popularity_distribution, use_container_width=True)

st.markdown("---")

plot_columns3 = st.columns(2)
plot_columns3[0].plotly_chart(fig_danceability_distribution, use_container_width=True)
plot_columns3[1].plotly_chart(fig_energy_vs_danceability, use_container_width=True)

st.markdown("---")

plot_columns4 = st.columns(2)
plot_columns4[0].plotly_chart(fig_dance_popularity_corr, use_container_width=True)
plot_columns4[1].plotly_chart(fig_loudness_vs_energy, use_container_width=True)

st.markdown("---")

plot_columns5 = st.columns(2)
plot_columns5[0].plotly_chart(fig_genre_count, use_container_width=True)
plot_columns5[1].plotly_chart(fig_artist_popularity, use_container_width=True)

st.markdown("---")
plot_columns6 = st.columns(1)
plot_columns6[0].plotly_chart(fig_explicit_count, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
st.markdown("""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """, unsafe_allow_html=True)
