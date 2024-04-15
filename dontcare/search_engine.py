from typing import Dict, List
from collections import defaultdict
import os

def process_text(text):
    # Process text: convert to lowercase, remove spaces and special characters
    processed_text = ''.join(char.lower() for char in text if char.isalnum() or char.isspace())
    words = processed_text.split()
    unigrams = words
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
    return unigrams, bigrams

def     add_to_index(corpus_index_map: Dict[str, List[int]], terms: List[str], document_id: int) -> None:
    # Add both unigrams and bigrams to the index map
    for term in terms:
        corpus_index_map[term].append(document_id)

def read_and_process_files(folder_path):
    # Initialize the corpus index map with default to list for automatic list creation
    corpus_index_map = defaultdict(list)

    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it is a file
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    unigrams, bigrams = process_text(content)

                    # Save information to the dictionary
                    add_to_index(corpus_index_map, unigrams + bigrams, filename)
            except Exception as e:
                print(f"Error reading file '{filename}': {e}")

    return corpus_index_map

def query_single_term_or_bigram(corpus_index_map: Dict[str, List[int]], query: str) -> List[int]:
    # Return the list of document IDs for the queried term or bigram.
    return corpus_index_map.get(query.strip(), [])

def query_with_and_not(corpus_index_map: Dict[str, List[int]], term1: str, term2: str) -> List[int]:
    # Find document IDs for term1 and exclude those that also appear for term2.
    return [doc_id for doc_id in corpus_index_map.get(term1.strip(), []) if doc_id not in corpus_index_map.get(term2.strip(), [])]

def query_with_or_not(corpus_index_map: Dict[str, List[int]], term1: str, term2: str) -> List[int]:
    # Find document IDs for term1 and for any term not equal to term2.
    result = set(corpus_index_map.get(term1.strip(), []))
    for term, doc_ids in corpus_index_map.items():
        if term != term2.strip():
            result.update(doc_ids)
    return list(result)

def query_with_and(corpus_index_map: Dict[str, List[int]], term1: str, term2: str) -> List[int]:
    # Find the intersection of document IDs for both terms.
    return list(set(corpus_index_map.get(term1.strip(), [])) & set(corpus_index_map.get(term2.strip(), [])))

def query_with_or(corpus_index_map: Dict[str, List[int]], term1: str, term2: str) -> List[int]:
    # Find the union of document IDs for both terms.
    return list(set(corpus_index_map.get(term1.strip(), [])).union(set(corpus_index_map.get(term2.strip(), []))))

def main():
    # Change the path to the folder containing your files
    folder_path = 'C:/Users/Admin/Downloads/reuters_test/reuters/test'
    corpus_index_map = read_and_process_files(folder_path)

    # Example queries and their results
    queries = [
        "tom",
        "tom AND jerry",
        "tom OR jerry",
        "tom AND NOT jerry",
        "tom OR NOT jerry",
        "its proposed AND NOT acquisition of"
    ]

    for query in queries:
        query_result = []
        if "AND NOT" in query:
            query_result = query_with_and_not(corpus_index_map, *query.split(" AND NOT "))
        elif "OR NOT" in query:
            query_result = query_with_or_not(corpus_index_map, *query.split(" OR NOT "))
        elif "AND" in query:
            query_result = query_with_and(corpus_index_map, *query.split(" AND "))
        elif "OR" in query:
            query_result = query_with_or(corpus_index_map, *query.split(" OR "))
        else:
            query_result = query_single_term_or_bigram(corpus_index_map, query)

        # Sort the query_result before printing
        sorted_result = sorted(query_result)
        print(f"Query: '{query}' - Search Result: {sorted_result}")

if __name__ == "__main__":
    main()
