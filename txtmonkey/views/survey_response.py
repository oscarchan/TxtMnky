from pyramid.view import view_config

import json

import logging

logger = logging.getLogger(__name__)

@view_config(route_name="survey_display", request_method='POST', renderer='../templates/retrieveResponse.jinja2')
def survey_display(context, request):
    survey_results = model.session.query(model.SurveyResponse).filter(model.SurveyResponse == survey_id).all()
    return survey_results

