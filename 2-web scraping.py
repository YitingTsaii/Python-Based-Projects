import requests
from bs4 import BeautifulSoup

def get_ca_movie_titles():
    request_url = 'https://www.fantasy-sky.com/ContentList.aspx?section=002'
    ans = []
    
    #change movie name to English
    cookie_lang = {
        'COOKIE_LANGUAGE': 'en'
    }
    
    for num in range(1,5):
        params = {
            'section': '002',
            'category': '0020' + str(num) 
            #'category':'0020{}'.format(num) #another way
        }
        response = requests.get(request_url, params= params, cookies = cookie_lang)
        soup = BeautifulSoup(response.text)
        for e in soup.select('.movies-name'):
            #print(e.text)
            ans.append(e.text)
    return ans

#movie_list = get_ca_movie_titles()
#print(len(movie_list))
#print(movie_list)

def get_movie_rating_from_title(movie_title):  
    request_url = 'https://www.imdb.com/find'
    query_str_params = {
        'q': movie_title,
        's': 'tt',
        'ttype': 'ft',
        'ref_': 'fn_ft'
    }
    response = requests.get(request_url, params= query_str_params)
    soup = BeautifulSoup(response.text)
    add_url = soup.select('.result_text a')[0].get('href')
    my_url = 'https://www.imdb.com' + add_url
    
    params = {
        'ref_': 'nv_sr_srsg_4'
    }
    response = requests.get(my_url, params = params)
    soup = BeautifulSoup(response.text)
    rating = float(soup.select('strong span')[0].text)
    return rating

#get_movie_rating_from_title('inception')

def find_highest_rated_movies():
    movie_list = get_ca_movie_titles()
    ratings = []
    pattern_to_be_replaced = "Disney and Pixar's "
    
    for movie in movie_list:
        try:
            replaced_movie = movie.replace(pattern_to_be_replaced, '')
            rating = get_movie_rating_from_title(replaced_movie) 
            ratings.append(rating)
            print('The rating for ' + movie + ':' + str(rating))
        except:
            print('The rating for ' + movie + ': NA')
            ratings.append(0)
    max_rating = max(ratings)
    max_rating_movies = []
    for rating, movie in zip(ratings, movie_list):
        if rating == max_rating:
            max_rating_movies.append(movie)
    return max_rating_movies

max_rate_movie = find_highest_rated_movies()
print("The highest rated movie is", max_rate_movie)