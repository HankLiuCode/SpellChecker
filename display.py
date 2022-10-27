import streamlit as st
import spell as sp

# TODO
# drop-down list of sample words
# text field for users to type their own word

# sidebar containing a checkbox to choose to display the original word
def show_box(user_input, corrected):
    is_same = user_input == corrected
    if is_same:
        st.success(user_input + " is the correct spelling")
    else:
        st.error("Correction: " + corrected)


st.header("SpellChecker Demo")

selected = st.selectbox("Choose a word or..", ["apple", "lamon", "speling", "hapy" ])
text_input = st.text_input("type your own !")

user_input = text_input or selected
corrected = sp.correction(user_input)

show_original = st.sidebar.checkbox("Show original word", value=True)
if show_original:
    st.write("original word: " + user_input)

show_box(user_input, corrected)
