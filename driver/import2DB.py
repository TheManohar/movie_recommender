def createDBfromIMDB():
    import pandas as pd
    import sqlite3
    import sys
    sys.path.insert(0, '../drivers')

    df1 = pd.read_csv('../rawData/title.akas.tsv', sep='\t') 
    df2 = pd.read_csv('../rawData/title.ratings.tsv', sep='\t') 
    df3 = pd.read_csv('../rawData/title.basics.tsv', sep='\t')

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
    CREATE TABLE IF NOT EXISTS moviesDB (
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

    db = sqlite3.connect('movies2.db')
    db.executescript(DB_SETUP)

    for i, row in dfM2.iterrows():
        query = 'INSERT INTO moviesDB VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        db.execute(query, (i, row['ordering'], row["title"], row["language"], row["isOriginalTitle"], row["averageRating"], row["numVotes"], row['titleType'], row['primaryTitle'], row['originalTitle'], row['startYear'], row['endYear'], row['runtimeMinutes'], row['genres'], ))

    db.commit()
    db.close()

    print('\n### Congrats! Database movies.db created! ###')

createDBfromIMDB()
