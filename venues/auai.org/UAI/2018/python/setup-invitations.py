#!/usr/bin/python

"""
A script for managing invitations.

You can create, enable, or disable most invitations in ICLR 2018 from this script.

Usage:

python toggle-invitations.py Public_Comment --enable
python toggle-invitations.py Public_Comment --disable
"""

# Import statements
import argparse
import csv
import getpass
import sys
import re
import openreview
from openreview import invitations
from openreview import tools
import requests
import config
import pprint
import os

conference = 'auai.org/UAI/2018'
mask_authors_group = conference + "/Paper<number>/Authors"
mask_reviewers_group = conference + "/Paper<number>/Reviewers"
mask_areachair_group = conference + "/Paper<number>/Area_Chairs"
mask_anonac_group = conference + "/Paper<number>/Area_Chair[0-9]+"
mask_anonreviewer_group = conference + "/Paper<number>/AnonReviewer[0-9]+"
mask_allusers_group = conference + "/Paper<number>/All_Users"
mask_unsubmitted_group = conference + "/Paper<number>/Reviewers/Unsubmitted"
mask_submitted_group = conference + "/Paper<number>/Reviewers/Submitted"
program_chairs_id = conference + '/Program_Chairs'
blind_submission_inv_id = conference + '/-/Blind_Submission'

