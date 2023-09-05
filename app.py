import pandas as pd
import streamlit as st
from launch_analysis import *
from parsing import *




st.title("МедТекстСкан")
st.subheader("Демо версия")

uploaded_file = st.file_uploader("Выберите файл")
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)

numerical_box = st.text_area('Введите текст', key = 'numerical')
binary_box = st.text_area('Введите текст', key = 'binary')

print(numerical_box)


if st.button('Начать обработку'):
    waiting_text = 'Пожалуйста, подождите...'
    with st.spinner(waiting_text):
        question_dict_dict = parse_boxes(numerical_box, binary_box)
        fin_df = ds_processing(input_df, question_dict_dict)
        st.dataframe(fin_df)
