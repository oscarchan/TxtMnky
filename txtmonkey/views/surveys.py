from pyramid.view import view_config

import json

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

@view_config(route_name="survey_create", request_method='POST', renderer='templates/mytemplate.jinja2')
def index(context, request):
    """
    an home page of survey length webap.
    - provide a simple survey form for quick look up of survey
    """

    twilio_id = request.params['twilio_id']
    respondent_numbers = request.params['respondent_number']
    question = request.params['question']
    

    # --- validation ---


    account_sid = "AC7225c1d30d2cce103ea56289e3fc6ed8"
    auth_token  = "6efbc4e502a9672e69fddf93c981cbbe"
    client = TwilioRestClient(account_sid, auth_token)
    phone_from = "+4155994769"
    message = client.sms.messages.create(body="Testing 123",
                                         to="+14082561324",
                                         from_=phone_from)
                                     

    message.sid
    return {}


