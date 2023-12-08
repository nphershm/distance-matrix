#Distance Matrix v2
# URL Constructor
# Nick Hershman\
## updated 20220924 - used addresses for DAO and DAF...

import json
import requests
import time
from datetime import datetime
from license import api_key ## provides google api license for distance matrix

# Creates URL for distance matrix.


## My functions
def get_origin_str(origins = []):    
    origins_str = ''
    for i in origins:
        origins_str += i.replace(' ','+')
        origins_str += '|'
    origins_str = origins_str[:-1]
    return origins_str

def get_URL(origins = '', destinations = ''):
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='
    url = base_url + origins + '&destinations=' + destinations +'&key='+ api_key
    return url

def parse_json(fname = 'distmatrix2.json',origin_names =[], my_data = []): 
    """ Parses the response to give driving distances to tenths of a mile
    between locations. """
    # pass
    data = ''
    # print('parse_json for',len(origin_names),'origins')
    # print(origin_names)

    if not my_data:
        with open(fname, 'r', encoding='utf-8') as myfile:
            data=json.load(myfile)
    else:
        data = my_data

    distmatrix = []
    for i in range(len(data['rows'])):
        #print('From',origins[i])
        this_row = data['rows'][i] #orig school name
        row_data = [origin_names[i]]
        for j in range(len(this_row['elements'])):
            row_data.append(this_row['elements'][j]['distance']['text']+' ('+this_row['elements'][j]['duration']['text']+')')
        distmatrix.append(row_data)
    return distmatrix

def display_responses(responses = [], address_dict = {}):
    ## origins stay same for
    num_extra = int(len(responses)**.5)
    my_data = {} #origin, distances...
    
    for i in range(len(responses)):
        ##if i % num_extra == 0: ## new orig_group...
        ##print('\n***')
        ## Don't need to show origins --- they are listed by address_dict call.
        ## print('Origins:')
        ## for k in responses[i][0]: print(address_dict[k])
        #print('Destinations:')
        ## for k in responses[i][1]: print(address_dict[k])

        #print('Data')
        for l in responses[i][2]:
            this_origin = address_dict[l[0]]
            this_origin_data_str = ','.join(map(str,l[1:len(l)]))
            # print(this_origin+','+this_origin_data_str)

            if this_origin in my_data.keys(): ## append values
                my_data[this_origin] = my_data[this_origin]+','+this_origin_data_str
            else:
                my_data[this_origin] = this_origin_data_str
    results = ''
    for k, v in my_data.items():
        results += k+','+v+'\n'
    return(results)

origins = []

district = {'DAO': '1260 NW Waterhouse Ave Beaverton OR',
            'DAF': '16550 SW Merlo Rd Beaverton OR',
            '5th Street': '10615 SW 5th St Beaverton OR'}

es = {
    'Aloha-Huber Park':'5000 SW 173rd Ave Beaverton OR 97007',
    'Barnes':'13730 SW Walker Rd Beaverton OR 97005',
    'Beaver Acres':'2125 SW 170th Ave Beaverton OR 97003',
    'Bethany':'3305 NW 174th Ave Beaverton OR 97006',
    'Bonny Slope':'11775 NW McDaniel Rd Portland OR 97229',
    'Cedar Mill':'10265 NW Cornell Rd Portland OR 97229',
    'Chehalem':'15555 SW Davis Rd Beaverton OR 97007',
    'Cooper Mountain':'7670 SW 170th Ave Beaverton OR 97007',
    'Elmonica':'16950 SW Lisa Ct Beaverton OR 97006',
    'Errol Hassell':'18100 SW Bany Rd Beaverton OR 97007',
    'Findley':'4155 NW Saltzman Rd Portland OR 97229',
    'Fir Grove':'6300 SW Wilson Ave Beaverton OR 97008',
    'Greenway':'9150 SW Downing Dr Beaverton OR 97008',
    'Hazeldale':'20080 SW Farmington Rd Beaverton OR 97007',
    'Hiteon':'13800 SW Brockman Rd Beaverton OR 97008',
    'Jacob Wismer':'5477 NW Skycrest Pkwy Portland OR 97229',
    'Kinnaman':'4205 SW 193rd Ave Aloha OR 97078',
    'Mckay':'7485 SW Scholls Ferry Rd Beaverton OR 97008',
    'McKinley':'1500 NW 185th Ave Beaverton OR 97006',
    'Montclair':'7250 S Vermont St Portland OR 97223',
    'Nancy Ryles':'10250 SW Cormorant Dr Beaverton OR 97007',
    'Oak Hills':'2625 NW 153rd Ave Beaverton OR 97006',
    'Raleigh Hills':'5225 SW Scholls Ferry Rd Portland OR 97225',
    'Raleigh Park':'3670 SW 78th Ave Portland OR 97225',
    'Ridgewood':'10100 SW Inglewood St Portland OR 97225',
    'Rock Creek':'4125 NW 185th Ave Portland OR 97229',
    'Sato':'7775 NW Kaiser Rd Portland OR 97229',
    'Scholls Heights':'16400 SW Loon Dr, Beaverton, OR 97007',
    'Sexton Mountain': '15645 SW Sexton Mountain Rd Beaverton OR 97007',
    'Springville K-8': '6655 NW Joss Ave Portland OR 97229',
    'Terra Linda': '1998 NW 143rd Ave Portland OR 97229',
    'Vose':'11350 SW Denney Rd Beaverton OR 97008',
    'West Tualatin View':'8800 SW Leahy Rd Portland OR 97225',
    'William Walker':'2350 SW Cedar Hills Blvd Beaverton OR 97005'
}

