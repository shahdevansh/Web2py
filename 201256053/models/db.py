# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
import datetime

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

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

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
## 1. movie (id, name, hero, director, release_date) #e.g. hero would be pointer to
## 2. artist table
## 4. song (id, name, length, singer, composer, movie, singing_actor)
## 5. rating (id, user, song, rating) #user would point to auth_user table
## rating should be an integer in range 0 upto 5.
##
##
####################
#####################################################

genres=("Action","Drama","Comedy","Romance","Thriller","Horror","Classic")
typ=("Actor","Singer","Director","Composer")

db.define_table('Artists',
SQLField('Artist','string',notnull=True,required=True,length=255),
SQLField('Type','string',required=True,requires=IS_IN_SET(typ)),
SQLField('Description','text'),format='%(Artist)s')

db.define_table('Movies',
Field('Name','string',notnull=True,required=True,length=255,label='Enter Movie Name'),
Field('Hero',db.Artists,requires=IS_IN_DB(db(db.Artists.Type=="Actor"),'Artists.id','Artists.Artist')),
Field('Director',db.Artists,requires=IS_IN_DB(db(db.Artists.Type=="Director"),'Artists.id','Artists.Artist')),
Field('Singer',db.Artists,requires=IS_IN_DB(db(db.Artists.Type=="Singer"),'Artists.id','Artists.Artist')),
Field('ReleasedOn','date'),
Field('Genre','string',requires=IS_IN_SET(genres)),format='%(Artist)s')
#movie (id, name, hero, director, release_date) #e.g. hero would be pointer to
#song (id, name, length, singer, composer, movie, singing_actor)

db.define_table('Songs',
Field('Name','string',notnull=True,required=True),
Field('Length','time'),
Field('Singer',db.Artists,requires=IS_IN_DB(db(db.Artists.Type=="Singer"),'Artists.id','Artists.Artist')),
Field('Composer','string',requires=IS_IN_DB(db(db.Artists.Type=="Composer"),'Artists.id','Artists.Artist')),
Field('ActorSinging','string',label="Actor Staged",requires=IS_IN_DB(db(db.Artists.Type=="Actor"),'Artists.id','Artists.Artist')),
Field('Movie','string',requires=IS_IN_DB(db,'Movies.id','Movies.Name')),
Field('Upload','upload'),format='%(Name)s')

# rating (id, user, song, rating) 

db.define_table('Rating',
Field('User','string',default=session.visitor_name,requires=IS_IN_DB(db,'auth_user.id','auth_user.email')),
Field('Song',db.Songs,requires=IS_IN_DB(db,'Songs.id','Songs.Name')),
Field('Rating','integer',requires=IS_INT_IN_RANGE(0,6),notnull=True,required=True))
