import streamlit as st
import json
import csv
import pandas as pd
from PIL import Image
import numpy as np
import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# CSV-Datei im Lese-Modus öffnen
with open('Parameter_test.csv', 'r') as f:
    reader = csv.reader(f,delimiter=';')
    data = [row for row in reader]
        
#Json-Datei im Lese-Modus öffnen
#with open('data.json', 'r') as f:
 #   data = json.load(f)

# json-Datei im Lese-Modus öffnen
#with open('Parameter_test.json', 'r') as f:
 #   reader = csv.reader(f, delimiter=';')
  #  data = [row for row in reader]

# CSS-Code für die Farbe
css = """
<style>
body {
    background-color: #F5DEED; /* Hintergrundfarbe */
}

h1 {
    color: #F5DEED; /* Textfarbe */
}
</style>
"""

# CSS-Code in der Streamlit-App anzeigen
st.markdown(css, unsafe_allow_html=True)

# Benutzername und Passwort erstellen
correct_username = {"zhaw": "1234", "adrian": "aaaa", "samuel": "ssss", "sangi": "1111", "achu": "4444"}

# Login Seite
def login():
    st.write("# Login")
    login_option = st.radio("Login or Sign up", ("Login", "Sign up"))

    # Text einfügen
    st.write(
        "Die Funktion 'Sign Up' ist verfügbar nach App Freigabe durch A. Rutzer und S. Wehrli!",
        unsafe_allow_html=True,
    )

    if login_option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        
        if login_button:
            if username in correct_username and password == correct_username[username]:
                st.success("Login successful!")
                st.session_state["logged_in"] = True
            else:
                st.error("Invalid username or password")

    elif login_option == "Sign up":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        signup_button = st.button("Sign up")



        if signup_button:
            if new_password == confirm_password:
                st.success("Sign up successful! Please log in.")
                correct_username[new_username] = new_password
            else:
                st.error("Passwords do not match")
                

