#!/usr/bin/env python

import re
import wsgiref.handlers, os
import webapp2
import sys
import logging
import xml.etree.ElementTree as ET
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from genxmlif import GenXmlIfError
from minixsv import pyxsval 
from Models import *

#for search
from google.appengine.api import search
from google.appengine.api import users
import urllib
import string
from urlparse import urlparse
from cgi import parse_qs

from copy import deepcopy
from xml.etree import ElementTree
from xml.dom import minidom

xmlVar = ""
index1 = search.Index(name = 'CrisesIndex', 
					   consistency = search.Index.PER_DOCUMENT_CONSISTENT)
index2 = search.Index(name = 'OrganizationIndex', 
					  consistency = search.Index.PER_DOCUMENT_CONSISTENT)
index3 = search.Index(name = 'PersonIndex', 
					  consistency = search.Index.PER_DOCUMENT_CONSISTENT)


#start of try to implement search
class Search (webapp2.RequestHandler):
	"""handles search requests"""

	def FindDocuments(query_string, limit, cursor):
	
		index4 = search.Index(name = 'CrisesIndex', consistency  = search.Index.PER_DOCUMENT_CONSISTENT)
		index5 = search.Index(name = 'OrganizationIndex', consistency  = search.Index.PER_DOCUMENT_CONSISTENT)
		

		
		document = search.Document(
			doc_id = 'cri1',
			fields = [search.TextField(name='ide', value = 'abduction'),
					search.TextField(name='name', value = 'Obama'),
					search.TextField(name='ttype', value = 'crisis'),
					search.TextField(name='history', value = 'myhistory this is my obama history'),
					search.TextField(name='help', value = 'myhelp'),
					search.TextField(name='resources', value = 'myrescources'),
					search.TextField(name='type', value = 'mytype'),
					search.TextField(name='city', value = 'mycity'),
					search.TextField(name='region', value = 'myregion'),
					search.TextField(name='country', value = 'mycountry is the one and only obama'),
					search.TextField(name='currency', value= 'mycurrency is with obama')],
			language='en')

		try:
			index4.add(document)
			
		except search.Error :
			pass
			
		document = search.Document(
			doc_id = 'cri2',
			fields = [search.TextField(name='ide', value = 'drug'),
					search.TextField(name='name', value = 'myname2'),
					search.TextField(name='ttype', value = 'crisis'),
					search.TextField(name='history', value = 'myhistory2 this obama is my history '),
					search.TextField(name='help', value = 'Obam'),
					search.TextField(name='resources', value = 'myrescources are helps me'),
					search.TextField(name='type', value = 'mytype '),
					search.TextField(name='city', value = 'Obam'),
					search.TextField(name='region', value = 'myregion this region obama is'),
					search.TextField(name='country', value = 'mycountry'),
					search.TextField(name='currency', value= 'mycurrency')],
			language='en')

		try:
			index4.add(document)
			
		except search.Error :
			pass
			
		myquery = query_string
		
		try:
			subject_desc = search.SortExpression(
            expression = 'name',
            direction=search.SortExpression.DESCENDING,
            default_value='')
			
			sort = search.SortOptions(expressions=[subject_desc], limit=1000)
			
			options1 = search.QueryOptions(
            sort_options=sort,
            returned_fields=['ide','name','ttype'],
            returned_expressions=[ search.FieldExpression(name = 'hist_snip', expression = 'snippet("obama", history)')  ],
            snippeted_fields=['name', 'history', 'help', 'resources', 'type', 'city', 'region', 'country', 'currency'])
			
			
			query1 = search.Query(query_string=query_string, options=options1)
			
			search_results = index4.search(query1)
			returned_count =  len(search_results.results)
			number_found = search_results.number_found
			biglist = []
			sniplist = []
			gothere = ''
			for doc in search_results:
				lillist = []
				for fields in doc.fields:
					if fields.name == 'ide':
					  lillist.append(fields.value)
					if fields.name == 'name':
					  lillist.append(fields.value)
					if fields.name == 'ttype':
					  lillist.append(fields.value)
				gothere = "got out of doc.fields looop"
				if doc.expressions == None:
				  gothere = "no expressions"
				gothere = len(doc.expressions)
				for expr in doc.expressions:
					gothere = "got inside doc.expressions"
					explist = []
					if expr.name == 'name':
					  explist.append(expr.value)
					if expr.name == 'history':
					  explist.append(expr.value)
					if expr.name == 'help':
					  explist.append(expr.value)
					if expr.name == 'resources':
					  explist.append(expr.value)
					if expr.name == 'type':
					  explist.append(expr.value)
					if expr.name == 'city':
					  explist.append(expr.value)
					if expr.name == region:
					  explist.append(expr.value)
					if expr.name == country:
					  explist.append(expr.value)
					if expr.name == 'currency':
					  explist.append(expr.value)
					if expr.name == 'hist_snip':
					  gothere = "hey!!!"
					  explist.append(expr.value)
					lillist.append(explist)
					gothere = "got to this end"
				biglist.append(lillist)
			
		except search.Error:
			pass
		
	
	def get (self):
	  """handles a get request with a query."""
		# uri = urlparse (self.request.uri)
		# query = ''
		# if uri.query:
		# 	query = parse_qs(uri.query)
		# 	query = query['query'][0]
		
	  global index1
	  global index2
	  global index3
		
	  query_string = self.request.get('searchKeyword') #this holds the string we want to search for
		
	  biglist = []
	  sniplist = []
	  gothere = ''
	  try:
		subject_desc = search.SortExpression(
            expression = 'name',
            direction=search.SortExpression.ASCENDING,
            default_value='')

        # Sort up to 1000 matching results by subject in descending order
		sort = search.SortOptions(expressions=[subject_desc], limit=1000)

        # Set query options
		options1 = search.QueryOptions(
            sort_options=sort,
            returned_fields=['ide','name', 'primaryimage', 'ttype', 'history'],
            snippeted_fields=[ 'name', 'history', 'help', 'resources', 'type', 'city', 'region', 'country', 'currency'])
			
		options2 = search.QueryOptions(
            sort_options=sort,
            returned_fields=['ide', 'name', 'primaryimage', 'ttype', 'history'],
            snippeted_fields=['name', 'history', 'type', 'city', 'region', 'country'])
			
		options3 = search.QueryOptions(
            sort_options=sort,
            returned_fields=['ide', 'name', 'primaryimage', 'ttype', 'bio'],
            snippeted_fields=['name', 'bio', 'type', 'nationality'])

		query1 = search.Query(query_string=query_string, options=options1)
		query2 = search.Query(query_string=query_string, options=options2)
		query3 = search.Query(query_string=query_string, options=options3)

		results1 = index1.search(query1)
		results2 = index2.search(query2)
		results3 = index3.search(query3)
		
		returned_count = len(results1.results) + len(results2.results) + len(results3.results)
		num_hits = results1.number_found + results2.number_found + results3.number_found
		total_sdocuments = results1.results + results2.results + results3.results
		
		
		for doc in total_sdocuments:
				lillist = []
				for fields in doc.fields:
					if fields.name == 'ide':
					  lillist.append(fields.value)
					if fields.name == 'name':
					  lillist.append(fields.value)
					if fields.name == 'ttype':
					  lillist.append(fields.value)
					if fields.name == 'primaryimage':
					  lillist.append(fields.value)

					if fields.name == 'history':
					  lillist.append(fields.value)
					elif fields.name == 'bio':
					  lillist.append(fields.value)

				gothere = "got out of doc.fields looop"
				if doc.expressions == None:
				  gothere = "no expressions"
				gothere = len(doc.expressions)
				for expr in doc.expressions:
					gothere = "got inside doc.expressions"
					explist = []
					if expr.name == 'name':
					  explist.append(expr.value)
					if expr.name == 'history':
					  explist.append(expr.value)
					if expr.name == 'help':
					  explist.append(expr.value)
					if expr.name == 'resources':
					  explist.append(expr.value)
					if expr.name == 'type':
					  explist.append(expr.value)
					if expr.name == 'city':
					  explist.append(expr.value)
					if expr.name == 'region':
					  explist.append(expr.value)
					if expr.name == 'country':
					  explist.append(expr.value)
					if expr.name == 'currency':
					  explist.append(expr.value)
					if expr.name == 'bio':
					  explist.append(expr.value)
					if expr.name == 'nationality':
					  explist.append(expr.value)
					  
					if expr.name == 'hist_snip':
					  gothere = "hey!!!"
					  explist.append(expr.value)
					  
					lillist.append(explist)
					gothere = "got to this end"
				biglist.append(lillist)
		
	  except search.Error:
		logging.exception('Search failed')
		
		
	  allcrises = []
	  found = False
	  if (num_hits > 0):
			# message = "Found " + str(num_hits) + " hits for " + query_string + " and " + str(returned_count) + " results"
			message = "Search results for \'" + query_string + "\'"

	  else :
			message = "No results available for \'" + query_string + "\'"
			
	  template_values = {'criseslist':biglist, 'display':message}

	  path = os.path.join(os.path.dirname(__file__), 'search.html')
	  self.response.out.write(template.render(path, template_values)) 
			
			
		# print query_string
		# try:
		# 	results = search.Index(name = "Crisis").search(query_string)
		# 	for scored_documents in results:
		# 		print scored_documents
		# 		print "i ran"
		# except search.Error:
		# 	logging.exception('Search failed')
		# 	print "i did an exception"
		# for index in db.get_indexes():
		#     print "Kind: %s" % index.kind()

		#construct sort options
		# query_options = search.QueryOptions(limit = 3)
		# query_obj = search.Query(query_string = query, options = query_options)
		# results = search.Index(name = _INDEX_NAME).search(query=query_obj)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class MyHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(template.render('home.html', {}))        
    
