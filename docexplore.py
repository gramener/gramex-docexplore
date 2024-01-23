# This assumes you have pip installed pandas (0.1), langchain (0.1) and langchain-openai (0.0)

import argparse
import json
import numpy as np
import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain.storage.file_system import LocalFileStore

# Use OpenAI embeddings to find similarity between documents and topics
file_store = LocalFileStore(os.path.expanduser('~/.langchain-embeddings'))
base = OpenAIEmbeddings()
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(base, file_store, namespace=base.model)


def main():
    # Parse command line options
    parser = argparse.ArgumentParser(
        description='Generate docexplore data from Excel',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('path', nargs='?', default='docexplore.xlsx', help='Path to Excel file')
    parser.add_argument('--cutoff', type=float, default=0.75, help='Minimum similarity cutoff')
    parser.add_argument('--output', '-o', default='docexplore.json', help='Output file')
    args = parser.parse_args()

    # Read the docs and topics
    data = pd.read_excel(args.path, sheet_name=None)
    docs = data['docs']['para']
    topics = data['topics']['topic'] + ': ' + data['topics']['subtopic']
    result = {
        'docs': data['docs'].to_dict(orient='records'),
        'topics': data['topics'].to_dict(orient='records'),
    }

    # Compute similarity
    doc_embed = np.array(cached_embeddings.embed_documents(docs))
    topic_embed = np.array(cached_embeddings.embed_documents(topics))
    similarity = np.dot(doc_embed, topic_embed.T)

    result['matches'] = matches = []
    for row in range(len(similarity)):
        for col in range(len(similarity[row])):
            if similarity[row][col] >= args.cutoff:
                matches.append({'doc': row, 'topic': col, 'similarity': similarity[row][col]})

    with open(args.output, 'w') as f:
        f.write(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
