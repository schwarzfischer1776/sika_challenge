import pandas as pd
import panel as pn

import pickle

import openai 
import json 



openai.api_key = "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"

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




initial_value = [
{"You": "first journal entry"},
{"Theo":  """Trying new fabrication method, namely to try new high-resolution mask for fabrication of photonic chip. 
        First attempt of using SU8 as a high-resolution mask. Made one initial attempt for developing SU8 using the following parameters: 
        Spin-Coating SU8 Soft Bake (3 min. at 60 degrees)
        Photolithography Exposure (lambda = 450 nm, P = 15 muW, t = 2 min.)
        Development (3 min. in SU8 developer)
        Looking at Chip under the microscope;
        This attempt Failed; The development step dissolved all the SU8 for an unknown reason"""},
{"Theo": """As yesterday's attempt of using SU8 as a high-resolution mask. Made further attempts for developing SU8 
        using the same steps as yesterday with various different parameters, all failed. The development step still dissolved all the SU8 for an unknown reason"""},
{"Theo":  """Third attempt of using SU8 as a high-resolution mask. Realized that I skipped a step (the post-exposure step) that was flagged as optional in the SU8 manual. Introducing the step turned out to make the process work. The steps I followed for my working version:
        1. Spin-Coating SU8
        Soft Bake (3 min. at 60 degrees)
        Photolithography Exposure (lambda = 450 nm, P = 15 muW, t = 2 min.)
        Post-Exposure Bake (4 min.)
        Development (3 min. in SU8 developer)
        Looking at the chip under the microscope. This time I saw the SU8 on the chip after the development! --> method worked
        """},
{"Felix": """tries to built a quantum repeater; for that one necessary step is to design a good on chip cavity; 
 for testing his design he wants to characterise the chip on the RT setup."""},
{"Felix": """trying to couple to the chip. Coupling not possible for unknown reason. Data jumps around weirdly. Tried methods that did not lead to sucess:
    - checking laser frequency
    - changing chip we know couples
    - checking pigtail connections
    - checking that laser exites through fiber with visible laser
    - turning off ventilation system to reduce noise"""},
{"Felix": """still no idea why not working; Finally he figures out what the problem is:
    - detection diode not calibrated correctly"""},
{"You": """first attempt of coating tapered fiber with SU8 by using different experimental parameters; 
 nothing seen under microscope meaning either development step dissolved everything or the SU8 did not stick to fiber"""}
]
# Deserialize the list from the binary file (unpickling)
#with open('my_list.pkl', 'rb') as file:
    #initial_value = pickle.load(file)
    #a = "test"

chat_box = pn.widgets.ChatBox(
    value=initial_value,
    message_icons={
        "You": "https://user-images.githubusercontent.com/42288570/246667322-33a2a320-9ea3-4e79-8fb8-fcb5b6eac9c0.png",
        "Theo": "https://user-images.githubusercontent.com/42288570/246671017-d3a26763-f7f5-4e8d-8933-cb69670f90a8.svg",
        "Felix": "https://user-images.githubusercontent.com/42288570/246667325-ad4e3434-d173-4463-bb98-5c5d4a892b25.png",
        "GPT4": "https://user-images.githubusercontent.com/42288570/246667324-5cf26789-765f-4f76-a8bf-49309d2ae84f.png",
    },
    show_names=True,
)


print("got here")

def update_safe(event):
    #with open('my_list.pkl', 'wb') as file:
        #pickle.dump(chat_box.value, file)

    formatted_messages = []
    formatted_messages.append({"role": "system", "content": """You are supposed to help
                           with the knowledge management system
                           of a research group. You are given the journal entries of different users (given by the name after the string "from user" taken over time while working on different projects. 
            It may be the case, that the newest problem the user faces (the last message) can be solved by some old entries or at least old entries can
                           help the user to find the problem better. 
                           Please give the message numbers of the messages that you think are relevant for the newest problem the user faces and give a summary
                           of what the user could do to solve the problem. 
                           Ignore the last consecutive messages from the same user as he still knows what is problem is.
                           If no message is relevant, write "no message is relevant".
                           I there are relevant messages, return it in the following format:
                            {
                           Relevant messages: [message number 1, message number 2, ...]
                            Summary: {summary}}
                           The summary should be somthing in the direction of:
                           Hey _insert_user_name, other people might have had the same problem before. Based on the questions _insert_massage_numbers 
                           you could consider trying....
                           Try clustering the messages into different problem solving approaches, if there are several, but please only if.
                           """})
    
    # Transform the message list into the desired format
    msg_nr = 0
    for msg in chat_box.value:
        msg_nr += 1
        for role, content in msg.items():
            formatted_messages.append({"role": "user", "content": "Mesage Nr.: " + str(msg_nr) + " from user " + role + ": " + content})


    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=formatted_messages
    )

    reply = completion.choices[0].message

    a = False
    count = 0
    numbers = []
    while not a:
        try:
            completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=formatted_messages
            )

            reply = completion.choices[0].message["content"]
            start = reply.index("[")
            end = reply.index("]")
            numbers = [int(i) for i in reply[start+1:end].split(",")]
            chat_box.value.append({"GPT4": reply})
            a = True
        except Exception as E:
            print(E)
            count += 1
            a = False
            if count >+ 5:
                a = True
                print("failed")
                exit()

        styled_panes = []
        msg_nr = 0
        pane_style = {
            'background-color': 'white',
            'border-radius': '10px',  # Rounded corners
            'box-shadow': '2px 2px 5px 2px rgba(0, 0, 0, 0.2)',  # Shadow
            'padding': '10px',  # Padding
            'margin': '10px'  # Margin between panes
        }

            
        for msg in chat_box.value:
            msg_nr += 1
            if msg_nr in numbers:
                for role, content in msg.items():
                    print(role, content)
                    content = f'User: {role}, Message: {content}'
                    styled_pane = pn.pane.Str(content, style=pane_style)
                    chat_box.append({"Machine 3": "How do you do fellow machines?"})
                    styled_panes.append(styled_pane)


        # Create a Panel column to display the styled panes
        styled_column = pn.Column(*styled_panes)

        # Display the Panel column
        styled_column.servable()
    
print("got here2 ")
chat_box.param.watch(update_safe, 'value')

print("got here3")
chat_box.servable()