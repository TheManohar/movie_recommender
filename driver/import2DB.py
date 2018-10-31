''' Select atribute database == 'GroupLens' or  'IMDB'! '''

def createDBfromIMDB():
    import pandas as pd
    import sqlite3
    import sys
    sys.path.insert(0, '../drivers')

    df1 = pd.read_csv('../rawData/title_akas.tsv', sep='\t') 
    df2 = pd.read_csv('../rawData/title_ratings.tsv', sep='\t') 
    df3 = pd.read_csv('../rawData/title_basics.tsv', sep='\t')

    df1.set_index('titleId', inplace = True)
    df2.set_index('tconst', inplace = True)
    df3.set_index('tconst', inplace = True)
    print(df1.head())
    print(df2.head())
    print(df3.head())

    dfM1 = pd.merge(df1, df2, left_index = True, right_index = True, how = 'outer')
    print(dfM1.head())
    dfM2 = pd.merge(dfM1, df3, left_index = True, right_index = True, how = 'outer')
    print(dfM2.head()) 

    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS moviesIMDB (
        id VARCHAR(255),
        ordering INTEGER,
        title VARCHAR(255),
        language VARCHAR(255),
        isOriginalTitle BOOLEAN,
        averageRating FLOAT,
        numVotes INTEGER,
        titleType VARCHAR(255),
        primaryTitle VARCHAR(255),
        originalTitle VARCHAR(255),
        startYear INTEGER,
        endYear INTEGER,
        runtimeMinutes INTEGER,
        genres VARCHAR(255)
    );
    """

    db = sqlite3.connect('moviesIMDB.db')
    db.executescript(DB_SETUP)

    for i, row in dfM2.iterrows():
        query = 'INSERT INTO moviesIMDB VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        db.execute(query, (i, row['ordering'], row["title"], row["language"], row["isOriginalTitle"], row["averageRating"], row["numVotes"], row['titleType'], row['primaryTitle'], row['originalTitle'], row['startYear'], row['endYear'], row['runtimeMinutes'], row['genres'], ))

    db.commit()
    db.close()

    print('\n### Congrats! IMDB Database moviesIMDB.db created! ###')

def createDBfromGrouplens():
    # https://grouplens.org/datasets/movielens/
    import pandas as pd
    import sqlite3
    import sys
    sys.path.insert(0, '../drivers')

    df1 = pd.read_csv('../rawData/ml-latest-small/links.csv')
    df2 = pd.read_csv('../rawData/ml-latest-small/movies.csv')
    df3 = pd.read_csv('../rawData/ml-latest-small/ratings.csv')
    df4 = pd.read_csv('../rawData/ml-latest-small/tags.csv')

    df1.set_index('movieId', inplace = True)
    df2.set_index('movieId', inplace = True)
    df3.set_index('movieId', inplace = True)
    df4.set_index('movieId', inplace = True)
      
    print(df1.head())
    print(df2.head())
    print(df3.head())
    print(df4.head())

    dfM1 = pd.merge(df1, df2, left_index = True, right_index = True, how = 'outer')
    print(dfM1.head())
    dfM2 = pd.merge(dfM1, df3, left_index = True, right_index = True, how = 'outer')
    print(dfM2.head())
    dfM3 = pd.merge(dfM2, df4[['tag']], left_index = True, right_index = True, how = 'outer')
    print(dfM3.head())
      
    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS moviesGroupLens (
        id VARCHAR(255),
        imdbId INTEGER,
        tmdbId INTEGER,
        title VARCHAR(255),
        genres VARCHAR(255),
        rating FLOT,
        timestamp INTEGER,
        tag VARCHAR(255)
        );
        """

    db = sqlite3.connect('moviesGroupLens.db')
    db.executescript(DB_SETUP)

    for i, row in dfM3.iterrows():
        query = 'INSERT INTO moviesGroupLens VALUES (?,?,?,?,?,?,?,?)'
        db.execute(query, (i, row['imdbId'], row["tmdbId"], row["title"], row["genres"], row["rating"], row["timestamp"], row['tag']))

    db.commit()
    db.close()

    print('\n### Congrats! GroupLens Database moviesGroupLens.db created! ###')

import sys
database = sys.argv[1]
print("{}".format(database))

if database == 'IMDB':
    createDBfromIMDB()
elif database == 'GroupLens':
    createDBfromGrouplens()
else:
    print('Select with database to use!')


