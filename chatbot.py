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
        rule = "You are a helpful assistant. Follow these steps to answer the user queries. Step 1 - First  to find the relevant content in this " \
               "text. Enclose all your work for this step within triple quotes (\"\"\"). Step 2 - summarize, " \
               "and then return short responses. Enclose all your work for this step within triple quotes (\"\"\"). " \
               "This text extracted from Mineral report pdf. "
        initial_message = {"role": "system", "content": rule + initial_message_text}
        self.messages.append(initial_message)
        # Make the API request for initial message

        # response = openai.Completion.create(
        #     model="gpt-3.5-turbo",
        #     messages=initial_message,
        #     max_token=100
        # )
        #
        # answer = response['choices'][0]['message']['content']
        # self.append_to_history(user_id, "Assistant", answer)
        # return answer

    def chat(self, text):
        # Prepare the message
        self.messages.append({"role": "user", "content": text})

        # Make the API request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        # Extract and return the model's answer
        answer = response['choices'][0]['message']['content']
        return answer

# chat_obj = ChatBot()
#
# # Send the initial message
# chat_obj.send_initial_message("Your initial message text here.")
#
# # Chat with the API
# response = chat_obj.chat("Your question text here.", "user-123")
# print(f'Assistant: {response}')

# cbot = ChatBot()
# cbot.send_initial_message("hi,I am William", 12)