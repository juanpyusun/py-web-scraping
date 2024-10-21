import requests

# URL of the POST request - need to inspect the HTML or use devtools to obtain
url = "target_url_of_post_request"

# Define parameters sent with the POST request
# (if there are additional ones, define them as well)
user = "Your username goes here"
password = "Your password goes here"

# Arrange all parameters in a dictionary format with the right names from the website at name attribute
payload = {
    "user[email]": user,
    "user[password]": password
}

# Create a session so that we have consistent cookies
s = requests.Session()

# Submit the POST request through the session
p = s.post(url, data = payload)
p.status_code


# You are now logged in and can proceed with scraping the data, here the cookies are stored in the session
# .
# .
# .

# Don't forget to close the session when you are done
s.close()