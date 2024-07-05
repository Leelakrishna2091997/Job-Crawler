from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import smtplib
import time
import pandas as pd

# import requests

# url = "https://jobs.netflix.com/search"
# page = requests.get(url)
# text = BeautifulSoup(page.text, 'html')

# Send an email to the user with the csv file, template of information.
data_frame = {}
# Close the WebDriver
csv_file = "netflix-links.csv"


def send_email(to_email, subject, template_vars ={}):
    # Load the email template
    with open('email_template.html', 'r') as file:
        template = file.read()

    # Replace placeholders with actual values
    for key, value in template_vars.items():
        template = template.replace('{{ ' + key + ' }}', value)

    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'leelakrishna2091997@gmail.com'  # Replace with your Gmail address
    smtp_password = 'kyyn fimy avcq atla'  # Replace with your app-specific password or Gmail password if 2FA is not enabled
    from_email = smtp_username
    body = "Please find today's job links"

    # Create the email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email


    # Attach the HTML content to the email
    msg.attach(MIMEText(template, 'html'))

    msg.attach(MIMEText(body, 'plain'))


    # Open the CSV file in binary mode
    with open(csv_file, 'rb') as attachment:
        # Create a MIMEBase object
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

        # Encode the payload using Base64
        encoders.encode_base64(part)

        # Add header to the attachment
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {csv_file}',
        )

        # Attach the MIMEBase object to the email message
        msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

# Scrape the data present on the home page without search and create a csv file with the data object

def run_selenium_script():
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    # Uncomment if you want to run headless
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        # Open the web page
        driver.get("https://jobs.netflix.com/search")

        # Find the search field element (adjust the selector as needed)
        search_field = driver.find_element("id", "autocomplete-input")  # Example using name attribute

        # Enter text into the search field
        search_field.send_keys("Software Engineer")

        # Optionally, submit the search form
        search_field.send_keys(Keys.RETURN)
        
        # Add any other actions here

        # Wait indefinitely to keep the browser open
        print("Script completed. The browser will remain open.")
        time.sleep(5)
        
        # Identify the results of the search content
        element = driver.find_element(By.CSS_SELECTOR, '[data-testid="search-content"]')

        links = element.find_elements(By.TAG_NAME, 'a')
        export_cols = ['title', 'link']
        df = pd.DataFrame(columns=export_cols)
        for child in links:
            scraped_data = child.text
            scraped_link = child.get_attribute("href")
            # export_data.append({'title': scraped_data, 'link': scraped_link}) 
            length = len(df)
            df.loc[length] = [scraped_data, scraped_link]
        # print("Dataframe",df)
        global data_frame
        data_frame = df
        

    except Exception as e:
        print(f"An error occurred: {e}")

    # Do not close the driver
    # driver.quit()  # Comment out or remove this line


# driver.quit()

# print(text)


if __name__ == "__main__":
    run_selenium_script()
    data_frame.to_csv(csv_file, index = False)
    # send_email("kodipunjula.v@northeastern.edu", "testing scraper")
    send_email("yellareddy.c@northeastern.edu", "Baaga enjoy cheyyi happy ga")
