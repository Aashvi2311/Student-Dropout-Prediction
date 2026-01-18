import streamlit as st
import requests

st.title("Student Dropout Prediction Dashboard")
st.header("Predict dropout risk using LightGBM and FastAPI")

admission_grade = st.number_input("Enter admission grade")
prev_qual_grade = st.number_input("Enter previous qualification grade")
curr_units_1_grade = st.number_input("Enter grade average in 1st sem")
curr_units_2_grade = st.number_input("Enter grade average in 2nd sem")
course_map = {
    "Biofuel Production Technologies": 33,
    "Animation and Multimedia Design": 171, 
    "Social Service (evening attendance)": 8014,
    "Agronomy": 9003,
    "Communication Design": 9070,
    "Veterinary Nursing": 9085,
    "Informatics Engineering": 9119,
    "Equinculture": 9130,
    "Management": 9147,
    "Social Service": 9238,
    "Tourism": 9254,
    "Nursing": 9500,
    "Oral Hygiene": 9556,
    "Advertising and Marketing Management": 9670,
    "Journalism and Communication": 9773,
    "Basic Education": 9853,
    "Management (evening attendance)": 9991
}
choice= st.selectbox("Select course",list(course_map.keys()))
course_value = course_map[choice]
age = st.slider("Choose age at enrollment")

curr_units_approved_1 = st.slider("Number of curricular units apporved in 1st sem")
curr_units_approved_2 = st.slider("Number of curricular units apporved in 2nd sem")

mother_occupation_map ={
    "Student": 0, 
    "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers": 1, 
    "Specialists in Intellectual and Scientific Activities": 2, 
    "Intermediate Level Technicians and Professions": 3, 
    "Administrative staff": 4, 
    "Personal Services, Security and Safety Workers and Sellers": 5, 
    "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry": 6, 
    "Skilled Workers in Industry, Construction and Craftsmen": 7, 
    "Installation and Machine Operators and Assembly Workers": 8, 
    "Unskilled Workers": 9, 
    "Armed Forces Professions": 10,
    "Other Situation": 90, 
    "Leave blank": 99, 
    "Health professionals": 122, 
    "Teachers": 123, 
    "Specialists in information and communication technologies (ICT)": 125, 
    "Intermediate level science and engineering technicians and professions": 131, 
    "Technicians and professionals, of intermediate level of health": 132, 
    "Intermediate level technicians from legal, social, sports, cultural and similar services": 134, 
    "Office workers, secretaries in general and data processing operators": 141, 
    "Data, accounting, statistical, financial services and registry-related operators": 143, 
    "Other administrative support staff": 144, 
    "Personal service workers": 151, 
    "Sellers": 152, 
    "Personal care workers and the like": 153,
    "Skilled construction workers and the like, except electricians": 171, 
    "Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like": 173, 
    "Workers in food processing, woodworking, clothing and other industries and crafts": 175, 
    "Cleaning workers": 191, 
    "Unskilled workers in agriculture, animal production, fisheries and forestry": 192, 
    "Unskilled workers in extractive industry, construction, manufacturing and transport": 193, 
    "Meal preparation assistants": 194
}
choice_1 = st.selectbox("Select mother's occupation",list(mother_occupation_map.keys()))
value_1 = mother_occupation_map[choice_1]
father_occupation_map = {
    "Student": 0, 
    "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers": 1, 
    "Specialists in Intellectual and Scientific Activities": 2, 
    "Intermediate Level Technicians and Professions": 3, 
    "Administrative staff": 4, 
    "Personal Services, Security and Safety Workers and Sellers": 5, 
    "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry": 6, 
    "Skilled Workers in Industry, Construction and Craftsmen": 7, 
    "Installation and Machine Operators and Assembly Workers": 8, 
    "Unskilled Workers": 9, 
    "Armed Forces Professions": 10, 
    "Other Situation": 90, 
    "Leave blank": 99,
    "Armed Forces Officers": 101,
    "Armed Forces Sergeants": 102,
    "Other Armed Forces personnel": 103,
    "Directors of administrative and commercial services": 112,
    "Hotel, catering, trade and other services directors": 114,
    "Specialists in the physical sciences, mathematics, engineering and related techniques": 121,
    "Health professionals": 122, 
    "Teachers": 123, 
    "Specialists in finance, accounting, administrative organization, public and commercial relations": 124, 
    "Intermediate level science and engineering technicians and professions": 131, 
    "Technicians and professionals, of intermediate level of health": 132, 
    "Intermediate level technicians from legal, social, sports, cultural and similar services": 134,
    "Information and communication technology technicians": 135,
    "Office workers, secretaries in general and data processing operators": 141, 
    "Data, accounting, statistical, financial services and registry-related operators": 143, 
    "Other administrative support staff": 144, 
    "Personal service workers": 151, 
    "Sellers": 152, 
    "Personal care workers and the like": 153,
    "Protection and security services personnel": 154, 
    "Market-oriented farmers and skilled agricultural and animal production workers": 161, 
    "Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence": 163, 
    "Skilled construction workers and the like, except electricians": 171,
    "Skilled workers in metallurgy, metalworking and similar": 172,
    "Skilled workers in electricity and electronics": 174,
    "Workers in food processing, woodworking, clothing and other industries and crafts": 175, 
    "Fixed plant and machine operators": 181,
    "Assembly workers": 182, 
    "Vehicle drivers and mobile equipment operators": 183, 
    "Cleaning workers": 191, 
    "Unskilled workers in agriculture, animal production, fisheries and forestry": 192, 
    "Unskilled workers in extractive industry, construction, manufacturing and transport": 193, 
    "Meal preparation assistants": 194, 
    "Street vendors (except food) and street service providers": 195
}
choice_2 = st.selectbox("Select father's occupation",list(father_occupation_map.keys()))
value_2 = father_occupation_map[choice_2]

#Send data to API
if st.button("Predict"):
    input_data = {
    "Course": course_value,
    "Mother's occupation": value_1,
    "Father's occupation": value_2,
    "Admission grade": admission_grade,
    "Age at enrollment": age,
    "Curricular units 1st sem (approved)": curr_units_approved_1,
    "Curricular units 1st sem (grade)": curr_units_1_grade,
    "Curricular units 2nd sem (approved)": curr_units_approved_2,
    "Curricular units 2nd sem (grade)": curr_units_2_grade,
    "Previous qualification grade": prev_qual_grade
    }
    response = requests.post("http://127.0.0.1:8000/predict", json={"data": input_data})
    result = response.json()

    st.success(f"Dropout Probability: {result['dropout_probability']}")
    st.info(f"Risk Category: {result['risk_category']}")
    st.warning(f"Prediction: {result['prediction']}")

