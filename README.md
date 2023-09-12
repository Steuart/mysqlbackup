0.You should be using python3 and debian OS like me!

1.Upload the mian.py file to the /opt/mysqlbackup directory on the server

2.Configure a system service
```shell
[Unit]
Description=MySQL Backup Service
After=network.target
 
[Service]
ExecStart=/usr/bin/python3 /opt/mysqlbackup/main.py
WorkingDirectory=/opt/mysqlbackup
User=root
Group=root
Restart=always
 
[Install]
WantedBy=multi-user.target
```

3.Enable service
```shell
systemctl enable mysqlbackup
systemctl start mysqlbackup
```
4.Check service status
```shell
systemctl status mysqlbackup

```
If all is well you will see app.log in the /opt/mysqlbackup directory