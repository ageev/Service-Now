import requests, json, csv

template_request = dict.fromkeys(["caller_id", "location", "category", "subcategory", "impact", "urgency", "short_description", "description", "state", "assignment_group"])

usernames = {'PROD' : 'name1', 'DEV' : 'name2', 'SANDBOX' : 'name3' }
passwords = {'PROD' : 'DasIstMeinP@ssw0rd!', 'DEV' : 'DasIstMeinP@ssw0rd!', 'SANDBOX' : 'DasIstMeinP@ssw0rd!' }
urls = {'PROD' : 'https://prod.service-now.com', 'DEV' : 'https://dev.service-now.com', 'SANDBOX' : 'https://sandbox.service-now.com' }

def set_environment():
    global environment, input_file, ticket_log

    environment = "PROD"
    input_file = "input.csv"
    ticket_log = "tickets.log"
    # to do - set the environment based on users input or cmd arguments. Default to sandbox

def main():
    # step 0. Choose the einvironment
    set_environment()

    # step 1. Read the input data to set of dicts. One dict per future ticket per string in CSV file
    csvfile = open(input_file, 'r')
    data = list(csv.DictReader(csvfile, delimiter=',', dialect='excel'))  # list() will read everything in memory
    csvfile.close()

    # add missing fields to the data array based on template
    for r in data:
        ticket_data = template_request.copy()
        ticket_data.update(r)
        ticket_number = create_incident(ticket_data)
        print(f'[+] Incident {ticket_number} created in {environment}')
        with open(ticket_log, 'a') as f:
            f.write(ticket_number + '\n')

def create_incident(data):
    url = f"{urls[environment]}/api/now/table/incident?sysparm_display_value=true"

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # data = {"caller_id" : "",
    #         "location" : "", 
    #         "category" : "Information Security",
    #         "subcategory" : "Phishing",
    #         "impact" : "2",
    #         "urgency" : "2",
    #         "short_description" : "This is a Test", #subject
    #         "description" : "Something went wrong",
    #         "state" : "1",
    #         "assignment_group" : "IT",
    #         #"assigned_to":"John Smith",
    #         }


    response = requests.post(url, auth=(usernames[environment], passwords[environment]), headers=headers ,data=json.dumps(data))
    #print(json.dumps(data, indent=4, sort_keys=True))

    # Check for HTTP codes other than 201
    if response.status_code == 201: 
        #print (json.dumps(response.json(), indent=4, sort_keys=True))
        try:
            return response.json()['result']['number']
        except Exception as e:
            print(f'[!] Error: {e!r}')
            #continue
    else:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json(), 'Data:', json.dumps(data))
        exit()


if __name__ == "__main__":
        main()