# Seite für Willkommensnachricht nach erfolgreicher Anmeldung
def welcome():

    # Sidebar mit Optionen
    st.sidebar.write("## Menu")
    options = ["Analytics", "Videos", "Feedback", "About Us"]
    choice = st.sidebar.selectbox("Select Option", options)
    
    # Display anzeigen
    if choice == "Analytics":
        
        st.write("# Welcome to Q-Check!")
        #Schriftart, erstes Wort krusiv
        st.markdown(""" <h2 style='font-size: 20px;'><em>Qualitycheck</em> is an open-source app framework built specifically to check quality control range in your laboratory.</h2> """, unsafe_allow_html=True)

        #verschiedene Tabs horizontal
        tab1, tab2, tab3, tab4 = st.tabs(["Hematogram II", "Hematogram V", "Shortcut & Definitions", "Graphic"])

        with tab1:
            st.header("Hematogram II")
            st.write("""<h2 style='font-size: 20px;'>Calculations for Quality Control</h2>
                        """, unsafe_allow_html=True)
            st.markdown("*Indication:* Anemia, infections, intoxications, collagenosis, leukemia and other systemic hematological diseases, malignant tumors, control of therapies, bone marrow depression (radiation, chemotherapy, immunosuppression).", unsafe_allow_html=True)

            # Parameter erstellt
            st.write("Enter values:")
            parameter_options = ['RBC', 'HGB', 'HCT', 'WBC', 'MCH', 'MCHC', 'MCV', 'PLT']
            input1 = st.selectbox("parameter hematogram II", parameter_options, index=0)
            var_mean_val =0.001 #variablen definiert
            var_low_val =0.001
            var_max_val =0.001
            
            search_string = input1
            for item in data:
               if search_string in item[0]: #output (String vergleichen mit array)
                   var_max_val=float((item[1]))
                   var_low_val=float((item[2]))
                   var_mean_val=float((item[3]))
             
            #Print mit 3 Dezimalstellen
            mean_val = st.number_input("company mean hematogram II", value=var_mean_val, step=0.001, format="%.3f")
            low_val = st.number_input("company range low hematogram II", value=var_low_val, step=0.001, format="%.3f")
            max_val = st.number_input("company range high hematogram II", value=var_max_val, step=0.001, format="%.3f")
            
    
            # Calculate the coefficient of variation
            def calculate_value(mean, low):
                result = (mean - low) / 3
                return result

            #Klick Button mit 2 Stellen nach Komma
            if st.button("Calculate"):
                result = calculate_value(mean_val, low_val)
                st.write("The calculated 1s value is:", format(result,".3f"))
                coefficient_of_variation = result / mean_val *100
                st.write("The calculated coefficient of variation is:", format(coefficient_of_variation,".2f") ,"%")
               
            #Bild1 hinzugefügt mit Spruch
            imageDrops = Image.open('bilder/drops.jpg')
            st.image(imageDrops, caption='"Good quality is not what we put into it. It is what the client or customer gets out of it." - Peter Drucker', use_column_width=True)


        with tab2:
            st.header("Hematogram V")
            st.write("""<h2 style='font-size: 20px;'>Calculations for Quality Control</h2>
                       """, unsafe_allow_html=True)
            st.markdown("*Indication:* Anemia, infections, intoxications, collagenosis, leukemia and other systemic hematological diseases, malignant tumors, control of therapies, bone marrow depression (radiation, chemotherapy, immunosuppression).", unsafe_allow_html=True)

            #Paramter erstellt für tab 2
            st.write("Enter values:")
            parameter_options = ['RBC', 'EO', 'HGB', 'HCT', 'WBC', 'MCH', 'MCHC', 'MCV', 'MONO', 'NEUT', 'PLT']
            input2 = st.selectbox("parameter hematogram V ", parameter_options, index=0)
            var_mean_val =0.001 #variablen definiert 
            var_low_val =0.001
            var_max_val =0.001
            
            search_string = input2
            for item in data:
               if search_string in item[0]: #output (String vergleichen mit array)
                   var_max_val=float((item[1]))
                   var_low_val=float((item[2]))
                   var_mean_val=float((item[3]))
            #Print
            mean_val2 = st.number_input("company mean hematogram V", value=var_mean_val, step=0.001, format="%.3f")
            low_val2 = st.number_input("company range low hematogram V", value=var_low_val, step=0.001, format="%.3f")
            input4 = st.number_input("company range high hematogram V", value=var_max_val, step=0.001, format="%.3f")
            
            # Calculate the coefficient of variation 
          
            def calculate_value(mean, low):
                result = (mean - low) / 3
                return result
            
            #Klick button
            if st.button("Calculate."):
                result = calculate_value(mean_val2, low_val2)
                st.write("The calculated 1s value is:", format(result,".3f"))
                coefficient_of_variation = result / mean_val2 *100
                st.write("The calculated coefficient of variation is:", format(coefficient_of_variation,".2f") ,"%")
                
            #Bild 2 hinzugefügt
            imageRed = Image.open('bilder/red.jpg')
            st.image(imageRed, caption='"Quality control is not a department, it is everyones job." - W. Edwards Deming', use_column_width=True)
               
        
        #defintion tab
        with tab3:
           st.write('<style>h2 {font-size: 28px; font-weight: bold, sans-serif;}</style>', unsafe_allow_html=True)
           st.header('Shortcuts & Definitions')
           
           # Pandas DataFrame für die Definitionen erstellt -> Tabelle
           df_definitions = pd.DataFrame({
               'Shortcut': ['BASO', 'RBC', 'EO', 'HGB', 'HCT', 'WBC', 'LYMPH', 'MCH', 'MCHC', 'MCV', 'MONO', 'NEUT', 'PLT'],
               'Full Name': ['Basophils', 'Red Blood Cells', 'Eosinophils', 'Hemoglobin', 'Hematocrit', 'White Blood Cells', 'Lymphocytes', 'Mean Corpuscular Hemoglobin', 'Mean Corpuscular Hemoglobin Concentration', 'Mean Corpuscular Volume', 'Monocytes', 'Neutrophils', 'Platelets'],
               'Definition': [
                   'Basophils are a type of white blood cell that works closely with your immune system to defend your body from allergens, pathogens and parasites. Basophils release enzymes to improve blood flow and prevent blood clots.',
                   'A type of blood cell that is made in the bone marrow and found in the blood. Red blood cells contain a protein called hemoglobin, which carries oxygen from the lungs to all parts of the body.',
                   'Eosinophils are one of several white blood cells that support your immune system. Sometimes, certain medical conditions and medications cause high eosinophil levels.',
                   'Hemoglobin is the iron-containing oxygen-transport metalloprotein present in red blood cells of almost all vertebrates as well as the tissues of some invertebrates.',
                   'The amount of whole blood that is made up of red blood cells.',
                   'White blood cells are part of the body\'s immune system. They help the body fight infection and other diseases. Types of white blood cells are granulocytes (neutrophils, eosinophils, and basophils), monocytes, and lymphocytes (T cells and B cells).',
                   'Lymphocytes are a type of white blood cell. They help your body\'s immune system fight cancer and foreign viruses and bacteria.',
                   'Mean Corpuscular Hemoglobin is a calculation of the average amount of hemoglobin contained in each of a person\'s red blood cells.',
                   'Mean corpuscular hemoglobin concentration is a measurement of the average amount of hemoglobin in a single red blood cell as it relates to the volume of the cell.',
                   'A mean erythrocyte single-volume blood test measures the average size of your red blood cells.',
                   'Monocytes are a type of white blood cell in your immune system. Monocytes turn into macrophage or dendritic cells when an invading germ or bacteria enters your body. The cells either kill the invader or alert other blood cells to help destroy it and prevent infection.',
                   'Neutrophils help your immune system fight infections and heal injuries. Neutrophils are the most common type of white blood cell in your body.',
                   'Platelets are the smallest component of your blood that control bleeding. Platelets cluster together to form a clot and prevent bleeding at the site of an injury.'
            
        ]
               
               
    })
           
           # Tabelle anzeigen
           st.table(df_definitions)
           
        with tab4:
            st.write("""<h2 style='font-size: 20px; color: grey;'>This page is temporarly progress, we will be back soon!</h2>
                   """, unsafe_allow_html=True)
            st.write("""<h2 style='font-size: 20px; color: #d1b8c8; font-style: italic;'>-Team Q-Check </h2>
                          """, unsafe_allow_html=True)
            st.header("Graphic")
            st.write("""<h2 style='font-size: 20px;'>Charts and Graphs</h2>
                   """, unsafe_allow_html=True)
       
            chart_options = ['Bar Chart', 'Line Chart', 'Pie Chart']
            selected_chart = st.selectbox("Select Chart Type", chart_options)

        if selected_chart == "Bar Chart":
            x = ['A', 'B', 'C', 'D', 'E']
            y = [10, 7, 5, 3, 1]

        elif selected_chart == "Bar Chart":
            st.header('Bar Chart Example')
            x = np.linspace(0, 10, 100)
            y = np.sin(x)

        elif selected_chart == "Line Chart":
            st.header('Line Chart Example')
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            
        elif selected_chart == "Pie Chart":
            st.header('Pie Chart Example')
            labels = ['Category 1', 'Category 2', 'Category 3']
            sizes = [30, 50, 20]         
        

    #About us tab, Schriftart und Grösse definiert
    if choice == "Videos":
    
        st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
        st.title('Videos')
        st.write("<p style='font-size: 30px; color: grey; text-decoration: none;'>Discovering solutions, delivering results</p>", unsafe_allow_html=True)

        st.markdown(
         """
         <p style='font-size: 18px;'>Welcome to our website! Here you will find an extensive collection of instructional videos designed to help you acquire new skills and expand your knowledge in various areas.
         Our goal is to make education accessible and enjoyable. We firmly believe that learning is a lifelong process and that everyone should have the opportunity to educate themselves, regardless of time, location, or financial resources. With our instructional videos, we offer you the flexibility to set your own learning pace and choose the topics that interest you the most.
         Our videos are created by experienced professionals and experts in their respective fields. We place great emphasis on delivering high-quality content that is precise and easy to understand. Whether you want to enhance your professional skills, explore a new hobby, or simply broaden your knowledge, we have a diverse range of topics that cater to your interests.
         Our intuitive user interface allows you to browse the instructional videos by categories or search for specific topics. We regularly update our content to ensure that you stay up to date and have access to the latest knowledge.
         We firmly believe that learning can be not only informative but also entertaining. Therefore, we place great emphasis on engaging presentation and interactive elements in our videos. We want you to have fun while learning and simultaneously grow as an individual.
         So, what are you waiting for? Dive into our world of instructional videos and discover new horizons. Get ready to expand your knowledge, acquire new skills, and ignite your passions. The possibilities are limitless, and we are here to accompany you on this exciting educational journey.
         Ready to get started? Browse through our videos and experience the power of hands-on learning. Enjoy and best of luck!</p>
         <p style='font-size: 20px;'>Visit our website to learn more about our services, and let us help you optimize your hematology laboratory's performance. Our team is here to support you with any additional information or help you require.</p>
         """, unsafe_allow_html=True)
      
        #Bild3 hinzugefügt mit Spruch
        imageabout = Image.open('bilder/lab.jpg')
        st.image(imageabout, caption='"Learning never exhausts the mind." - Leonardo da Vinci', use_column_width=True)
       

        # Read more Button erstellt
        read_more = st.button('VIDEOS')

        if read_more:
            # ganzer Text wird angezeigt, wenn man es klickt
            st.write()
            
            # Pfad zum vorhandenen Video
            video_path = "videos/CRP.mp4"
            video_file = open(video_path, "rb")
            save_bytes = video_file.read()
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)
           
            # Pfad zum vorhandenen Video
            video_path = "videos/hematology.mp4"
            video_file = open(video_path, "rb")
            save_bytes = video_file.read()
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)

            # Pfad zum vorhandenen Video
            video_path = "videos/blood.mp4"
            video_file = open(video_path, "rb")
            save_bytes = video_file.read()
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)
            