class Upload(webapp2.RequestHandler):
    def post(self):
        global xmlVar
        xmlFile = self.request.get('xml')
        import_type = self.request.get('type')
	schema = open((os.path.abspath('schema.xsd')), 'r').read()
        # tempname = ET.fromstring(xmlFile)
        # xmlVar = (ET.fromstring(xmlFile))
        # xmlVar = xmlFile
        # logging.info(xmlVar)
	valid = ValidateSchema(xmlFile, schema)
	if(valid == 0):
		self.response.out.write("Import Unsuccessful. Xml-file does not match schema")
	elif(valid == -1):
		self.response.out.write("Import Unsuccessful. File needs to be xml")
	else :
        	tree = printXML(xmlFile, import_type)
        	self.response.out.write("Import Successful (Close tab)")

        
#         NOTE: THE FOLLOWING 2 LINES ARE HOW WE INITIALLY 'EXPORTED' THE XML TO THE SCREEN
# 		self.response.content_type = "text/xml"
#         self.response.out.write(ET.tostring(xmlVar))

#
# Uses minixsv library to validate schema
#
def ValidateSchema(xmlData, schema):
	valid = 1
	try:
		pyxsval.parseAndValidateString(xmlData, schema, xmlIfClass= pyxsval.XMLIF_MINIDOM)
	except pyxsval.XsvalError,errstr:
		#Validation aborted
		valid = 0
	except GenXmlIfError, errstr:
		#Parsing aborted
		valid = -1
	return valid

