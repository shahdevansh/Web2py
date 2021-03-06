# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime

def form1():
    form=SQLFORM(db.Artists,fields=['Artist','id','Description'])
    return dict(form=form)
    
def form2():
    form=SQLFORM(db.Movies,fields=['Name','Hero','Director','Singer','ReleasedOn','Genre'])
    return dict(form=form)
    
def form3():
    form=SQLFORM(db.Songs,fields=['Name','Length','Singer','Composer','ActorSinging','Movie','Upload'])
    return dict(form=form)
    
def form4():
    form=SQLFORM(db.Rating,fields=['User','Song','Rating'])
    return dict(form=form)

def query6():
    iid=request.args[0]
    iid=int(iid)
    rows=db().select(db.Artists.ALL)
    b=rows[0]['id']
    d=rows[iid-b]
    if (d['Type']=='Actor'):
        records=db(db.Movies.Hero==iid).select(db.Movies.Name)
        return dict(records=records)
    elif (d['Type']=='Singer'):
        records=db(db.Songs.Singer==iid).select(db.Songs.Name)
        return dict(records=records)
    elif (d['Type']=='Director'):
        records=db(db.Movies.Director==iid).select(db.Movies.Name) 
        return dict(records=records)
    elif (d['Type']=='Composer'):
        records=db(db.Songs.Composer==iid).select(db.Songs.Name)
        return dict(records=records)
    
def query4():
    rows=db((db.Movies.ReleasedOn<datetime.date(2000,1,1)) & (db.Movies.id==db.Songs.Movie)&(db.Songs.Singer==db.Artists.id)).select(db.Songs.Name,db.Artists.Artist)
    return dict(rows=rows)
    
def query2():
 r = db((db.Artists.Artist=='Balu')&(db.Songs.Singer==db.Artists.id)).select(db.Songs.Name)
 return dict(r=r)
        
def query1():
    rows = db((db.Artists.Type=="Singer")).select(db.Artists.ALL)
    iid=rows[2]['id']
    rows=db((db.Songs.Singer==db.Artists.id)&(db.Artists.id==iid)).select(db.Songs.Name)
    print iid
    return dict(rows=rows)
    
def query3():
    rows = db((db.Artists.Artist=='Balu')&(db.Songs.Singer==db.Artists.id) & (db.Movies.Name=='Shankarabharanam')&(db.Songs.Movie==db.Movies.id)).select(db.Songs.Name)
    return dict(rows=rows)
            
def query5():
    rows = db((db.Rating.Rating>=4)&(db.Songs.id==db.Rating.Song)&(db.Artists.id==db.Songs.ActorSinging)).select(db.Songs.Name,db.Artists.Artist,db.Rating.Rating)
    
    return dict(rows=rows)
        

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to Myapp!"
    return dict(message=T('Hello World'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
