import os
import re
import praw
import json
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv
load_dotenv()

#list of all the common english words that MIGHT be in the name of the product
stopwords = set(stopwords.words('english'))
#essential to scrape data off of reddit
reddit = praw.Reddit(
    client_id = os.environ.get("client_id"),
    client_secret = os.environ.get("client_secret"),
    user_agent = os.environ.get("user_agent"),
)
#the main analysing and file saving function
from groq import Groq
def analyser(product, sub):
    #to access groq
    filename = f"data/{sub}_{product.replace(' ', '_')}.json"
    client = Groq(
        api_key= os.environ.get("groq_key"),
    )
    #the prompt that specifies everything to groq
    prompt =(
        f"I am going to send you a json file of 10 reddit posts, their title, score, and comments."
        f"The subreddit is {sub} and the search query is {product}."
        f"You must read all the comments and then give out a general review of {product} with the positives and negatives of the product."
        "Consider the score of each comment and the replies to that comment too. "
        "Your output must be a python dictionary in the following format:"
        "{\n"
        "  'product_name': '<product_name>',\n"
        "  'subreddit': '<subreddit_name>',\n"
        "  'positives': ['<positive_point_1>', '<positive_point_2>', ...],\n"
        "  'negatives': ['<negative_point_1>', '<negative_point_2>', ...],\n"
        "  'best_for': ['<skin_concern_1>', '<skin_concern_2>', ...],\n"
        "  'not_recommended_for': ['<reason_1>', '<reason_2>', ...]\n"
        "  'ratio': (positive to negative comments ratio)"
        "} \n"
        "Ensure the output is well-structured as a Python dictionary. It MUST be a valid JSON and there should be no extraneous text. Thank you!"
    )
    #loading the data into memory
    with open(filename, "r") as f:
        data = json.load(f)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt} Here is the data: {data}",
            }
        ],
        model="llama3-8b-8192",
    )
    #receiving output from groq
    content = chat_completion.choices[0].message.content
    return content
    
#filtering the output
def converter(content, sub, product):
    start = content.find("{")
    end = content.find("}") + 1
    content = content[start:end]
    for i in range(len(content) - 1):
        if content[i] == "'":
            if content[i - 1].isalpha() and content[i + 1].isalpha():
                continue
            else:
                content = content[:i] + '"' + content[i+1:]
    try:
        final = json.loads(content)
        saving = f"reviews/{sub}_{product.replace(' ', '_')}.json"
        with open(saving, "w") as f:
            json.dump(final, f, indent= 2)
    except json.JSONDecodeError:
        print(f"Couldn't convert the output into JSON. Here's the output: \n{content}")

#function to read and print json file
def reader(address):
    with open(address, "r") as f:
        review = json.load(f)
    print(review['product_name'])
    print(f"r/{review['subreddit']}")
    print("Positives: ")
    for positive in review['positives']:
        print(positive)
    print("Negatives: ")
    for negative in review['negatives']:
        print(negative)
    print("Best for: ")
    for point in review['best_for']:
        print(point)
    print("Not recommended for: ")
    for point in review['not_recommended_for']:
        print(point)
    print(f"Ratio of positive comments to negative comments: {review['ratio']}")

#function to check if comments have the relevant words
def relevancy(text, words: list[str]):
    text = text.lower()
    for word in words:
        if word.lower() in text:
            return True
    return False
#function to get all the replies to a comment
def get_replies(comment, indent = 1):
    answer = ''
    for reply in comment.replies:
        answer += f"{'  ' * indent}Reply: {reply.body} Score: {reply.score}\n"
        if len(reply.replies) > 0:
            answer += get_replies(reply, indent + 1)
    return answer
#main scraper
def reddit_scraper(product, filename, sub = "SkincareAddiction"):
    #generating relevant words from the product name
    relevant_words = [word for word in word_tokenize(product) if word not in stopwords] + ["this"]
    #temporary data before making the json
    data = []
    for submission in reddit.subreddit(sub).search(query= product, limit= 5):
        #temporary data before adding it to the aforementioned data array
        submission_data = {
            'title': submission.title,
            'ratio': submission.upvote_ratio,
            'comments': []
        }

        submission.comments.replace_more(limit= None)
        for top_level_comment in submission.comments:
            #checking if the comment is relevant or not
            if relevancy(top_level_comment.body, relevant_words) and 'bot' not in top_level_comment.body:
                comment_data = {
                    'body': top_level_comment.body,
                    'score': top_level_comment.score,
                }
                submission_data['comments'].append(comment_data)
        
        data.append(submission_data)
    #adding everything to a json file
    with open (filename, "w") as f:
        json.dump(data, f, indent = 2)


    
    

