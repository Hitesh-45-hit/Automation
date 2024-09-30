from PIL import Image, ImageDraw, ImageFont, ImageTk, features
from datetime import datetime, date
import pandas as pd
import requests
import os
import time
import re
import json
import uuid

#All common variables that we use
Coords = [900,595]      #name cooridinates
Coords1 = [880,805]     #date cooridinates
Coords2 = [950,805]     #date cooridinates                                
Coords3  = [1020,805]   #month cooridinates 
Coords4  = [1090,805]   #month cooridinates 
Coords5  = [1160,805]   #year cooridinates 
Coords6  = [1230,805]   #year cooridinates 
Coords7  = [1300,805]   #year cooridinates 
Coords8  = [1370,805]   #year cooridinates 
colour = '#0F4FA4'      #colour for name and birthdate
Font = ImageFont.truetype("C:/Users/Administrator/AppData/Local/Microsoft/Windows/Fonts/Kalam-Bold.ttf", 80)
Font1= ImageFont.truetype("C:/Users/Administrator/AppData/Local/Microsoft/Windows/Fonts/Sahitya-Regular.ttf",100)
direction = 'rtl' #Right to Left
Alignment= 'right'
today = date.today()

#To delete the previous files
def delete_image_files_in_folder(folder_path):
    try:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Add more image extensions if needed
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                _, file_extension = os.path.splitext(filename)
                if file_extension.lower() in image_extensions:
                    os.remove(file_path)
                    print(f"Image file deleted: {file_path}")
                else:
                    print(f"Skipped: {file_path} (Not an image file)")
            else:
                print(f"Skipped: {file_path} (Not a file)")
        print("Deletion of images files completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    folder_path = "C:/Bhavartha/SiteData"  # Replace this with the path to your target folder
    delete_image_files_in_folder(folder_path)

def is_valid_mobile_number(mobile_number):
    # Check if the number is exactly 12 digits with 91 and consists only of digits
    mobile_number_str = str(mobile_number)
    if re.match(r'^\d{12}$', mobile_number_str):
        return True
    else:
        return False

#To translate the english date into marathi date
def translate_to_hindi_numerals(dmy):
    # Define the translation table for digits 0 to 9 in Hindi numerals
    hindi_numerals = str.maketrans("0123456789", "०१२३४५६७८९")
    # Convert the year to a string and use the translate method to convert digits
    translated_marathi = str(dmy).translate(hindi_numerals)
    return translated_marathi

def send_message(message):
    url = 'https://backend.aisensy.com/campaign/t1/api/v2'
    params = {
                "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2Mzc5YzkyYTEyYzUxMDFiOTRhODRjNiIsIm5hbWUiOiJCaGF2YXJ0aGEiLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjYzNzljOTJhMTJjNTEwMWI5NGE4NGMxIiwiYWN0aXZlUGxhbiI6Ik5PTkUiLCJpYXQiOjE3MTQ5MjA1OTR9.q4S5R4I56k3V8b_nA8H7ZHMorPq4_2tjClGnK2bjK_A",
                "campaignName": "Status_Update",
                "destination": "917972239751",
                "userName": "Hitesh",
                "templateParams": [message],                  
            }
    json_data = json.dumps(params)
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})

# def send_message2(message):
#     url2 = 'https://wap.whatapi.in/api/send'
#     params = {
#         'number': '917038825330', 
#         'type':'text',
#         'message': message,
#         'instance_id': '659BBB8DA4E2B',
#         'access_token': '6502ca54ae524'
#     }
#     response = requests.get(url2, params=params)
    
