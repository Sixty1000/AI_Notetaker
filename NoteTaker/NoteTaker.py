import os
from google.cloud import vision

from openai import OpenAI
client_gpt = OpenAI(api_key="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")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'quiet-spirit-442216-f2-9231c515826d.json'

input_file = file = open("text_input.txt", encoding="utf8")

def detect_text(path):
    client = vision.ImageAnnotatorClient()
    with open(path, "rb") as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    #texts[0] includes all text seen in image
    #texts[1-n] include all finer grained elements
    texts = response.text_annotations
    
    if response.error.message:
        raise Exception(
            "Error"
        )
    
    return texts[0].description

image_path = "test_run.JPG"
input_txt = detect_text(image_path)


def query_input(text_input):
    chat_completion = client_gpt.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system", 
            "content":"Summarize the prompt given in 5 sentences."
            },
            {"role":"user",
            "content": text_input
            }
        ]
    )

    print(chat_completion.choices[0].message.content)

query_input(input_txt)
