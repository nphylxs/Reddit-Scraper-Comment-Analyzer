The program goes through the specified communities and looks for reviews of the product you enter. Then it filters through the comments and send it to Groq for analysis.

After analysis, the data is printed on the screen in form of a dictionary. Both the scraped data and the analysis are saved as JSON files in /data and /reviews respectfully.

Can be used to automate the process of scouring reddit and reading reviews. We can obtain the following information using this program:
* the positive aspects
* the negative aspects
* when the product is best to use
* when the product should be avoided
* ratio of positive to negative comments (must be as high as possible)

## Required libraries:
1. nltk
2. Groq
3. dotenv
4. os
5. praw
6. json

## Usage:
Run the main.py file. 

It will ask for the name of product first, please enter a valid name. 

Then it will ask for the subreddits. Enter them one at a time. Once you're done, input "search" as the subreddit name. 

It checks /data folder for the data in case the program has already searched for the particular product in that specific subreddit. If no, then it goes to reddit. 

Then, to analyze, it checks if the analysis has already been done by looking at the /reviews file. If no, it sends the data to Groq. 

Finally, Groq's output is given out to the terminal. 

