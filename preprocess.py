import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import sys
import os

# Add root directory to path if needed
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm_helper import llm  # Ensure this file exists and contains `llm` instance

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)  # list of posts
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {tag: unified_tags.get(tag, tag) for tag in current_tags}  # fallback to original tag
        post['tag'] = new_tags  # tag is a dict now

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4, ensure_ascii=False)


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)

    template = '''You will be given a list of tags. Your task is to unify them by grouping similar ones.

1. Tags should be grouped semantically.
   - "Jobseekers", "Job Hunting" → "Job Search"
   - "Motivation", "Inspiration" → "Motivation"
2. Use title case for final tag names, e.g., "Job Search", "Mental Health"
3. Output **only valid JSON**. No explanation or markdown.
4. Format: { "original_tag_1": "UnifiedTag", "original_tag_2": "UnifiedTag", ... }

Here is the list of tags:
{tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    try:
        response = chain.invoke({'tags': unique_tags_list})
        json_parser = JsonOutputParser()
        result = json_parser.parse(response.content)
    except Exception as e:
        raise OutputParserException("Context too big or invalid JSON output.") from e

    return result


def extract_metadata(post_text):
    template = '''
You are given a LinkedIn post. Extract number of lines, language, and two most relevant tags.

1. Return a valid JSON. No preamble.
2. JSON should have keys: line_count, language, tags.
3. tags is an array of up to two strings.
4. Language: "English" or "Hinglish" only.
5. Do NOT include explanation or markdown.

Here is the post:
{post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    try:
        response = chain.invoke({'post': post_text})
        json_parser = JsonOutputParser()
        result = json_parser.parse(response.content)
    except Exception as e:
        raise OutputParserException("Metadata extraction failed.") from e

    return result


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
