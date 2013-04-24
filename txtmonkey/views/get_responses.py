from pyramid.view import view_config
from txtmonkey.models import (session,
                                Survey,
                                SurveyRespondent,
                                SurveyResponse,
                                )

import json
from twilio.rest import TwilioRestClient    

import logging

from sqlalchemy import desc

logger = logging.getLogger(__name__)
def get_messages():
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "AC7225c1d30d2cce103ea56289e3fc6ed8"
    auth_token  = "6efbc4e502a9672e69fddf93c981cbbe"
    client = TwilioRestClient(account_sid, auth_token)
     
    # A list of message objects with the properties described above
    messages = client.sms.messages.list(to = "+14155994769")
    return messages

def convert_messages_to_responses(messages):
    responses = []
    
    for message in messages:
        respondent_number = message.from_
        creation_date = message.date_created
        sms_id = message.sid
        answer = message.body
        
        response = session.query(SurveyResponse).filter(SurveyResponse.sms_id == sms_id).all()
        
        if not response: # skip it is already added
            respondent = session.query(SurveyRespondent).filter(SurveyRespondent.respondent_number == respondent_number)\
                .filter(SurveyRespondent.creation_date <= creation_date)\
                .order_by(desc(SurveyRespondent.creation_date)).first()

            if respondent:  # found right survey associate with the end users
                survey_id = respondent.survey_id
				
                response = SurveyResponse(survey_id = survey_id, respondent_number = respondent_number, response= answer, sms_id = sms_id) 
                responses.append(response)
            else:
                logger.warn("unable to find survey for respondent; number=%s" % respondent_number)
        else:
            logger.debug("already added sms_id=%s" % sms_id)
                
    return responses
			
def store_responses(responses):
    for response in responses:
        session.add(response)
        session.flush()
