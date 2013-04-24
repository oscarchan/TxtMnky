from pyramid.view import view_config
from txtmonkey.models import (session,
                                Survey,
                                SurveyRespondent,
                                SurveyResponse,
                                )

import json
from twilio.rest import TwilioRestClient    

import logging

logger = logging.getLogger(__name__)
def get_messages():
	# Your Account Sid and Auth Token from twilio.com/user/account
	account_sid = "AC7225c1d30d2cce103ea56289e3fc6ed8"
	auth_token  = "6efbc4e502a9672e69fddf93c981cbbe"
	client = TwilioRestClient(account_sid, auth_token)
	 
	# A list of message objects with the properties described above
	messages = client.sms.messages.list(to = "+14155994769")
	return messages

def store_responses(survey_id,responses):
	for response in responses:
		new_response =SurveyResponse(survey_id = survey_id, respondent_number = response.from_, response=response.body)
    	session.add(new_response)
    	session.flush()
