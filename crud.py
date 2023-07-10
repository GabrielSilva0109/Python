import streamlit as st;

with st.form(key="include_cliente"):
    input_name = st.text_input(label="Insira seu nome")
    input_age = st.number_input(label="Insira sua Idade")
    input_occupation = st.selectbox("Selecione sua profissão", ["Desenvolvedor, Musico, Desiner, Professor"])
    input_button_submit = st.form_submit_button("Enviar")



