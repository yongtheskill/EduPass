TO SSH INTO SERVER:
--
eb ssh <p>
source /opt/python/run/venv/bin/activate <p>
source /opt/python/current/env<p>
cd /opt/python/current/app<p>
python manage.py (commands)


<p>

<h1>SIMULATE FINGERPRINT SENSOR SUCCESS/FAIL</h1>
<p>payment/auth/success/</p>
<p>payment/auth/fail/</p>
--
<p>Payment status:</p>
<p>payment/auth/status/<p>

<p>
<h1>Raspberry pi config</h1>
--
<a href="https://tutorials-raspberrypi.com/how-to-use-raspberry-pi-fingerprint-sensor-authentication/">Fingerprint sensor site</a>

<p></p>
<p>sudo bash</p>
<p>wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | apt-key add -</p>
<p>wget http://apt.pm-codeworks.de/pm-codeworks.list -P /etc/apt/sources.list.d/</p>
<p>apt-get update</p>
<p>apt-get install python-fingerprint --yes</p>
--
<p>Code</p>
<p>pip install requests</p>