class Export(webapp2.RequestHandler):
    def appendName (self, model, current):
        """appends the name for every model to the xml"""
        name = ET.SubElement(current, 'name')
        name.text = model.name

    def appendLoc (self, info, query):
        """appends the location for every model to the xml"""
        loc = ET.SubElement(info, "loc")
        for info in query:
            city = ET.SubElement(loc, 'city')
            city.text = info.city
            region = ET.SubElement(loc, 'region')
            region.text = info.region
            country = ET.SubElement(loc, 'country')
            country.text = info.country

    def appendRef (self, current, pImageQ, imageQ, videoQ, socialQ, extQ):
        """appends the ref attributes for every model to the xml"""
        ref = ET.SubElement(current, 'ref')
        #get primary image
        primImage = ET.SubElement(ref, 'primaryImage')
        for primaryImage in pImageQ:
            site = ET.SubElement(primImage, "site")
            site.text = primaryImage.site
            title = ET.SubElement(primImage, "title")
            title.text = primaryImage.title
            url = ET.SubElement(primImage, "url")
            url.text = primaryImage.url
            description = ET.SubElement(primImage, "description")
            description.text = primaryImage.description
        #get images
        for imageItem in imageQ:
            image = ET.SubElement(ref, 'image')
            site = ET.SubElement(image, 'site')
            site.text = imageItem.site
            title = ET.SubElement(image, 'title')
            title.text = imageItem.title
            url = ET.SubElement(image, 'url')
            url.text = imageItem.url
            description = ET.SubElement(image, 'description')
            description.text = imageItem.description
        #get videos
        for videoItem in videoQ:
            video = ET.SubElement(ref, 'video')
            site = ET.SubElement(video, 'site')
            site.text = videoItem.site
            title = ET.SubElement(video, 'title')
            title.text = videoItem.title
            url = ET.SubElement(video, 'url')
            url.text = videoItem.url
            description = ET.SubElement(video, 'description')
            description.text = videoItem.description
        #get social
        for socialItem in socialQ:
            social = ET.SubElement(ref, 'social')
            site = ET.SubElement(social, 'site')
            site.text = socialItem.site
            title = ET.SubElement(social, 'title')
            title.text = socialItem.title
            url = ET.SubElement(social, 'url')
            url.text = socialItem.url
            description = ET.SubElement(social, 'description')
            description.text = socialItem.description
        #get ext
        for extItem in extQ:
            ext = ET.SubElement(ref, 'ext')
            site = ET.SubElement(ext, 'site')
            site.text = extItem.site
            title = ET.SubElement(ext, 'title')
            title.text = extItem.title
            url = ET.SubElement(ext, 'url')
            url.text = extItem.url
            description = ET.SubElement(ext, 'description')
            description.text = extItem.description

    def appendMisc (self, current, model):
        """appends the misc for every model to the xml"""
        miscItems = ET.SubElement(current, 'misc')
        miscItems.text = model.misc

    def appendCrisis (self, root, crisisQuery):
        """appends the crisies to the xml"""
        listOfCrisis = []
        for crisis in crisisQuery:
            #create root crisis
            key = {'id' : crisis.ide}
            current = ET.Element('crisis', key)

            #get the name
            Export().appendName(crisis, current)

            #get the info
            info = ET.SubElement(current, "info")
            crisisInfoQuery = db.GqlQuery("SELECT * FROM CrisisInfo WHERE ide IN (\'" + crisis.ide + "\')")
            for crisisInfo in crisisInfoQuery:
                history = ET.SubElement(info, 'history')
                history.text = crisisInfo.history
                help = ET.SubElement(info, 'help')
                help.text = crisisInfo.help
                resources = ET.SubElement(info, 'resources')
                resources.text = crisisInfo.resources
                type_ = ET.SubElement(info, 'type')
                type_.text = crisisInfo.type

            #get the time
            timeNode = ET.SubElement(info, "time")
            crisisTimeQuery = db.GqlQuery("SELECT * FROM CrisisDateType WHERE ide IN (\'" + crisis.ide + "\')")
            for timeInfo in crisisTimeQuery:
                time = ET.SubElement(timeNode, 'time')
                time.text = timeInfo.time
                day = ET.SubElement(timeNode, 'day')
                day.text = timeInfo.day
                month = ET.SubElement(timeNode, 'month')
                month.text = timeInfo.month
                year = ET.SubElement(timeNode, 'year')
                year.text = timeInfo.year
                misc = ET.SubElement(timeNode, 'misc')
                misc.text = timeInfo.misc

            #get the location
            crisisLocQuery = db.GqlQuery("SELECT * FROM CrisisLocationType WHERE ide IN (\'" + crisis.ide + "\')")
            Export().appendLoc(info, crisisLocQuery)

            #get the impact, human and economic
            impact = ET.SubElement(info, "impact")
            human = ET.SubElement(impact, "human")
            crisisImHumanQuery = db.GqlQuery("SELECT * FROM CrisisHumanImpacts WHERE ide IN (\'" + crisis.ide + "\')")
            for humanInfo in crisisImHumanQuery:
                deaths = ET.SubElement(human, "deaths")
                deaths.text = humanInfo.deaths
                displaced = ET.SubElement(human, "displaced")
                displaced.text = humanInfo.displaced
                injured = ET.SubElement(human, "injured")
                injured.text = humanInfo.injured
                missing = ET.SubElement(human, "missing")
                missing.text = humanInfo.missing
                misc = ET.SubElement(human, "misc")
                misc.text = humanInfo.misc
            economic = ET.SubElement(impact, "economic")
            crisisImEcoQuery = db.GqlQuery("SELECT * FROM CrisisEconomicImpact WHERE ide IN (\'" + crisis.ide + "\')")
            for ecoInfo in crisisImEcoQuery:
                amount = ET.SubElement(economic, "amount")
                amount.text = ecoInfo.amount
                currency = ET.SubElement(economic, "currency")
                currency.text = ecoInfo.currency
                misc = ET.SubElement(economic, "misc")
                misc.text = ecoInfo.misc

            #done getting info, get ref
            pImageQ = db.GqlQuery("SELECT * FROM CrisisPrimImage WHERE ide IN (\'" + crisis.ide + "\')")
            imageQ = db.GqlQuery("SELECT * FROM CrisisImage WHERE ide IN (\'" + crisis.ide + "\')")
            videoQ = db.GqlQuery("SELECT * FROM CrisisVideo WHERE ide IN (\'" + crisis.ide + "\')")
            socialQ = db.GqlQuery("SELECT * FROM CrisisSocial WHERE ide IN (\'" + crisis.ide + "\')")
            extQ = db.GqlQuery("SELECT * FROM CrisisExt WHERE ide IN (\'" + crisis.ide + "\')")
            Export().appendRef(current, pImageQ, imageQ, videoQ, socialQ, extQ)

            #misc
            Export().appendMisc(current, crisis)

            #related orgs and persons
            key = {'id' : crisis.relatedorg}
            relatedOrg = ET.SubElement(current, 'org', key)
            key = {'id' : crisis.relatedppl}
            relatedPerson = ET.SubElement(current, 'person', key)

            #append to list
            listOfCrisis.append(current)

        return listOfCrisis

    def appendOrgs (self, root, orgQuery):
        """appends the organizations to the xml"""
        listOfOrgs = []
        for org in orgQuery:
            #create root org
            key = {'id' : org.ide}
            current = ET.Element('organization', key)

            #get the name
            Export().appendName(org, current)

            #get the info
            info = ET.SubElement(current, "info")
            orgInfoQuery = db.GqlQuery("SELECT * FROM OrganizationInfo WHERE ide IN (\'" + org.ide + "\')")
            for orgInfo in orgInfoQuery:
                type_ = ET.SubElement(info, 'type')
                type_.text = orgInfo.type
                history = ET.SubElement(info, 'history')
                history.text = orgInfo.history            

            # #get the contact, child of info
            orgContactQuery = db.GqlQuery("SELECT * FROM OrganizationContactType WHERE ide IN (\'" + org.ide + "\')")
            contact = ET.SubElement(info, 'contact')
            for orgContact in orgContactQuery:
                phone = ET.SubElement(contact, 'phone')
                phone.text = orgContact.phone
                email = ET.SubElement(contact, 'email')
                email.text = orgContact.email

            #get address, child of contact
            orgAddQuery = db.GqlQuery("SELECT * FROM OrganizationFullAddr WHERE ide IN (\'" + org.ide + "\')")
            mail = ET.SubElement(contact, 'mail')
            for orgAdd in orgAddQuery:
                address = ET.SubElement(mail, 'address')
                address.text = orgAdd.address
                city = ET.SubElement(mail, 'city')
                city.text = orgAdd.city
                state = ET.SubElement(mail, 'state')
                state.text = orgAdd.state
                country = ET.SubElement(mail, 'country')
                country.text = orgAdd.country
                zipC = ET.SubElement(mail, 'zip')
                zipC.text = orgAdd.zipC

            #get the location
            orgLocQuery = db.GqlQuery("SELECT * FROM OrganizationLocationType WHERE ide IN (\'" + org.ide + "\')")
            Export().appendLoc(info, orgLocQuery)

            #done getting info, get ref
            pImageQ = db.GqlQuery("SELECT * FROM OrganizationPrimImage WHERE ide IN (\'" + org.ide + "\')")
            imageQ = db.GqlQuery("SELECT * FROM OrganizationImage WHERE ide IN (\'" + org.ide + "\')")
            videoQ = db.GqlQuery("SELECT * FROM OrganizationVideo WHERE ide IN (\'" + org.ide + "\')")
            socialQ = db.GqlQuery("SELECT * FROM OrganizationSocial WHERE ide IN (\'" + org.ide + "\')")
            extQ = db.GqlQuery("SELECT * FROM OrganizationExt WHERE ide IN (\'" + org.ide + "\')")
            Export().appendRef(current, pImageQ, imageQ, videoQ, socialQ, extQ)

            #misc
            Export().appendMisc(current, org)

            #related orgs and persons
            key = {'id' : org.relatedcrisis}
            relatedCrisis = ET.SubElement(current, 'crisis', key)
            key = {'id' : org.relatedppl}
            relatedPerson = ET.SubElement(current, 'person', key)

            #append to list
            listOfOrgs.append(current)

        return listOfOrgs

    def appendPerson (self, root, pplQuery):
        """appends the people to the xml"""
        listOfPpl = []
        for ppl in pplQuery:
            #create root ppl
            key = {'id' : ppl.ide}
            current = ET.Element('person', key)

            #get the name
            Export().appendName(ppl, current)

            #get the info
            info = ET.SubElement(current, "info")
            pplInfoQuery = db.GqlQuery("SELECT * FROM PersonInfo WHERE ide IN (\'" + ppl.ide + "\')")
            for pplInfo in pplInfoQuery:
                type_ = ET.SubElement(info, 'type')
                type_.text = pplInfo.type

                #get birthday, different model, child of info
                birthday = ET.SubElement(info, 'birthdate')
                pplBirthQuery = db.GqlQuery("SELECT * FROM PersonDateType WHERE ide IN (\'" + ppl.ide + "\')")
                for pplBirth in pplBirthQuery:
                    time = ET.SubElement(birthday, 'time')
                    time.text = pplBirth.time
                    day = ET.SubElement(birthday, 'day')
                    day.text = pplBirth.day
                    month = ET.SubElement(birthday, 'month')
                    month.text = pplBirth.month
                    year = ET.SubElement(birthday, 'year')
                    year.text = pplBirth.year
                    misc = ET.SubElement(birthday, 'misc')
                    misc.text = pplBirth.misc

                #get nationality and biography, child of info
                nationality = ET.SubElement(info, 'nationality')
                nationality.text = pplInfo.nationality
                biography = ET.SubElement(info, 'biography')
                biography.text = pplInfo.biography

            #done getting info, get ref
            pImageQ = db.GqlQuery("SELECT * FROM PersonPrimImage WHERE ide IN (\'" + ppl.ide + "\')")
            imageQ = db.GqlQuery("SELECT * FROM PersonImage WHERE ide IN (\'" + ppl.ide + "\')")
            videoQ = db.GqlQuery("SELECT * FROM PersonVideo WHERE ide IN (\'" + ppl.ide + "\')")
            socialQ = db.GqlQuery("SELECT * FROM PersonSocial WHERE ide IN (\'" + ppl.ide + "\')")
            extQ = db.GqlQuery("SELECT * FROM PersonExt WHERE ide IN (\'" + ppl.ide + "\')")
            Export().appendRef(current, pImageQ, imageQ, videoQ, socialQ, extQ)

            #misc
            Export().appendMisc(current, ppl)

            #related orgs and persons
            key = {'id' : ppl.relatedcrisis}
            relatedCrisis = ET.SubElement(current, 'crisis', key)
            key = {'id' : ppl.relatedorg}
            relatedOrg = ET.SubElement(current, 'org', key)

            #append to list
            listOfPpl.append(current)

        return listOfPpl


    def get(self):
        #create root node
        root = ET.Element('worldCrises')

        #get crises
        crisisQuery = db.GqlQuery("SELECT * FROM Crisis")
        listOfCrisis = Export().appendCrisis(root, crisisQuery)
        root.extend(listOfCrisis)

        #get organization
        orgQuery = db.GqlQuery("SELECT * FROM Organization")
        listOfOrgs = Export().appendOrgs(root, orgQuery)
        root.extend(listOfOrgs)

        #get people
        pplQuery = db.GqlQuery("SELECT * FROM Person")
        listOfPpl = Export().appendPerson(root, pplQuery)
        root.extend(listOfPpl)

        #format tree, write to screen
        self.response.content_type = "text/xml"
        self.response.out.write(ET.tostring(root))

