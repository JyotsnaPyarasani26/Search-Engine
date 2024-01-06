# Search-Engine
# Objective:
The objective of the project is to scrape publication data from the Coventry University PurePortal website, preprocess the obtained data, build a search engine, and create a web application using Flask for users to search and retrieve relevant publications based on their queries.

# Steps Involved:
# Web Scraping:

The project begins with web scraping using the requests library to access the publication pages of the Coventry University PurePortal.
The BeautifulSoup library is used to parse the HTML content and extract information such as authors, publication year, title, publication page link, and authors' profile page links.
The scraping is performed iteratively over multiple pages, and the data is stored in lists.
# Data Cleaning and Preprocessing:

The extracted data is organized into a pandas DataFrame for ease of manipulation.
Authors' names are processed to remove unwanted characters and converted to lowercase.
Authors and title columns are tokenized, removing punctuation and stopwords, and then stemming is applied.
# Building an Index:

A search index is created using a defaultdict from the collections module to map each word to the corresponding document IDs in the DataFrame.
This index is later used to quickly retrieve documents containing specific words.
# Search Functionality:

A search function is implemented to find documents containing one or more query terms. The function uses the index to retrieve matching document IDs.
A search and ranking function utilizes TF-IDF (Term Frequency-Inverse Document Frequency) to calculate the relevance of documents to the search query.
# Flask Web Application:

A Flask web application is developed to provide a user interface for searching the publications.
# The application has two main routes:
The home route ('/') renders a search page where users can input their queries.
On form submission, the search results are displayed using a ranking mechanism based on TF-IDF.
