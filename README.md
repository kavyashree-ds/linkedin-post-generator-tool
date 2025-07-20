# 📝 LinkedIn Post Generator Tool

A powerful AI-based tool that auto-generates professional LinkedIn posts based on user-selected tag, tone, language, and post length — all with no preamble or filler. The system intelligently analyzes example posts, extracts metadata, unifies tags, and uses few-shot learning with LLaMA 3 (via Groq API) to generate new posts that mimic realistic writing styles.

## 🚀 Features

- Generates realistic, preamble-free LinkedIn posts
- Learns writing style from sample posts using few-shot prompting
- Categorizes posts by language, line count, and tags
- Unifies tags using semantic understanding (via LLM)
- Supports English and Hinglish
- Uses LangChain + Groq’s LLaMA 3 API

## 📂 Project Structure

linkedin-post-generator-tool/
├── data/
│ ├── raw_posts.json # Original user posts
│ └── processed_posts.json # Enriched posts with metadata
├── llm_helper.py # Handles Groq API and LLM response
├── preprocess.py # Extracts line count, tags, language, unifies tags
├── few_shot.py # Filters examples by length, language, tag
├── post_generator.py # Generates new LinkedIn posts
└── README.md # Project documentation (this file)
