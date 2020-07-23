"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
    application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

    For further help with the Streamlit framework, see:

    https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Data Visulization
import matplotlib.pyplot as plt

# Custom Libraries
from utils import data_loader as dl
from eda import eda_functions as eda
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

path_to_s3 = ('../unsupervised_data/')

# Data Loading
title_list = dl.load_movie_titles('../unsupervised_data/unsupervised_movie_data/movies.csv')
train_df = dl.load_dataframe('../unsupervised_data/unsupervised_movie_data/train.csv', index=None)
movies_df = dl.load_dataframe('../unsupervised_data/unsupervised_movie_data/movies.csv', index=None)

# Loading a css stylesheet
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("resources/css/style.css")

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Introduction", "Exploratory Data Analysis", "Directors Profiles", "Recommender System", "Solution Overview"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        # movie_list = pd.merge(train_df, title_list, on = 'movieId', how ='left').groupby('title')['ratings'].mean()
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")
    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")
    # ------------- EDA -------------------------------------------
    if page_selection == "Exploratory Data Analysis":
        st.title("Exploratory Data Analysis")
        # st.write("Observations from the Data Exploration")
        # Declare subpages
        page_options_eda = ["User Interactions", "Movies", "Directors", "Cast", "Plot Keywords"]
        page_selection_eda = st.selectbox("Choose Area of Exploration", page_options_eda)
        if page_selection_eda == "User Interactions":
        # Most Active
            st.subheader("Most Active Users")
            top_user = st.checkbox('Include top user?',value=False)
            ## include top user
            if top_user == True:
                ratings = train_df
            else:
                ratings = train_df[train_df['userId']!=72315]
            ## choose top k
            n = st.number_input('Enter number of users (1-20)',min_value=5, max_value=50, step = 5, value=10)
            ratings_plot = eda.user_ratings_count(ratings, n)
            st.pyplot()
            st.write('write something about top users')
        # Ratings Distribution
            st.subheader('Ratings Distribution')
            eda.number_users_per_rating(ratings)
            st.pyplot()
            st.write('write something about ratings ditribution')

        # Rating v number of ratings
            st.subheader('Ratings trends')
            eda.mean_ratings_scatter(ratings, color ='red')
            plt.title('Mean user ratings by number of ratings given')
            st.pyplot()
            st.write('write something about scatter')
            eda.mean_ratings_scatter(ratings, column ='movieId')
            plt.title('Mean movie rating by number of ratings received')
            st.pyplot()
            st.write('write something about scatter')

        if page_selection_eda == "Movies":
            st.write('best and worst movies by genre')
            ratings = train_df[train_df['userId']!=72315]
            counts = st.number_input('Choose min ratings', min_value=0, max_value=15000, value = 10000, step=1000)
            ns= st.number_input('Choose n movies', min_value=5, max_value=20, value=10,step=5)
            eda.plot_ratings(count=counts, n=ns)
            
            st.pyplot() 
        if page_selection_eda == "Directors":
            st.write('best and worst directors, wordclouds to feed directors page')
        
        if page_selection_eda == "Cast":
            st.write('best and worst cast, word clouds')
        
        if page_selection_eda == "Plot Keywords":
            st.write('best and worst plots, word clouds')

            

    if page_selection == "Introduction":
        info_pages = ["Problem landscape", "Problem Statement", "Contributors"]
        info_page_selection = st.selectbox("", info_pages)
        if info_page_selection == "Problem landscape":
            st.markdown("<h1 style='text-align: center;'>Introduction</h1>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center;'>A movie recommendation web app based on content and collaborative filtering, capable of accurately predicting movies a user might like based on their preferences.</h4>", unsafe_allow_html=True)
            st.image('resources/imgs/banner.png',use_column_width=True)
            st.markdown("In today's technology driven world, recommender systems are critical to ensuring users can make appropriate decisions about the content they engage with daily. Recommender systems help users select similar items when something is being chosen online. Netflix or Amazon would suggest different movies and titles that might interest individual users. In education, these systems may be used to suggest learning material that could improve educational outcomes. These types of algorithms lead to service improvement and customer satisfaction. Current recommendation systems - content-based filtering and collaborative filtering - use difference information sources to make recommendations.\n\n")
            st.write("Web app intro...")
        
        
        if info_page_selection == "Problem Statement":
            st.write('write something here')

        if info_page_selection == "Contributors":
            st.write('add something here')

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
