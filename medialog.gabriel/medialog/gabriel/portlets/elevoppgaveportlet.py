from plone.app.portlets.browser import formhelper
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope import schema
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from plone import api

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('medialog.gabriel')

# TODO: If you require i18n translation for any of your schema fields below,

class IElevoppgavePortlet(IPortletDataProvider):
    """A portlet which renders elevoppgave 'metadata'.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)
        


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IElevoppgavePortlet)
    
    header = u""
   
    def __init__(self, header=u"",  text=''):
        self.header = header
        self.text = text
    
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header
        

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('elevoppgaveportlet.pt')
    render = _template
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)


class AddForm(formhelper.AddForm):
    schema = IElevoppgavePortlet
    label = _(u"Add Elevoppgave Portlet")
    description = _(u"This portlet displays forfatterinfo etc.")

    def create(self, data):
        return Assignment(**data)


class EditForm(formhelper.EditForm):
    schema = IElevoppgavePortlet
    label = _(u"Edit OppgavePortlet")
    description = _(u"This portlet displays forfatterinfo etc..")
