import requests
import urllib3
from bs4 import BeautifulSoup
import io
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to get top 250 movies from IMDb
def get_top_25_movies():
    url = "https://www.imdb.com/chart/top"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    movies = []
    for item in soup.select(".ipc-title-link-wrapper")[:25]:
        # Remove the query params from the URL
        # print(item)
        moviie_detail_Url = item['href']
        movie_url = item['href'].split('?')[0]  #https://www.imdb.com/t2131312/reviews
        movies.append({
            "title": item.text,
            "detailUrl": f"https://www.imdb.com{moviie_detail_Url}",
            "reviewUrl": f"https://www.imdb.com{movie_url}"
        })
    return movies

def get_top_250_movies():
    url = "https://www.imdb.com/chart/top"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    movies = []
    for script in soup.find_all('script', type='application/ld+json'):
        data = json.loads(script.string)
        if isinstance(data, dict) and data.get("@type") == "ItemList":
            for item in data.get("itemListElement", []):
                if isinstance(item, dict) and item.get("item", {}).get("@type") == "Movie":
                    moviie_detail_Url = item["item"].get("url")
                    review_Url = item["item"].get("url")
                    movies.append({
                        "title": item["item"].get("name"),
                        "detailUrl": moviie_detail_Url,
                        "reviewUrl": review_Url
                    })
    return movies
        # print(data)

# Function to get reviews of a movie
def get_reviews(movie_url):
    url = f"{movie_url}reviews"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    print(url)
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    # with io.open('reviewResponse.txt', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())
    #     print("File writing complete")
    reviews = [review.text for review in soup.select("div.ipc-html-content-inner-div")]
    return reviews

def get_movie_metaData(movie_detail_url):
    print("In details functions")
    url = movie_detail_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    # print(url)
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())

    # gettingMovieName
    movie_Name = soup.find("span", class_="hero__primary-text").text

    # gettingGenre
    genre = []
    scroller_div=soup.find('div', attrs={"data-testid": "interests"}).find('div', class_='ipc-chip-list__scroller')
    a_tags = scroller_div.find_all('a')
    for a_tag in a_tags:
            span_tag = a_tag.find('span')
            if span_tag:
                genre.append(span_tag.text)
    
    #fetching yearOfRelease / Age Restricion / time
    ulTags = soup.find_all('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt')

    othertags = []
    for ul_tag in ulTags:
        li_tags = ul_tag.find_all('li')
        for li_tag in li_tags:
            # Find the 'a' tag inside the 'li' tag and print its text
            a_tag = li_tag.find('a')
            if a_tag:
                othertags.append(a_tag.text)
    
    data = {}

    data["movie_Name"] = movie_Name
    data["genre"] = genre   
    data["other"]=othertags

    # print(data)
    return data



# Main function
def main():

    # get_movie_metaData("https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1")

    movies = get_top_250_movies()[:100]
    data = {}
    # print(movies)
    totalCount = 0
    for movie in movies:
        print(f"Analyzing reviews for: {movie['title']}")
        details = get_movie_metaData(movie['detailUrl'])
        reviews = get_reviews(movie['reviewUrl'])
        data[movie['title']] = {
            "details": details,
            "reviews": reviews
        }
        print(len(reviews))
        totalCount+=len(reviews)
    
    print("total Count "+str(totalCount))
    
    # Save the movie reviews dictionary to a JSON file
    with io.open('data2.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        print("Movie reviews saved to data2.json")

    # movies = get_top_250_movies()
    # movies = movies[:100]

    # print(len(movies))
    # for movie in movies:
    #     print(movie)

if __name__ == "__main__":
    main()
