# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################
import re
from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()
typ=('faculty','student','corporation')
insti=('IIT','IIM','IIIT','NIT','MSU','AIIMS','IISc')
auth.settings.extra_fields ['auth_user'] = [
    Field('Address','text'),
    Field('Phone','integer'),
    Field('City','string'),
    Field('Image','upload'),
    Field('Institute','string',requires=IS_IN_SET(insti)),
    Field('typ','string',requires=IS_IN_SET(typ))]
##reate all tables needed by auth if not custom tables
auth.define_tables()
## configure email
db.auth_user.email.unique = True
db.auth_user.email.requires=IS_EMAIL(forced=('^.*\.edu(|\..*)$'))
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'sweetdevansh@gmail.com'
mail.settings.login = 'sweetdevansh:DSDruYPc1411'

## configure auth policy
#auth.settings.registration_requires_verification = False
#auth.settings.registration_requires_approval = False
#auth.settings.reset_password_requires_verification = False
#auth.settings.formstyle = 'table3cols'


## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
##################################################
#######################
auth.settings.registration_requires_approval = False
institype=('Techincal','Business','Liberal Arts','Mass Comm','Research','Medical','Agriculture and Farming','Other')
db.define_table('Institutes',
    Field('Name','string'),
    Field('City','string'),
    Field('Strength','integer'),
    Field('Citations','integer'),
    Field('Specialization','string',requires=IS_IN_SET(institype)),
    Field('Logo','upload'))
sex=('Male','Female')
db.define_table('StudentPersonal',
    Field('Name','string',requires=IS_IN_DB(db(db.auth_user.typ=="student"),'auth_user.id','auth_user.first_name')),
    Field('Age','integer'),
    Field('Address','text'),
    Field('Phone','integer'),
    Field('Image','upload'),
    Field('Gender','string',requires=IS_IN_SET(sex)))

db.define_table('FacultyPersonal',
    Field('Name','string',requires=IS_IN_DB(db(db.auth_user.typ=="faculty"),'auth_user.id','auth_user.name')),
    Field('Age','integer'),
    Field('Me','string'),
    Field('Gender','string',requires=IS_IN_SET(sex)))
   
area=('Computer Science','Humanities','Medical','Other')
course=('High School','UG','PG','PhD','Post PhD')

db.define_table('StudentAcademic',
    Field('Name','string',requires=IS_IN_DB(db(db.auth_user.typ=="student"),'auth_user.id','auth_user.name')),
    Field('CGPA','double'),
    Field('Interests','string',requires=IS_IN_SET(area)),
    Field('Course','string',default="UG",requires=IS_IN_SET(course)))
    
db.define_table('FacultyAcademic',
    Field('Name','string',requires=IS_IN_DB(db(db.auth_user.typ=="faculty"),'auth_user.id','auth_user.name')),
    Field('Points','integer',default=0),
    Field('Interests','string',requires=IS_IN_SET(area)))
    
db.define_table('Relationships',
    Field('Student','reference auth_user',requires=IS_IN_DB(db(db.auth_user.typ=="student"),'auth_user.id','auth_user.first_name')),
    Field('Mentor','reference auth_user',requires=IS_IN_DB(db(db.auth_user.typ=="faculty"),'auth_user.id','auth_user.first_name')))
    
db.define_table('Project',
    Field('Name','string'),
    Field('Description','text'),
    Field('Owner','string',writable=False,requires=IS_IN_DB(db(db.auth_user.typ=='faculty'),'auth_user.id','auth_user.first_name')),
    Field('Area','string',requires=IS_IN_SET(area)),
    Field('Course','string',requires=IS_IN_SET(course)),
    Field('ZipFile','upload'))
    
db.define_table('archive',
    Field('Name','reference Project',requires=IS_IN_DB(db,'Project.id','Project.Name')),
    Field('ZipFile','upload'))
    
    
db.define_table('Rate',
  Field('Project','reference Project',requires=IS_IN_DB(db,'Project.id','Project.Name')),
  Field('rating', 'integer',
          requires=IS_IN_SET(range(1,6))))
          
db.define_table('Comment',
  Field('Project','reference Project',requires=IS_IN_DB(db,'Project.id','Project.Name')),
  Field('Comment', 'text'))

#db.Product.rating.widget = RatingWidget()
db.define_table('StuProject',
    Field('ProjectName','reference Project',requires=IS_IN_DB(db,'Project.id','Project.Name')),
    Field('StudentName','reference auth_user',requires=IS_IN_DB(db(db.auth_user.typ=='student'),'auth_user.id','auth_user.first_name')))
  
db.define_table('Request',
    Field('ProjectName','reference Project',requires=IS_IN_DB(db,'Project.id','Project.Name')),
    Field('StudentName','reference auth_user',requires=IS_IN_DB(db(db.auth_user.typ=='student'),'auth_user.id','auth_user.first_name')))
       
db.define_table('item',
                Field('title',notnull=True),
                Field('file','upload'),
                Field('message','text'),
                Field('posted_by',db.auth_user,default=auth.user_id,
                      readable=False,writable=False),
                Field('posted_on','datetime',default=request.now,
                      readable=False,writable=False))
