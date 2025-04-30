class UsernameEmailInUser(Exception):
    def __init__(self, message: str | None = None):
        base = "Username or email already exists"
        if message:
            base += f": {message}"
        super().__init__(base)
