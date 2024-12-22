from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Selenium WebDriver
def configure_driver():
    options = Options()
    # Remove '--headless' to show the browser
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    service = Service('C:/Users/nastu/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Function to scrape the number of items
def get_item_count(driver, url):
    driver.get(url)
    try:
        # Save a screenshot for debugging
        driver.save_screenshot(r'C:\Users\nastu\Documents\screenshot.png')

        # Wait for the element to load
        count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'lblNumberItem'))
        )
        return int(count_element.text.strip())
    except Exception as e:
        # Save an error screenshot
        driver.save_screenshot(r'C:\Users\nastu\Documents\error_screenshot.png')
        raise ValueError("Item count element not found on the page!")


# Send email notification
def send_email(new_count):
    sender_email = "nastulczyk.pav@gmail.com"  # Replace with your email
    receiver_email = "pavel.nastulczyk@icloud.com"  # Replace with the recipient's email
    password = "fmyb oeqg wbya conm"  # Replace with your email password or app-specific password
    
    subject = "Item Count Changed!"
    body = f"The item count on the page has changed. New count: {new_count}"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function
def main():
    url = "https://www.alza.cz/levne-iphone/18851638.htm#f&cst=2,3,1&cud=0&pg=1&pn=1&prod=&sc=500"
    driver = configure_driver()
    try:
        last_count = get_item_count(driver, url)
        print(f"Initial item count: {last_count}")
        
        while True:
            current_count = get_item_count(driver, url)
            
            # Print whether the item count has changed
            if current_count != last_count:
                print(f"Item count updated! New count: {current_count}")
                send_email(current_count)
                last_count = current_count
            else:
                print("Item count has not changed.")
            
            # Wait before checking again
            time.sleep(60)  # Check every 10 minutes
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