class gaeunit(webapp2.RequestHandler) :
    def get(self):
        self.response.out.write("")
		
def printXML(xml, import_type):

    global xmlVar
    global index1
    global index2
    global index3
    
    if import_type == 'replacement' :
    	db.delete(db.Query(keys_only=True))
						  
						  
    tree = ET.fromstring(xml)
    xmlVar = tree
    root = tree.iter()
    temp1 = root.next()
    xmlIt = temp1.iter()

    cris = temp1.iterfind("crisis")
        
    for x in cris :
        	
    	crisiside = 0;
    	
    	q = db.GqlQuery("SELECT * FROM Crisis " + 
    		"WHERE ide = :1", x.iter().next().attrib.get('id'))

    	if q.count() > 0 :
    		results = q.fetch(10)
    		db.delete(results)

    	# if q.count() == 0 :
    	
    	myname = x.iterfind("name").next().text
    	CrisisResult = Crisis(name = myname)
    	CrisisResult.misc = x.iterfind("misc").next().text
    	crisiside = x.iter().next().attrib.get('id')
    	CrisisResult.ide = crisiside
    	CrisisResult.relatedorg = x.iterfind('org').next().attrib.get('idref')
    	CrisisResult.relatedppl = x.iterfind('person').next().attrib.get('idref')
    	CrisisResult.put()
    	
    	crisInfo = x.iterfind("info").next().iter().next()
    	CrisisResultInfo = CrisisInfo(parent_ = CrisisResult)
    	history = crisInfo.iterfind("history").next().text
    	CrisisResultInfo.history = history
    	help = crisInfo.iterfind("help").next().text
    	CrisisResultInfo.help = help
    	resources = crisInfo.iterfind("resources").next().text
    	CrisisResultInfo.resources = resources
    	mytype = crisInfo.iterfind("type").next().text
    	CrisisResultInfo.type = mytype
    	CrisisResultInfo.ide = crisiside
    	CrisisResultInfo.put()
    	
    	crisTime = crisInfo.iterfind("time").next().iter().next()
    	CrisisResultTime = CrisisDateType(parent_ = CrisisResultInfo)
    	CrisisResultTime.time = crisTime.iterfind("time").next().text
    	CrisisResultTime.day = crisTime.iterfind("day").next().text
    	CrisisResultTime.month = crisTime.iterfind("month").next().text
    	CrisisResultTime.year = crisTime.iterfind("year").next().text
    	CrisisResultTime.misc = crisTime.iterfind("misc").next().text
    	CrisisResultTime.ide = crisiside
    	CrisisResultTime.put()
    	
    	crisLoc = crisInfo.iterfind("loc").next().iter().next()
    	CrisisResultLoc = CrisisLocationType(parent_ = CrisisResultInfo)
    	city = crisLoc.iterfind("city").next().text
    	CrisisResultLoc.city = city
    	region = crisLoc.iterfind("region").next().text
    	CrisisResultLoc.region = region
    	country = crisLoc.iterfind("country").next().text
    	CrisisResultLoc.country = country
    	CrisisResultLoc.ide = crisiside
    	CrisisResultLoc.put()
    	
    	crisImpact = crisInfo.iterfind("impact").next().iter().next()
    	CrisisResultImpact = CrisisImpactType(parent_ = CrisisResultInfo)
    	CrisisResultImpact.put()
    	
    	crisHuman = crisImpact.iterfind("human").next().iter().next()
    	CrisisResultHuman = CrisisHumanImpacts(parent_ = CrisisResultImpact)
    	CrisisResultHuman.deaths = crisHuman.iterfind("deaths").next().text
    	CrisisResultHuman.displaced = crisHuman.iterfind("displaced").next().text
    	CrisisResultHuman.missing = crisHuman.iterfind("missing").next().text
    	CrisisResultHuman.injured = crisHuman.iterfind("injured").next().text
    	CrisisResultHuman.misc = crisHuman.iterfind("misc").next().text
    	CrisisResultHuman.ide = crisiside
    	CrisisResultHuman.put()
    	
    	crisEconomic = crisImpact.iterfind("economic").next().iter().next()
    	CrisisResultEconomic = CrisisEconomicImpact(parent_ = CrisisResultImpact)
    	CrisisResultEconomic.amount = crisEconomic.iterfind("amount").next().text
    	currency = crisEconomic.iterfind("currency").next().text
    	CrisisResultEconomic.currency = currency
    	CrisisResultEconomic.misc = crisEconomic.iterfind("misc").next().text
    	CrisisResultEconomic.ide = crisiside
    	CrisisResultEconomic.put()
    	
    	crisRef = x.iterfind("ref").next().iter().next()
    	CrisisResultRef = CrisisExtType(parent_ = CrisisResult)
       	CrisisResultRef.put()
    	
    	crisPrimImage = crisRef.iterfind("primaryImage").next().iter().next()
    	CrisisResultPrimImage = CrisisPrimImage(parent_ = CrisisResultRef)
    	CrisisResultPrimImage.site = crisPrimImage.iterfind("site").next().text
    	CrisisResultPrimImage.title = crisPrimImage.iterfind("title").next().text
    	primurl = crisPrimImage.iterfind("url").next().text
    	CrisisResultPrimImage.url = primurl
    	if crisPrimImage.find("description") is not None :
        	CrisisResultPrimImage.description = crisPrimImage.iterfind("description").next().text
    	CrisisResultPrimImage.ide = crisiside
    	CrisisResultPrimImage.put()
    	
    	crisImage = crisRef.iterfind("image")
    	for y in crisImage :
        	CrisisResultImage = CrisisImage(parent_ = CrisisResultRef)
        	CrisisResultImage.site = y.iterfind("site").next().text
        	CrisisResultImage.title = y.iterfind("title").next().text
        	CrisisResultImage.url = y.iterfind("url").next().text
        	if y.find("description") is not None :
		    	CrisisResultImage.description = y.iterfind("description").next().text
			CrisisResultImage.ide = crisiside
	    	CrisisResultImage.put()
	    	
    	crisVideo = crisRef.iterfind("video")
    	for y in crisVideo :
	    	CrisisResultVideo = CrisisVideo(parent_ = CrisisResultRef)
	    	CrisisResultVideo.site = y.iterfind("site").next().text
	    	CrisisResultVideo.title = y.iterfind("title").next().text
	    	CrisisResultVideo.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	CrisisResultVideo.description = y.iterfind("description").next().text
			CrisisResultVideo.ide = crisiside
	    	CrisisResultVideo.put()
	    	
    	crisSocial = crisRef.iterfind("social")
    	for y in crisSocial :
	    	CrisisResultSocial = CrisisSocial(parent_ = CrisisResultRef)
	    	CrisisResultSocial.site = y.iterfind("site").next().text
	    	CrisisResultSocial.title = y.iterfind("title").next().text
	    	CrisisResultSocial.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	CrisisResultSocial.description = y.iterfind("description").next().text
			CrisisResultSocial.ide = crisiside
	    	CrisisResultSocial.put()
	    	
    	crisExt = crisRef.iterfind("ext")
    	for y in crisExt :
	    	CrisisResultExt = CrisisExt(parent_ = CrisisResultRef)
	    	CrisisResultExt.site = y.iterfind("site").next().text
	    	CrisisResultExt.title = y.iterfind("title").next().text
	    	CrisisResultExt.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	CrisisResultExt.description = y.iterfind("description").next().text
			CrisisResultExt.ide = crisiside
	    	CrisisResultExt.put()
			
		document = search.Document(
			doc_id = crisiside,
			fields = [search.TextField(name='ide', value = crisiside),
					search.TextField(name='name', value = myname),
					search.TextField(name='primaryimage', value = primurl),
					search.TextField(name='ttype', value = 'crisis' ),
					search.TextField(name='history', value = history),
					search.TextField(name='help', value = help),
					search.TextField(name='resources', value = resources),
					search.TextField(name='type', value = mytype),
					search.TextField(name='city', value = city),
					search.TextField(name='region', value = region),
					search.TextField(name='country', value = country),
					search.TextField(name='currency', value= currency)],
			language='en')


		
    	try:
    		index1.add(document)
    	except search.Error :
			pass
			
    org = temp1.iterfind("organization")
    for x in org :
    	orgide = 0
    
    	q = db.GqlQuery("SELECT * FROM Organization " + 
    		"WHERE ide = :1", x.iter().next().attrib.get('id'))

    	if q.count() > 0 :
    		results = q.fetch(10)
    		db.delete(results)

    	# if q.count() == 0 :
    	myname = x.iterfind("name").next().text
    	OrganizationResult = Organization(name = myname)
    	OrganizationResult.misc = x.iterfind("misc").next().text
    	orgide = x.iter().next().attrib.get('id')
    	OrganizationResult.ide = orgide
    	OrganizationResult.relatedcrisis = x.iterfind('crisis').next().attrib.get('idref')
    	OrganizationResult.relatedppl = x.iterfind('person').next().attrib.get('idref')
    	OrganizationResult.put()
    	
    	orgInfo = x.iterfind("info").next().iter().next()
    	OrganizationResultInfo = OrganizationInfo(parent_ = OrganizationResult)
    	history = orgInfo.iterfind("history").next().text
    	OrganizationResultInfo.history = history
    	mytype = orgInfo.iterfind("type").next().text
    	OrganizationResultInfo.type = mytype
    	OrganizationResultInfo.ide = orgide
    	OrganizationResultInfo.put()
    	
    	orgLoc = orgInfo.iterfind("loc").next().iter().next()
    	OrganizationResultLoc = OrganizationLocationType(parent_ = OrganizationResultInfo)
    	OrganizationResultLoc.city = orgLoc.iterfind("city").next().text
    	OrganizationResultLoc.region = orgLoc.iterfind("region").next().text
    	OrganizationResultLoc.country = orgLoc.iterfind("country").next().text
    	OrganizationResultLoc.ide = orgide
    	OrganizationResultLoc.put()
    	
    	orgContact = orgInfo.iterfind("contact").next().iter().next()
    	OrganizationResultContact = OrganizationContactType(parent_ = OrganizationResultInfo)
    	OrganizationResultContact.phone = orgContact.iterfind("phone").next().text
    	OrganizationResultContact.email = orgContact.iterfind("email").next().text
    	OrganizationResultContact.ide = orgide
    	OrganizationResultContact.put()
    	
    	orgAddress = orgContact.iterfind("mail").next().iter().next()
    	OrganizationResultAddress = OrganizationFullAddr(parent_ = OrganizationResultContact)
    	OrganizationResultAddress.address = orgAddress.iterfind("address").next().text
    	city = orgAddress.iterfind("city").next().text
    	OrganizationResultAddress.city = city
    	state = orgAddress.iterfind("state").next().text
    	OrganizationResultAddress.state = state
    	country = orgAddress.iterfind("country").next().text
    	OrganizationResultAddress.country = country
    	OrganizationResultAddress.zipC = orgAddress.iterfind("zip").next().text
    	OrganizationResultAddress.ide = orgide
    	OrganizationResultAddress.put()
    	    	
    	orgRef = x.iterfind("ref").next().iter().next()
    	OrganizationResultRef = OrganizationExtType(parent_ = OrganizationResult)
       	OrganizationResultRef.put()
    	
    	orgPrimImage = orgRef.iterfind("primaryImage").next().iter().next()
    	OrganizationResultPrimImage = OrganizationPrimImage(parent_ = OrganizationResultRef)
    	OrganizationResultPrimImage.site = orgPrimImage.iterfind("site").next().text
    	OrganizationResultPrimImage.title = orgPrimImage.iterfind("title").next().text
    	primurl = orgPrimImage.iterfind("url").next().text
    	OrganizationResultPrimImage.url = primurl
    	if orgPrimImage.find("description") is not None :
	    	OrganizationResultPrimImage.description = orgPrimImage.iterfind("description").next().text
		OrganizationResultPrimImage.ide = orgide
    	OrganizationResultPrimImage.put()
    	
    	orgImage = orgRef.iterfind("image")
    	for y in orgImage :
	    	OrganizationResultImage = OrganizationImage(parent_ = OrganizationResultRef)
	    	OrganizationResultImage.site = y.iterfind("site").next().text
	    	OrganizationResultImage.title = y.iterfind("title").next().text
	    	OrganizationResultImage.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	OrganizationResultImage.description = y.iterfind("description").next().text
			OrganizationResultImage.ide = orgide
	    	OrganizationResultImage.put()
	    	
    	orgVideo = orgRef.iterfind("video")
    	for y in orgVideo :
	    	OrganizationResultVideo = OrganizationVideo(parent_ = OrganizationResultRef)
	    	OrganizationResultVideo.site = y.iterfind("site").next().text
	    	OrganizationResultVideo.title = y.iterfind("title").next().text
	    	OrganizationResultVideo.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	OrganizationResultVideo.description = y.iterfind("description").next().text
			OrganizationResultVideo.ide = orgide
	    	OrganizationResultVideo.put()
	    	
    	orgSocial = orgRef.iterfind("social")
    	for y in orgSocial :
	    	OrganizationResultSocial = OrganizationSocial(parent_ = OrganizationResultRef)
	    	OrganizationResultSocial.site = y.iterfind("site").next().text
	    	OrganizationResultSocial.title = y.iterfind("title").next().text
	    	OrganizationResultSocial.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	OrganizationResultSocial.description = y.iterfind("description").next().text
			OrganizationResultSocial.ide = orgide
	    	OrganizationResultSocial.put()
	    	
    	orgExt = orgRef.iterfind("ext")
    	for y in orgExt :
	    	OrganizationResultExt = OrganizationExt(parent_ = OrganizationResultRef)
	    	OrganizationResultExt.site = y.iterfind("site").next().text
	    	OrganizationResultExt.title = y.iterfind("title").next().text
	    	OrganizationResultExt.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	OrganizationResultExt.description = y.iterfind("description").next().text
			OrganizationResultExt.ide = orgide
	    	OrganizationResultExt.put()

	    
    	document = search.Document(
			doc_id = orgide,
			fields = [search.TextField(name='ide', value = orgide),
					search.TextField(name='name', value = myname ),
					search.TextField(name='primaryimage', value = primurl ),
					search.TextField(name='ttype', value = 'organization' ),
					search.TextField(name='history', value = history),
					search.TextField(name='type', value = mytype ),
					search.TextField(name='city', value = city),
					search.TextField(name='region', value = state),
					search.TextField(name='country', value = country)],
			language='en')
		
		
    	try:
			index2.add(document)
			
    	except search.Error :
			pass
			