invitation_templates = {
    'Official_Comment': {
        'id': conference + '/-/Paper<number>/Official_Comment',
        'readers': ['everyone'],
        'writers': [conference],
        'invitees': [
            mask_reviewers_group,
            #mask_authors_group,
            mask_areachair_group,
            program_chairs_id],
        'noninvitees': [mask_unsubmitted_group],
        'signatures': [conference],
        'process': os.path.join(os.path.dirname(__file__), '../process/commentProcess.js'),
        'reply': {
            'forum': '<forum>',
            'replyto': None,
            'readers': {
                'description': 'Select all user groups that should be able to read this comment. Selecting \'All Users\' will allow paper authors, reviewers, area chairs, and program chairs to view this comment.',
                'values-dropdown': [
                    #mask_allusers_group,
                    #mask_authors_group,
                    mask_reviewers_group,
                    mask_areachair_group,
                    program_chairs_id
                ]
            },
            'nonreaders': {
                'values': [mask_unsubmitted_group]
            },
            'signatures': {
                'description': '',
                'values-regex': '|'.join([
                    mask_anonreviewer_group,
                    #mask_authors_group,
                    mask_anonac_group,
                    program_chairs_id,
                    conference
                ]),
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values-copied':  [conference, '{signatures}']
            },
            'content': invitations.content.comment
        }
    },
    'Official_Review': {
        'id': conference + '/-/Paper<number>/Official_Review',
        'readers': ['everyone'],
        'writers': [conference],
        'invitees': [mask_reviewers_group],
        'noninvitees': [
            mask_submitted_group,
            mask_areachair_group
            ],
        'signatures': [conference],
        'duedate': 1524355199000, # Saturday, April 21, 2018 11:59:59 PM
        'process': os.path.join(os.path.dirname(__file__), '../process/officialReviewProcess.js'),
        'reply': {
            'forum': '<forum>',
            'replyto': '<forum>',
            'readers': {
                'description': 'The users who will be allowed to read the reply content.',
                'values': [conference, mask_authors_group, mask_reviewers_group, mask_areachair_group, program_chairs_id]
            },
            'nonreaders': {
                'values': [mask_unsubmitted_group]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': mask_anonreviewer_group
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values': [conference]
            },
            'content': invitations.content.review
        }
    },
    'Meta_Review': {
        'id': conference + '/-/Paper<number>/Meta_Review',
        'readers': ['everyone'],
        'writers': [conference],
        'invitees': [mask_areachair_group],
        'noninvitees': [],
        'signatures': [conference],
        'process': os.path.join(os.path.dirname(__file__), '../process/metaReviewProcess.js'),
        'reply': {
            'forum': '<forum>',
            'replyto': '<forum>',
            'readers': {
                'description': 'Select all user groups that should be able to read this comment. Selecting \'All Users\' will allow paper authors, reviewers, area chairs, and program chairs to view this comment.',
                'values': [conference, mask_areachair_group, program_chairs_id]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': mask_anonac_group
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values-regex': mask_anonac_group
            },
            'content': {
                'title': {
                    'order': 1,
                    'value-regex': '.{1,500}',
                    'description': 'Brief summary of your review.',
                    'required': True
                },
                'recommendation': {
                    'order': 2,
                    'value-radio': [
                        '(3) Strong accept',
                        '(2) Weak accept',
                        '(1) Reject'
                      ],
                    'required': True
                },
                'metareview': {
                    'order': 3,
                    'value-regex': '[\\S\\s]+',
                    'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons',
                    'required': True
                },
                'presentation format': {
                    'order': 4,
                    'value-radio': [
                        'Oral',
                        'Poster',
                    ],
                    'required': True
                },
                'best paper':{
                    'order': 5,
                    'description': 'Nominate as best paper (if student paper, nominate for best student paper)',
                    'value-radio': [
                        'Yes',
                        'No'
                    ],
                    'required': False
                },
                'best student paper':{
                    'order': 6,
                    'description': 'Nominate as best student paper',
                    'value-radio': [
                        'Yes',
                        'No'
                    ],
                    'required': False
                }
            }
        }
    },
    'Review_Rating': {
        'id': conference + '/-/Paper<number>/Review_Rating',
        'readers': [conference, program_chairs_id, mask_areachair_group],
        'writers': [conference],
        'invitees': [
            mask_areachair_group,
            program_chairs_id,
            conference
        ],
        'noninvitees': [],
        'signatures': [conference],
        'duedate': openreview.tools.timestamp_GMT(year=2018, month=5, day=19),
        'reply': {
            'forum': '<forum>',
            'replyto': '<forum>',
            'readers': {
                'description': 'This rating is only visible to the UAI program chairs.',
                'values': [program_chairs_id]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': '{}|{}'.format(mask_anonac_group, program_chairs_id)
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values-regex': '{}|{}'.format(mask_anonac_group, program_chairs_id)
            },
            'content': {
                'title': {
                    'value': 'Review ratings for Paper<number>',
                    'description': 'Anonymous ratings of review quality. These will not be shared without your explicit consent.',
                    'order': 0
                },
                'AnonReviewer1': {
                    'description': 'Rating for this reviewer',
                    'order': 7,
                    'value-radio': [
                        '5. Reviewer feedback was very informative, factually correct and constructive.',
                        '4. Reviewer feedback was informative but it contained some factual errors or missing points which were later acknowledged.',
                        '3. Reviewer feedback was mostly informative, but not entirely accurate.',
                        '2. Reviewer feedback was not very informative.',
                        '1. Reviewer feedback was incorrect or reviewer did not seem to have read the paper in enough detail.'
                    ],
                    'required': True,
                },
                'AnonReviewer2': {
                    'description': 'Rating for this reviewer',
                    'order': 8,
                    'value-radio': [
                        '5. Reviewer feedback was very informative, factually correct and constructive.',
                        '4. Reviewer feedback was informative but it contained some factual errors or missing points which were later acknowledged.',
                        '3. Reviewer feedback was mostly informative, but not entirely accurate.',
                        '2. Reviewer feedback was not very informative.',
                        '1. Reviewer feedback was incorrect or reviewer did not seem to have read the paper in enough detail.'
                    ],
                    'required': True,
                },
                'AnonReviewer3': {
                    'description': 'Rating for this reviewer',
                    'order': 9,
                    'value-radio': [
                        '5. Reviewer feedback was very informative, factually correct and constructive.',
                        '4. Reviewer feedback was informative but it contained some factual errors or missing points which were later acknowledged.',
                        '3. Reviewer feedback was mostly informative, but not entirely accurate.',
                        '2. Reviewer feedback was not very informative.',
                        '1. Reviewer feedback was incorrect or reviewer did not seem to have read the paper in enough detail.'
                    ],
                    'required': True,
                },
            }
        }
    },
    'Final_Decision': {
        'id': conference + '/-/Paper<number>/Final_Decision',
        'readers': ['everyone'],
        'writers': [conference],
        'invitees': [conference, program_chairs_id],
        'noninvitees': [],
        'signatures': [conference],
        'reply': {
            'forum': '<forum>',
            'replyto': '<forum>',
            'readers': {
                'description': 'The readers of this note',
                'values': [conference, program_chairs_id, mask_authors_group, mask_reviewers_group, mask_areachair_group ]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values': [program_chairs_id]
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values': [conference, program_chairs_id],
            },
            'content': {
                'title': {
                    'order': 1,
                    'value': 'Paper<number> Final Decision',
                },
                'decision': {
                    'order': 2,
                    'value-radio': [
                        'Accept',
                        'Reject'
                      ],
                    'required': True
                },
                'comment': {
                    'order': 3,
                    'value-regex': '[\\S\\s]+',
                    'description': 'Additional commentary about the decision',
                    'required': False
                },
                'presentation format': {
                    'order': 4,
                    'value-radio': [
                        'Oral',
                        'Poster',
                    ],
                    'required': False
                }
            }
        }
    }
}

def get_invitation_template(template_id, disable=False):
    invitation_template = invitation_templates[template_id]
    if disable:
        invitation_template['invitees'] = []
    return invitation_template

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('invitations', nargs='*', help="invitation id: " + ", ".join(invitation_templates.keys()))
parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation. otherwise, enables the invitation')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.invitations == ['all']:
    invitations_to_process = invitation_templates.keys()
else:
    invitations_to_process = args.invitations

assert all(id in invitation_templates.keys() for id in args.invitations), "Invalid invitation. You must choose from the following: {}".format(invitation_templates.keys())

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

papers = client.get_notes(invitation = 'auai.org/UAI/2018/-/Blind_Submission')

for paper in papers:
    for template_id in invitations_to_process:
        invitation_template = get_invitation_template(template_id, disable=args.disable)
        new_inv = invitations.from_template(invitation_template, paper)
        client.post_invitation(new_inv)

