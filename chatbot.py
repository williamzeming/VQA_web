import re

import openai
import json


# openai.api_key = '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'

class ChatBot:
    def __init__(self):
        self.chat_history = {}
        self.messages = []
        openai.api_key = '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'

    def send_initial_message(self, initial_message_text):
        self.messages = []
        # rule = "You are a helpful assistant. Follow these steps to answer the user queries. Step 1 - First to find the relevant content in this \
        #        text. Enclose all your work for this step within triple quotes (\"\"\"). \
        #        Must locate the Page Number and section everytime, Please answer the following question in the format reply+' Sources: [Page number: page_no, Section: sectionName]', hash key mark and Sources is necessary,Write the Sources exactly as they are formatted and add them to the end. \
        #        This text extracted from Mineral report pdf. "

        rule = "You are a helpful assistant. Follow these steps to answer the user queries. Step 1 - First to find the relevant content in this \
                       text. Enclose all your work for this step within triple quotes (\"\"\"). \
                       This text extracted from Mineral report pdf. "

        initial_message = {"role": "system", "content": rule + initial_message_text}
        self.messages.append(initial_message)

    def chat(self, text):
        # Prepare the message
        self.messages.append({"role": "user", "content": text})

        # Make the API request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.8
        )

        # Extract and return the model's answer
        text = response['choices'][0]['message']['content']
        # try:
        #     pattern = re.compile(r'Sources: (\[.*?\])')
        #     # Extracting "Sources:" content
        #     source_content = re.findall(pattern, text)[0]
        #     # Getting content outside the "Sources:" pattern
        #     remaining_content = re.split(pattern, text)[0].strip()
        #     result = remaining_content + "##Sources: " + source_content
        # except Exception as e:
        #     print(text)
        #     return text
        return text

