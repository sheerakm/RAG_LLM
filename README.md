A naive-ish RAG chatbot 

in main.py, I process the input using the llama then retrieve my previously scraped data from firebase and feed it to llama again
and in pdf_rag, I create a local vector db, and save my pdf data after splitting it, and then retrieve it after a question is being asked
based on euclidian distance of the vectors

for the model I use ollama + llama3 
