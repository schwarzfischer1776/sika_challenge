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


message = [
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
for msg in message:
    msg_nr += 1
    for role, content in msg.items():
        formatted_messages.append({"role": "user", "content": "Mesage Nr.: " + str(msg_nr) + " from user " + role + ": " + content})


completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=formatted_messages
)

print(completion.choices[0].message)