# 	BEGIN PROCESSING PERSON DATA
	pers = temp1.iterfind("person")
    
    for x in pers : 
    	pplide = 0

    	q = db.GqlQuery("SELECT * FROM Person " + 
    		"WHERE ide = :1", x.iter().next().attrib.get('id'))

    	if q.count() > 0 :
    		results = q.fetch(10)
    		db.delete(results)

    	# if q.count() == 0 :
    	
    	myname = x.iterfind("name").next().text
    	PersonResult = Person(name = myname)
    	PersonResult.misc = x.iterfind("misc").next().text
    	pplide = x.iter().next().attrib.get('id')
    	PersonResult.ide = pplide
    	PersonResult.relatedcrisis = x.iterfind('crisis').next().attrib.get('idref')
    	PersonResult.relatedorg = x.iterfind('org').next().attrib.get('idref')
    	PersonResult.put()
    	
    	persInfo = x.iterfind("info").next().iter().next()
    	PersonResultInfo = PersonInfo(parent_ = PersonResult)
    	mytype = persInfo.iterfind("type").next().text
    	PersonResultInfo.type = mytype
    	nationality = persInfo.iterfind("nationality").next().text
    	PersonResultInfo.nationality = nationality
    	bio = persInfo.iterfind("biography").next().text
    	PersonResultInfo.biography = bio
    	PersonResultInfo.ide = pplide
    	PersonResultInfo.put()
    	
    	persTime = persInfo.iterfind("birthdate").next().iter().next()
    	PersonResultTime = PersonDateType(parent_ = PersonResultInfo)
    	PersonResultTime.time = persTime.iterfind("time").next().text
    	PersonResultTime.day = persTime.iterfind("day").next().text
    	PersonResultTime.month = persTime.iterfind("month").next().text
    	PersonResultTime.year = persTime.iterfind("year").next().text
    	PersonResultTime.misc = persTime.iterfind("misc").next().text
    	PersonResultTime.ide = pplide
    	PersonResultTime.put()
    	    	
    	persRef = x.iterfind("ref").next().iter().next()
    	PersonResultRef = PersonExtType(parent_ = PersonResult)
       	PersonResultRef.put()
    	
    	persPrimImage = persRef.iterfind("primaryImage").next().iter().next()
    	PersonResultPrimImage = PersonPrimImage(parent_ = PersonResultRef)
    	PersonResultPrimImage.site = persPrimImage.iterfind("site").next().text
    	PersonResultPrimImage.title = persPrimImage.iterfind("title").next().text
    	primurl = persPrimImage.iterfind("url").next().text
    	PersonResultPrimImage.url = primurl
    	if persPrimImage.find("description") is not None :
	    	PersonResultPrimImage.description = persPrimImage.iterfind("description").next().text
		PersonResultPrimImage.ide = pplide
    	PersonResultPrimImage.put()
    	
    	persImage = persRef.iterfind("image")
    	for y in persImage :
	    	PersonResultImage = PersonImage(parent_ = PersonResultRef)
	    	PersonResultImage.site = y.iterfind("site").next().text
	    	PersonResultImage.title = y.iterfind("title").next().text
	    	PersonResultImage.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	PersonResultImage.description = y.iterfind("description").next().text
			PersonResultImage.ide = pplide
	    	PersonResultImage.put()
	    	
    	persVideo = persRef.iterfind("video")
    	for y in persVideo :
	    	PersonResultVideo = PersonVideo(parent_ = PersonResultRef)
	    	PersonResultVideo.site = y.iterfind("site").next().text
	    	PersonResultVideo.title = y.iterfind("title").next().text
	    	PersonResultVideo.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	PersonResultVideo.description = y.iterfind("description").next().text
			PersonResultVideo.ide = pplide
	    	PersonResultVideo.put()
	    	
    	persSocial = persRef.iterfind("social")
    	for y in persSocial :
	    	PersonResultSocial = PersonSocial(parent_ = PersonResultRef)
	    	PersonResultSocial.site = y.iterfind("site").next().text
	    	PersonResultSocial.title = y.iterfind("title").next().text
	    	PersonResultSocial.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	PersonResultSocial.description = y.iterfind("description").next().text
			PersonResultSocial.ide = pplide
	    	PersonResultSocial.put()
	    	
    	persExt = persRef.iterfind("ext")
    	for y in persExt :
	    	PersonResultExt = PersonExt(parent_ = PersonResultRef)
	    	PersonResultExt.site = y.iterfind("site").next().text
	    	PersonResultExt.title = y.iterfind("title").next().text
	    	PersonResultExt.url = y.iterfind("url").next().text
	    	if y.find("description") is not None :
		    	PersonResultExt.description = y.iterfind("description").next().text
			PersonResultExt.ide = pplide
	    	PersonResultExt.put()
    	
    	document = search.Document(
			doc_id = pplide,
			fields = [search.TextField(name='ide', value = pplide),
					search.TextField(name='name', value = myname),
					search.TextField(name='primaryimage', value = primurl),
					search.TextField(name='ttype', value = 'person'),
					search.TextField(name='bio', value = bio),
					search.TextField(name='type', value = mytype ),
					search.TextField(name='nationality', value = nationality)],
			language='en')
		
		
    	try:
			index3.add(document)
    	except search.Error :
			pass
			
    return True

