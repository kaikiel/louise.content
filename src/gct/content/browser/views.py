# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from email.mime.text import MIMEText
from gct.content.browser.configlet import IDict
import json
from plone.protect.interfaces import IDisableCSRFProtection
from gct.content.browser.base_inform_configlet import IInform 
from zope.interface import alsoProvides
from zope.globalrequest import getRequest


class ProductView(BrowserView):
    template = ViewPageTemplateFile('templates/product_view.pt')
    def __call__(self):
        imgList = []
        coverImg = self.context.cover
        productImgs = api.content.find(context=self.context, depth=1)
        imgNameList = ['img1', 'img2', 'img3', 'img4', 'img5']
        for imgName in imgNameList:
            if getattr(self.context, imgName):
                imgList.append('{}/@@images/{}/big'.format( self.context.absolute_url(), imgName) )
        if imgList == []:
            imgList.append(self.context.absolute_url()+'/@@images/cover/big')
        self.imgList = imgList
        
        self.title = self.context.title
        self.modelNo = self.context.modelNo
        self.beApplicable = self.context.beApplicable
        self.characteristic = self.context.characteristic
        self.body = self.context.body.raw if self.context.body != None else None
        
        return self.template()


class CoverView(BrowserView):
    template = ViewPageTemplateFile('templates/cover_view.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()

        featureList = self.context.feature
        self.featureList = featureList

	return self.template()


class FolderProductView(BrowserView):
    template = ViewPageTemplateFile('templates/folder_product_view.pt')
    def __call__(self):
	return self.template()


class FolderNewsView(BrowserView):
    template = ViewPageTemplateFile('templates/folder_news_view.pt')
    def __call__(self):
	return self.template()


class ContactUs(BrowserView):
    template = ViewPageTemplateFile('templates/contact_us.pt')
    def __call__(self):
        request = self.request
        self.address = api.portal.get_registry_record('address', interface=IInform, default='').replace('\r\n', '<br>')
        self.cellphone = api.portal.get_registry_record('cellphone', interface=IInform, default='')
	name = request.get('name')
	email = request.get('email')
	message = request.get('message')
	if name and email and message:
	    body_str = """Name:{}<br/>Email:{}<br/>Message:{}""".format(name, email, message)
            mime_text = MIMEText(body_str, 'html', 'utf-8')
            receive_email = api.portal.get_registry_record('test', interface=IInform, default='')
            api.portal.send_email(
                recipient=receive_email,
                sender=email,
                subject="{} 意見提供".format(name),
                body=mime_text.as_string(),
            )
	api.portal.show_message(message='發送成功!'.decode('utf-8'), request=request)
        return self.template()


class NewsItemView(BrowserView):
    template = ViewPageTemplateFile('templates/news_item_view.pt')
    def __call__(self):
        request = self.request
        return self.template()


class SubscribeEmail(BrowserView):
    def __call__(self):
	request = self.request
	email = request.get('email')
	subscribe_list = api.content.get(path='/subscribe_list')
	subscribe_list.description += '%s,' %email

class UpdateConfiglet():
    def __call__(self):
	productBrains = api.content.find(path="gct/products", portal_type="Product")
	data = {}
	try:
            request = self.request
        except:
	    request = getRequest()

        alsoProvides(request, IDisableCSRFProtection)
	# data[buggy] = [0,{'1/4': 0, '1/8': 5} ]
	# data[${cayegory}] = [${category_count}, { ${subject}: ${subject_count} }]
        try:
            for item in productBrains:
	        category = item.p_category
	        subject = item.p_subject

	        if data.has_key(category):
                    data[category][0] += 1
		    if data[category][1].has_key(subject):
		        data[category][1][subject] += 1
		    else:
		        data[category][1][subject] = 1
	        else:
		    data[category] = [1, {subject: 1}]

            data = json.dumps(data).decode('utf-8')
	    api.portal.set_registry_record('dict', data, interface=IDict)
            return "Successful"
        except  Exception as e:
            return e
