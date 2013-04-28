from google.appengine.ext import db

class Crisis(db.Model):
	name = db.StringProperty()
	misc = db.TextProperty()
	ide = db.StringProperty()
	relatedorg = db.StringProperty()
	relatedppl = db.StringProperty()
	
class CrisisInfo(db.Model):
	parent_ = db.ReferenceProperty(Crisis, required=True, collection_name='CrisisInfos')
	history = db.TextProperty()
	help = db.StringProperty()
	resources = db.StringProperty()
	type = db.StringProperty()
	ide = db.StringProperty()
	
class CrisisDateType(db.Model):
	parent_ = db.ReferenceProperty(CrisisInfo, required=True, collection_name='CrisisTimes')
	time = db.StringProperty()
	day = db.StringProperty()
	month = db.StringProperty()
	year = db.StringProperty()
	misc = db.StringProperty()
	ide = db.StringProperty()

	
class CrisisLocationType(db.Model):
	parent_ = db.ReferenceProperty(CrisisInfo, required=True, collection_name='CrisisLocations')
	city = db.StringProperty()
	region = db.StringProperty()
	country = db.StringProperty()
	ide = db.StringProperty()
	
class CrisisImpactType(db.Model):
	parent_ = db.ReferenceProperty(CrisisInfo, required=True, collection_name='CrisisImpacts')
	ide = db.StringProperty()
			
class CrisisHumanImpacts(db.Model):
	parent_ = db.ReferenceProperty(CrisisImpactType, required=True, collection_name='CrisisHumanImpacts')
	deaths = db.StringProperty()
	displaced = db.StringProperty()
	injured = db.StringProperty()
	missing = db.StringProperty()
	misc = db.StringProperty()
	ide = db.StringProperty()

	
class CrisisEconomicImpact(db.Model):
	parent_ = db.ReferenceProperty(CrisisImpactType, required=True, collection_name='CrisisEconomicImpacts')
	amount = db.StringProperty()
	currency = db.StringProperty()
	misc = db.StringProperty()
	ide = db.StringProperty()

	
class CrisisExtType(db.Model):
	parent_ = db.ReferenceProperty(Crisis, required=True, collection_name='CrisisExtTypes')
	ide = db.StringProperty()
	
	
class CrisisPrimImage(db.Model):
	parent_ = db.ReferenceProperty(CrisisExtType, required=True, collection_name='CrisisPrimImages')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()

	
class CrisisImage(db.Model):
	parent_ = db.ReferenceProperty(CrisisExtType, required=True, collection_name='CrisisImages')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()

	
class CrisisVideo(db.Model):
	parent_ = db.ReferenceProperty(CrisisExtType, required=True, collection_name='CrisisVideos')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()

	
class CrisisSocial(db.Model):
	parent_ = db.ReferenceProperty(CrisisExtType, required=True, collection_name='CrisisSocials')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class CrisisExt(db.Model):
	parent_ = db.ReferenceProperty(CrisisExtType, required=True, collection_name='CrisisExts')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()


# 	BEGIN ORGANIZATION MODEL

class Organization(db.Model):
	name = db.StringProperty()
	misc = db.StringProperty()
	ide = db.StringProperty()
	relatedcrisis = db.StringProperty()
	relatedppl = db.StringProperty()
	
class OrganizationInfo(db.Model):
	parent_ = db.ReferenceProperty(Organization, required=True, collection_name='OrganizationInfos')
	history = db.TextProperty()
	type = db.StringProperty()
	ide = db.StringProperty()
	
class OrganizationLocationType(db.Model):
	parent_ = db.ReferenceProperty(OrganizationInfo, required=True, collection_name='OrganizationLocations')
	city = db.StringProperty()
	region = db.StringProperty()
	country = db.StringProperty()
	ide = db.StringProperty()
	
class OrganizationContactType(db.Model):
	parent_ = db.ReferenceProperty(OrganizationInfo, required=True, collection_name='OrganizationContacts')
	phone = db.StringProperty()
	email = db.StringProperty()
	ide = db.StringProperty()
	
class OrganizationFullAddr(db.Model):
	parent_ = db.ReferenceProperty(OrganizationContactType, required=True, collection_name='OrganizationAddresses')
	address = db.StringProperty()
	city = db.StringProperty()
	state = db.StringProperty()
	country = db.StringProperty()
	zipC = db.StringProperty()
	ide = db.StringProperty()

class OrganizationExtType(db.Model):
	parent_ = db.ReferenceProperty(Organization, required=True, collection_name='OrganizationExtTypes')
	ide = db.StringProperty()
	
class OrganizationPrimImage(db.Model):
	parent_ = db.ReferenceProperty(OrganizationExtType, required=True, collection_name='OrganizationPrimImages')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class OrganizationImage(db.Model):
	parent_ = db.ReferenceProperty(OrganizationExtType, required=True, collection_name='OrganizationImages')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class OrganizationVideo(db.Model):
	parent_ = db.ReferenceProperty(OrganizationExtType, required=True, collection_name='OrganizationVideos')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class OrganizationSocial(db.Model):
	parent_ = db.ReferenceProperty(OrganizationExtType, required=True, collection_name='OrganizationSocials')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class OrganizationExt(db.Model):
	parent_ = db.ReferenceProperty(OrganizationExtType, required=True, collection_name='OrganizationExts')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	

# 	BEGIN PERSON MODEL

class Person(db.Model):
	name = db.StringProperty()
	misc = db.StringProperty()
	ide = db.StringProperty()
	relatedcrisis = db.StringProperty()
	relatedorg = db.StringProperty()
	
class PersonInfo(db.Model):
	parent_ = db.ReferenceProperty(Person, required=True, collection_name='PersonInfos')
	type = db.StringProperty()
	nationality = db.StringProperty()
	biography = db.TextProperty()
	ide = db.StringProperty()

	
class PersonDateType(db.Model):
	parent_ = db.ReferenceProperty(PersonInfo, required=True, collection_name='PersonTimes')
	time = db.StringProperty()
	day = db.StringProperty()
	month = db.StringProperty()
	year = db.StringProperty()
	misc = db.StringProperty()
	ide = db.StringProperty()
		
class PersonExtType(db.Model):
	parent_ = db.ReferenceProperty(Person, required=True, collection_name='PersonExtTypes')
	ide = db.StringProperty()
	
class PersonPrimImage(db.Model):
	parent_ = db.ReferenceProperty(PersonExtType, required=True, collection_name='PersonPrimImages')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class PersonImage(db.Model):
	parent_ = db.ReferenceProperty(PersonExtType, required=True, collection_name='PersonImages')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class PersonVideo(db.Model):
	parent_ = db.ReferenceProperty(PersonExtType, required=True, collection_name='PersonVideos')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class PersonSocial(db.Model):
	parent_ = db.ReferenceProperty(PersonExtType, required=True, collection_name='PersonSocials')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()
	
class PersonExt(db.Model):
	parent_ = db.ReferenceProperty(PersonExtType, required=True, collection_name='PersonExts')
	site = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	description = db.TextProperty()
	ide = db.StringProperty()