from pyramid.view import view_config

from datetime import datetime, date, timedelta
import time

from txtmonkey.models import (session,
                                Survey,
                                SurveyRespondent,
                                SurveyResponse,
                                )

import logging

from twilio.rest import TwilioRestClient    

'''
  Config 
  hard coded the survey server and other things
'''
twilio_service_host = 'https://api.twilio.com'

sms_message_url = twilio_service_host + '/2010-04-01/Accounts/{AccountSid}/SMS/Messages'


'''
   Assistance classes
'''
logger = logging.getLogger(__name__)

@view_config(route_name="survey_create", request_method='POST', renderer='../templates/mytemplate.jinja2')
def index(context, request):
    """
    an home page of survey length webap.
    - provide a simple survey form for quick look up of survey
    """

    twilio_id = request.params['twilio_id']
    respondent_numbers = split_numbers(request.params['respondent_number'])
    question = request.params['question']

    account_sid = "AC7225c1d30d2cce103ea56289e3fc6ed8"
    auth_token  = "6efbc4e502a9672e69fddf93c981cbbe"
    phone_from = "+14155994769"
    
    respondent_numbers.append("+14082561324")

    # --- validation ---
    if 10 < len(question) and len(question) > 140:
        return { "error": "invalid question: len=%s" % len(question) }

    if len(respondent_numbers) == 0:
        return { "error": "missing respondent_numbers: len=%s" % len(respondent_numbers) }
        

    client = TwilioRestClient(account_sid, auth_token)

    # --- db ---
    now = datetime.now()
    # store the survey
    with session.begin():
        survey = Survey(twilio_owner_id = account_sid,
                        question = question,
                        creation_date = now)
        session.add(survey)
        session.flush()

        for number in respondent_numbers:
            respondent = SurveyRespondent(respondent_number = number, 
                             survey_id = survey.id)
            session.add(respondent)
    
            message = client.sms.messages.create(body=question,
                                         to=number,
                                         from_=phone_from)
                                     
    request.session.flash('Survey was created successfully.')
        
    url = request.route_url('survey_result', survey_id = survey.id) 
    return HTTPFound(location=url)

def split_numbers(raw_numbers):
    if raw_numbers is None:
        return []

    phone_numbers = [ number.strip() for number in raw_numbers.split(',') if len(number.strip()) > 0]

    return phone_numbers
