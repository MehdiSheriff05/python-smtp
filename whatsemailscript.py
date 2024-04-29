import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import colorama
from colorama import Fore

# Declarations and intialization
colorama.init(autoreset=True)
 
# My creds
email = "" # put in your email here
password = "" # put in your google password here

# Declare students list
students = []
file_path = "" # images directory file path here
file_extension = # pic format, either .jpg, .png, or .jpeg
csv_name = # mention the name of your csv

def main():
    read_csv()
    start_server()
    send_pictures(students)

# Start Server
def start_server():
    print("Connecting to server...")
    global server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    print("Succesfully connected to server")
    print()

# Read the csv file and get data
def read_csv():
    with open(csv_name) as file:
        reader = csv.reader(file)
        for email, pic, first, middle, last, phone in reader:
            students.append(
                {"email": email.strip(), 
                "pic": pic.strip(), 
                "first":first.title().strip(), 
                "middle":middle.title().strip(), 
                "last":last.title().strip(), 
                "phone":phone.strip()}
                )
    print("Students list completed!")
    print()

def send_pictures(students):
    for student in students:
        global first_name, last_name, student_email, student_phone
        first_name = student["first"]
        last_name = student["last"]
        student_email = student["email"]
        student_phone = f"+{student['phone']}"
        student_pic = student["pic"]
        
        # Email subject, any variables to be included in the f-string to be put in {}
        subject = f""

        # Make the body of the email, put your custom message here and any variables such as the first_name in {}
        body = f"""

        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = student["email"]
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        filename = f"{file_path}{student_pic}{file_extension}"

        # Open the file in python as a binary
        attachment= open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + f"{first_name}{last_name}.jpg")
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Send email and whatsapp message
        print(Fore.BLUE + f"{student_pic} - {first_name} {last_name}")
        print(Fore.YELLOW + "Sending email......")
        server.sendmail(email, student_email, text)
        print(Fore.GREEN + "Email successful...")
        print()

    # Close the port
    server.quit()

if __name__ == "__main__":
    main()