#Feedback tab, Schriftart und Grösse definiert
    if choice == "Feedback":

        st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
        st.title('Feedback')
    
        st.markdown(
     """
     <p style='font-size: 20px;'>
     Welcome to our feedback page!

    We are delighted to have you here and appreciate your valuable feedback. Your opinion is of great importance to us as it helps us continuously improve our services to meet your expectations.
    This feedback page provides you with an opportunity to share your thoughts, suggestions, and comments with us. Whether you have praise, constructive criticism, improvement ideas, or questions, we are eager to hear your feedback.
    We firmly believe that feedback is a crucial component of our growth. It enables us to address the needs and desires of our customers and enhance your experiences with our services.
    Your feedback is not only welcome but also taken seriously. We will carefully review each response and utilize them to implement positive changes and enhance our performance.
    We would like to express our sincere gratitude for taking the time to share your feedback with us. Together, we can contribute to making your experiences with our company even better.
    We look forward to receiving your feedback and are excited to hear your impressions! 
    Yours sincerely, Q-Check Team </p>
     """, unsafe_allow_html=True)

        #Bild3 hinzugefügt mit Spruch
        imageabout = Image.open('bilder/feedback.jpg')
        st.image(imageabout, caption='"Feedback is the breakfast of champions."', use_column_width=True)

        st.write("""<h2 style='font-size: 20px; color: grey;'>This section is still in progress!</h2>
                   """, unsafe_allow_html=True)
        st.write("""<h2 style='font-size: 20px; color: #d1b8c8; font-style: italic;'>-Team Q-Check </h2>
                          """, unsafe_allow_html=True)

        email = st.text_input("Please enter your email address:")
        feedback = st.text_area("Please enter your feedback:", "")

        if st.button("Submit Feedback"):
        # E-Mail-Einstellungen
            smtp_server = 'smtp.example.com'
            smtp_port = 587
            sender_email = email
            sender_password = 'your_password'
            receiver_email = 'rukunakk@students.zhaw.ch'

            st.write("Thank you for your feedback! Your feedback has been successfully submitted.")
      

    #About us tab, Schriftart und Grösse definiert
    if choice == "About Us":
    
        st.write('<style>h1{font-size: 36px; font-weight: bold;}</style>', unsafe_allow_html=True)
        st.title('Who are we?')
        st.write("<p style='font-size: 30px; color: grey; text-decoration: none;'>Discovering solutions, delivering results</p>", unsafe_allow_html=True)

        st.markdown(
         """
         <p style='font-size: 20px;'>Welcome to our hematology quality control website, where we provide comprehensive solutions for ensuring accurate and reliable results in your hematology laboratory. 
         Our team of experts has years of experience in the field, and we understand the importance of quality control in providing the best possible care to patients. 
         We offer a range of products and services, including proficiency testing, validation, and training, all designed to help you achieve and maintain the highest standards of quality control in hematology. 
         Our focus on quality control means that you can trust in the accuracy and precision of your results, enabling you to provide the highest standard of care to your patients.
         </p>
         <p style='font-size: 20px;'>Visit our website to learn more about our services, and let us help you optimize your hematology laboratory's performance. Our team is here to support you with any additional information or help you require.</p>
         """, unsafe_allow_html=True)
        #Bild3 hinzugefügt mit Spruch
        imageabout = Image.open('bilder/about.jpg')
        st.image(imageabout, caption='"The science of today is the technology of tomorrow." - Edward Teller', use_column_width=True)
    

        # Text Personas
        long_text = """
        The app was created for Nila Walker. Nila is a 32-year-old woman and works as a biomedical laboratory 
        diagnostician at Roche. Nila has a lot of responsibilities in the company, so she doesn't have time to recalculate 
        the range of norm values ​​for the controls with each new lot number. Due to the stress, it has also happened that she entered the range 
        values ​​incorrectly. This was discovered when the controls were repeatedly out of the norm.
        That's why we decided to make Nila's everyday work a little easier and design an app that 
        calculates the standard values ​​​​for quality control.
        """

        # Read more Button erstellt
        read_more = st.button('How it all started...')

        if read_more:
            # ganzer Text wird angezeigt, wenn man es klickt
            st.write(long_text)
        else:
                # wir wollten nicht, dass schon gewisse Wörter vorher erscheinen, deshalb 0
            st.write(long_text[:0])




# Haupt App
def app():
    # abrufen, ob User eingeloggt ist, wenn nicht..
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # User nicht eingeloggt, dann erscheint ->login page
    if not st.session_state["logged_in"]:
        login()
    else:
        # welcome Seite nach erfolgreiche Login 
        welcome()

# app laufen lassen
if __name__ == '__main__':
	app()