ms = {
    'Cedar Park':'11100 SW Park Way Portland OR 97225', #Cedar Park 
    'Conestoga':'12250 SW Conestoga Dr Beaverton OR 97008', #Conestoga 
    'Meadow Park':'14100 SW Downing St Beaverton OR 97006 ', #Meadow Park 
    'Five Oaks':'1600 NW 173rd Ave Beaverton OR 97006', #Five Oaks 
    'Stoller':'14141 NW Laidlaw Rd Portland OR 97229', #Stoller 
    'Mountain View':'17500 SW Farmington Rd Beaverton OR 97007', #Mt View 
    'Tumwater':'650 NW 118th Ave Portland OR 97229', #Tumwater
    'Whitford':'7935 SW Scholls Ferry Rd Beaverton OR 97008', #Whitford
    'Highland Park':'7000 SW Wilson Ave Beaverton OR 97008' #Highland Park 
}

k8 = {
    'Aloha-Huber Park':'5000 SW 173rd Ave Beaverton OR 97007', #Aloha-Huber Park 
    'Springville':'6655 NW Joss Ave Portland OR 97229', #Springville 
    'Raleigh Hills':'5225 SW Scholls Ferry Rd Portland OR 97225' #Raleigh Hills 
    }

opt = {
    'ACMA':'11375 SW Center St Beaverton OR 97005', #ACMA
    'ISB':'17770 SW Blanton St Beaverton OR 97078', #ISB
    'BASE':'10740 NE Walker Rd Hillsboro OR 97006', #BASE
    'FLEX':'10740 NE Walker Rd Suite B Hillsboro OR 97006' #FLEX
    }

hs = {
    'Aloha HS':'18550 SW Kinnaman Rd Aloha OR 97007', #Aloha 
    'Beaverton HS':'13000 SW 2nd St Beaverton OR 97005', #Beaverton
    'Mountainside HS':'12500 SW 175th Ave Beaverton OR 97007', #Mountainside
    'Southridge HS':'9625 SW 125th Ave Beaverton OR 97008', #Southridge
    'Sunset HS':'13840 NW Cornell Rd Portland OR 97229', #Sunset 
    'Westview HS':'4200 NW 185th Ave Portland OR 97229' #Westview
    }

other = {
    'Community School/Merlo':'1841 SW Merlo Dr Beaverton OR 97006', #Community School
    'Early College HS': '17705 NW Springville Rd, Portland, OR 97229', #Early College @ PCC Rock Creek
    'Terra Nova':'10351 NW Thompson Rd, Portland, OR 97229' #Terra Nova
    }


## construct dicts and address list
origins_dict = district | es | ms | opt | hs | other #builds dict of school:address

address_dict = dict([(value, key) for key, value in origins_dict.items()]) #creates address:school dict
addresses = []
for k, v in origins_dict.items():
    addresses.append(v)

## Check addresses
## for i in addresses: print(i, address_dict[i])

## How will the script work?
## errors out if request contains more than 25 origins or 25 destinations... but I can stack requests and then re-arrange from results...
## request one: origin[1] + destination 1
## request two: origin[1] + destination 2
## then combine results of destination 1 and 2  for origin[1] and meet limitations

max_items = 10
num_groups = int(len(addresses)/max_items)+1
print("There are",len(addresses),"addresses so we need",num_groups,"groups.")

num_Grequests = num_groups**2
my_input = input('Make '+str(num_Grequests)+' requests? At cost of '+str(.50*num_Grequests/1000)+'(y/n)?  ')

responses = []
results = ''
successes = 0
if (my_input) == 'y':
    for i in range(num_groups):
        my_orig = addresses[i*max_items:min(len(addresses),(i+1)*max_items)]
        for j in range(num_groups):
            my_dest = addresses[j*max_items:min(len(addresses),(j+1)*max_items)]
            ## troubleshoot these groupings...
            ## print('group',i,'-',j,'***')
            ## print('origins:',len(my_orig),'by destinations',len(my_dest))
            
            ## Construct request url
            my_orig_str = get_origin_str(my_orig)
            my_dest_str = get_origin_str(my_dest)
            my_url = get_URL(my_orig_str, my_dest_str)

            # Fetch distance_matrix
            print('fetching:***\n', my_url,'\n***')
            response = requests.get(my_url)
            data = response.json()

            sleep = 1
            while not data['status'] == "OK":
                sleep *= 2 #eponential backoff
                print('Error with google request... wait '+str(sleep) + ' seconds and try again')
                print(response.text)
                for k in range(sleep):
                    time.sleep(1)
                    print(k+1,end=' ')
                response = requests.get(my_url)
                data = response.json()
            if data['status'] == 'OK':
                successes += 1
                print('Successful request #' + str(successes)+'... woot!')
                responses.append((my_orig,my_dest,parse_json(origin_names = addresses[i*max_items:min(len(addresses),(i+1)*max_items)],
                                                             my_data = data)))
                ## print('Data appended to responses')
    ## now process responses
    ## responses((orig, dest, data (orig, dist, dist, dist,...))
    results = display_responses(responses, address_dict)

else: print('Distance Calculator stopped input: '+my_input)

my_input = input('Display results? (y/n)')

if my_input == "y": print(results)

## write distances-date.txt

today = datetime.today().strftime('%Y-%m-%d')
with open(f'distances-{today}.csv', 'w') as file:
    file.write(results)
