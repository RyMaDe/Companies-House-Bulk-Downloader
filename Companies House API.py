import requests
import json
import urllib.request
import os #to clear the screen
import config #apikey

#global variables
apiKey = config.apiKey
url = 'https://api.companieshouse.gov.uk'
comp_search = '/search/companies?q=' #append search term

back = False
back_co = ""
back_off = ""
back_disq = ""
index = ""

def SearchIndex():
    """Initial page where user selects what to search"""

    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen

    global back, index
    back = False

    print("1) Companies")
    print("2) Officers")
    print("3) Disqualified Officers")
    index = input("Please select search option: ")

    if index == "1":
        memory.append((SelectCompany,None))
    elif index == "2":
        memory.append((SelectOfficer,None))
    elif index == "3":
        memory.append((SelectDisqOfficer,None))

def SelectDisqOfficer():
    """Search disqualified officers"""

    global back, back_disq, memory
    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen

    if back == False:
        term = input("Enter the name of a diqualified officer: ")
        if term == "":
            memory = [(SearchIndex,None)]
        back_disq = term
    else:
        term = back_disq
        back = False

    response = requests.get(url+"/search/disqualified-officers?q="+term, auth=(apiKey,"")).json()
    #Disqualified officer API get request

    num_items = min(response["total_results"], response["items_per_page"])

    for _ in range(num_items-1,-1,-1):
        print("[%d]" % _, end =" ")
        print(response["items"][_]["title"])
        print(response["items"][_]["description"])
        print(response["items"][_]["address_snippet"], "\n")

    if num_items>0:
        while True:
            disqOfficer = input("Select officer by number or type back to return (enter to restart): ")

            if disqOfficer.isdigit() and int(disqOfficer) in range(num_items):
                disqOfficerLink = response["items"][int(disqOfficer)]["links"]["self"]
                memory.append((DisqPersonPage,disqOfficerLink))
                break
            elif disqOfficer == "back":
                back = False
                break
            elif disqOfficer == "":
                memory = [(SearchIndex,None)]
                break

            print("\033[F",end = "\r") #to make the input line appear once only
            print(" "*(68+len(disqOfficer)))
            print("\033[F",end = "\r")

def DisqPersonPage(disqOfficer):
    """Provides the details of the disqualified officer"""

    global memory, back
    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
    disq_response = requests.get(url+disqOfficer, auth = (apiKey,"")).json()

    print(disq_response["forename"],disq_response["surname"])
    try:
        print(disq_response["date_of_birth"], "  ", disq_response["nationality"])
    except KeyError:
        pass
    print("Disqualified duration: ", end = " ")
    print(disq_response["disqualifications"][0]["disqualified_from"], end =" - ")
    print(disq_response["disqualifications"][0]["disqualified_until"], "\n")

    print("Disqualified for conduct while acting for:")
    print(disq_response["disqualifications"][0]["company_names"], "\n")

    print("Reasons:")
    print(disq_response["disqualifications"][0]["reason"]["act"])
    print(disq_response["disqualifications"][0]["reason"]["description_identifier"], "\n")

    Disq = input("Type back or press Enter to return: ")
    if Disq == "back":
        back = True
    memory.pop()

def SelectOfficer():
    """Search through officers of companies"""

    global back, back_off, memory
    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
    officerSearch = "/search/officers?q="

    if back == False:
        term = input("Enter the name of an officer: ")
        if term == "":
            memory = [(SearchIndex,None)]
        back_off = term
    else:
        term = back_off
        back = False

    response = requests.get(url+officerSearch+term, auth=(apiKey,'')).json()

    num_items = min(response['total_results'],response['items_per_page'])

    for _ in range(num_items-1,-1,-1):
        print("[%d]" % _, end =" ")
        print(response["items"][_]["title"])
        print(response["items"][_]["description"])
        print(response["items"][_]["address_snippet"], "\n")

    if num_items>0:
        while True:
            officer = input("Select officer by number or type back to return (enter to restart): ")
            if officer.isdigit() and int(officer) in range(num_items):
                officerLink = response["items"][int(officer)]["links"]["self"]
                memory.append((PersonPage,officerLink))
                break
            elif officer == "back":
                back = False
                break
            elif officer == "":
                memory = [(SearchIndex,None)]
                break

            print("\033[F",end = "\r") #to make the input line appear once only
            print(" "*(68+len(officer)))
            print("\033[F",end = "\r")

