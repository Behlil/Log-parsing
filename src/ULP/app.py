import streamlit as st
import pandas as pd
from Linux_tools import *
from HealthApp_tools import *
import plotly.express as px
import matplotlib.pyplot as plt



def main():
    st.title("Résultats de l'analyse du fichier journal avec ULP")

    # Afficher la barre latérale pour les filtres et autres actions
    with st.sidebar:
        st.header("Options")

        # Ajouter un menu déroulant pour sélectionner le type de données à charger
        data_type = st.selectbox("Sélectionner le fichier à analyser :", ["Linux", "HealthApp"])

    
    if data_type == "Linux":
        with st.sidebar:
            
            st.write("Télécharger le fichier journal structuré :")
            download = st.button("Générer le fichier journal structuré")
            if download:
                
                download_file(r"C:/Users/OUQSSIM/Desktop/st/GSITD/src/ULP/demo_result/Linux.log_structured.csv")
        run_linux_analysis()

        

    elif data_type == "HealthApp":
        file_path = r"C:/Users/OUQSSIM/Desktop/st/GSITD/src/ULP/demo_result/HealthApp.log_structured.csv"
        data = load_data(file_path)
        # Nettoyer les données pour afficher uniquement les colonnes nécessaires
        data = clean_data(data)
        # Afficher les données dans un dataframe Streamlit
        st.write("Voici les résultats de l'éxtraction du Modèle d’événement :")
        st.dataframe(data)
        # Afficher un graphique à partir des données
        st.write("La fréquence des Modules :")
        modules_freq = modules_frequency()
        st.bar_chart(modules_freq, x='Module', y='count')
        
        
        # plot error frequency
        st.write("La fréquence des erreurs :")
        error_freq = count_error_frequency()
        err_fig = px.pie(error_freq, values='count', names='Module', title='Error Frequency')
        st.plotly_chart(err_fig)

        # add a select box to choose the logs by day, time or month
        st.write("Afficher les journaux par :")
        plot_by = st.selectbox("Sélectionner le type de journal à afficher :", ["Jour", "Heure", "Mois"])
        # plot logs by day if selected
        
        logs_by_day_data = logs_by_day()
        logs_by_hour_data = logs_by_hour()
        logs_by_month_data = logs_by_month()
        if plot_by == "Jour":
            
            st.bar_chart(logs_by_day_data, x='day', y='count')
            # st.dataframe(logs_by_day_data )

        # plot logs by hour if selected
        elif plot_by == "Heure":
            
            st.bar_chart(logs_by_hour_data, x='hour', y='count')

        # plot logs by month if selected
        elif plot_by == "Mois":
            
            st.bar_chart(logs_by_month_data, x='month', y='count')
        # show the plot
        
        with st.sidebar:
            # add a button to download the structured log file
            st.write("Télécharger le fichier journal structuré :")
            download = st.button("Générer le fichier journal structuré")
            if download:
                
                download_file(r"C:/Users/OUQSSIM/Desktop/st/GSITD/src/ULP/demo_result/HealthApp.log_structured.csv")

    else:
        st.write("Veuillez sélectionner un type de données à afficher.")



def load_data(file_path):
    # Charger les données extraites à partir du fichier CSV
    data = pd.read_csv(file_path)

    return data

# write a function to keep only the content, event template and regex columns
def clean_data(data):
    # renames the column content to EventContent
    data.rename(columns={'Content': 'EventContent'}, inplace=True)
    return data[['EventContent', 'EventTemplate', 'Regex']]

def run_linux_analysis():
    """
    Runs the analysis process.

    This function loads data from a file, cleans the data, displays it in a Streamlit dataframe,
    and plots a graph based on the data. It also allows the user to select the type of errors to display.

    Parameters:
        None

    Returns:
        None
    """
    file_path = r"C:/Users/OUQSSIM/Desktop/st/GSITD/src/ULP/demo_result/Linux.log_structured.csv"
    data = load_data(file_path)
    # Nettoyer les données pour afficher uniquement les colonnes nécessaires
    data = clean_data(data)
    # Afficher les données dans un dataframe Streamlit
    st.write("Voici les résultats de l'aextraction du Modèle d’événement :")
    st.dataframe(data, height=500, width=5000)
    # Afficher un graphique à partir des données
    st.write("La fréquence des services :")
    fig = plot_services_frequency()
    st.plotly_chart(fig)

      
    error_type = st.selectbox("Sélectionner le type d'érreurs :", ["All", "Authentification", "Memoire"])

    st.write("Les occurrences d'erreurs :")
    fig1 = plot_error_occurrences_by_service(error_type)
    st.plotly_chart(fig1)

def download_file(file_path):
    import base64
    # Add a download button to download the structured log file
    with open(file_path, 'r') as file:
        csv = file.read()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="Linux.log_structured.csv">Télécharger le fichier journal structuré</a>'
    st.markdown(href, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
