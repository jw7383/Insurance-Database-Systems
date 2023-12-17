import streamlit as st
from datetime import date
import requests
import pandas as pd

def go_to_quote_page():
    st.session_state['page'] = 'quote'

def go_to_main_page():
    st.session_state['page'] = 'main'

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def calculate_age_category(age):
    if 18 <= age <= 24:
        return "18-24"
    if 25 <= age <= 29:
        return "25-29"
    if 30 <= age <= 34:
        return "30-34"
    if 25 <= age <= 29:
        return "35-39"
    if 40 <= age <= 44:
        return "40-44"
    if 45 <= age <= 49:
        return "45-49"
    if 50 <= age <= 54:
        return "50-54"
    if 55 <= age <= 59:
        return "55-59"
    if 60 <= age <= 64:
        return "60-64"
    if 65 <= age <= 69:
        return "65-69"
    if 70 <= age <= 74:
        return "70-74"
    if 75 <= age <= 79:
        return "75-79"
    if 80 <= age:
        return "80+"
    
def feet_inches_to_cm(feet, inches):
    total_inches = feet * 12 + inches
    return total_inches * 2.54

def lb_to_kgs(lb):
    return lb * 0.453592

def calculate_bmi(height, weight):
    return round(weight/height**2 * 703)

def show_main_page():
    st.title("Jason Health Insurance Company's Insurance Quote Application")
    st.write("Welcome to the Health Insurance Quote Application. Our company is pleased to offer you a variety of health insurance products. Click below to get started.")
    st.button("Request Quote", on_click=go_to_quote_page)
    st.write("Disclaimer: This is purely for educational purposes and is not intended to provide any real products or services.")

