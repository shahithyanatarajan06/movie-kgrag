from groq import Groq
import os
from dotenv import load_dotenv
import json
import re 

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a movie intent extractor.

Return ONLY valid JSON.

Possible types:
- similar_movie (needs: movie)
- top_rated
- by_actor (needs: actor)
- by_genre (needs: genre)

Examples:

User: Recommend movies like Inception
Return:
{"type":"similar_movie","movie":"Inception"}

User: Suggest a comedy film
Return:
{"type":"by_genre","genre":"Comedy"}

User: Movies of Leonardo DiCaprio
Return:
{"type":"by_actor","actor":"Leonardo DiCaprio"}

User: Show top rated movies
Return:
{"type":"top_rated"}
"""

def extract_intent(query):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":query}
        ],
        temperature=0
    )

    response = completion.choices[0].message.content.strip()

    # Extract JSON safely
    json_match = re.search(r"\{.*\}", response, re.DOTALL)

    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            return {"type": "error"}

    return {"type": "error"}