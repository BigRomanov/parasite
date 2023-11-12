import os
import sys
import paramiko
from scp import SCPClient

from parasite.host.config import HostConfig
from exceptions import *
from decorators import connected


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
        
    
    def connected(self) -> bool:
        if not self.ssh.is_active():
            return False
        
        # use the code below if is_active() returns True
        try:
            transport = self.ssh.get_transport()
            transport.send_ignore()
        except EOFError as e:
            return False
        return True
    
    @connected
    def run(self, cmd, as_root=False):
        stdin, stdout, stderr = self.ssh.exec_command(f'echo {self.config.password} | sudo -S {cmd}' if as_root else cmd, get_pty=True)
    
        status = stdout.channel.recv_exit_status()
        if status != 0:
            print(f"Status: {status}")    
            for line in stderr.readlines():
                print(f"ERR > {line}")
        else:
            for line in stdout.readlines():
                print(f"OUT > {line}")

        return stdin, stdout, stderr
    
    @connected
    def cp(self, src, dst, chmod = False) -> None:
        """
        Copy src to dst on remote host (create dst folder if does not exist)
        """
        if not self.connected():
            raise ParasiteDisconnected()
        
        # TODO: Refactor to ensure folder
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




