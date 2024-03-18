from secret_key import OPENAI_API_KEY
import keyboard
import streamlit as st
import os

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)
output_parser = StrOutputParser()


def main():
    st.title('Gpt Code Request')
    input_value_code = st.text_input("Enter your code", value="", max_chars=200, key=None ,kwargs=None, placeholder="Veuillez entrez votre code", label_visibility="visible")

    # SETUP 
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a full-stack developer, you are tasked with fixing the code that is sent to you. Without adding explanatory comments. You use the code {input_value_code}"),
        ("human", "{input_value}"),
    ])
    print('template', template)
    model = ChatOpenAI(model="gpt-3.5-turbo")
    chain = template | model | output_parser
    request = False

    # VERIFICATION FOR INPUT CODE
    checker_value_empty = is_input_value_empty(input_value_code)
    checker_entry_key = True  
    if checker_value_empty:
        st.write('Is empty')
        checker_entry_key = is_entry_key_press(input_value_code)
        if checker_entry_key:
            st.write('Press entry')
    
    request = layout_code_forecast(checker_entry_key, checker_value_empty, input_value_code)
    
    if request:
        verification_response(input_value_code, checker_value_empty, checker_entry_key, chat, input_value_code )


def is_entry_key_press(input_value):
    key = keyboard.press_and_release('enter')
    return True


def is_input_value_empty(input_value):
    if len(input_value) > 0:
        return False
    else:
        return True 


def layout_correction(input_value, chat, input_value_code):
    # Utiliser chat.invoke pour obtenir la correction
    response = chat.invoke([
        HumanMessage(
            content=input_value_code
        )
    ])

    # Extraire le contenu de la réponse
    corrected_code = response.content

    return corrected_code


def layout_code_forecast(checker_entry_key, checker_value_empty, input_value_code):
    if  checker_entry_key and not checker_value_empty:
        st.code(input_value_code, language='python')
        input_value = st.text_input("What is your issue ?", value="", max_chars=200, key=None ,kwargs=None, placeholder="Que puis-je faire pour vous ?", label_visibility="visible")
        return input_value 
    return False  


def verification_response(input_value, checker_value_empty, checker_entry_key, chat, input_value_code ):
    checker_value_empty = is_input_value_empty(input_value)
    checker_entry_key = is_entry_key_press(input_value)
    if  checker_entry_key and not checker_value_empty:
        result = layout_correction(input_value, chat, input_value_code)
        st.code(result, language='python')


if __name__ == "__main__":
    main()