#Main function for execution
def happy_birthday():
    df = pd.read_excel('Employee-data.xlsx', engine='openpyxl')
    i=1   
    filename = f"C:/Bhavartha/Files/{today}.txt"
    fail_messages = []  # To accumulate fail messages
    success_messages = []  # To accumulate success messages
    invalid_mobiles= [] # To accumulate invalid mobile
    birthday_sent = False  # Flag to check if any birthday message was se
    with open(filename, "a",encoding="utf-8") as output_file:
        for _, values in df.iterrows():
            #extracting values from excel
            name = values['Name']
            ename = values['FullEnglish']
            Mno=str(values['Mobile'])
            birthdate = values['DOB']
            birthdate = datetime.date(birthdate)          
            #Spliting date and month into indivisual numbers 
            date_string = birthdate.strftime('%d-%m-%Y')      
            day,month,year=date_string.split('-')
            #Convert day into marathi date
            translated_day = translate_to_hindi_numerals(day)
            day_m=translated_day
            #Convert month into marathi month
            translated_month = translate_to_hindi_numerals(month)
            month_m=translated_month
            # print(day_m+month_m)
            day_digit_1 = day_m[0]
            day_digit_2 = day_m[1]
            month_digit_1 = month_m[0]
            month_digit_2 = month_m[1]
            #year must be current year on image
            current_year = datetime.now().year
            translated_year = translate_to_hindi_numerals(current_year)    #translate current year into marahti year
            year1 = str(translated_year)
            year_digit_1=year1[0]
            year_digit_2=year1[1]
            year_digit_3=year1[2]
            year_digit_4=year1[3]
            #Taking current mont and day for if condition  
            current_day = today.day
            current_month = today.month
            current_year=today.year
            #condition to check date and month is equal to current day and month
            if birthdate.month == current_month and birthdate.day == current_day:
                if is_valid_mobile_number(Mno):
                    # print("Happy birthday"+" "+name)
                    unique_id = str(uuid.uuid4())
                    img1 = Image.open("bhavartha.png")
                    I1 = ImageDraw.Draw(img1)  #draw on image
                    #draw name and birthdate on image
                    I1.text(Coords, name,colour, font=Font, align=Alignment,direction=direction)
                    I1.text(Coords1, day_digit_1,colour, font=Font1, align=Alignment,direction=direction)
                    I1.text(Coords2, day_digit_2,colour, font=Font1, align=Alignment,direction=direction)
                    I1.text(Coords3, month_digit_1,colour, font=Font1, align=Alignment,direction=direction)
                    I1.text(Coords4, month_digit_2,colour, font=Font1, align=Alignment,direction=direction)
                    I1.text(Coords5, year_digit_1,colour, font=Font1, align=Alignment,direction=direction)
                    I1.text(Coords6, year_digit_2,colour, font=Font1, align=Alignment,direction=direction)
                    I1.text(Coords7, year_digit_3,colour, font=Font1, align=Alignment,direction=direction)
                    I1.text(Coords8, year_digit_4,colour, font=Font1, align=Alignment,direction=direction)
                    img1.save(f'C:/Bhavartha/SiteData/{unique_id}.png')
                    #Message and medialink for whatsapp
                    Message=(name)
                    Media_url = f'http://15.206.191.118:80/{unique_id}.png'
                    #Call an api to send messages on whatsapp 
                    url = 'https://backend.aisensy.com/campaign/t1/api/v2'
                    params = {
                        "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2Mzc5YzkyYTEyYzUxMDFiOTRhODRjNiIsIm5hbWUiOiJCaGF2YXJ0aGEiLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjYzNzljOTJhMTJjNTEwMWI5NGE4NGMxIiwiYWN0aXZlUGxhbiI6Ik5PTkUiLCJpYXQiOjE3MTQ5MjA1OTR9.q4S5R4I56k3V8b_nA8H7ZHMorPq4_2tjClGnK2bjK_A",
                        "campaignName": "Birthday_message",
                        "destination": Mno,
                        "userName": name,
                        "templateParams": [Message],
                        "media": {
                            "url": Media_url,
                            "filename": "demo-file"
                        }
                    }
                    json_data = json.dumps(params)
                    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
                    # print(response.text)
                    print(response.status_code)
                    print(response.json())
                    # print(response.text)
                    if response.status_code != 200 :
                        output_file.write(f"Failed to send message to {name}:-{Mno}\n")
                        output_file.write(f"Response status code: {response.status_code}\n")
                        fail_message=(f"Failed to send message to {name}:-{Mno}")
                        fail_messages.append(fail_message)
                        birthday_sent = True  # Set the flag to True as a birthday message was sent
                    else:
                         output_file.write(f"Happy birthday {name}\n")
                         output_file.write(f"Message sent to {Mno}\n")
                         output_file.write(f"Response status code: {response.status_code}\n")
                         output_file.write(f"Response text: {response.text}\n")
                         sucess_message=(f"Message Sent suceessfully to {name}:-{Mno}")
                         success_messages.append(sucess_message)
                         birthday_sent = True  # Set the flag to True as a birthday message was sent
                    output_file.write("\n")  # Add a new line
                    i=i+1
                    time.sleep(30)
                else:
                    output_file.write(f"Invalid mobile number for {name} :- {Mno}\n") 
                    output_file.write("\n")  # Add a new line 
                    invalid_mobile=(f"Invalid mobile number for {name}:- {Mno}")
                    invalid_mobiles.append(invalid_mobile)  
                    birthday_sent = True  # Set the flag to True as a birthday message was sent
            else:
                print(name+" "+"has No birthday today")  
            # break
        if not birthday_sent:
            # Send a message indicating that no one has a birthday today
            no_birthday_message =( f"No one has a birthday on {today}.")
            output_file.write(f"No one has a birthday on {today}.")
            send_message(no_birthday_message)
            # send_message2(no_birthday_message)
        if fail_messages or success_messages or invalid_mobiles:
            success_message = "\n".join(success_messages)
            fail_message = "\n".join(fail_messages)
            invalid_mobile= "\n".join(invalid_mobiles)
            # send_message(success_message+"\n"+fail_message+"\n"+invalid_mobile)
            # send_message2(success_message+"\n"+fail_message+"\n"+invalid_mobile)
        output_file.close()
happy_birthday()