# THIS WAS FOR 2.5 - DOESN'T WORK FOR PYTHON 2.7
# def main():
#     logging.getLogger().setLevel(logging.DEBUG)
#     # app = webapp.WSGIApplication([
#     #     (r'.*', MyHandler)], debug=True)
#     app = webapp2.WSGIApplication([
#   ('/xmlUpload', Upload), ('/', MyHandler)], debug=True)
#     wsgiref.handlers.WSGIHandler().run(app)

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

class uploadpage(webapp2.RequestHandler):
    # global xmlVar
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'upload.html')
        self.response.out.write(template.render(path, {})) 

class criseslist(webapp2.RequestHandler):
    # global xmlVar
    def get(self):
    	allcrises = []
    	alist = []
    	length = 100

    	items = db.GqlQuery("SELECT * FROM Crisis")                           
        for i in items:
            alist = []
            alist.append(i.name)
            alist.append(i.ide)
            allcrises.append(alist)
            length += 48

        allcrises.sort()

    	template_values = {'criseslist':allcrises, 'length': length}

        path = os.path.join(os.path.dirname(__file__), 'crises.html')
        self.response.out.write(template.render(path, template_values)) 

class organizationslist(webapp2.RequestHandler):
    # global xmlVar
    def get(self):

    	allorgs = []
    	alist = []
    	length = 100
    	items = db.GqlQuery("SELECT * FROM Organization")                           
        for i in items:
            alist = []
            alist.append(i.name)
            alist.append(i.ide)
            allorgs.append(alist)
            length += 48

        allorgs.sort()
    	template_values = {'orglist':allorgs, 'length': length}

        path = os.path.join(os.path.dirname(__file__), 'organizations.html')
        self.response.out.write(template.render(path, template_values)) 

class peoplelist(webapp2.RequestHandler):
    # global xmlVar
    def get(self):

    	allppl = []
    	alist = []
    	length = 100

    	items = db.GqlQuery("SELECT * FROM Person")                           
        for i in items:
            alist = []
            alist.append(i.name)
            alist.append(i.ide)
            allppl.append(alist)
            length += 48

        allppl.sort()
    	template_values = {'ppllist':allppl, 'length': length}

        path = os.path.join(os.path.dirname(__file__), 'people.html')
        self.response.out.write(template.render(path, template_values)) 


