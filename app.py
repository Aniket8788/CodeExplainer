#@title Insert PaLM API Key here

import google.generativeai as palm
import os
palm.configure(api_key='AIzaSyBo7zMVdOMLwisTQ8zD7nlJ5SSjX55yPbA')



# Use the palm.list_models function to find available models
# PaLM 2 available in 4 sizes: Gecko, Otter, Bison and Unicorn (largest)
# https://developers.generativeai.google/models/language

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

# Set your input text
prompt = "Why is the sky blue?"
# prompt = "What is Quantum Computing? Explain like I'm 5."

completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0,
    # temperature=0 >> more deterministic results // temperature=1 >> more randomness
    max_output_tokens=100
    # maximum length of response
)

print(completion.result)


def get_completion(prompt):
  completion = palm.generate_text(
      model=model,
      prompt=prompt,
      temperature=0,
      # The maximum length of the response
      max_output_tokens=500,
      )
  response = completion.result
  return response


# input_code = f"""
# x = [1, 2, 3, 4, 5]
# y = [i**2 for i in x if i%2 == 0]
# print(y)
# """

input_code = f"""
def my_func(x):
    if x > 5:
        return "High"
    else:
        return "Low"
result = my_func(4) + my_func(6) + my_func(4)
print(result)
"""


prompt =f"""
Your task is to act as a Python Code Explainer.
I'll give you a Code Snippet.
Your job is to explain the Code Snippet step-by-step.
Also, compute the final output of the code.
Code Snippet is shared below, delimited with triple backticks:
```
{input_code}
```
"""

print(prompt)

print(get_completion(prompt))

python_code_examples = f"""
---------------------
Example 1: Code Snippet
x = 10
def foo():
    global x
    x = 5
foo()
print(x)

Correct answer: 5
Explanation: Inside the foo function, the global keyword is used to modify the global variable x to be 5.
So, print(x) outside the function prints the modified value, which is 5.
---------------------
Example 2: Code Snippet
def modify_list(input_list):
    input_list.append(4)
    input_list = [1, 2, 3]
my_list = [0]
modify_list(my_list)
print(my_list)

Correct answer: [0, 4]
Explanation: Inside the modify_list function, an element 4 is appended to input_list.
Then, input_list is reassigned to a new list [1, 2, 3], but this change doesn't affect the original list.
So, print(my_list) outputs [0, 4].
---------------------
"""

# language = "Python"

input_code = f"""
def my_func(x):
    if x > 5:
        return "High"
    else:
        return "Low"
result = my_func(4) + my_func(6) + my_func(4)
print(result)
"""

# input_code = f"""
# def func(x):
#     if x > 0:
#         return x + func(x-1)
#     return 0

# result = func(5)
# print(result)
# """



prompt = f"""
Your task is to act as a Python Code Explainer.
I'll give you a Code Snippet.
Your job is to explain the Code Snippet step-by-step.
Break down the code into as many steps as possible.
Share intermediate checkpoints along with results.
State your Steps and Checkpoints in your output.
Few good examples of Python code output between #### separator:
####
{python_code_examples}
####
Code Snippet is shared below, delimited with triple backticks:
```
{input_code}
```
"""

print(prompt)

print(get_completion(prompt))

import streamlit as st
import google.generativeai as palm
import logging
import time


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure the PaLM API Key
palm.configure(api_key='AIzaSyBo7zMVdOMLwisTQ8zD7nlJ5SSjX55yPbA')

# Ensure you specify the model name correctly (you may need to adjust this)
model = 'models/text-bison-001'  # Example model name; replace with the actual model name if different

def get_completion(code_snippet):
    python_code_examples = """
    ---------------------
    Example 1: Code Snippet
    x = 10
    def foo():
        global x
        x = 5
    foo()
    print(x)
    Correct output: 5
    Code Explanation: Inside the foo function, the global keyword is used to modify the global variable x to be 5.
    So, print(x) outside the function prints the modified value, which is 5.
    ---------------------
    Example 2: Code Snippet
    def modify_list(input_list):
        input_list.append(4)
        input_list = [1, 2, 3]
    my_list = [0]
    modify_list(my_list)
    print(my_list)
    Correct output: [0, 4]
    Code Explanation: Inside the modify_list function, an element 4 is appended to input_list.
    Then, input_list is reassigned to a new list [1, 2, 3], but this change doesn't affect the original list.
    So, print(my_list) outputs [0, 4].
    ---------------------
    """

    prompt = f"""
    Your task is to act as a Python Code Explainer.
    I'll give you a Code Snippet.
    Your job is to explain the Code Snippet step-by-step.
    Break down the code into as many steps as possible.
    Share intermediate checkpoints & steps along with results.
    Few good examples of Python code output between #### separator:
    ####
    {python_code_examples}
    ####
    Code Snippet is shared below, delimited with triple backticks:
    ```
    {code_snippet}
    ```
    """

    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            logging.debug(f"Sending request to PaLM API with prompt: {prompt}")
            completion = palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0,
                max_output_tokens=500
            )
            response = completion.result
            logging.debug(f"Received response from PaLM API: {response}")
            return response
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying... ({attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                logging.error("Max retries reached. Returning error.")
                return str(e)

# Streamlit UI
st.title("Python Code Explainer...")

code_snippet = st.text_area("Insert Code Snippet", height=300)

if st.button("Submit"):
  st.balloons()
  
  explanation = get_completion(code_snippet)
  st.text_area("Explanation Here", explanation, height=500)
