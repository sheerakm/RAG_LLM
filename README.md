A modular RAG chatbot from my tax lien app, where you can ask questions on the educational material 
and hopefully on the data


in main.py, I process the input using the llama then retrieve my previously scraped data from firebase and feed it to llama again
and in pdf_rag, I create a local vector db, and save my pdf data after splitting it, and then retrieve it after a question is being asked
based on euclidian distance of the vectors

for the model I use ollama + llama3 


PLAN!
manually adding tags to pages of our tutorials + using the title of each page 
get summaries for each document from llama (need to create chunks as there is a limit to context window, feed to llama and then add periovus summary for ocntext + new chunk)
and then use these + documents for embedding (can I do a metadata search like I do for firebase?!)
then get the most relevant embedding + prompt to respond 
at the end I shall add duckduckgo search to get the first 5 results scrape probably with selenium and also feed to llm (after summarizing everything with another smaller model) basically in the post retrival step



