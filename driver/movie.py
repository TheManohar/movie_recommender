import pandas as pd
PATH = "../rawData/movie_recommendations.xlsx"
df = pd.read_excel(PATH)
print("""
    Kristians and Felipes Movie Recommender:
    Enter your favourite genre or reviwer
    and the program will recommend a movie.
""")

#TODO: we need to ask for the reviewer

print("enter a genre (or leave it empty): ", end="")
genre = input()

if genre:
    g = df[df['Genre'] == genre]
else:
    g = df


if g.shape[0] > 0:
    result = g.sort_values('Rating', ascending=False)
    print(result.head(3).sample(1))
else:
    print("Sorry, no results!")



