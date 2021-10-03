import streamlit as st
from fonctions import *
import socket


st.set_page_config(page_title='Station',page_icon=":car:",  layout = 'wide', initial_sidebar_state = 'collapsed')


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def main():
	

	_, col2, _ = st.columns([1, 2, 1])
	with col2:
		st.title("Station WebApp")
		
	menu = ["Station","Shop"]
	choice = st.sidebar.selectbox("Dahboard",menu)

	if choice == "Station":
		st.text("")
		st.text("")
		show_station()

	elif choice == "Shop":

		st.subheader('Shop , *Visualization!* :sunglasses:') # Infos
		show_shop()






if __name__ == '__main__':
	main()