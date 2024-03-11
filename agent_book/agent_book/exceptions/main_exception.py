class AgentBookException(Exception):
    def __init__(self, message: str, value: str = None):
        if value:
            message = f"Value `{value}` is wrong: {message}"
        super().__init__(message)
