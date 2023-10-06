# Here are the basic libraries for the basic operations
from unittest import result
import pandas as pd
import pickle
import requests

# for using Stickers and animations
from streamlit_lottie import st_lottie

# Streamlit is used for the Web UI
import streamlit as st

# for vectorization and Cosine Distance or similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel






# from here I am fetching the posters
def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key={}".format(movie_id, st.secrets["API_KEY"])
    data = requests.get(url)


    # handling the response 404 error
    if data.status_code == 404:       
        return "https://ndpp.co.in/wp-content/uploads/2018/01/sorry-image-not-available.jpg"
     
    data = data.json()   
    poster_path = data['poster_path'] 
     
    # if poster is not available for the movie 
    if poster_path == None :
        return "https://ndpp.co.in/wp-content/uploads/2018/01/sorry-image-not-available.jpg"
    
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    
    return full_path



def Movies_on_the_basis_of_genre(Genre = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign',
 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'], c=1):
    x = Final_Movies_list['genres']
    d = Final_Movies_list.drop(['genres'], axis = 1)
    x = pd.concat([d, x], axis = 1)
    x['Genres'] = Final_Movies_list['genres']
    x = x.explode('genres')
    x= x[(x['genres'] == Genre.lower())][[ 'weigh_avg_rating', 'id', 'title', 'Genres', 'cast','overview',]].sort_values(by = 'weigh_avg_rating',
                            ascending = False).reset_index(drop = True).head(c)
    return x


# optimized_recommendations function
def optimized_recommendations(title, n):
    
    # index of movie title
    idx = indices[title]
    
    # finding similarity scores and sorting the resultant movies in descending order of sim_scores
    
    # enumerate function holds the indixes while calculating similarity
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    
    # here is the whole movie data required for applying average weighted technique 
    movie_req = Final_Movies_list.iloc[movie_indices][['id', 'title', 'genres', 'cast','overview', 'weigh_avg_rating']]
    
    
    result = movie_req.sort_values('weigh_avg_rating', ascending=False).head(n)
    
    return result
# # # # # # # # # # # end of the functions # # # # # # # # # #  # # #



# From here I am starting the reading

Final_Movies_list = pd.read_pickle('New_data.pkl')

# Converting list to create a single string
Final_Movies_list['details'] = Final_Movies_list['details'].apply(lambda x: " ".join(x))



vec = TfidfVectorizer(max_features = 4501, stop_words = 'english')

vec_matrix = vec.fit_transform(Final_Movies_list['details'])


# using sklearn library calculating cosine similarity

cosine_sim = linear_kernel(vec_matrix, vec_matrix)


# Title of Movies
Title_list = Final_Movies_list['title'].values


# fetching indexes of movie titles
indices = pd.Series(Final_Movies_list.index, index = Final_Movies_list['title'])


#Stoting Top-rated movies 
Top_rated_movies = Final_Movies_list.sort_values('weigh_avg_rating', ascending=False).head(50)



st.set_page_config(page_title="Recommendation engine", page_icon="https://www.kindpng.com/picc/m/30-300778_transparent-movie-marquee-png-movie-icon-png-flat.png", layout="wide")

# header section


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")    


hey = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_khzniaya.json")    
welcome = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_1TcivY.json")    
with st.container():
    st.write("---")
    l_col, r_col = st.columns(2)
    with l_col:
        st.subheader("Hello, my name is Akshay, :wave:")
        st.subheader("I am currently pursuing my B.Tech in Mathematics and Computing from Delhi Technological University.")
        st_lottie(welcome, height=150, key="Welcome" )
        st.header("To my website presenting the Movie Recommendation Engine")
        

    with r_col:
        st_lottie(hey, height=300, key="Hello")    
st.write("---")


Genre = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign',
 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']
if __name__ == '__main__':

    st.header('Movie Recommendation Search Engine') 
    Str = ['--------Select--------', 'Recommend Movies on the basis of selected Genre', 'Recommend similar movies on the basis of a selected movie','Recommend Top-rated Movies']   
    Str_options = st.selectbox('How may I recommend movies to you ?', Str)

    # recommending movies on the basis on genre

    if Str_options == Str[1]:
        genre_selected = st.selectbox('Please Select a Genre', Genre)
        movie_count = st.slider("Select the Frequency",1,25,5)
        if st.button('Click here To Recommend'):
            st.balloons() 

    
            st.subheader("Here are the Recommendations For you")
            st.subheader("I Hope You like these movies")
            
            
            result = Movies_on_the_basis_of_genre(genre_selected, movie_count)
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                pos = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    pos.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].Genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(pos[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1

    # recommending movies according to optimized_recommendaion function
                   
    elif Str_options == Str[2]:
        movie_selected = st.selectbox('Please Select a Movie', Title_list)
        movie_count = st.slider("Select the Frequency",1,25,5)
        if st.button('Click here To Recommend'):
            st.balloons() 

            movie = Final_Movies_list[Final_Movies_list['title'] == movie_selected]

            st.subheader("You Selected This Movie")
            with st.container():
                index = movie.index[0]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

            with st.container():    
                with col1:
                    st.image(fetch_poster(movie['id'][index]), width = 150, caption = movie['title'][index])
                
                with col2:
                    st.write(movie['genres'][index])

                with col3:
                    st.write(movie['cast'][index])    

                with col4:
                    st.write(movie['overview'][index])        
            st.write("---")

            st.subheader("Here are the Recommendations For you")
            st.subheader("I Hope You like these movies")
            result = optimized_recommendations(movie_selected,movie_count)
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1
    # recommending Top rated Movies
    elif Str_options == Str[3]:
        movie_count = st.slider("Select the Frequency",1,50,10)
        if st.button('Click here To Recommend'): 
            st.balloons()
            st.subheader("Here are the Recommendations For you")
            st.subheader("I Hope You like these movies")
            result = Top_rated_movies
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1

    else:
        st.write('Please Select a option')

st.write("---")
st.title("Thank You For Visiting This Website :heart: :blue_heart: :purple_heart:")



# ---- CONTACT ----
with st.container():
    st.write("---")
    st.subheader("Give Your Suggestions here!")
    st.write("##")

    # Documention: https://formsubmit.co/
    contact_form = """
    <form action="https://formsubmit.co/239akshay01@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()
