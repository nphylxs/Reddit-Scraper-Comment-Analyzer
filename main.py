import os
from functions import reddit_scraper, analyser, reader, converter

def main():
    product = input("Product Name: ").lower().strip()
    print("Type the subreddits whose comments you want to read. \nOnce you're done, input \"Search\" to begin search. ")
    subs = []
    while True:
        name = input("Subreddit name: ").strip()
        if name.lower() == "search":
            break
        subs.append(name)

    if subs:
        for sub in subs:
            filename = f"data/{sub}_{product.replace(' ', '_')}.json"
            print(f"Searching r/{sub}")
            if not os.path.exists(filename):
                reddit_scraper(product, filename, sub)
            print("Done!")

    else:
        print("No subreddit entered. Searching the default subreddit, r/SkincareAddiction")
        filename = f"data/SkincareAddiction_{product.replace(' ', '_')}.json"
        if not os.path.exists(filename):
            reddit_scraper(product, filename)
        print("Done!")
        subs.append("SkincareAddiction")
    
    print("Starting the analyzing process!")
    for sub in subs:
        saving = f"reviews/{sub}_{product.replace(' ', '_')}.json"
        if not os.path.exists(saving):
            data = analyser(product, sub)
            converter(data, sub, product)
        reader(saving)
            
if __name__ == "__main__":
    main()
