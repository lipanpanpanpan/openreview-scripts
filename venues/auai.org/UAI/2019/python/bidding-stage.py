import argparse
import openreview
from openreview import invitations
import datetime
import os
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)


    conference.open_bids(due_date = datetime.datetime(2019, 3, 11, 11, 59), request_count = 50, with_area_chairs = True)
    conference.set_reviewerpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 reviewers. It will be regularly updated as the conference progresses, \
            so please check back frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
            <p>\
            Update your profile to include your most up-to-date information, including emails,  \
                work history and relations, to ensure proper conflict-of-interest detection \
                during the paper matching process.\
            </p>\
        <br>\
        <h4>Bidding Phase</h4>\
            <p>\
            <em><strong>Please note that the bidding has begun. You are requested to do the\
            following by 23:59 PM Samoa Time, Match 10th 2019</strong></em>:\
            <ul>\
                <li>Provide your reviewing preferences by bidding on papers using the Bidding \
                Interface.</li>\
                <li><strong><a href="/invitation?id=auai.org/UAI/2019/Conference/-/Bid">Go to \
                Bidding Interface</a></strong></li>\
            </ul>\
            </p>\
        <br>'
    })
    conference.set_areachairpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 area chairs. It will be regularly updated as the conference progresses, \
            so please check back frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
            <p>\
            Update your profile to include your most up-to-date information, including emails,  \
                work history and relations, to ensure proper conflict-of-interest detection \
                during the paper matching process.\
            </p>\
        <br>\
        <h4>Bidding Phase</h4>\
            <p>\
            <em><strong>Please note that the bidding has begun. You are requested to do the\
            following by 23:59 PM Samoa Time, Match 10th 2019</strong></em>:\
            <ul>\
                <li>Provide your reviewing preferences by bidding on papers using the Bidding \
                Interface.</li>\
                <li><strong><a href="/invitation?id=auai.org/UAI/2019/Conference/-/Bid">Go to \
                Bidding Interface</a></strong></li>\
            </ul>\
            </p>\
        <br>'
    })
