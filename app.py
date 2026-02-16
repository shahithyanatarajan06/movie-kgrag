import streamlit as st
from llm import extract_intent
from db import get_similar, get_top_rated, get_by_genre, get_by_actor

st.title("🎬 Movie Recommender (Neo4j + Groq)")

query = st.text_input("Ask something...")

if st.button("Search"):

    if not query:
        st.warning("Please enter a question.")
        st.stop()

    intent = extract_intent(query)

    if not intent or intent.get("type") == "error":
        st.error("LLM failed to extract intent.")
        st.stop()

    if intent["type"] == "similar_movie":
        results = get_similar(intent["movie"])

    elif intent["type"] == "top_rated":
        results = get_top_rated()

    elif intent["type"] == "by_genre":
        results = get_by_genre(intent["genre"])

    elif intent["type"] == "by_actor":
        results = get_by_actor(intent["actor"])

    else:
        results = ["Not supported yet"]

    st.subheader("Results")
    if results:
        for movie in results:
            st.write(movie)
    else:
        st.write("No results found.")