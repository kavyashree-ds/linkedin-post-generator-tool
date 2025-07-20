from llm_helper import llm
from few_shot import FewShotPosts

few_shot=FewShotPosts()

def get_length_str(length):
    if length=="Short":
        return "1 to 13 lines"
    if length=="Medium":
        return "14 to 20 lines"
    if length=="Long":
        return "21 to 26 lines"
    
def get_promt(length,language,tag):
    length_str=get_length_str(length)
    promt=f'''
    Generate a LinkedIn post using the following content. Do NOT include any introductions, headers, or phrases like 'Here's a LinkedIn post'. Only output the post content exactly.
    1.Topic: {tag}
    2.Length: {length}
    3.Language:{language}

   If Language is Hinglish then it means it is a mix of Hindi and English.
   The script for the generated post shold always be English.

'''
    examples=few_shot.get_filtered_posts(length,language,tag)
    if len(examples)>=0:
        promt+="4)use the writing style as per the following examples"
        for i,post in enumerate(examples):
            post_text=post['text']
            promt+=f"\n\n Example {i+1}: \n\n {post_text}"
            if i==1:
                break
    return promt


def generate_post(length,language,tag):
    promt=get_promt(length,language,tag)
    response=llm.invoke(promt)
    return response.content

if __name__ == "__main__":
    post=generate_post("Medium","English","Job Search")
    print(post)