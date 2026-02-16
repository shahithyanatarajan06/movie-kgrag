from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

def get_similar(movie):
    query = """
    MATCH (m:Movie)
    WHERE toLower(m.title) = toLower($title)
    MATCH (m)-[:BELONGS_TO]->(g)<-[:BELONGS_TO]-(rec:Movie)
    WHERE rec.title <> m.title
    RETURN DISTINCT rec.title AS movie
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query, title=movie)
        return [r["movie"] for r in result]

def get_top_rated():
    query = """
    MATCH (m:Movie)
    RETURN m.title AS movie
    ORDER BY m.rating DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        return [r["movie"] for r in result]
    
def get_by_genre(genre):
    query = """
    MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre {name:$genre})
    RETURN m.title AS movie
    ORDER BY m.rating DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query, genre=genre)
        return [r["movie"] for r in result]
    
def get_by_actor(actor):
    query = """
    MATCH (a:Actor {name:$actor})-[:ACTED_IN]->(m:Movie)
    RETURN m.title AS movie
    ORDER BY m.rating DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query, actor=actor)
        return [r["movie"] for r in result]