def SelectCompany():
    """Search for UK companies"""

    global back, back_co, memory

    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
    if back == False:
        term = input("Enter the name of a UK Company: ")
        if term =="":
            memory = [(SearchIndex,None)]
        back_co=term
    else:
        term = back_co
        back = False
    response = requests.get(url+comp_search+term, auth=(apiKey,'')).json()

    num_items = min(response['total_results'], response['items_per_page'])
    for _ in range(num_items-1,-1,-1):
        print("[%d]" % _, end = "  ")
        print(response['items'][_]['title'])
        print(response['items'][_]['company_number'])
        print(response['items'][_]['address_snippet'],"\n")

    if num_items>0: #If User enters input that produces results
        while True:
            company = input("Select company by number for further details (or type back to return): ")

            if company.isdigit() and int(company) in range(num_items):
                company = response['items'][int(company)]['links']['self']#url of the company
                memory.append((CompanyPage,company))
                break
            elif company == "back":
                back = False
                break
            elif company == "":
                memory = [(SearchIndex,None)]
                break

            print("\033[F",end = "\r") #to make the input line appear once only
            print(" "*(71+len(company)))
            print("\033[F",end = "\r")

def CompanyPage(company):
    """Page that shows details of the company
    
    You can also navigate to the officers and the
    filing history of the company.    
    """

    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
    global memory, back, index

    comp_response = requests.get(url+company, auth=(apiKey,'')).json()

    print(comp_response['company_name'])
    print("Company Number:", comp_response['company_number'])
    print("Status:", comp_response['company_status'])
    print("Incorporated:", comp_response['date_of_creation'])
    if comp_response['company_status'] == "dissolved":
        print("Cessation:",comp_response['date_of_cessation'])
    print("\n"+comp_response['registered_office_address']['address_line_1'])
    try:
        print(comp_response['registered_office_address']['locality'], end=", ")
    except:
        pass
    print(comp_response['registered_office_address']['postal_code'],"\n")
    try:
        print("Prior accounts made to: ", comp_response['accounts']['last_accounts']['period_end_on'])
    except:
        pass
    try:
        print("Next accounts made to: ", comp_response['accounts']['next_made_up_to'])
    except:
        pass
    try:
        print("Next accounts due: ", comp_response['accounts']['next_accounts']['due_on'])
    except:
        pass

    print("\n(Type back to return to search results or anything to start again)")
    print("1) Access Filing")
    print("2) Access People")
    access = input("Access: ")

    if access.isdigit() and int(access) in range(1,3):
        if int(access) == 1:
            memory.append((FilingHistory,comp_response))
        elif int(access) == 2:
            memory.append((People,comp_response))
    elif access == "back":
        if len(memory)==3: #So that when starting fresh (memory is empty), it doesn't show previous search results
            back = True
        memory.pop()
    else:
        if index == "1":
            memory = [(SearchIndex,None), (SelectCompany,None)]
        elif index == "2":
            memory = [(SearchIndex,None), (SelectOfficer,None)]

def People(comp_response):
    """Shows list of people involved in a business"""

    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
    global url, memory, index
    #Officers
    officers = comp_response['links']['officers']
    officers_response = requests.get(url+officers+"?q=&items_per_page=100", auth =(apiKey,'')).json()

    officers_num = min(officers_response["active_count"],officers_response["items_per_page"])
    print("ACTIVE OFFICERS:")
    print("Name",end =" "*50)
    print("Role", end=" "*30)
    print("Appointed")

    total = 0
    count = 0
    total_num = 0
    while True:
        total += officers_num
        for i in range(officers_num):
            print(str(total_num),officers_response["items"][i]["name"], end = " "*(54-len(officers_response["items"][i]["name"])-len(str(total_num))-1))
            print(officers_response["items"][i]["officer_role"], end = " "*(34-len(officers_response["items"][i]["officer_role"])))
            try:
                print(officers_response["items"][i]["appointed_on"])
            except KeyError:
                print("N/A")
            total_num+=1
        if total == officers_response["active_count"] or total ==1000:
            break
        else:
            count+=1
            officers_response = requests.get(url+officers+"?q=&items_per_page=100&start_index="+str(count)+"00", auth =(apiKey,'')).json()
            officers_num = min(officers_response["active_count"]-officers_response["start_index"],officers_response["items_per_page"])

    #PSC
    try:
        psc = comp_response['links']['persons_with_significant_control']
        psc_response = requests.get(url+psc, auth=(apiKey,'')).json()

    except KeyError:
        print("\nNo recorded Person with Significant Control")
    else:
        print("\nACTIVE PSC:")
        psc_num = min(psc_response["active_count"],psc_response["items_per_page"])
        for i in range(psc_num):
            print("Name:", psc_response["items"][i]["name"])
            print("Notified:", psc_response["items"][i]["notified_on"])
            try:
                print(psc_response["items"][i]["natures_of_control"][0].replace("-"," "))
                print(psc_response["items"][i]["natures_of_control"][1].replace("-"," "))
                print(psc_response["items"][i]["natures_of_control"][2].replace("-"," "))
            except:
                print(end = "\n")
            else:
                print(end = "\n")
    choice = input("Please select an officer or type back to return: ")

    if choice.isdigit() and 0<=int(choice)<officers_response["active_count"]:
        officers_response = requests.get(url+officers+"?q=&items_per_page=1&start_index="+choice, auth =(apiKey,'')).json()
        appointments = officers_response["items"][0]["links"]["officer"]["appointments"]

        memory.append((PersonPage,appointments))
    elif choice == "back":
        memory.pop()
    else:
        if index == "1":
            memory = [(SearchIndex,None), (SelectCompany,None)]
        elif index == "2":
            memory = [(SearchIndex,None), (SelectOfficer,None)]

