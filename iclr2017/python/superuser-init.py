#!/usr/bin/python

"""
Setup python script takes as input the CSV files above and creates group for 
ICLR.cc/2017/pc, areachairs, individual ACs, reviewers-invited, and creates 
reviewers-invited.web Javascript for handling reviewer invitations; if they 
accept, their email address is added to group ICLR.cc/2017/reviewers.

"""

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('-a','--areachairs', help="csv file containing the email addresses of the area chairs")
parser.add_argument('-r','--reviewers', help="csv file containing the email addresses of the candidate reviewers")
parser.add_argument('-u','--baseurl', help="base URL for the server to connect to")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

if openreview.user['id'].lower()=='openreview.net':
    ## Initialize the groups list
    iclr            = Group('ICLR.cc',      
        readers     = ['OpenReview.net'], 
        writers     = ['OpenReview.net','ICLR.cc/2017/pcs'], 
        signatures  = ['OpenReview.net'], 
        signatories = ['ICLR.cc','ICLR.cc/2017/pcs'], 
        members     = [] )

    iclr2017        = Group('ICLR.cc/2017', 
        readers     = ['everyone'],       
        writers     = ['ICLR.cc','ICLR.cc/2017','ICLR.cc/2017/pcs'],  
        signatures  = ['ICLR.cc'], 
        signatories = ['ICLR.cc/2017','ICLR.cc/2017/pcs'], 
        members     = ['ICLR.cc/2017/pcs'], 
        web         = '../webfield/iclr2017_webfield.html')

    iclr2017conference = Group('ICLR.cc/2017/conference', 
        readers     = ['everyone'], 
        writers     = ['ICLR.cc/2017','ICLR.cc/2017/conference','ICLR.cc/2017/pcs'], 
        signatures  = ['ICLR.cc/2017'],
        signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'], 
        members     = ['ICLR.cc/2017/pcs'],  
        web         = '../webfield/iclr2017conference_webfield.html')

    iclr2017conferenceorganizers = Group('ICLR.cc/2017/conference/organizers',
        readers     = ['everyone'], 
        writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/organizers','ICLR.cc/2017/pcs'], 
        signatures  = ['ICLR.cc/2017/conference'],
        signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs', 'ICLR.cc/2017/conference/organizers'], 
        members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/conference'])

    iclr2017conferenceACsOrganizers = Group('ICLR.cc/2017/conference/ACs_and_organizers',
        readers     = ['everyone'],
        writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/ACs_and_organizers','ICLR.cc/2017/pcs'],
        signatures  = ['ICLR.cc/2017/conference'],
        signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/ACs_and_organizers'],
        members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs','ICLR.cc/2017/conference']
        )

    iclr2017reviewersACsOrganizers = Group('ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers',
        readers     = ['everyone'],
        writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers','ICLR.cc/2017/pcs'],
        signatures  = ['ICLR.cc/2017/conference'],
        signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers'],
        members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs','ICLR.cc/2017/conference/reviewers','ICLR.cc/2017/conference']
        )

    iclr2017workshop = Group('ICLR.cc/2017/workshop', 
        readers     = ['everyone'],
        writers     = ['ICLR.cc/2017','ICLR.cc/2017/pcs'],
        signatures  = ['ICLR.cc/2017'], 
        signatories = ['ICLR.cc/2017/workshop'],
        members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'], 
        web         = '../webfield/iclr2017workshop_webfield.html')

    groups = [iclr, iclr2017, iclr2017conference, iclr2017conferenceorganizers, iclr2017conferenceACsOrganizers,iclr2017reviewersACsOrganizers, iclr2017workshop]

    iclr2017programchairs = Group('ICLR.cc/2017/pcs', 
                                readers=['everyone'], 
                                writers=['ICLR.cc/2017'],
                                signatures=['ICLR.cc/2017'],
                                signatories=['ICLR.cc/2017/pcs'],
                                members=[]) 
    ## Read in a csv file with the names of the program chair(s).
    ## Each name in the csv will be set as a member of ICLR.cc/2017/pc
    if args.programchairs != None:
        program_chairs = []
        
        with open(args.programchairs, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for email in row:
                    program_chairs.append(email)
        iclr2017programchairs.signatories=program_chairs
        iclr2017programchairs.members=program_chairs

    groups.append(iclr2017programchairs)

    iclr2017areachairs = Group('ICLR.cc/2017/areachairs', 
                                readers=['everyone'],
                                writers=['ICLR.cc/2017','ICLR.cc/2017/pcs'],
                                signatures=['ICLR.cc/2017'],
                                signatories=['ICLR.cc/2017/areachairs'],
                                members=[])

    ## Read in a csv file with the names of the area chairs.
    if args.areachairs != None:
        all_areachair_members = []
        with open(args.areachairs, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for email in row:
                    all_areachair_members.append(email)
        iclr2017areachairs.members=all_areachair_members

    groups.append(iclr2017areachairs)

    iclr2017reviewersinvited    = Group('ICLR.cc/2017/conference/reviewers-invited', 
                                        readers=['ICLR.cc/2017/pcs','ICLR.cc/2017'], 
                                        writers=['ICLR.cc/2017/pcs'],
                                        signatures=['ICLR.cc/2017/pcs'],
                                        signatories=['ICLR.cc/2017/conference/reviewers-invited'],
                                        members=[])
    iclr2017reviewers   = Group('ICLR.cc/2017/conference/reviewers', 
                                        readers=['everyone'],
                                        writers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
                                        signatures=['ICLR.cc/2017/conference'],
                                        signatories=['ICLR.cc/2017/conference/reviewers'],
                                        members=[])
    iclr2017reviewersdeclined   = Group('ICLR.cc/2017/conference/reviewers-declined',
                                        readers=['everyone'],
                                        writers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
                                        signatures=['ICLR.cc/2017/conference'],
                                        signatories=['ICLR.cc/2017/conference/reviewers'],
                                        members=[])
    ## Read in a csv file with the names of the reviewers.
    ## Each name will be set as a member of ICLR.cc/2017/reviewers-invited.
    ## groups for 'reviewers' and for 'reviewers-declined' are also generated, but are not yet populated with members.
    if args.reviewers != None:
        reviewers_invited = []
        
        with open(args.reviewers, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for email in row:
                    reviewers_invited.append(email)
        iclr2017reviewersinvited.members=reviewers_invited;

    groups = groups+[iclr2017reviewersinvited, iclr2017reviewers, iclr2017reviewersdeclined]




    ## Post the groups
    for g in groups:
        print "Posting group: "+g.id
        openreview.post_group(g)



    ## Add the conference group to the host page
    openreview.post_group(openreview.get_group('host').add_member(iclr2017))

else:
    print "You must be the super user to run this script"