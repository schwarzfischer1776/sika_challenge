import openai 
import json 



openai.api_key = #"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"


# imports
import pandas as pd
import tiktoken
import matplotlib.pyplot as plt 
import numpy as np 


from openai.embeddings_utils import get_embedding

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# load & inspect dataset
df = pd.DataFrame()

df["text_field"] = ["apple", "oranges", "banana", "pineapple", "car", "mercedes", "tree", "carbondioxide"]

encoding = tiktoken.get_encoding(embedding_encoding)

df["embedding"] = df.text_field.apply(lambda x: get_embedding(x, engine=embedding_model))
df.to_csv("text_field.csv")

df = pd.read_csv("text_field.csv")

for i,j in enumerate(df["embedding"]):
    df["embedding"][i] = json.loads(j) 

for i in df["embedding"]:
    print(type(i))

similarity_matrix = [ [np.dot(np.array(i),np.array(j))  for i in df["embedding"] ] for j in df["embedding"] ]

plt.imshow(similarity_matrix, cmap='hot', interpolation='nearest')
plt.show()