def PersonPage(appointments):
    """Provides the details of a company officer
    
    This will also list the companies the officer is and has been
    involved in.
    """

    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
    global url, memory, index, back
    appointment_response = requests.get(url+appointments+"?q=&items_per_page=50", auth =(apiKey,'')).json()

    appointment_num = min(appointment_response["total_results"],appointment_response["items_per_page"])

    print(appointment_response["name"])
    try: #Some officers can be companies w/o DOB
        print(appointment_response["date_of_birth"]["month"],"/",appointment_response["date_of_birth"]["year"], end ="\n\n")
    except KeyError:
        pass
    total = appointment_num
    total_num=0
    while True:
        for i in range(appointment_num):
            print("[%d]" % total_num, end = " ")
            print(appointment_response["items"][i]["appointed_to"]["company_name"], end="   ")
            print(appointment_response["items"][i]["appointed_to"]["company_number"], end = "   ")
            print(appointment_response["items"][i]["appointed_to"]["company_status"])
            print("   ", "Role:", appointment_response["items"][i]["officer_role"], end ="   ")
            print("Appointed:", appointment_response["items"][i]["appointed_on"], end = "   ")
            try:
                print("RESIGNED:", appointment_response["items"][i]["resigned_on"], end = "\n\n")
            except KeyError:
                print("\n")
            total_num+=1
        if total == appointment_response["total_results"]:
            break
        else:
            appointment_response = requests.get(url+appointments+"?q=&items_per_page=50&start_index="+str(total), auth =(apiKey,'')).json()
            appointment_num = min(appointment_response["total_results"]-appointment_response["start_index"],appointment_response["items_per_page"])
            total+=appointment_num

    choice = input("Please select a company by number or type back to return: ")

    if choice.isdigit() and 0<=int(choice)<total_num:
        if int(choice)<=total_num-1-appointment_num: #time efficient as no need to make another get request if not necessary
            appointment_response = requests.get(url+appointments+"?q=&items_per_page=1&start_index="+choice, auth =(apiKey,'')).json()
            company = appointment_response["items"][0]["links"]["company"]
        else:
            company = appointment_response["items"][int(choice)-(total_num-appointment_num)]["links"]["company"]
        memory.append((CompanyPage,company))
    elif choice == "back":
        if len(memory) == 3:#So that when starting fresh (memory is empty), it doesn't show the previous search results
            back = True
        memory.pop()
    else:
        if index == "1":
            memory = [(SearchIndex,None), (SelectCompany,None)]
        elif index == "2":
            memory = [(SearchIndex,None), (SelectOfficer,None)]

