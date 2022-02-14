from django.db import models

# Create your models here.
# def find_player(search_term):
#     endpoint = "https://search.espncricinfo.com/ci/content/site/search.html"
#     params = {"search": search_term}
#     response = requests.get(endpoint, params=params)
#     soup = BeautifulSoup(response.content, "html.parser")
#     results = soup.find("ul", attrs={"class": re.compile("player-list")})
#     while results == None:
#         search_term = input("Player not found. Please enter another player name")
#         params = {"search": search_term}
#         response = requests.get(endpoint, params=params)
#         soup = BeautifulSoup(response.content, "html.parser")
#         results = soup.find("ul", attrs={"class": re.compile("player-list")})
#     player_names = []
#     player_ids = []
#     for player in results.find_all("li"):
#         link = player.a["href"]
#         full_name = player.p.get_text()
#         initialised = player.h3.get_text()
#         country = player.find("p", attrs={"class": re.compile("country")}).string
#         player_names.append(f"{full_name} ({initialised}; {country})")
#         player_ids.append(re.search("/\d*\.", link).group()[1:-1])
#     if len(player_names) == 1:
#         player_name = player_names[0].split(",")[0]
#         player_id = int(player_ids[0])
#     else:
#         n = len(player_names)
#         print(f"\n{n} results found:")
#         for i in range(n):
#             print(i + 1, player_names[i])
#         selection = int(input(f"\nPlease select by entering a number between 1 and {n}:"))
#         player_name = player_names[selection - 1].split(",")[0]
#         player_id = int(player_ids[selection - 1])
#     return Player(player_id, player_name)