def createDBfromIMDB():
    import pandas as pd
    import sqlite3
    import sys
    sys.path.insert(0, '../drivers')

    df1 = pd.read_csv('../rawData/title.akas.tsv', sep='\t') 
    df2 = pd.read_csv('../rawData/title.ratings.tsv', sep='\t') 
    df1.set_index('titleId', inplace = True)
    df2.set_index('tconst', inplace = True)
    print(df1.head())
    print(df2.head())

    df3 = pd.merge(df1, df2, left_index = True, right_index = True, how = 'outer')
    print(df3.head())


    DB_SETUP = """
    CREATE TABLE IF NOT EXISTS moviesDB (
        id VARCHAR(255),
        ordering INTEGER,
        title VARCHAR(255),
        language VARCHAR(255),
        isOriginalTitle BOOLEAN,
        averageRating FLOAT,
        numVotes INTEGER
    );
    """

    db = sqlite3.connect('movies.db')
    db.executescript(DB_SETUP)

    for i, row in df3.iterrows():
        query = 'INSERT INTO moviesDB VALUES (?,?,?,?,?,?,?)'
        db.execute(query, (i, row['ordering'], row["title"], row["language"], row["isOriginalTitle"], row["averageRating"], row["numVotes"]))

    db.commit()
    db.close()

    print('\n### Congrats! Database movies.db created! ###')

createDBfromIMDB()
