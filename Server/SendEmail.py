import sys
from email import encoders
import email, smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




if __name__ == "__main__":


	filename = "personPictured.png"
	# print("\n\nHELLO from SendEmail.py\n\n")
	if len(sys.argv) == 2:
		filename = sys.argv[1]

	subject 	   = "Intruder detected !"
	sender_email   = "testschool2021@gmail.com"
	receiver_email = "testschool2021@gmail.com"
	password 	   = "8JuPQB7Hjxr4ZUQ"
	
	body = "" \
		"Hello,\n\n" \
		"An intruder was detected by the application.\n" \
		"Please find in attachment the intruder pictured at this very moment.\n\n" \
		"Intruder Detector App"

	# Create a multipart message and set headers
	message 		   = MIMEMultipart()
	message["From"]    = sender_email
	message["To"] 	   = receiver_email
	message["Subject"] = subject

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	# Open PDF file in binary mode
	with open(filename, "rb") as attachment:
	    # Add file as application/octet-stream
	    # Email client can usually download this automatically as attachment
	    part = MIMEBase("application", "octet-stream")
	    part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	part.add_header(
	    "Content-Disposition",
	    f"attachment; filename= {filename}",
	)

	# Add attachment to message and convert message to string
	message.attach(part)
	text = message.as_string()

	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    print("\t-> Send email ... ", end="")
	    server.sendmail(sender_email, receiver_email, text)

	print(" Done !")
