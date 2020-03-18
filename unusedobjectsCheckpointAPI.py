#import the used modules
import requests, json, urllib3, os.path, datetime

#Disable the warning that the certificate is not a valid one.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# fucntion to do the API call
def api_call(command, json_payload, sid):
    try:
        #Compose the URL that we are going to send to mgmt server of Check Point
        url = 'https://' + ip_addr + ':' + str(port) + '/web_api/' + command
        #Compose the headers for the API call.
        if sid == '':
            request_headers = {'Content-Type': 'application/json'}
        else:
            request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}
        #The post with the module requests.
        r = requests.post(url, data=json.dumps(json_payload), headers=request_headers, verify=False)
        return r.json()
    except:
        print("API call failed")


# function to login to Check Point management server
def login():
    try:
        payload = {'user': user, 'password': password}
        # API call to login
        response = api_call('login', payload, '')
        return response["sid"]
    except:
        return response["message"]


# function to end the session (logout) with Check Point mgmt server.
def logout(sid):
    try:
        payload = {}
        response = api_call('logout', payload, sid)
        return response["message"]
    except:
        return response["message"]


#Function to call the unusedobject from Check Point mgmt server.
def showunusedobjects(limit):
    try:
        payload = {'limit': limit}
        response = api_call('show-unused-objects', payload, sid)
        return response["objects"]
    except:
        return response["message"]

# IP address of the management server
ip_addr = 'X.X.X.X'
# Port number for the API call (default:443)
port = 'Port'
# username to login the mgmt server
user = 'Username'
# matching password of user
password = 'Password'
# Login to get sid
sid = login()

try:
    #Define log file name
    logfilename = "unusedhostobjectlist.txt"
    #create log file and overwrite the content. More information: https://www.w3schools.com/python/python_file_write.asp
    hostlist = open(logfilename,"w")
    #Write header to file
    hostlist.write("Name - ipv4 ")
    hostlist.write("\n")
except:
    print("Error with creating log file.")
try:
    #create JSON file name
    JSONfilename = "unusedhostobjectlist.json"
    #create JSON file and overwrite the content
    JSONfile = open(JSONfilename,"w")
except:
    print("Error with creating JSON file.")

# Get x (1-500) number of unused object from the mgmt server.
hosts = showunusedobjects('500')

# variable to determine what previous key was
x = "Other"
#Loop through the list of unused objects.  More information: https://www.w3schools.com/python/python_lists.asp
#Each item is a dictionary. More information: https://www.w3schools.com/python/python_dictionaries.asp
for host in hosts:
    #Create the JSON file by adding row by row
    JSONfile.write(str(host))
    #Go to newline in file
    JSONfile.write("\n")
    #Type of object
    objecttype = host.get("type")
    #Check if the object type is host (you can also do this for group, network, service-tcp, dynamic-object, ...)
    #More information: https://www.w3schools.com/python/python_conditions.asp
    if objecttype == "host":
        #Loop each item of Dictionary to see the values of the unused host objects
        for value in host:
            #We are only interested in the keys: name and ipv4-address
            if value == "name":
                #Check what previous key was. If it's Other than the previous key was something else than name and write only the value to file.
                if x == "Other":
                    #Write only the value to the file
                    hostlist.write(host[value])
                #Check what previous key was. If it's Name than write first an newline to the file and than the key value.
                elif x == "Name":
                    hostlist.write("\n")
                    hostlist.write(host[value])
                x = "Name"
            #Check if de key value is ipv4-address and if this is true then write a dash and the key value to file.
            if value == "ipv4-address":
                hostlist.write(" - ")
                hostlist.write(host[value])
                x == "Other"

#Close the log and JSON file. It is a good practice to always close the file when you are done with it.
#More information: https://www.w3schools.com/python/python_file_open.asp
hostlist.close()
JSONfile.close()
#Logout by the mgmt server of Check Point
logoutmessage = logout(sid)
print(logoutmessage)
