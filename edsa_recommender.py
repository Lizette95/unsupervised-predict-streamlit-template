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
                # try:
                with st.spinner('Crunching the numbers...'):
                    top_recommendations = collab_model(movie_list=fav_movies,
                                                        top_n=10)
                st.title("We think you'll like:")
                for i,j in enumerate(top_recommendations):
                    st.subheader(str(i+1)+'. '+j)
            # except:
            #     st.error("Oops! Looks like this algorithm does't work.\
            #                 We'll need to fix it!")
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
        page_options_eda = ["User Interactions", "Movies", "Genres", "Directors"]
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

            intro = open('resources/markdown/intro.md').read()
            st.markdown(intro, unsafe_allow_html=True)##########
            
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
            #ratings = train_df[train_df['userId']!=72315]
            counts = st.number_input('Choose min ratings', min_value=0, max_value=15000, value = 10000, step=1000)
            ns= st.number_input('Choose n movies', min_value=5, max_value=20, value=10,step=5)
            eda.plot_ratings(count=counts, n=ns, color='red', best=True, method='mean')
            #plt.tight_layout()
            st.pyplot()
            st.write('By filtering movies with less than 10000 ratings, we find that the most popular movies are unsurprising titles. The Shawshank Redemption and The Godfather unsurprisingly top the list. What is interesting is that Movies made post 2000 do not feature often. Do users have a preference to Older movies?')

            eda.plot_ratings(count=counts, n=ns, color='green', best=False, method='mean')
            #plt.tight_layout()
            st.pyplot()
            st.write('Obviously, people did not like Battlefield too much and with 1200 ratings, they really wanted it to be known. It is interesting how many sequels appear in the list')
            

        if page_selection_eda == "Directors":
            st.write('best and worst directors, wordclouds to feed directors page')
        
        # if page_selection_eda == "Cast":
        #     st.write('best and worst cast, word clouds')
        
        # if page_selection_eda == "Plot Keywords":
        #     st.write('best and worst plots, word clouds')

        if page_selection_eda == "Genres":
            st.subheader('Which genres are the most frequently observed?')
            #eda.feat_extractor(df, col)
            #st.write('write something here')

            genres= eda.feature_frequency(movies_df, 'genres')
            st.write('write something here')

            eda.feature_count(genres.sort_values(by = 'count', ascending=False), 'genres')
            st.pyplot()
            st.write('Drama is the most frequently occuring genre in the database. Approximately 5000 movies have missing genres. We can use the IMDB and TMDB IDs together with the APIs to fill missing data. Further, IMAX is not a genre but rather a proprietary system for mass-viewings.')
            st.subheader('The above figure does not tell us anything about the popularity of the genres, lets calculate a mean rating and append it to the Data')
            genres['mean_rating']=eda.mean_calc(genres)
            show_data = st.checkbox('Show raw genre data?')
            if show_data:
                st.write(genres.sort_values('mean_rating', ascending=False))
            st.write('Film-Noir describes Hollywood crime dramas, particularly those that emphasize cynical attitudes and sexual motivations. The 1940s and 1950s are generally regarded as the "classic period" of American film-noir. These movies have the highest ratings but this may be as a result of its niche audence. The same logic can be applied to IMAX movies, as such, we will only include genres with a count of 500 or more.')
            eda.genre_popularity(genres.sort_values(by='mean_rating'))
            st.pyplot()
            st.write('The scores are almost evenly distributed with the exceptions of Documentaries, War, Drama, Musicals, and Romance and Thriller, Action, Sci-Fi, and Horror, which rate higher than average and below average respectively.')


    if page_selection == "Introduction":
        info_pages = ["General Information", "Contributors"]
        info_page_selection = st.selectbox("", info_pages)
        if info_page_selection == "General Information":
            st.image('resources/imgs/banner.png',use_column_width=True)
            st.markdown("<h1 style='text-align: center;'>The Flixters JHB_RM4</h1>", unsafe_allow_html=True)
            st.markdown(open('resources/markdown/intro.md').read(), unsafe_allow_html=True)
            see_raw = st.checkbox("Show data")
            if see_raw:
                st.write(dl.load_dataframe('resources/data/ratings.csv', index='userId').head(10))
                st.write(dl.load_dataframe('resources/data/movies.csv',index='movieId').head(10))
        
        if info_page_selection == "Contributors":
            st.markdown("<h1 style='text-align: center;'>Contributors</h1>", unsafe_allow_html=True)
            st.markdown("\n\n")
            
            # Lizette
            st.markdown("<h3 style='text-align: center;'>Lizette Loubser</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Team Coordinator and Machine Learning Engineer</p>", unsafe_allow_html=True)
            st.image('resources/imgs/Lizette.jpg', width=120)
            st.markdown("<a href='http://www.linkedin.com/in/lizette-loubser' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
            st.markdown("<a href='https://github.com/Lizette95' target='_blank'>GitHub</a>", unsafe_allow_html=True)
            
            # Bulelani
            st.markdown("<h3 style='text-align: center;'>Bulelani Nkosi</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Streamlit Coordinator and Data Analyst</p>", unsafe_allow_html=True)
            st.image('resources/imgs/Bulelani.jpg', width=120)
            st.markdown("<a href='https://www.linkedin.com/in/bulelanin' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
            st.markdown("<a href='https://github.com/BNkosi' target='_blank'>GitHub</a>", unsafe_allow_html=True)
                        
            # Neli
            st.markdown("<h3 style='text-align: center;'>Nelisiwe Mabanga</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Data Journalist and Analyst</p>", unsafe_allow_html=True)
            st.image('resources/imgs/nelly.jpeg', width=120)
            st.markdown("<a href='https://www.linkedin.com/in/nelisiwe-mabanga-8bb409106/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
            st.markdown("<a href='https://github.com/Phiwe-Mabanga' target='_blank'>GitHub</a>", unsafe_allow_html=True)
            
            # Nolu
            st.markdown("<h3 style='text-align: center;'>Noluthando Khumalo</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Streamlit App Design</p>", unsafe_allow_html=True)
            st.image('resources/imgs/Thando.jpg', width=120)
            st.markdown("<a href='https://www.linkedin.com/in/noluthando-khumalo-3870ab191/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
            st.markdown("<a href='https://github.com/ThandoKhumalo' target='_blank'>GitHub</a>", unsafe_allow_html=True)
            
            # Nompilo
            st.markdown("<h3 style='text-align: center;'>Nompilo Nhlabathi</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Streamlit App Design</p>", unsafe_allow_html=True)
            st.image('resources/imgs/Nompilo.png', width=120)
            st.markdown("<a href='http://www.linkedin.com/in/nompilo-nhlabathi-2701791b2' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
            st.markdown("<a href='https://github.com/mapilos' target='_blank'>GitHub</a>", unsafe_allow_html=True)
            
            # Sizwe
            st.markdown("<h3 style='text-align: center;'>Sizwe Bhembe</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Team member</p>", unsafe_allow_html=True)
            st.image('resources/imgs/Sizwe.jpg', width=120)
            st.markdown("<a href='https://www.linkedin.com/in/sizwe-bhembe-372880101' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
            #st.markdown("<a href='github.com/sjbhembe' target='_blank'>GitHub</a>", unsafe_allow_html=True)
            
    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
