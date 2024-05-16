from session import Session
import os

# creates instance of session
session = Session()

session.navigate_to_home()


# login using your google account with a verified email!
session.login('email', 'password')


get_new_offers = session.start_searching()