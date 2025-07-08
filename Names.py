### Import Section
from google_drive import update_file, download_file
import streamlit as st
import pandas as pd
import numpy as np
import time


### Variables Section
relations = [":rainbow[***جدو نادي***]",
			 ":rainbow[***جدو أشرف***]",
			 ":rainbow[***تيتا نبيلة***]",
             ":rainbow[***تيتا بثينة***]", 
			 "***عمو***:sunglasses:", 
			 "***عمتو***:heart:", 
			 "***خالو***:movie_camera:"]


### Functions Section

@st.cache_data(show_spinner=False, max_entries=1000)
def df_names():
	names = ["فاطمة", "زينب", "رقية", "عائشة", "خديجة", "اسيا", "اروي", "اميرة", "تسنيم", "علا", "سندس", "سمر", "ندي", "نوران", "حنان", "جيهان", "هبة",
         "يارا", "علا", "فرح", "فريدة", "داليا", "دلال", "رزان", "رغد", "رنا", "ريم", "رفيدة", "روميساء", "ريماس", "ريحانة", "رحمة"]
		
	# Convert names list into pandas dataframe
	names = {"names": names}
	names = pd.DataFrame(names, index=range(1,33))
	
	return names

def segment_control():	
	if st.session_state.choice == ":rainbow[***جدو نادي***]":
		st.session_state.selected_choice = "جدو نادي"
		message = "***يارب يبقي يومك حلو يا جدو نادي***"
		st.session_state.container1.header(message)
	elif st.session_state.choice == ":rainbow[***جدو أشرف***]":
		st.session_state.selected_choice = "جدو أِشرف"
		message = "***يارب يبقي يومك حلو يا جدو أشرف***"
		st.session_state.container1.header(message)
	elif st.session_state.choice == ":rainbow[***تيتا نبيلة***]":
		st.session_state.selected_choice = "تيتا نبيلة"
		st.session_state.male_female = False
		message = "***يا مرحب بيكي يا تيتا نبيلة***"
		st.session_state.container1.header(message)
	## تيتا
	elif st.session_state.choice == ":rainbow[***تيتا بثينة***]":
		st.session_state.selected_choice = "تيتا بثينة"
		st.session_state.male_female = False
		message = "***يا مرحب بيكي يا تيتا بثينة***"
		st.session_state.container1.header(message)
	## عمو
	elif st.session_state.choice == "***عمو***:sunglasses:":
		st.session_state.selected_choice = "عمو"
		message = "***مسا مسا يا عمو***"
		st.session_state.container1.header(message)
	## عمتو
	elif st.session_state.choice == "***عمتو***:heart:":
		st.session_state.selected_choice = "عمتو"
		st.session_state.male_female = False
		message = "***ازيك يا ام حمزة***"
		st.session_state.container1.header(message)
	elif st.session_state.choice == "***خالو***:movie_camera:":
		st.session_state.selected_choice = "خالو"
		message = "***اهلا اهلا يا ابو نسب***"
		st.session_state.container1.header(message)
	

	if st.session_state.selected_choice in st.session_state.names_dict:
		if st.session_state.selected_choice != "عمو":
			st.session_state.end = True
			message = "انت اختارت قبل كدا مينفعش تختار تاني"
			st.session_state.container1.write(message)
		elif len(st.session_state.names_dict["عمو"]) >= 6:
			st.session_state.end = True
			message = "انت اختارت قبل كدا مينفعش تختار تاني"
			st.session_state.container1.write(message)
	else:
		st.session_state.before_end = False
		if st.session_state.male_female:
			st.session_state.container1.subheader("هتساعدنا نختار اسم النونا ؟")
		else:
			st.session_state.container1.subheader("هتساعدينا نختار اسم النونا ؟")			

def button_click():
	time.sleep(1)
	st.session_state.container2.write(":red[***دول كانوا بابا وماما وجيه دوري انا دلوقتي***]")
	st.session_state.before_end = True
	st.session_state.end = False

@st.dialog("اختار اسم")
def choose_name(baby_names):
	if st.session_state.male_female:	## male
		message = "***اختار اسم ليا من القايمة أو ضيف انت الاسم الي عايزه***"
	else:								## female
		message = "***اختاري اسم ليا من القايمة أو ضيفي انتي الاسم الي عايزاه***"
	
	with st.form("Choose name"):
		st.multiselect(message,
					   baby_names,
					   placeholder="select name",
					   max_selections=3,
					   key="name",
					   accept_new_options=True)
		submit = st.form_submit_button("دوس هنا لما تخلص")
	
	if submit:
		names = st.session_state.name
		st.session_state.names_dict[st.session_state.selected_choice] = names
		st.session_state.end = True
		st.rerun()


def main():
	if "end" in st.session_state and st.session_state.end:
		return
	
	## Download the excel sheet for stored names from google drive and save it into internal session state variable 
	st.session_state.names_dict = download_file("Names.xlsx", "1Pp-KTLoN9gJEO1v-ubT9iPS0dl_chU4f").to_dict("list")
	
	if "session_text" not in st.session_state:
		st.session_state.session_text = list()
	
	if ["container1", "container2"] not in st.session_state:
		st.session_state.container1 = st.empty().container()
		st.session_state.container2 = st.empty().container()
		
	st.session_state.visibility = "collapsed"
	st.session_state.disabled = True
	st.session_state.male_female = True
	
	## Sidebar containers
	st.session_state.sidebar1 = st.sidebar.empty()
	st.session_state.sidebar2 = st.sidebar.empty()
	st.session_state.sidebar3 = st.sidebar.empty()
	st.session_state.sidebar4 = st.sidebar.empty()
	
	# Welcome Message
	st.session_state.sidebar1.header("""
					***اهلا بيكم:heart:***
					***اقرأوا كويس التعليمات دي***
					""")

	# Instructions
	st.session_state.sidebar2.write("""
					***هتختاروا الأول نسبكم للنونا***
					***كل واحد يختار لحد 3 اسامي ولو حابين تضيفوا اسم في الاخر ضيفوا***
				   """)
	st.session_state.sidebar3.divider()
	
	# Generate radio button for selecting relations
	st.session_state.sidebar4.segmented_control("***تقرب ايه للنونا ؟***", relations, key="choice", on_change=segment_control)

	time.sleep(2)
	
	# baby names
	baby_names = df_names()
	
	# Button Stage
	if "before_end" in st.session_state and not st.session_state.before_end:
		st.session_state.container2.button("ايوا هساعدكم", key="flag", on_click=button_click)
	
	# Choice Stage
	if ("end" in st.session_state) and (st.session_state.before_end) and (not st.session_state.end):
		choose_name(baby_names)


if __name__ == "__main__":
	### Call Main Function
	main()
	
	### End of Application
	if "end" in st.session_state and st.session_state.end:
		## Delete or empty the text in the sidebar
		st.session_state.sidebar1.empty()
		st.session_state.sidebar2.empty()
		st.session_state.sidebar3.empty()
		st.session_state.sidebar4.empty()
		
		## Delete all printed text
		st.session_state.container1.empty()
		st.session_state.container2.empty()
		
		st.success("شكرا علي المساعدة")
		st.balloons()
		
		## convert the internal sessions state dictionary into pandas dataframe
		names_df = pd.DataFrame(st.session_state.names_dict)

		## Save the names dataframe into excel sheet for names
		names_df.to_excel("Names.xlsx", index=False)

		## Update the names sheet in google drive
		update_file("Names.xlsx", "1Pp-KTLoN9gJEO1v-ubT9iPS0dl_chU4f", "Names.xlsx")
	