def FilingHistory(comp_response):
    """Lists the filing history of a company"""

    global url, memory, index
    filing = comp_response['links']['filing_history']

    total = 0
    category=""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') #clear the screen
        
        dl_names = []
        filing_response = requests.get(url+filing+"?q=&start_index="+str(total)+"&category="+category,auth=(apiKey,'')).json()
        
        #print page number:
        print("page:", (total//25)+1,"of", filing_response['total_count']//25 +1)

        num_items = min(filing_response['total_count']-int(filing_response['start_index']),filing_response['items_per_page'])

        for file in range(num_items):
            print("[%d]" % file, end=" ")
            date1 = filing_response['items'][file]['date']+" "
            desc = filing_response['items'][file]['description']+" "
            if desc == "legacy ": #This provides more info for legacy docs
                desc = filing_response['items'][file]['description_values']["description"]+" "
            try:
                name = filing_response['items'][file]['description_values']['officer_name']+" "
            except:
                name = ""
            try:
                date2 = filing_response['items'][file]['action_date']
            except:
                date2=""

            #Cleaning up the description
            desc = desc.replace("-with-name", "")
            desc = desc.replace("-termination-date","")
            desc = desc.replace("-change-date","")
            desc = desc.replace("limited-liability-partnership", "llp")
            desc = desc.replace("with-accounts-type", "type")
            desc = desc.replace("-with-appointment-date", "")

            dl_name = date1+desc+name+date2
            dl_names.append(dl_name)
            print(dl_name)
        print("\n(Type back to return to the company page or anything to start again)")
        print("Type prev or next to navigate all history, or page followed by a number. Type filter and a term to filter.")
        files_to_dl = input("Select files by number to download: ").split() #enter the numbers

        if files_to_dl == ["back"]:
            memory.pop()
            break
        elif files_to_dl == []: #user enters a space or nothing at all
            if index == "1":
                memory = [(SearchIndex,None), (SelectCompany,None)]
            elif index == "2":
                memory = [(SearchIndex,None), (SelectOfficer,None)]
            break
        elif files_to_dl == ["next"]:
            if total+num_items < filing_response["total_count"]:
                total+=num_items
            else:
                input("This is the max range. Press enter to continue")
            pass
        elif files_to_dl == ["prev"]:
            if total > 0:
                total-=min(25,filing_response["total_count"])
            else:
                input("This is the first page. Press enter to continue")
            pass
        elif files_to_dl[0] == "page": #so user can navigate via page
            if len(files_to_dl) == 1:
                input("Please select a valid page that is in range. Press enter to continue")
            elif files_to_dl[1].isdigit()==True and int(files_to_dl[1]) in range(1,filing_response['total_count']//25 +2):
                total = 25*(int(files_to_dl[1])-1)
            else:
                input("Please select a valid page that is in range. Press enter to continue")
        elif files_to_dl[0] == "all": #type all to dowload everything
            FilingDownload(list(range(num_items)),filing_response,dl_names)
        elif files_to_dl[0] == "filter": # filter by: accounts
            if len(files_to_dl)==1:
                input("You must enter an item to filter by or enter off. Press enter to continue.")
            else:
                total = 0
                category = ""
                for item in files_to_dl[1:]:
                    if item == "accounts":
                        category += "accounts,"
                    elif item == "officers":
                        category+= "officers,"
                    elif item == "confstat":
                        category+= "confirmation-statement,"
                    elif item == "capital":
                        category+= "capital,"
                    elif item == "incorporation":
                        category+= "incorporation,"
                    elif item == "charges":
                        category+= "mortgage,"
                    elif item == "off":
                        category = ""
                        break
        else: #Download files
            if "".join(files_to_dl).isdigit():
                files_to_dl = list(map(int,files_to_dl))
                check = lambda x: True if x in range(num_items) else False
                if all(map(check, files_to_dl)):
                    FilingDownload(files_to_dl,filing_response,dl_names)
                else:
                    print("Invalid input. You must enter numbers in the correct range.")
                    input("Press enter to continue")
            else:
                if index == "1":
                    memory = [(SearchIndex,None), (SelectCompany,None)]
                elif index == "2":
                    memory = [(SearchIndex,None), (SelectOfficer,None)]
                break

def FilingDownload(files_to_dl,filing_response,dl_names):
    """Downloads files that have been selected and passed to it"""

    files_to_dl.sort()

    #find the names of all files in the directory to prevent overwriting
    names = set(f for f in os.listdir('.') if os.path.isfile(f))

    for file in files_to_dl:
        doc = filing_response['items'][file]['links']['self']
        url = "https://beta.companieshouse.gov.uk"+doc+"/document?format=pdf&download=1"

        #Below code is to make sure you are not overwriting files
        if dl_names[file]+".pdf" in names:
            count=1
            check = dl_names[file]+" ["+str(count)+"]"
            while check+".pdf" in names:
                count+= 1
                check = dl_names[file]+" ["+str(count)+"]"
            dl_names[file] = check
        names.add(dl_names[file]+".pdf")

        try: #Sometimes a link is provided in api but not accessible online
            urllib.request.urlretrieve(url, dl_names[file]+'.pdf')
        except:
            print("File", file, "is not available")

    print("Download complete")
    input("press enter to continue")

memory = [(SearchIndex,None)]
#Used to direct the program to the correct function

if __name__== "__main__":
    while True:
        if memory[-1][0] == SelectCompany:
            memory[-1][0]()
        elif memory[-1][0] == CompanyPage:
            memory[-1][0](memory[-1][1])
        elif memory[-1][0] == FilingHistory:
            memory[-1][0](memory[-1][1])
        elif memory[-1][0] == People:
            memory[-1][0](memory[-1][1])
        elif memory[-1][0] == PersonPage:
            memory[-1][0](memory[-1][1])
        elif memory[-1][0] == SearchIndex:
            memory[-1][0]()
        elif memory[-1][0] == SelectOfficer:
             memory[-1][0]()
        elif memory[-1][0] == SelectDisqOfficer:
             memory[-1][0]()
        elif memory[-1][0] == DisqPersonPage:
             memory[-1][0](memory[-1][1])
