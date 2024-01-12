import streamlit as st
import pandas as pd
import numpy as np


st.title ("Test Streamlit and Pandas :smile:")

# @st.cache_data
# def rand_data():
# 	df =pd.DataFrame (
# 		{
# 			"apples" :np.random.randint(10, 50, size=8),
# 			"bears" :np.random.randint(100, 500, size=8),
# 			"bananas" :np.random.randint(10, 50, size=8),
# 		})
# 	return df

# table_data = rand_data()

# hundle_rate= st.text_input ("enter hundle rate")

# if hundle_rate:
# 	new_rate =int(hundle_rate)*3
# 	st.write (new_rate)


with st.form ("Fund Terms") :
	st.header ("Please enter fund terms")

	a, b, c = st.columns ([1,1,1])

	with a:
		# preffered = st.slider ("preffered return in %:", 0, 20)
		preffered = st.selectbox ("preffered return in %:", [0,5,8,9,10])

	with b:
		carry = st.selectbox ("carried interest in %:", [0,5,10,15,20])

	with c:
		catch_up = st.selectbox ("catch up in %:", [0,100])

	invested = st.text_input("invested amount $")
	total_re = st.text_input("total cash return amount $")

	submitted = st.form_submit_button("calculate !")

if submitted:
	gain = int(total_re) - int(invested)
	lp_1 = int(invested) * preffered /100  # prefferred return
	
	#  0% catch_up
	if catch_up ==0 :
		gp_share = (gain - lp_1) *carry/100  # GP carry
		lp_2 = (gain - lp_1)*(100-carry)/100

	if catch_up == 100:
		gp_catch = lp_1 * carry /100
		gp_share = (gain - lp_1- gp_catch ) *carry/100  + gp_catch# GP carry
		lp_2 = (gain - lp_1- gp_catch)*(100-carry)/100


	st.write ("LP share:", lp_1+lp_2+ int(invested))
	st.write ("GP share:", gp_share)

# st.experimental_data_editor(table_data)
# st.line_chart(table_data)
# st.bar_chart(table_data)