class dynamic_crisis(webapp2.RequestHandler):
    # global xmlVar
    def get(self, pageid):
        # self.response.content_type = "text/xml"
		data = db.GqlQuery( "SELECT * FROM Crisis WHERE ide IN (\'" + pageid + "\')")
		data2 = db.GqlQuery("SELECT * FROM CrisisInfo WHERE ide IN (\'" + pageid + "\')")
		data3 = db.GqlQuery("SELECT * FROM CrisisLocationType WHERE ide IN (\'" + pageid + "\')")
		data4 = db.GqlQuery("SELECT * FROM CrisisHumanImpacts WHERE ide IN (\'" + pageid + "\')")
		data5 = db.GqlQuery("SELECT * FROM CrisisEconomicImpact WHERE ide IN (\'" + pageid + "\')")
		data6 = db.GqlQuery("SELECT * FROM CrisisPrimImage WHERE ide IN (\'" + pageid + "\')")
		data7 = db.GqlQuery("SELECT * FROM CrisisSocial WHERE ide IN (\'" + pageid + "\')")
		data8 = db.GqlQuery("SELECT * FROM CrisisExt WHERE ide IN (\'" + pageid + "\')")
		data9 = db.GqlQuery("SELECT * FROM CrisisImage WHERE ide IN (\'" + pageid + "\')")
		data10 = db.GqlQuery("SELECT * FROM CrisisVideo WHERE ide IN (\'" + pageid + "\')")


		result = data.fetch(1)
		info = data2.fetch(1)
		loc = data3.fetch(1)
		himpact = data4.fetch(1)
		eimpact = data5.fetch(1)
		primaryimage = data6.fetch(1)
		social = data7.fetch(4)
		external = data8.fetch(1)
		images = data9.fetch(4)
		vids = data10.fetch(10)

		name = None
		history = None
		help = None
		resources = None
		ttype = None
		city = None
		region = None
		country = None
		deaths = None
		displaced = None
		injured = None
		missing = None
		amount = None
		currency = None
		pimage = None
		exttitle = None
		exturl = None
		twitterurl = None
		twittertitle = None
		facebooktitle = None
		facebookurl = None
		rpname = None
		rpurl = None
		rppic = None
		roname = None
		rourl = None
		ropic = None

		related = []
		for i in result:
			name = i.name
			
			rpurl = "/person/"
			rpurl += i.relatedppl			
			rourl = "/organization/"
			rourl += i.relatedorg

			rpquery = db.GqlQuery( "SELECT * FROM Person WHERE ide IN (\'" + i.relatedppl + "\')")
			rpquery2 = db.GqlQuery( "SELECT * FROM PersonPrimImage WHERE ide IN (\'" + i.relatedppl + "\')")

			theperson = rpquery.fetch(1)
			theperson2 = rpquery2.fetch(1)
			
			for pp in theperson:
				rpname = pp.name

			for pp2 in theperson2:
				rppic = pp2.url
				if rppic == None:
					rppic == "/images/noimage.png"



			roquery = db.GqlQuery( "SELECT * FROM Organization WHERE ide IN (\'" + i.relatedorg + "\')")
			roquery2 = db.GqlQuery( "SELECT * FROM OrganizationPrimImage WHERE ide IN (\'" + i.relatedorg + "\')")

			theorg = roquery.fetch(1)
			theorg2 = roquery2.fetch(1)

			for oo in theorg:
				roname = oo.name

			for oo2 in theorg2:
				ropic = oo2.url
				if ropic == None:
					ropic == "/images/noimage.png"


		for j in info:
			help = j.help
			resources = j.resources
			ttype = j.type
			history = j.history

		for k in loc:
			city = k.city
			region = k.region
			country = k.country

		for l in himpact:
			deaths = l.deaths
			displaced = l.displaced
			injured = l.injured
			missing = l.missing

		for m in eimpact:
			amount = m.amount
			currency = m.currency

		for n in primaryimage:
			pimage = n.url

		for p in external:
			exttitle = p.title
			exturl = p.url


		sociallist = []

		for q in social:
			if q.site == 'facebook':
				facebooktitle = q.title
				facebookurl = q.url

			if q.site == 'Facebook':
				facebooktitle = q.title
				facebookurl = q.url

			if q.site == 'twitter':
				twittertitle = q.title
				twitterurl = q.url

			if q.site == 'Twitter':
				twittertitle = q.title
				twitterurl = q.url

		pics = set([])

		for im in images:
			pics.add(im.url)

		videos = set([])

		for v in vids:
			if v.site != None:
				if "youtube" in v.site or "Youtube" in v.site or "YouTube" in v.site:
					if len(videos) < 4:
						vidid = video_id(v.url)
						if vidid != None:
							videos.add(vidid)


        # items = db.GqlQuery("SELECT * FROM Crisis")                           

            # alist.append(i.name)
            # alist.append(i.ide)
 

		template_values = 	{ 'name': name, 'history':history, 'help': help, 'resources': resources, 'type': ttype, 'city': city, 'region': region, 'country': country, 
							  'deaths': deaths, 'displaced': displaced, 'injured': injured, 'missing': missing, 'amount': amount, 'currency': currency, 
							  'primaryimage': pimage, 'exttitle': exttitle, 'exturl': exturl, 'facebookurl': facebookurl, 'facebooktitle': facebooktitle,
							  'twittertitle': twittertitle, 'twitterurl': twitterurl, 'pics': pics, 'videos': videos, 'rpname': rpname,
							  'rpurl': rpurl, 'rppic': rppic, 'roname': roname, 'rourl': rourl, 'ropic': ropic,
							}

		path = os.path.join(os.path.dirname(__file__), 'template_crisis.html')
		self.response.out.write(template.render(path, template_values))  

class dynamic_org(webapp2.RequestHandler):
    # global xmlVar
    def get(self, pageid):
        # self.response.content_type = "text/xml"
		data = db.GqlQuery( "SELECT * FROM Organization WHERE ide IN (\'" + pageid + "\')")
		data2 = db.GqlQuery("SELECT * FROM OrganizationInfo WHERE ide IN (\'" + pageid + "\')")
		data3 = db.GqlQuery("SELECT * FROM OrganizationLocationType WHERE ide IN (\'" + pageid + "\')")
		data4 = db.GqlQuery("SELECT * FROM OrganizationContactType WHERE ide IN (\'" + pageid + "\')")
		data5 = db.GqlQuery("SELECT * FROM OrganizationFullAddr WHERE ide IN (\'" + pageid + "\')")
		data6 = db.GqlQuery("SELECT * FROM OrganizationPrimImage WHERE ide IN (\'" + pageid + "\')")
		data7 = db.GqlQuery("SELECT * FROM OrganizationSocial WHERE ide IN (\'" + pageid + "\')")
		data8 = db.GqlQuery("SELECT * FROM OrganizationExt WHERE ide IN (\'" + pageid + "\')")
		data9 = db.GqlQuery("SELECT * FROM OrganizationImage WHERE ide IN (\'" + pageid + "\')")
		data10 = db.GqlQuery("SELECT * FROM OrganizationVideo WHERE ide IN (\'" + pageid + "\')")


		result = data.fetch(1)
		info = data2.fetch(1)
		loc = data3.fetch(1)
		contact = data4.fetch(1)
		address = data5.fetch(1)
		primaryimage = data6.fetch(1)
		social = data7.fetch(4)
		external = data8.fetch(1)
		images = data9.fetch(4)
		vids = data10.fetch(10)

		name = None
		history = None
		ttype = None
		city = None
		region = None
		country = None
		phone = None
		email = None
		add = None
		addcity = None
		addstate = None
		addcountry = None
		addzip = None
		pimage = None
		exttitle = None
		exturl = None
		twitterurl = None
		twittertitle = None
		facebooktitle = None
		facebookurl = None
		rpname = None
		rpurl = None
		rppic = None
		rcname = None
		rcurl = None
		rcpic = None

		for i in result:
			name = i.name

			rpurl = "/person/"
			rpurl += i.relatedppl			
			rcurl = "/crisis/"
			rcurl += i.relatedcrisis



			rpquery = db.GqlQuery( "SELECT * FROM Person WHERE ide IN (\'" + i.relatedppl + "\')")
			rpquery2 = db.GqlQuery( "SELECT * FROM PersonPrimImage WHERE ide IN (\'" + i.relatedppl + "\')")

			theperson = rpquery.fetch(1)
			theperson2 = rpquery2.fetch(1)
			
			for pp in theperson:
				rpname = pp.name

			for pp2 in theperson2:
				rppic = pp2.url
				if rppic == None:
					rppic == "/images/noimage.png"


			rcquery = db.GqlQuery( "SELECT * FROM Crisis WHERE ide IN (\'" + i.relatedcrisis + "\')")
			rcquery2 = db.GqlQuery( "SELECT * FROM CrisisPrimImage WHERE ide IN (\'" + i.relatedcrisis + "\')")

			thecrisis = rcquery.fetch(1)
			thecrisis2 = rcquery2.fetch(1)

			for cc in thecrisis:
				rcname = cc.name

			for cc2 in thecrisis2:
				rcpic = cc2.url
				if cc2.url == None:
					rcpic == "/images/noimage.png"


			logging.info("****************")
			logging.info(rppic)
			logging.info(rcpic)

		for j in info:
			history = j.history
			ttype = j.type

		for k in loc:
			city = k.city
			region = k.region
			country = k.country

		for l in contact:
			phone = l.phone
			email = l.email

		for m in address:
			add = m.address
			addcity = m.city
			addstate = m.state
			addcountry = m.country
			addzip = m.zipC

		for n in primaryimage:
			pimage = n.url

		for p in external:
			exttitle = p.title
			exturl = p.url


		sociallist = []

		for q in social:
			if q.site == 'facebook':
				facebooktitle = q.title
				facebookurl = q.url

			if q.site == 'Facebook':
				facebooktitle = q.title
				facebookurl = q.url

			if q.site == 'twitter':
				twittertitle = q.title
				twitterurl = q.url

			if q.site == 'Twitter':
				twittertitle = q.title
				twitterurl = q.url
				
		pics = set([])

		for im in images:
			pics.add(im.url)

		videos = set([])

		for v in vids:
			if v.site != None:
				if "youtube" in v.site or "Youtube" in v.site or "YouTube" in v.site:
					if len(videos) < 4:
						vidid = video_id(v.url)
						if vidid != None:
							videos.add(vidid)


		template_values = 	{ 'name': name, 'history': history, 'type': ttype, 'city': city, 'region': region, 'country': country, 
							  'phone': phone, 'email': email, 'add': add, 'addcity': addcity, 'addstate': addstate, 'addcountry': addcountry, 
							  'addzip': addzip, 'primaryimage': pimage, 'exttitle': exttitle, 'exturl': exturl, 'facebookurl': facebookurl, 
							  'facebooktitle': facebooktitle, 'twittertitle': twittertitle, 'twitterurl': twitterurl, 'pics': pics, 'videos': videos,
							  'rpname': rpname, 'rpurl': rpurl, 'rppic': rppic, 'rcname': rcname, 'rcurl': rcurl, 'rcpic': rcpic,
							}
		path = os.path.join(os.path.dirname(__file__), 'template_org.html')
		self.response.out.write(template.render(path, template_values))


