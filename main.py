import pandas as pd
from collections import defaultdict
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the DataFrame here (example assumes CSV file)
df2 = pd.read_csv('fully cleaned.csv')

# Initialize the Flask app
app = Flask(__name__)

# Step 1: Create the index
index = defaultdict(list)


# Step 2: Iterate through the DataFrame and populate the index
for idx, row in df2.iterrows():
    doc_id = idx  # The index of the row in the DataFrame serves as the document ID
    authors = row['Authors']
    title = row['Title']
    
    # Check if authors and title are not NaN (not missing values)
    if pd.notna(authors):
        authors = authors.split()  # Split the authors into individual words
    else:
        authors = []
        
    if pd.notna(title):
        title = title.split()  # Split the title into individual words
    else:
        title = []
    
    # Update the index with each word and its corresponding document ID
    for word in authors + title:
        index[word].append(doc_id)

# Now, the 'index' dictionary contains words as keys and a list of corresponding document IDs as values.


# Function to perform a search and return the matching documents
def search(query):
    query_terms = query.lower().split()  # Preprocess the query in the same way as the documents
    matching_doc_ids = set()  # Use a set to store the matching document IDs to avoid duplicates
    
    # Iterate through each query term and find matching document IDs from the index
    for term in query_terms:
        doc_ids = index.get(term, [])  # Get the list of document IDs for the query term
        matching_doc_ids.update(doc_ids)  # Add the document IDs to the set of matching IDs
    
    # Retrieve the matching documents from the DataFrame
    matching_documents = df2.loc[list(matching_doc_ids)]
    
    return matching_documents




# Function to calculate TF-IDF scores and rank the results
def search_and_rank(query, df2):
    # Replace NaN values in 'Authors' and 'Title' columns with empty strings
    df2['Authors'] = df2['Authors'].fillna('')
    df2['Title'] = df2['Title'].fillna('')

    # Combine the 'Authors' and 'Title' columns into a single text column for TF-IDF
    df2['Text'] = df2['Authors'] + ' ' + df2['Title']

    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the TF-IDF vectorizer on the combined text
    tfidf_matrix = vectorizer.fit_transform(df2['Text'])

    # Convert the query into a TF-IDF vector
    query_vector = vectorizer.transform([query])

    # Calculate the cosine similarity between the query vector and the document vectors
    cosine_similarities = (tfidf_matrix * query_vector.T).toarray().flatten()

    # Add a new column 'Relevance' to the DataFrame with the cosine similarities
    df2['Relevance'] = cosine_similarities

    # Sort the DataFrame by the 'Relevance' column in descending order
    ranked_df = df2.sort_values(by='Relevance', ascending=False)

    # Drop the 'Text' and 'Relevance' columns to clean up the DataFrame
    ranked_df.drop(columns=['Text', 'Relevance'], inplace=True)

    return ranked_df







@app.route('/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        query = request.form['query']
        matching_results = search(query)
        ranked_results = search_and_rank(query, matching_results)
        
        # Convert the DataFrame to a list of dictionaries for custom formatting
        formatted_results = ranked_results.to_dict(orient='records')
        
        return render_template('search_results.html', results=formatted_results)
    return render_template('search_page.html')


if __name__ == '__main__':
    app.run(debug=True)