def show_quote_page():
    st.title("Get Your Insurance Quote")

    st.button("Return to Main Page", on_click=go_to_main_page)

    st.header("Contact and Personal Information")
    
    name = st.text_input("Name")

    dob = st.date_input("Date of Birth")

    address = st.text_input("Address")

    sex = st.selectbox("Sex", 
                       ("",
                        "Male",
                        "Female"))

    if dob:
        dob_formatted = dob.strftime('%Y-%m-%d')
        age = calculate_age(dob)
        age_category = calculate_age_category(age)

    st.header("Height and Weight")

    col1, col2 = st.columns(2)

    with col1:
        feet = st.number_input("Feet", min_value=0, max_value=8, step=1, format="%i")

    with col2:
        inches = st.number_input("Inches", min_value=0, max_value=11, step=1, format="%i")

    if feet and inches:
        height_cm = feet_inches_to_cm(feet, inches)
        st.write(f"height in cm: {height_cm}")

    weight = st.number_input("Enter your weight in pounds", min_value=0, max_value=500)

    if weight:
        weight_kg = lb_to_kgs(weight)
        st.write(f"weight in kg: {weight_kg}")

    if feet and inches and weight:
        bmi = calculate_bmi(feet + inches*12, weight)
        st.write(f"bmi: {bmi}")

    st.header("General Health")
                            
    general_health = st.selectbox("Would you say that in general your health is",
                                    ("",
                                     "Excellent",
                                     "Very Good", 
                                     "Good",
                                     "Fair", 
                                     "Poor"))

    checkup = st.selectbox("About how long has it been since you last visited a doctor for a routine checkup? (A routine checkup is a general physical exam, not an exam for a specific injury, illness, or condition.)",
                            ("",
                             "Within the past year",
                             "Within the past 2 years",
                             "Within the past 5 years",
                             "5 or more years ago", 
                             "Never"))

    exercise = st.selectbox("During the past month, other than your regular job, did you participate in any physical activities or exercises such as running, calisthenics, golf, gardening, or walking for exercise?",
                            ("",
                             "Yes",
                             "No"))

    st.header("Medical history")
    
    st.subheader("Has a doctor, nurse, or other health professional ever told you that you had any of the following?")

    skin_cancer = st.selectbox("Skin cancer?",
                            ("",
                             "Yes",
                            "No"))
    other_cancer = st.selectbox("Any other types of cancer?",
                                ("",
                                 "Yes",
                                 "No"))
    depression = st.selectbox("A depressive disorder (including depression, major depression, dysthymia, or minor depression)?",
                              ("",
                               "Yes",
                               "No"))
    arthritis = st.selectbox("Some form of arthritis, rheumatoid arthritis, gout, lupus, or fibromyalgia?",
                            ("",
                             "Yes",
                             "No"))

    st.header("Smoking, Food, and Drink Consumption.")
    
    st.subheader("Your best guess is fine.")

    smoking_history = st.selectbox("Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]",
                           ("",
                            "Yes",
                            "No"))

    alcohol_consumption = st.slider("During the past 30 days, how many days did you have at least one drink of any alcoholic beverage such as beer, wine, a malt beverage or liquor?",
                            0, 30, step=1)
    
    fruit_consumption = st.slider("During the past month, how many times you eat fruit? Count fresh, frozen, or canned fruit.",
                            0, 100, step=1)

    green_vegetables_consumption = st.slider("During the past month, how many times did you eat green vegetables?.",
                            0, 100, step=1)

    fried_potato_consumption = st.slider("During the past month, how many times did you eat fried potatoes?.",
                            0, 100, step=1)

    all_fields_filled = name and dob and address and sex and feet and inches and weight and general_health and checkup and exercise and skin_cancer and other_cancer and depression and arthritis and smoking_history and alcohol_consumption and fruit_consumption and green_vegetables_consumption and fried_potato_consumption

    if st.button("Calculate Quote"):
        if all_fields_filled and "" not in [sex, skin_cancer, general_health, checkup, exercise, skin_cancer, other_cancer, depression, arthritis, smoking_history]:
            st.write("Calculating quote...")
            api_url = "https://w7f1cr100a.execute-api.us-east-1.amazonaws.com/v1"
            customer_data = {
                "name": name,
                "dob": dob_formatted,
                "address": address
            }

            customer_response = requests.post(f"{api_url}/customers", json=customer_data)
            if customer_response.status_code == 200:
                st.write(f"Customer information submitted")
                medical_data = {
                "general_health": general_health,
                "checkup": checkup,
                "exercise": exercise,
                "skin_cancer": skin_cancer,
                "other_cancer": other_cancer,
                "depression": depression,
                "arthritis": arthritis,
                "sex": sex,
                "age_category": age_category,
                "height": height_cm,
                "weight": weight_kg,
                "bmi": bmi,
                "smoking_history": smoking_history,
                "alcohol_consumption": alcohol_consumption,
                "fruit_consumption": fruit_consumption,
                "green_vegetables_consumption": green_vegetables_consumption,
                "fried_potato_consumption": fried_potato_consumption
            }

                medical_response = requests.post(f"{api_url}/medical-information", json=medical_data)
                if medical_response.status_code == 200:
                    st.write(f"Medical information submitted")
                    st.write("Calculating risk... (Please be patient, this can take up to a minute.)")
                    risk_response = requests.post(f"{api_url}/calculate-risk", json=medical_data)
                    if risk_response.status_code == 200:
                        risk_data = risk_response.json()
                        premium_response = requests.post(f"{api_url}/calculate-premium", json=risk_data)
                        if premium_response.status_code == 200:
                            premium_response_data = pd.read_json(premium_response.text)
                            premium_response_data.rename(columns={'productName': 'Product Name', 'premium': 'Quoted Premium'}, inplace=True)
                            premium_response_data['Quoted Premium'] = premium_response_data['Quoted Premium'].apply(lambda x: f"${x:,.2f}")
                            df = pd.DataFrame(premium_response_data)
                            st.dataframe(df[['Product Name', 'Quoted Premium']], hide_index=True)
                        else:
                            st.write("Something went wrong calculating the premiums.")
                    else:
                        st.write("Something went wrong calculating the risk.")
                else:
                    st.write("Something went wrong submitting the medical information.")
            else:
                st.write("Something went wrong submitting the customer information.")


        else:
            st.error("There are missing values, please fill in all fields.")

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'main'

    if st.session_state['page'] == 'main':
        show_main_page()
    elif st.session_state['page'] == 'quote':
        show_quote_page()

if __name__ == "__main__":
    main()