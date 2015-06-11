from __future__ import unicode_literals



#===================================================================================================
#  Repository
#===================================================================================================
class Repository(object):
    '''
    Represents a source control repository used in a continuous integration job.

    :ivar unicode url:
        Repository clone URL

    :ivar unicode branch:
        Branch used in a particular job

    :ivar unicode name:
        Repository name, determined from URL.

        e.g.
            url = 'https://server/repo.git'
            name = 'repo'
    '''
    def __init__(self, url, branch='master'):
        self.url = url
        self.branch = branch


    @property
    def name(self):
        import re
        return re.match('.*/([^\./]+)(\.git/?)?$', self.url).groups()[0]
