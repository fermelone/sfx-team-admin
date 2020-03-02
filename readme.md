# Admin Scripts

## Required configuration
Please populate the `config.yaml` with your
- User API Access Token (which can be gathered from your profile screen inside the organization)
- Realm

## Creating a new team & adding members to it

To create a Team and add member to the created team, simply populate the `members.txt` file with the emails to invite, one per line

`members.txt` example:

    email1@example.com
    email2@example.com
    email3@example.com

Then, when executing the create-team.py script, pass the -t "team name" param

Example: `python create-team.py -t "Customer Name Team"`

## Removing a team, its members and their user dashboard groups (basically cleaning-up)

To remove a Team and all its members, simply populate the `members.txt` file with the emails of the members to remove (we need this to double confirm what we are removing, including their dashboard groups), one per line

`members.txt` example:

    email1@example.com
    email2@example.com
    email3@example.com

Then, when executing the remove-team.py script, pass the -t "team name" param (optional -m for members file path)

Example: `python remove-team.py -t "Customer Name Team"`

The removal process performs the following steps:
- Retrieve the team information based on the team name specified
- Delete the team
- Delete its members
- Retrieve the member's dashboard group's info
- Delete the member's dashboard groups
