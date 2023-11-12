

class HostConfig:
    """
    Host configuration
    """
    def __init__(self, server, port, ssh_key, username, password) -> None:
        self.server = server
        self.port = port
        self.ssh_key = ssh_key
        self.username = username
        self.password = password