import pandas as pd
PATH = "../rawData/movie_recommendations.xlsx"
df = pd.read_excel(PATH)
# find and remove duplicate movie entries (to avoid problems with unstack)
duplicates = df.index
df.index.drop_duplicates()

print(df.head(10))
print(df.groupby('Reviewer')['Rating'].mean)

#df[df['Rating'] == df['Rating'].max().head(10)]

df.sort_values('Rating', ascending = False, inplace = True)
print(df.head(5).sample(1))

df.set_index('Name', inplace=True)
print(df.head(5))

long = df.stack()
print(long.shape)
print(df.shape)
print(long.head(10))

short = long.head(15)
print("short",short)
wide = short.unstack(1) #unstack based on Gender (second column in the short)
print(wide)


