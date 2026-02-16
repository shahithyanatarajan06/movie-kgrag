import pandas as pd
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

df = pd.read_csv("data/movies.csv")

def load():
    with driver.session() as session:
        for _, row in df.iterrows():

            session.run("""
            MERGE (m:Movie {title:$title})
            SET m.year=$year, m.rating=$rating
            """, title=row["title"], year=int(row["year"]), rating=float(row["rating"]))

            # Genres
            for g in str(row["genre"]).split("|"):
                session.run("""
                            MATCH (m:Movie {title:$title})
                            MERGE (g:Genre {name:$genre})
                            MERGE (m)-[:BELONGS_TO]->(g)
                        """, title=row["title"], genre=g.strip())

            # Actors
            for a in row["actors"].split("|"):
                session.run("""
                MERGE (a:Actor {name:$actor})
                MERGE (m:Movie {title:$title})
                MERGE (a)-[:ACTED_IN]->(m)
                """, actor=a.strip(), title=row["title"])

            # Director
            session.run("""
            MERGE (d:Director {name:$director})
            MERGE (m:Movie {title:$title})
            MERGE (d)-[:DIRECTED]->(m)
            """, director=row["director"], title=row["title"])

    print("Data Loaded!")

if __name__ == "__main__":
    load()