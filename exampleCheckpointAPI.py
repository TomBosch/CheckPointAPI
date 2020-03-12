import requests, json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#fucntion to do the API call
def api_call(command, json_payload, sid):
    try:
        url = 'https://' + ip_addr + ':' + str(port) + '/web_api/' + command
        if sid == '':
            request_headers = {'Content-Type': 'application/json'}
        else:
            request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}
        r = requests.post(url, data=json.dumps(json_payload), headers=request_headers, verify=False)
        return r.json()
    except:
        print("API call failed")


#function to login to Checkpoint management server
def login():
    try:
        payload = {'user': user, 'password': password}
        #API call to login
        response = api_call('login', payload, '')
        return response["sid"]
    except:
        return response["message"]


#function to end the session (logout)
def logout(sid):
    try:
        payload = {}
        response = api_call('logout', payload, sid)
        return response["message"]
    except:
        return response["message"]


#function to show one specific host
def showhost(name):
    try:
        payload = {'name': name}
        response = api_call('show-host', payload, sid)
        return response["name"]
    except:
        return response["message"]


#function to show x (variable limit) number of hosts
def showhosts(limit):
    try:
        payload = {'limit': limit}
        response = api_call('show-hosts', payload, sid)
        return response["objects"]
    except:
        return response["message"]


#IP address of the management server
ip_addr = 'X.X.X.X'
#Port number for the API call : default 443
port = 'XXX'
#username to login the mgmt server
user = 'username'
#matching password of user
password = 'password'
#Login to get sid
sid = login()

#print("session id: " + sid)
host = showhost('servername')
print(host)
#print x number of  hosts
hosts = showhosts('2')
print(json.dumps(hosts))
logoutmessage = logout(sid)
print(logoutmessage)
