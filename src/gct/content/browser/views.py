# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


class DownloadFileView(BrowserView):
    template = ViewPageTemplateFile('templates/download_file_view.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        fileBrains = api.content.find(context=portal['file_content'], portal_type='File')
        self.fileBrains = fileBrains
        return self.template()
