# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def points():
	x=db((db.Rated.ItemID == request.args(0)) & (db.Rated.UserID == auth.user_id)).select()
	if x:
		db.person.insert(UserID=auth.user_id,ItemID=request.args(0))
		y = x.first()
		y.rating = y.rating + int(request.args(1))
		#db(db.Item.id == request.args(0)).update(Rating+=int(request.args(1)))
		response.flash("Done")
		redirect('/default/listall')
	else:
		redirect('listall')
		

def listall():
	x = db(db.Item.id>=0).select()
	return dict(x=x)

@auth.requires_login()
def new():
	form = crud.create(db.Item)
	return dict(form=form)

@auth.requires_login()
def update():
	form = []
	if db((request.args(0)==db.Item.id) & (db.Item.User == auth.user_id)).select():
		form = crud.update(db.Item,request.args(0))
	else:
		response.flash('Unauthorized access')
		redirect('listall')
	return dict(form=form)
	
def delete():
	form = []
	if db((request.args(0)==db.Item.id) & (db.Item.User == auth.user_id)).select():
		form = crud.delete(db.Item,request.args(0))
	else:
		redirect('listall')
	return dict(form=form)
	

@auth.requires_login()
def update():
	form = crud.update(db.Item,request.args(0))
	return dict(form=form)

def list_cat():
	x = db(request.args(0)==db.Item.Category).select() or redirect(URL('index'))
	return dict(x=x)

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to web2py!"
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

