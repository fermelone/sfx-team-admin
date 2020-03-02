import json
import requests
import base64
import yaml
import argparse

## Arguments
parser = argparse.ArgumentParser(description='SignalFx - Team Creator')
parser.add_argument('-t', '--teamname', help='Specify the team name to be created', default='Customer Team')
args = vars(parser.parse_args())

## Configuration
# Load configuration file
with open('config.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Set SFx Base API URL
sfx_api = 'https://api.' + cfg['signalfx']['realm'] + '.signalfx.com/v2'

# Set SignalFx API headers
headers = {
    'Content-Type': 'application/json',
    'X-SF-TOKEN': cfg['signalfx']['session_token']
}

## Functions
def invite_members():
    # Create the members array
    members_array = []
    with open('members.txt') as members_file:
        for member in members_file:
            members_array.append({
                "email":member.rstrip('\n')
        })
    # Create JSON payload members to be added
    memberData = {
        "members" : members_array
    }
    print('> Creating team for ' + str(len(memberData["members"])) + ' users...')
    response = requests.post(sfx_api + '/organization/members', headers=headers, json=memberData)
    print("Response: Status code: ", response.status_code)
    return response.content

def create_team(invitedMembers):
    invitedMemberIds = []

    for invitedMember in invitedMembers["members"]:
        invitedMemberIds.append(invitedMember["id"])
    
    teamData = {
        "name": args['teamname'],
        "members": invitedMemberIds
    }

    requests.post(sfx_api + '/team', headers=headers, json=teamData)

def create_team():
    print('>> Team Creator <<')
    print('--------------------------')
    # Invite members
    inviteResult = invite_members()
    # Create team with invited members
    create_team(json.loads(inviteResult))
    print('> Team creation complete')

if __name__ == "__main__":
    create_team()