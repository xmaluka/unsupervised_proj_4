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
from PIL import Image
#Plots
import seaborn as sns
import matplotlib.style as style 
sns.set(font_scale=1)
import matplotlib.pyplot as plt
#import plotly.figure_factory as ff

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

data_path = '../unsupervised_data/unsupervised_movie_data/'
#dataframe of movie titles
#def genre_titles(filename,genre):
#    filename = '../edsa-recommender-system-predict/'+str(filename)
#    chunks = pd.read_csv(filename,chunksize=10000)
#    data = pd.DataFrame()
#    for chunk in chunks:
#        chunk = chunk[chunk.genres.apply(lambda x: genre in x)]
#        data = pd.concat([data,chunk])
#    data = data.title.tolist()
#    return(data)

# Data Loading

title_list = load_movie_titles('resources/data/movies.csv')
#ratings = pd.read_csv('../edsa-recommender-system-predict/train.csv')

def background_setup(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ['Welcome','Reccomender','EDA','Solution Overview','About','test_page']

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox('Choose Option', page_options)
    if page_selection == 'Welcome':
        def background_setup(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        background_setup('home_style.css')
#         Header contents
#        st.write('# Nextflix')
        st.image('resources/imgs/home_page/nextflix_home.png')
    if page_selection =='Reccomender':
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
#        Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))
#
        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]
#
#        Perform top-10 movie recommendation generation
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
#
#
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
    if page_selection == 'EDA':
        def genre_count(filename,list1):
            '''Plots the distribution of genres in the movies dataset'''
            filename = data_path+str(filename)
            chunks = pd.read_csv(filename,chunksize=10000)
            data = pd.DataFrame()
            count = 0
            dict_genres = {}
            for chunk in chunks:
                chunk_genres = ','.join([genres.replace('|',',') for genres in chunk.genres]).split(',')
                chunk_genres = [item for item in chunk_genres if item in list1]
                for genre in chunk_genres:
                    if genre in dict_genres:
                        dict_genres[genre]+=1
                    else:
                        dict_genres[genre]=1
            sorted_dict = sorted(dict_genres.items(), key=lambda x: x[1],reverse=True)
            genre, frequency = zip(*sorted_dict)
            plt.figure(figsize=(10,5))
            freq_plot = sns.barplot(x = frequency,y = list(genre),palette='pastel')
            freq_plot.set(title='Genre frequency',
                          xlabel='Genre_count',ylabel='Genre')
            plt.show()
            return (freq_plot)
        st.title('EDA') 
        genres_setlist = ['Action','Adventure','Animation',
                          'Children','Comedy',
                          'Crime','Documentary',
                          'Drama','Fantasy','Horror','Mystery',
                          'Romance','Sci-fi',
                          'Thriller','War','Western']
        genres = st.multiselect('select genres',genres_setlist)
#        st.write(genres)
        if len(genres) > 0:
            genre_count_figure = genre_count('movies.csv',genres).figure
            if st.checkbox('show genre counts in dataset'):
                st.write(genre_count_figure)
        if st.checkbox('Greatest Hits'):
            # Movie Titles List:
            titles = ['The Shawshank Redemption','Pulp Fiction','Forrest Gump','The Silence of The Lambs',
                      'The MATRIX','Star Wars: Episode IV - A New Hope','Schindler\'s List','Fight Club',
                      'Star Wars: Episode V - The empire Strikes Back','Braveheart','The Usual Suspects',
                      'Jurassic Park','Terminator 2: Judgment Day','The Lord of The Rings (TFOTR)','Raisers of The Lost Ark']
            #Images List
            images = ['resources/imgs/thumbnails/shawshank_redemption.png','resources/imgs/thumbnails/pulp_fiction.png',
                      'resources/imgs/thumbnails/forest_gump.png','resources/imgs/thumbnails/silence_of_the_lambs.png',
                      'resources/imgs/thumbnails/the_matrix.png','resources/imgs/thumbnails/star_wars.png',
                      'resources/imgs/thumbnails/schindlers_list.png','resources/imgs/thumbnails/fight_club.png',
                      'resources/imgs/thumbnails/star_wars_2.png','resources/imgs/thumbnails/braveheart.png',
                      'resources/imgs/thumbnails/the_usual_suspects.png','resources/imgs/thumbnails/jurassic_park.png',
                      'resources/imgs/thumbnails/terminator_2.png','resources/imgs/thumbnails/LOTR_FLOTR.png',
                      'resources/imgs/thumbnails/raiders_of_lost_ark.png']
            st.write(len(images),len(titles))
            
            
            shawshank_redemption =(st.subheader('1. The Shawshank Redemption'),st.image('resources/imgs/thumbnails/shawshank_redemption.png', width=100),st.write('Realese year:1994  \n Genre: Drama  \nRealese year:1994  \nRuntime: 2h 22min  \nAverage rating: 4.4  \nNumber of ratings: 32831  \nStoryline:  \nChronicles the experiences of a formerly successful banker as a prisoner in the gloomy jailhouse of Shawshank after being found guilty of a crime he did not commit. The film portrays the man\'s unique way of dealing with his new, torturous life; along the way he befriends a number of fellow prisoners, most notably a wise long-term inmate named Red.'))
            st.subheader('2. Pulp Fiction')
            st.image('resources/imgs/thumbnails/pulp_fiction.png', width=100)
            st.write('Release year: 1994  \nGenre: Comedy, Crime  \nRuntime: 2h.58min  \nRatings: 4.2  \nNumber of Ratings: 31697  \nStoryline:  \nJules Winnfield (Samuel L. Jackson) and Vincent Vega (John Travolta) are two hit men who are out to retrieve a suitcase stolen from their employer, mob boss Marsellus Wallace (Ving Rhames). Wallace has also asked Vincent to take his wife Mia (Uma Thurman) out a few days later when Wallace himself will be out of town. Butch Coolidge (Bruce Willis) is an aging boxer who is paid by Wallace to lose his fight. The lives of these seemingly unrelated people are woven together comprising a series of funny, bizarre and uncalled-for incidents.')
            st.subheader('3. Forrest Gump')
            st.image('resources/imgs/thumbnails/forest_gump.png', width=100)
            st.markdown('Release year: 1994  \nGenre: Drama, Romance  \nRuntime: 2h.22min  \nRatings: 4.1  \nNumber of Ratings: 32383  \nStoryline:  \nForrest Gump is a simple man with a low I.Q. but good intentions. He is running through childhood with his best and only friend Jenny. His \'mama\' teaches him the ways of life and leaves him to choose his destiny. Forrest joins the army for service in Vietnam, finding new friends called Dan and Bubba, he wins medals, creates a famous shrimp fishing fleet, inspires people to jog, starts a ping-pong craze, creates the smiley, writes bumper stickers and songs, donates to people and meets the president several times. However, this is all irrelevant to Forrest who can only think of his childhood sweetheart Jenny Curran, who has messed up her life. Although in the end all he wants to prove is that anyone can love anyone.')
            st.subheader('4. The Silence of The Lambs')
            st.image('resources/imgs/thumbnails/silence_of_the_lambs.png', width=100)
            st.markdown('Release year:  1991  \nGenre: Crime, Drama, Thriller  \nRuntime: 1h.58min  \nRatings: 4.2  \nNumber of Ratings: 29444  \nStoryline:  \nF.B.I. trainee Clarice Starling (Jodie Foster) works hard to advance her career, while trying to hide or put behind her West Virginia roots, of which if some knew, would automatically classify her as being backward or white trash. After graduation, she aspires to work in the agency\'s Behavioral Science Unit under the leadership of Jack Crawford (Scott Glenn). While she is still a trainee, Crawford asks her to question Dr. Hannibal Lecter (Sir Anthony Hopkins), a psychiatrist imprisoned, thus far, for eight years in maximum security isolation for being a serial killer who cannibalized his victims. Clarice is able to figure out the assignment is to pick Lecter\'s brains to help them solve another serial murder case, that of someone coined by the media as "Buffalo Bill" (Ted Levine), who has so far killed five victims, all located in the eastern U.S.')
            st.subheader('5. The MATRIX')
            st.image('resources/imgs/thumbnails/the_matrix.png', width=100)
            st.markdown('Release year: 1999  \nGenre: Action, Sci-Fi  \nRuntime: 2h.16min  \nRatings: 4.2  \nNumber of Ratings: 29014  \nStoryline:  \nThomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination. Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government. As a rebel against the machines, Neo must confront the agents: super-powerful computer programs devoted to stopping Neo and the entire human rebellion.')
            st.subheader('6. Star Wars: Episode IV - A New Hope')
            st.image('resources/imgs/thumbnails/star_wars.png', width=100)
            st.markdown('Release year: 1977  \nGenre: Action, Adventure, Fantasy  \nRuntime: 2h.1min  \nRatings: 4.2  \nNumber of Ratings: 27560  \nStoryline:  \nThe Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in their efforts to quell the rebellion against the Galactic Empire. Luke Skywalker and Han Solo, captain of the Millennium Falcon, work together with the companionable droid duo R2-D2 and C-3PO to rescue the beautiful princess, help the Rebel Alliance and restore freedom and justice to the Galaxy.')
            st.subheader('7. Schindler\'s List')
            st.image('resources/imgs/thumbnails/schindlers_list.png', width=100)
            st.markdown('Release year: 1993  \nGenre: Biography, Drama, History  \nRuntime: 3h.15min  \nRatings: 4.2  \nNumber of Ratings: 24004  \nStoryline:  \nOskar Schindler is a vain and greedy German businessman who becomes an unlikely humanitarian amid the barbaric German Nazi reign when he feels compelled to turn his factory into a refuge for Jews. Based on the true story of Oskar Schindler who managed to save about 1100 Jews from being gassed at the Auschwitz concentration camp, it is a testament to the good in all of us.')
            st.subheader('8. Fight Club')
            st.image('resources/imgs/thumbnails/fight_club.png', width=100)
            st.markdown('Release year: 1999  \nGenre: Drama  \nRuntime: 2h.19min  \nRatings: 4.2  \nNumber of Ratings: 23536  \nStoryline:  \nA nameless first person narrator (Edward Norton) attends support groups in an attempt to subdue his emotional state and relieve his insomniac state. When he meets Marla (Helena Bonham Carter), another fake attendee of support groups, his life seems to become a little more bearable. However when he associates himself with Tyler (Brad Pitt) he is dragged into an underground fight club and soap making scheme. Together the two men spiral out of control and engage in competitive rivalry for love and power. When the narrator is exposed to the hidden agenda of Tyler\'s fight club, he must accept the awful truth that Tyler may not be who he says he is.')
            st.subheader('9. Star Wars: Episode V - The empire Strikes Back')
            st.image('resources/imgs/thumbnails/star_wars_2.png', width=100)
            st.markdown('Release year: 1980  \nGenre:  Action, Adventure, Fantasy  \nRuntime: 2h.4min  \nRatings: 4.2  \nNumber of Ratings: 22956  \nStoryline:  \nLuke Skywalker, Han Solo, Princess Leia and Chewbacca face attack by the Imperial forces and its AT-AT walkers on the ice planet Hoth. While Han and Leia escape in the Millennium Falcon, Luke travels to Dagobah in search of Yoda. Only with the Jedi Master\'s help will Luke survive when the Dark Side of the Force beckons him into the ultimate duel with Darth Vader.')
            st.subheader('10. Braveheart')
            st.image('resources/imgs/thumbnails/braveheart.png', width=100)
            st.markdown('Release year: 1995  \nGenre: Biography, Drama, History  \nRuntime: 2h.58min  \nRatings: 4.0  \nNumber of Ratings: 23722  \nStoryline:  \nWilliam Wallace is a Scottish rebel who leads an uprising against the cruel English ruler Edward the Longshanks, who wishes to inherit the crown of Scotland for himself. When he was a young boy, William Wallace\'s father and brother, along with many others, lost their lives trying to free Scotland. Once he loses another of his loved ones, William Wallace begins his long quest to make Scotland free once and for all, along with the assistance of Robert the Bruce.')
            st.subheader('11. The Usual Suspects')
            st.image('resources/imgs/thumbnails/the_usual_suspects.png', width=100)
            st.markdown('Release year: 1995  \nGenre: Crime, Mystery, Thriller  \nRuntime: 1h.46min  \nRatings: 4.3  \nNumber of Ratings: 22032  \nStoryline:  \nFollowing a truck hijack in New York, five criminals are arrested and brought together for questioning. As none of them are guilty, they plan a revenge operation against the police. The operation goes well, but then the influence of a legendary mastermind criminal called Keyser Söze is felt. It becomes clear that each one of them has wronged Söze at some point and must pay back now. The payback job leaves 27 men dead in a boat explosion, but the real question arises now: Who actually is Keyser Söze?')
            st.subheader('12. Jurassic Park')
            st.image('resources/imgs/thumbnails/jurassic_park.png', width=100)
            st.markdown('Release year: 1993  \nGenre: Action, Advecture, Sci-Fi  \nRuntime: 2h.7min  \nRatings: 3.7  \nNumber of Ratings: 25518  \nStoryline:  \nHuge advancements in scientific technology have enabled a mogul to create an island full of living dinosaurs. John Hammond has invited four individuals, along with his two grandchildren, to join him at Jurassic Park. But will everything go according to plan? A park employee attempts to steal dinosaur embryos, critical security systems are shut down and it now becomes a race for survival with dinosaurs roaming freely over the island.')
            st.subheader('13. Terminator 2: Judgment Day')
            st.image('resources/imgs/thumbnails/terminator_2.png', width=100)
            st.markdown('Release year: 1991  \nGenre: Action, Sci-Fi  \nRuntime: 2h.17min  \nRatings: 4.0  \nNumber of Ratings: 23075  \nStoryline:  \nOver 10 years have passed since the first machine called The Terminator tried to kill Sarah Connor and her unborn son, John. The man who will become the future leader of the human resistance against the Machines is now a healthy young boy. However, another Terminator, called the T-1000, is sent back through time by the supercomputer Skynet. This new Terminator is more advanced and more powerful than its predecessor and it\'s mission is to kill John Connor when he\'s still a child. However, Sarah and John do not have to face the threat of the T-1000 alone. Another Terminator (identical to the same model that tried and failed to kill Sarah Conner in 1984) is also sent back through time to protect them. Now, the battle for tomorrow has begun.')
            st.subheader('14. The Lord of The Rings (TFOTR)')
            st.image('resources/imgs/thumbnails/LOTR_FLOTR.png',width=100)
            st.markdown('Release year: 2001  \nGenre: Action, Adventure, Drama  \nRuntime: 2h.58min  \nRatings: 4.1  \nNumber of Ratings: 22216  \nStoryline:  \nAn ancient Ring thought lost for centuries has been found, and through a strange twist of fate has been given to a small Hobbit named Frodo. When Gandalf discovers the Ring is in fact the One Ring of the Dark Lord Sauron, Frodo must make an epic quest to the Cracks of Doom in order to destroy it. However, he does not go alone. He is joined by Gandalf, Legolas the elf, Gimli the Dwarf, Aragorn, Boromir, and his three Hobbit friends Merry, Pippin, and Samwise. Through mountains, snow, darkness, forests, rivers and plains, facing evil and danger at every corner the Fellowship of the Ring must go. Their quest to destroy the One Ring is the only hope for the end of the Dark Lords reign.')
            st.subheader('15. Raisers of The Lost Ark')
            st.image('resources/imgs/thumbnails/raiders_of_lost_ark.png',width=100)
            st.markdown('Release year: 1981  \nGenre: Action, Adventure  \nRuntime: 1h.55m  \nRatings: 4.1  \nNumber of Ratings: 21982  \nStoryline:  \nThe year is 1936. An archeology professor named Indiana Jones is venturing in the jungles of South America searching for a golden statue. Unfortunately, he sets off a deadly trap but miraculously escapes. Then, Jones hears from a museum curator named Marcus Brody about a biblical artifact called The Ark of the Covenant, which can hold the key to humanely existence. Jones has to venture to vast places such as Nepal and Egypt to find this artifact. However, he will have to fight his enemy Rene Belloq and a band of Nazis in order to reach it.')
            
            #Next Button
            list_1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
            button = 'button' #Initialise program only
            def next_prev(button):
                next_counter = pd.read_csv('resources/imgs/thumbnails/next_button.csv')['value']
                next_value = next_counter[0]
                if button == 'next':
                    if next_value >= 14:
                        next_value = 0
                    else:
                        next_value = next_value + 1
                    next_counter[0] = next_value
                    next_counter.to_csv('resources/imgs/thumbnails/next_button.csv')
                if button == 'previous':
                    if next_value < 1:
                        next_value = 14
                    else:
                        next_value = next_value - 1
                    next_counter[0] = next_value
                    next_counter.to_csv('resources/imgs/thumbnails/next_button.csv')
                return(next_value)
            if st.button('next'):
                next_prev('next')
            if st.button('previous'):
                next_prev('previous')
            st.write(list_1[next_prev(button)])
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")
    if page_selection == 'test_page':
        st.write('1,2,3...test')

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
