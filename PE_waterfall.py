import streamlit as st
import plotly.graph_objects as go

class Term :
	def __init__ (self, preferred, carry, catch_up, fee):
		self.preferred = preferred
		self.carry	= carry
		self.catch_up = catch_up
		self.fee = fee

# this function return a dictionary. Heads: proceeds, GP, LP
# fee is outside the cost, commitment size is equal to cost.
def waterFall (Term, cost, proceeds, duration):
	
	fee 		= (Term.fee/100) * cost  # in dollar
	catch_up 	= Term.catch_up/100  # in %
	carry 		= Term.carry/100
	preferred 	= Term.preferred/100

	LpGpRatio = (1-carry)/carry
	gain = proceeds - cost

	lp_share = 0   # $0 at the beginning. 
	gp_share = fee * duration
	lp_pref =0

	if proceeds <= cost:   #  if proceeds <= (cost + fee)  option_2:  LP recover fee as well. 
		lp_share = proceeds 
	else :
		lp_share = cost 
		lp_pref = cost * (1+preferred)**duration - cost  

		if gain <=lp_pref :
			lp_share = proceeds
		else :
			lp_share += lp_pref
			if catch_up ==0 : #  0% catch_up
				gp_carry = (gain - lp_pref) *carry  # GP carry
				lp_carry = (gain - lp_pref)*(1-carry)
				lp_share +=lp_carry
				gp_share +=gp_carry
			else:
				dis_catchup = lp_pref/(LpGpRatio*catch_up+catch_up-1)
				print ('\ndis_catchup', dis_catchup)
				if dis_catchup <= (gain- lp_pref) :
					gp_catch = dis_catchup * catch_up
					lp_catch = dis_catchup *(1-catch_up)
					lp_share +=lp_catch
					gp_share +=gp_catch
					gp_carry = (gain - lp_pref -dis_catchup) *carry  # GP carry
					lp_carry = (gain - lp_pref -dis_catchup)*(1-carry)
					lp_share +=lp_carry
					gp_share +=gp_carry
					print ('enough catchup, lp, gp', lp_catch, gp_catch )
				else :
					gp_catch = (gain- lp_pref) * catch_up
					lp_catch = (gain- lp_pref) *(1-catch_up)
					lp_share +=lp_catch
					gp_share +=gp_catch
					print ('not enough catch up, lp, gp', lp_catch, gp_catch )

	# return gain, catch_up, carry, preferred, LpGpRatio, lp_share, gp_share
	return gain, lp_pref, lp_share, gp_share

st.subheader ("PE Distribution Water Fall :wave:")

with st.form ("Fund Terms") :
	st.subheader ("Please enter fund terms. Assume all LP capital invested in day one.")

	a, b, c = st.columns ([1,1,1])
	with a:
		preferred = st.selectbox ("Preferred return %:", [0,5,8,10,15], index= 3)
		invested = st.text_input("LP invested $", 1000)
	with b:
		carry = st.selectbox ("Carried interest %:", [0,5,10,15,20,30,50], index = 3)
		total_re = st.text_input("Expected total cash return $", 1500)
	with c:
		catch_up = st.selectbox ("GP catch up %:", [0,50,80,100], index = 1)
		management_fee = st.selectbox ("management fee %:", [0,1,2,3,5])

	duration = st.slider ("How many years:", 1,10)
	submitted = st.form_submit_button("Calculate !")

if submitted:
	lp_cost = int(invested)
	total_return = int(total_re)

	fund_term = Term(preferred, carry, catch_up, management_fee)
	profit, preferred, lp_share, gp_share = waterFall(fund_term, lp_cost, total_return, duration)

	# st.write ("Investment Gain ($):", round (profit))
	# st.write ("Preferred ($):", round (preferred,1))
	# st.write ("LP share ($):", round (lp_share,1))
	# st.write ("GP share ($):", round (gp_share,1))

	wString_1 = f"<h4>Investment Gain: ${profit: .2f} &nbsp;&nbsp;&nbsp; Preferred Return: ${preferred:.2f}</h4>"
	wString_2 = f"<h4>LP Portion: ${lp_share: .2f} &nbsp;&nbsp;&nbsp; GP Portion: ${gp_share:.2f}</h4>"
	st.markdown (wString_1, unsafe_allow_html=True)
	st.markdown (wString_2, unsafe_allow_html=True)

	total_return_list =[]
	lp_list =[]
	gp_list =[]

	step= (total_return-lp_cost)/20

	lp_fig, gp_fig = 0 , 0
	for i in range (int(lp_cost*0.3),   int(total_return*1.5), int(step)):
		aaa, bbb, lp_fig, gp_fig = waterFall(fund_term, lp_cost, i, duration)
		# st.write (i, lp_fig, gp_fig)
		total_return_list.append (i)
		lp_gain = lp_fig - lp_cost
		lp_list.append(lp_gain)
		gp_list.append (gp_fig)

	fig_3 = go.Figure()
	fig_3.add_trace (go.Scatter (x=total_return_list, y=lp_list, mode='lines', name = "LP Portion"))
	fig_3.add_trace (go.Scatter (x=total_return_list, y=gp_list, mode='lines', name = "GP Portion"))
	st.plotly_chart(fig_3)


