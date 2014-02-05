# coding: utf-8
from turbogears import expose
from turbogears.controllers import RootController, Controller

from turbogears.rest import RESTResource, RESTContainer


class ApplicationResource(RESTResource):
    def __init__(self, id, parent_container):
        super(ApplicationResource, self).__init__()
        self.application_id = id
        self.candidate_applications = parent_container

    @expose()
    def GET(self):
        return {
            'success': True,
            'application': {'application_id': self.application_id},
            'candidate_id': self.candidate_applications.candidate_id,
        }


@RESTContainer(ApplicationResource)
class CandidateApplicationsResource(RESTResource):
    def __init__(self, candidate_resource):
        self.candidate_resource = candidate_resource
        self.candidate_id = candidate_resource.candidate_id

    @expose()
    def default(self):
        return {'success': True, 'applications': [{'application_id': 12345}],
                'candidate_id': self.candidate_resource.candidate_id}


class CandidateResource(RESTResource):
    def __init__(self, id, parent_container):
        super(CandidateResource, self).__init__()
        self.candidate_id = id

        # in a real system, we'd
        # self.candidate = Candidate.get(id)

        # set up subordinate resources
        self.applications = CandidateApplicationsResource(self)

    @expose()
    def GET(self):
        return {'success': True, 'candidate': {'id': self.candidate_id}}

    @expose()
    def POST(self):
        return {'success': True}


# normally this would probably inherit from identity.SecureResource
@RESTContainer(CandidateResource)
class CandidateRootController(Controller):
    @expose()
    def GET(self):
        return 'candidate controller root<br/>' \
               '<a href="/">Back home</a>'


class Root(RootController):
    """The root controller of the application."""

    candidate = CandidateRootController()

    @expose()
    def index(self):
        return '<a href="/candidate">Candidate Controller</a><br/>' \
               '<a href="/candidate/1">Candidate 1 (GET)</a><br/>' \
               '<a href="/candidate/1/applications">Candidate 1 ' \
               'applications (GET)</a><br/>'
