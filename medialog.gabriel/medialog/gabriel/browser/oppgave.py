from pp.client.plone.browser.compatible import InitializeClass
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class OppgaveChapterView(BrowserView):
    """ Converter view for Oppgave.
    """

    template = ViewPageTemplateFile('oppgave_chapter.pt')

    def __call__(self, *args, **kw):
        return self.template(self.context)

InitializeClass(OppgaveChapterView)

