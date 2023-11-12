import os
import sys
import paramiko
from scp import SCPClient

from host_config import HostConfig
from exceptions import *


class Host:
    """
    Implements remote management of a Linux host (via ssh and sftp)
    """
    def __init__(self, config: HostConfig):
        self.config = config
        self.ssh = None

    def connect(self):
        if not self.ssh:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.config.server, 
                           self.config.port, 
                           self.config.username, 
                           self.config.password, 
                           key_filename=self.config.ssh_key)

            self.ssh = client
        else:
            raise ParasiteConnectException("Host already connected")
        
    
    def cp(self, src, dst, chmod = False):
        """
        Copy src to dst on remote host (create dst folder if does not exist)
        """
        sftp = self.ssh.open_sftp()

        dst_folder = os.path.dirname(dst)
        try:
            sftp.chdir(dst_folder)  # Test if remote_path exists
        except IOError:
            sftp.mkdir(dst_folder)  # Create remote_path
            sftp.chdir(dst_folder)
        
        sftp.put(src, dst)
        if chmod:
            sftp.chmod(dst, 0o777)
        sftp.close()




