# This script work with Cisco Firepower Management Center 6.4 and later
# for using this script please run it as example below:
# python.exe api_hitcoutn_v002.py http://<fmc_address> <username>
# this script check number of sensor and access policies and if there are more than
# one, ask you to choose your desirable sensor and access policy
# finally creates a excel file with name which distinguished by date, sensor name, access policy name

from pathlib import Path, PureWindowsPath
from openpyexcel import Workbook
from openpyexcel.styles import Color, PatternFill, Alignment, Font, Border, Side
from datetime import datetime
from requests.auth import HTTPBasicAuth

import os
import sys
import json
import requests
import urllib3
import getpass

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning)  # disable ssl warning


def dimensions(worksheet, column):
    # calculate width of cell
    column_len = 0
    for row in range(1, worksheet.max_row + 1):
        if len(str(worksheet.cell(row=row, column=column).value)) > column_len:
            column_len = len(worksheet.cell(row=row, column=column).value)
    return column_len


def cleaning_json(json_file, remove_item):
    # remove unwanted items in json file
    for item in remove_itme:
        for element in json_file['items']:
            element.pop(item, None)
    return json_file


if len(sys.argv) == 3:
    fmc_address = sys.argv[1]
    user = sys.argv[2]
    password = getpass.getpass(prompt='Password:\n')
else:
    print('USAGE Error!! \nInstruction:\n<https://fmc_address> <username>\n')
    exit()


domain_id = 'e276abec-e0f2-11e3-8169-6d9ed49b625f'

api_token_gen = '/api/fmc_platform/v1/auth/generatetoken'
api_sensor_id = f'/api/fmc_config/v1/domain/{domain_id}/devices/devicerecords?expanded=false'
api_access_policies = f'/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies?expanded=true'

url = fmc_address
uri_token_gen = url + api_token_gen
uri_sensor_id = url + api_sensor_id
uri_access_policies = url + api_access_policies

error_responde_code = [400, 401, 422]

# start generate token
# use token[0] as X-auth-access-token
# use toen[1] as X-auth-refresh-token

token = []

try:
    token_req = requests.post(url=uri_token_gen, auth=HTTPBasicAuth(
        user, password), verify=False,)

except requests.exceptions.Timeout:
    print('A connection attempt failed!!! \nBecause the connected party did not properly respond after a period of time, \nor \nestablished connection failed because connected host has failed to respond\n\n')
    exit()
except requests.exceptions.ConnectionError:
    print('A connection attempt failed!!! \nBecause the connected party did not properly respond after a period of time, \nor \nestablished connection failed because connected host has failed to respond\n\n')
    exit()

try:
    token_req_report = json.loads(token_req.content)
    if token_req.status_code in error_responde_code:
        for message in token_req_report['error']['messages']:
            print(message['description'], '\n\n')
        exit()
except json.decoder.JSONDecodeError:
    pass

for key in token_req.headers:
    if key == 'X-auth-access-token':
        token.append(token_req.headers['X-auth-access-token'])
    if key == 'X-auth-refresh-token':
        token.append(token_req.headers['X-auth-refresh-token'])

# end generation token

headers = {'Accept': 'application/json', 'Content-type': 'application/json', 'X-auth-access-token':
           token[0], 'X-auth-refresh-token': token[1]}

# start get device id

get_sensor_id = requests.get(url=uri_sensor_id, verify=False, headers=headers)

sensors = json.loads(get_sensor_id.content)

if len(sensors['items']) > 1:
    for sensor in range(len(sensors['items'])):
        print(sensor, sensors['items'][sensor]['name'])
    enter_sensor_id = int(input('Select Sensor Number:\n'))
    sensor_id = sensors['items'][enter_sensor_id]['id']
    sensor_name = sensors['items'][enter_sensor_id]['name']
else:
    sensor_id = sensors['items'][0]['id']
    sensor_name = sensors['items'][0]['name']
    print(f'{sensor_name} Selcected as Sensor')

# end get device id

# start get access policies id
get_access_policies = requests.get(
    url=uri_access_policies, verify=False, headers=headers)

policies = json.loads(get_access_policies.content)

