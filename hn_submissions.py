from operator import itemgetter

import requests

# Make an API call and store the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
# Assign result of API call to r.
r = requests.get(url)
# Print the result of calling the status_code function of r.
print(f"Status code: {r.status_code}")

# Process information about each submission.
# Convert the response object to a python list, store it in submission_ids.
submission_ids = r.json()
# Set up an empty list to store the dictionaries.
submission_dicts = []
# Loop through the first 30 submission IDs.
for submission_id in submission_ids[:30]:
    # Make a separate API call for each new submission.
    # Make a new API call for each submission by generating a URL containing
    # the current value of submission_id.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    # Print the ID and status of each request to see if it was successful.
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    # The API returns the information in json format.
    # r.json converts the json formatted information into a dictionary.
    # Store the dictionary in response_dict.
    response_dict = r.json()

    # Build a dictionary for each article.
    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
        }
    except KeyError:
        # This is a special YC post with comments disabled.
        continue
    else:
        submission_dicts.append(submission_dict)
# Sort the list of dictionaries by the number of comments.
# Pass 'comments' key to itemgetter function.
# itemgetter will pull the values associated with the comments key from
# each dictionary in the list.
# The sorted function will use the values as a basis for sorting the list.
# Reverse=True sorts the list largest to smallest.
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                            reverse=True)
# Loop through the list of submissions.
# Print each article's title, link, and number of comments.
for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")
