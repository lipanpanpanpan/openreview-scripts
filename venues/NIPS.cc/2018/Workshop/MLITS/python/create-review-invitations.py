#!/usr/bin/python

###############################################################################
# ex. python create-invitations.py --conf MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# To be run after submission due date to create review invitations for all the papers.
# For each paper:
# 1) create authorGroup (can see reviews, can't write a review)
#           reviewer group (reviewers for this paper)
#           and nonReviewerGroup (folks that aren't allowed to read the review at least not yet)
# 2) create review invitation
###############################################################################

## Import statements
import argparse

from openreview import *
import config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connecting to "+client.baseurl)

submissions = client.get_notes(invitation=config.SUBMISSION)
for paper in submissions:
    paper_num = str(paper.number)
    paperinv = config.CONFERENCE_ID + '/-/Paper' + paper_num
    print("Adding groups for Paper"+ paper_num)

    ## Paper Group
    paperGroup = config.CONFERENCE_ID + '/Paper' + paper_num
    client.post_group(openreview.Group(
        id=paperGroup,
        signatures=[config.CONFERENCE_ID],
        writers=[config.CONFERENCE_ID],
        members=[],
        readers=['everyone'],
        signatories=[]))

    ## Author group
    authorGroup = paperGroup + '/Authors'
    client.post_group(openreview.Group(
        id=authorGroup,
        signatures=[config.CONFERENCE_ID],
        writers=[config.CONFERENCE_ID],
        members=paper.content['authorids'],
        readers=[config.CONFERENCE_ID, config.PROGRAM_CHAIRS, authorGroup],
        signatories=[]))

    ## Reviewer group - people that can see the review invitation
    reviewerGroup = paperGroup + '/Reviewers'
    client.post_group(openreview.Group(
        id=reviewerGroup,
        signatures=[config.CONFERENCE_ID],
        writers=[config.CONFERENCE_ID],
        members=[],
        readers=[config.CONFERENCE_ID, config.PROGRAM_CHAIRS],
        signatories=[]))

    ## review invitation
    review_reply = {
        'forum':paper.id,
        'replyto':paper.id,
        'writers':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'signatures':{'values-regex': paperGroup + '/AnonReviewer[0-9]+'},
        'readers':{
            'values': [config.CONFERENCE_ID, config.PROGRAM_CHAIRS],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content':config.review_content
    }

    review_parameters = config.review_params
    review_parameters['reply'] = review_reply
    review_parameters['invitees'] = [paperGroup + '/Reviewers']
    invite = openreview.Invitation(paperinv + '/Official_Review',**review_parameters)

    client.post_invitation(invite)