if len(policies['items']) > 1:
    for policie in range(len(policies['items'])):
        print(policie, policies['items'][policie]['name'])
    enter_policy_id = int(input('Select Policy Number:\n'))
    access_policies_id = policies['items'][enter_policy_id]['id']
    policy_name = policies['items'][enter_policy_id]['name']
else:
    access_policies_id = policies['items'][0]['id']
    policy_name = policies['items'][0]['name']
    print(f'{policy_name} is selected')

# end get access policies id

# start refrshing hit counts

api_refresh_hitcount = f'/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies/{access_policies_id}/operational/hitcounts?filter=deviceId:{sensor_id}'

uri_refresh_hit = url + api_refresh_hitcount

put_refresh_hit = requests.put(
    url=uri_refresh_hit, verify=False, headers=headers)

if put_refresh_hit.status_code == 202:
    print(
        f'Access Rule {policy_name} hitcount is refreshed on {sensor_name} Sensor')
else:
    print(f'Warning!\nAccess Rule {policy_name} Not REFRESHED!!!')

# end refrshing hit counts

# start get access rule hit count

api_rule_hits = f'/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies/{access_policies_id}/operational/hitcounts?filter=deviceId:{sensor_id}&expanded=true'

uri_rule_hits = url + api_rule_hits

get_hit_count = requests.get(url=uri_rule_hits, verify=False, headers=headers)

hit_count = json.loads(get_hit_count.content)


remove_itme = ['links', 'paging']

for item in remove_itme:
    for element in hit_count['items']:
        element.pop(item, None)

hitcount_file_process = hit_count['items']

hitcount_file = hitcount_file_process

wb = Workbook()
ws = wb.active
ws.title = 'Hit Counts'

# create table body
for rule in hitcount_file:
    ws.cell(row=hitcount_file.index(rule) + 2,
            column=1, value=rule['metadata']['ruleIndex'])
    ws.cell(row=hitcount_file.index(rule) + 2,
            column=2, value=rule['rule']['name'])
    ws.cell(row=hitcount_file.index(rule) + 2,
            column=3, value=rule['rule']['id'])
    ws.cell(row=hitcount_file.index(rule) + 2,
            column=4, value=rule['hitCount'])
    ws.cell(row=hitcount_file.index(rule) + 2,
            column=5, value=rule['firstHitTimeStamp'])
    ws.cell(row=hitcount_file.index(rule) + 2,
            column=6, value=rule['lastHitTimeStamp'])

# create header of table
ws.cell(row=1, column=1, value='Index')
ws.cell(row=1, column=2, value='Rule Name')
ws.cell(row=1, column=3, value='Rule ID')
ws.cell(row=1, column=4, value='Hit Counts')
ws.cell(row=1, column=5, value='First Hint')
ws.cell(row=1, column=6, value='Last Hint')

# add border and alignment for all cells
thin = Side(border_style='thin', color='000000')
for row_cordinate in range(1, ws.max_row + 1):
    for column_cordinate in range(1, ws.max_column + 1):
        cell = ws.cell(row=row_cordinate, column=column_cordinate)
        cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
        cell.alignment = Alignment(horizontal='center', vertical='center')

# change color of headers row
for column in range(1, ws.max_column + 1):
    header_column = ws.cell(row=1, column=column)
    header_column.fill = PatternFill('solid', fgColor='11485D')
    header_column.alignment = Alignment(horizontal='center', vertical='center')
    header_column.font = Font(b=True, color='FFFFFF')

# excel cell dimensions
ws.column_dimensions['A'].width = dimensions(ws, 1)
ws.column_dimensions['B'].width = dimensions(ws, 2)
ws.column_dimensions['C'].width = dimensions(ws, 3)
ws.column_dimensions['D'].width = dimensions(ws, 4)
ws.column_dimensions['E'].width = dimensions(ws, 5)
ws.column_dimensions['F'].width = dimensions(ws, 6)

time_now = datetime.now()

# save excel file in desktop
userprofile_dir = os.getenv('USERPROFILE')
save_directory = f"{userprofile_dir}\\Desktop\\{time_now.month}{time_now.day}{time_now.year}-{sensor_name}-{policy_name}-HeatCounts.xlsx"
wb.save(Path(save_directory))
print('Done!')
