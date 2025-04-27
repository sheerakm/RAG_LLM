import json

import ollama
from get_data_from_firebase import *
MODEL = "llama3"

def check_county_or_state(question):
    system_prompt = (
        "You are an assistant that only answers with this format 'Yes, State, County'. or 'No'"
        " so I might ask questions about tax liens and about list of properties if it is about a certain location such as burbank, ca or burbank ca or anything similar"
        "then I expect you to return 'Yes, California, Los Angeles', as burbank is located in los angeles county, ca"
        "Do not add any information, if the state or county name is missing, return None in its place"
        "Does the following question mention any county or state? "
        f"Question: {question}"
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": system_prompt}]
    )
    return response['message']['content'].strip()

if __name__ == "__main__":
    user_question = input("Enter your question: ")
    result = check_county_or_state(user_question)

    attachment = []

    if result.find("No") != -1:
        print("nothing to add")
    if result.find('Yes') != -1:
        array = result.split(',')
        if array[2] != 'None':
            parcels = get_parcels_by_state_and_county(array[1].strip(), array[2].strip())
            for parcel in parcels:
                attachment.append(json.dumps(parcel))
        else:
            parcels = get_parcels_by_state(array[1].strip())
            for parcel in parcels:
                attachment.append(json.dumps(parcel))

    sentence = "\n".join(attachment)

    system_prompt = (
        'please answer the question, so I will give you all the data you need in json format, then ask you a question such as give me all the homes in glendale ca, you are supposed to answer based on the string data i give you' +user_question + attachment
    )

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": system_prompt}]
    )
    print(response['message']['content'].strip())




