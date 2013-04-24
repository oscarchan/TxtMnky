from pyramid.view import view_config
from txtmonkey.models import (session,
                                Survey,
                                SurveyRespondent,
                                SurveyResponse,
                                )

import json
from txtmonkey.views.get_responses import get_messages, store_responses, convert_messages_to_responses
import logging

logger = logging.getLogger(__name__)

@view_config(route_name="survey_display", request_method='GET', renderer='../templates/retrieveResponse.jinja2')
def survey_display(context, request):
    survey_id=request.matchdict["survey_id"]
    survey = session.query(Survey).filter(Survey.id == survey_id).first()
        
    messages=get_messages()
    responses = convert_messages_to_responses(messages)
    store_responses(responses)

    survey_results = session.query(SurveyResponse).filter(SurveyResponse.survey_id == survey_id).all()
    return {"survey_id" :survey_id, "question": survey.question, "responses": survey_results}

