# Feed Logs to `Sentry`

1. Register at [Sentry](https://sentry.io)

2. Update your `~/.profile` File's Variable at `export SENTRY_DSN=` with your actual Value, and reload it:
   
   ```bash
   [~]$ source .profile
   ```
   
   and/or update `/opt/apps/uwsgi.ini` File's Variable at `env = SENTRY_DSN=` with your actual Value, and restart the `uWSGI` Service:
   
   ```bash
   [/opt/apps]$ sudo uwsgi --reload /tmp/project-master.pid
   ```

# Feed Logs to `Papertrail`

1. Register at [Papertrail](https://papertrailapp.com/)

2. Go to [Setup Logging]([SolarWinds Cloud](https://papertrailapp.com/systems/setup?type=app&platform=unix)) Page for Reference

3. Log in to the `EC2` Instance

4. Download and install `remote-syslog`
   
   ```bash
   [~]$ cd /opt/apps
   [/opt/apps]$ wget https://github.com/papertrail/remote_syslog2/releases/download/v0.21/remote-syslog2_0.21_amd64.deb
   [/opt/apps]$ sudo dpkg -i remote-syslog2_0.21_amd64.deb
   ```

5. Modify a Sample File `/opt/apps/2remember/deployment/etc/log_files.yml`, specifically this Section:
   
   ```yaml
   destination:
     host:     logs4.papertrailapp.com
     port:     50129
     protocol: tls
   ```
   
   with your specific Settings, and copy it to the final Destination:
   
   ```bash
   [/opt/apps]$ sudo cp /opt/apps/2remember/deployment/etc/log_files.yml /etc
   ```

6. Daemonize and collect messages:
   
   ```bash
   [/opt/apps]$ sudo remote_syslog
   ```
   
   and check, if it's running (refer to [Troubleshooting]([Unix and BSD text log files (remote_syslog2) - Papertrail](https://www.papertrail.com/help/configuring-centralized-logging-from-text-log-files-in-unix/#remote_syslog)))
   
   ```bash
   [/opt/apps]$ ps auxww | grep [r]emote_syslog
   ```
   
   You should see in Output something, like
   
   ```bash
   root         566  0.0  0.4 708288  4860 ?        Sl   02:18   0:00 remote_syslog -c /etc/log_files.yml --pid-file=/var/run/remote_syslog.pid
   ```

7. Auto-start (see [here](https://github.com/papertrail/remote_syslog2/tree/v0.21?tab=readme-ov-file#auto-starting-at-boot))
   
   ```bash
   [/opt/apps]$ cp /opt/apps/2remember/deployment/etc/init.d/remote_syslog /etc/init.d/remote_syslog
   [/opt/apps]$ chmod 755 /etc/init.d/remote_syslog
   ```

8. 
