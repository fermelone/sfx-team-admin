import json
import requests
import base64
import yaml
import argparse

## Arguments
parser = argparse.ArgumentParser(description='SignalFx - Team Deletion')
parser.add_argument('-t', '--teamname', help='Specify the team name to be deleted', default='')
parser.add_argument('-m', '--membersFile', help='Specify the name of the file where the member list is located', default='members.txt')
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
def retrieve_team():
    print('> Searching for a team with the term: ' + args['teamname'])
    response = requests.get(sfx_api + '/team'+'?'+'limit=1'+'&'+'name='+args['teamname'] , headers=headers)
    teamData = json.loads(response.content)

    if len(teamData['results']) < 1: # Basically this means there's results found or not
        print("ERROR >> Couldn't find any team with the name: " + args['teamname'])
        return [] 
    else:
        #TODO show the name of the team and get confirmation from the user before continuing
        print("> Found team: " + teamData['results'][0]['name'])
        return teamData['results'][0] # Return first element based on content

def delete_team(teamId):
    print('>> Deleting team based on found id: ' + str(teamId))
    response = requests.delete(sfx_api + '/team/'+ teamId , headers=headers)
    #TODO get confirmation that the team was deleted

def delete_members(membersIdList):
    print('> Deleting ' + str(len(membersIdList)) + ' members')
    for member in membersIdList:
        response = requests.delete(sfx_api + '/organization/member/'+ member , headers=headers)
        print('>> Deleting member id: ' + member)
        #TODO confirm somehow that there are no issues when deleting each member

def retrieve_dashboard_groups(membersList):
    print('> Retrieving user dashboard groups')
    dashboardIdList = []
    for member in membersList:
        querystring = {"name":member}
        response = requests.get(sfx_api + '/dashboardgroup' , headers=headers, params=querystring)
        dashboardIdList.append(json.loads(response.content)['results'][0]['id'])
    
    return dashboardIdList

def remove_dashboard_groups(dashboardIdList):
    print('> Removing ' + str(len(dashboardIdList)) + ' user dashboard groups')
    for dashboardGroup in dashboardIdList:
        response = requests.delete(sfx_api + '/dashboardgroup/'+ dashboardGroup , headers=headers)
        print('>> Deleting dashboard group id: ' + dashboardGroup)
        #TODO confirm somehow that there are no issues when deleting each member

def remove_team():
    print('>> Team Remover <<')
    print('--------------------------')
    # Find a team based on -t search term passed
    foundTeamData = retrieve_team()
    # basically don't do anything if we can't find a team with the search term specified
    if len(foundTeamData) > 1:
        # Call delete_team with the results of finding a specified team
        delete_team(foundTeamData['id'])
        # Delete the members found previously
        delete_members(foundTeamData['members'])
        # Get the email list from a file and then passes it to retrieve_dashboard_groups
        # Create the members array
        members_array = []
        with open(args['membersFile']) as members_file:
            for member in members_file:
                members_array.append(member.rstrip('\n'))
        # Retrieves a list of user dashboard group IDs        
        dashboardIdList = retrieve_dashboard_groups(members_array)
        # Deletes the dashboard groups
        remove_dashboard_groups(dashboardIdList)
        print('> Team deletion complete')

if __name__ == "__main__":
    remove_team()