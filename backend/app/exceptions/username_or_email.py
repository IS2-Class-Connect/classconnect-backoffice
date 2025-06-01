class UsernameEmailInUser(Exception):
    def __init__(self):
        super().__init__("Username or email already exists")
