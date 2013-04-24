from pyramid.view import view_config
from txtmonkey.models import (session,
                                Survey,
                                SurveyRespondent,
                                SurveyResponse,
                                )

import json
import get_responses
import logging

logger = logging.getLogger(__name__)

@view_config(route_name="survey_display", request_method='GET', renderer='../templates/retrieveResponse.jinja2')
def survey_display(context, request):
    messages=get_responses.get_responses()
    survey_id=request.matchdict["survey_id"]
    survey_results = session.query(SurveyResponse).filter(survey_id == survey_id).all()
    import pdb
    pdb.set_trace()
    return survey_results