class dynamic_ppl(webapp2.RequestHandler):
    # global xmlVar
    def get(self, pageid):
        # self.response.content_type = "text/xml"
		data = db.GqlQuery( "SELECT * FROM Person WHERE ide IN (\'" + pageid + "\')")
		data2 = db.GqlQuery("SELECT * FROM PersonInfo WHERE ide IN (\'" + pageid + "\')")
		data3 = db.GqlQuery("SELECT * FROM PersonPrimImage WHERE ide IN (\'" + pageid + "\')")
		data4 = db.GqlQuery("SELECT * FROM PersonSocial WHERE ide IN (\'" + pageid + "\')")
		data5 = db.GqlQuery("SELECT * FROM PersonExt WHERE ide IN (\'" + pageid + "\')")
		data6 = db.GqlQuery("SELECT * FROM PersonDateType WHERE ide IN (\'" + pageid + "\')")
		data7 = db.GqlQuery("SELECT * FROM PersonImage WHERE ide IN (\'" + pageid + "\')")
		data8 = db.GqlQuery("SELECT * FROM PersonVideo WHERE ide IN (\'" + pageid + "\')")


		result = data.fetch(1)
		info = data2.fetch(1)
		primaryimage = data3.fetch(1)
		social = data4.fetch(4)
		external = data5.fetch(1)
		dob = data6.fetch(1)
		images = data7.fetch(4)
		vids = data8.fetch(10)

		name = None
		ttype = None
		nationality = None
		bio = None
		day = None
		month = None
		year = None
		pimage = None
		exttitle = None
		exturl = None
		twitterurl = None
		twittertitle = None
		facebooktitle = None
		facebookurl = None
		rcname = None
		rcurl = None
		rcpic = None
		roname = None
		rourl = None
		ropic = None

		for i in result:
			name = i.name
		
			rourl = "/organization/"
			rourl += i.relatedorg
			rcurl = "/crisis/"
			rcurl += i.relatedcrisis

			roquery = db.GqlQuery( "SELECT * FROM Organization WHERE ide IN (\'" + i.relatedorg + "\')")
			roquery2 = db.GqlQuery( "SELECT * FROM OrganizationPrimImage WHERE ide IN (\'" + i.relatedorg + "\')")

			theorg = roquery.fetch(1)
			theorg2 = roquery2.fetch(1)

			for oo in theorg:
				roname = oo.name

			for oo2 in theorg2:
				ropic = oo2.url
				if ropic == None:
					ropic == "/images/noimage.png"



			rcquery = db.GqlQuery( "SELECT * FROM Crisis WHERE ide IN (\'" + i.relatedcrisis + "\')")
			rcquery2 = db.GqlQuery( "SELECT * FROM CrisisPrimImage WHERE ide IN (\'" + i.relatedcrisis + "\')")

			thecrisis = rcquery.fetch(1)
			thecrisis2 = rcquery2.fetch(1)

			for cc in thecrisis:
				rcname = cc.name

			for cc2 in thecrisis2:
				rcpic = cc2.url
				if rcpic == None:
					rcpic == "/images/noimage.png"

		for j in info:
			ttype = j.type
			nationality = j.nationality
			bio = j.biography

		for k in dob:
			day = k.day
			month = k.month
			year = k.year

		for n in primaryimage:
			pimage = n.url

		for p in external:
			exttitle = p.title
			exturl = p.url


		sociallist = []

		for q in social:
			if q.site == 'facebook':
				facebooktitle = q.title
				facebookurl = q.url

			if q.site == 'Facebook':
				facebooktitle = q.title
				facebookurl = q.url

			if q.site == 'twitter':
				twittertitle = q.title
				twitterurl = q.url

			if q.site == 'Twitter':
				twittertitle = q.title
				twitterurl = q.url

		pics = set([])

		for im in images:
			pics.add(im.url)

		videos = set([])

		for v in vids:
			if v.site != None:
				if "youtube" in v.site or "Youtube" in v.site or "YouTube" in v.site:
					if len(videos) < 4:
						vidid = video_id(v.url)
						if vidid != None:
							videos.add(vidid)


		template_values = 	{ 'name': name, 'type': ttype, 'nationality': nationality, 'bio': bio, 'day': day, 'month': month, 'year': year,
							  'primaryimage': pimage, 'exttitle': exttitle, 'exturl': exturl, 'facebookurl': facebookurl, 
							  'facebooktitle': facebooktitle, 'twittertitle': twittertitle, 'twitterurl': twitterurl, 'pics': pics, 'videos': videos,
							  'roname': roname, 'rourl': rourl, 'ropic': ropic, 'rcname': rcname, 'rcurl': rcurl, 'rcpic': rcpic,
							}
		path = os.path.join(os.path.dirname(__file__), 'template_ppl.html')
		self.response.out.write(template.render(path, template_values))


#THIS REPLACES WHAT IS COMMENTED OUT ABOVE
app = webapp2.WSGIApplication([('/xmlUpload', Upload), ('/searchQuery', Search), ('/xmlExport', Export), ('/', MyHandler), 
	('/crisis/(.*)', dynamic_crisis), ('/organization/(.*)', dynamic_org), ('/person/(.*)', dynamic_ppl), ('/crises', criseslist), 
	('/organizations', organizationslist), ('/people', peoplelist), ('/upload', uploadpage)], debug=True)

if __name__ == "__main__":
    main()
