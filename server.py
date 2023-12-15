import socket
import ssl
import smtplib
import datetime
import pickle


# Configuration
server_address = 'www.facebook.com'
server_port = 443
timeout_seconds = 5
email_alerts = True
email_recipient = 'karthik12345pandi@gmail.com'
pickle_file = 'server_status_history.pkl'

def check_server_status():
    try:
        # Create a socket
        sock = socket.create_connection((server_address, server_port), timeout=timeout_seconds)

        # Create an SSL context and wrap the socket with SSL
        ssl_context = ssl.create_default_context()
        with ssl_context.wrap_socket(sock, server_hostname=server_address):
            # Server is reachable, perform additional checks if needed
            pass

        # Server is up, record the status
        record_server_status(True)
        print('Server is UP')

    except (socket.timeout, socket.error, ssl.SSLError) as e:
        # Server is down, record the status and send alerts
        record_server_status(False)
        send_email_alert(str(e))
        print(f'Server is DOWN. Error: {str(e)}')


def record_server_status(status):
    # Load existing history or create a new one
    try:
        with open(pickle_file, 'rb') as f:
            history = pickle.load(f)
    except (EOFError, FileNotFoundError):
        history = []

    # Record current status with timestamp
    timestamp = datetime.datetime.now()
    history.append({'timestamp': timestamp, 'status': status})

    # Save the updated history
    with open(pickle_file, 'wb') as f:
        pickle.dump(history, f)

def send_email_alert(message):
    print("Sending email alert...")
    if email_alerts:
        # Configure SMTP server and credentials
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'karthik.2003.sekar@gmail.com'
        smtp_password = 'ygzw kanq uizu yfpl'


        # Compose email message
        subject = 'Server Down Alert!'
        body = f'The server {server_address} is down. Error: {message}'
        email_message = f'Subject: {subject}\n\n{body}'

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            try:
                server.login(smtp_username, smtp_password)
                print("Login successful")
                server.sendmail(smtp_username, email_recipient, email_message)
                print("Email sent successfully")
            except smtplib.SMTPAuthenticationError as e:
                print(f"Login failed. Error: {e}")
            except Exception as e:
                print(f"Error sending email: {e}")

# Main execution
if __name__ == "__main__":
    check_server_status()
