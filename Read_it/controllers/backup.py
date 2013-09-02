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
def comments():
	x = request.args(0)
	form = SQLFORM(db.Comments,fields=['Comment'],formstyle="divs",hidden=dict(ItemID=int(request.args(0))))
	form.vars.ItemID = int(x)
	results=[]
	link = db(db.Item.id == request.args(0)).select()
	if form.process().accepted:
		response.flash = "Comment posted"
	else:
		response.flash = "Please post"
	results = db((db.Comments.ItemID == int(x)) & (db.Comments.AuthID == db.auth_user.id) & (db.Comments.ItemID==db.Item.id)).select(db.Comments.ALL,db.auth_user.ALL,db.Item.ALL)
	return dict(form=form,results=results,link=link)

def search():
	results=[]
	x=request.vars['s']
	results=db(db.Item.Heading.contains(x)).select()
	return dict(results=results)

def listuser():
	users = db(db.auth_user.id>1).select()
	return dict(users=users)
@auth.requires_membership('Admin')
def addcat():
	form=SQLFORM(db.Category)
	return dict(form=form)

@auth.requires_membership('Admin')
def removeuser():
	x = int(request.args(0))
	crud.delete(db.auth_user,x)
	redirect(URL(listuser))

@auth.requires_login()
def points():
	x=db((db.Rated.ItemID == request.args(0)) & (db.Rated.UserID == auth.user_id)).select()
	prev = 0
	if x:
		z=db((db.Item.id == request.args(0))).select()
		prev = x[0]['Points']
		z[0]['Rating'] = z[0]['Rating'] - x[0]['Points']
		db((db.Rated.ItemID == request.args(0)) & (db.Rated.UserID == auth.user_id)).delete()

	x=db((db.Rated.ItemID == request.args(0)) & (db.Rated.UserID == auth.user_id)).select()
	print prev
	if not x and (prev != int(request.args(1))):
		db.Rated.insert(UserID=auth.user_id,ItemID=request.args(0),Points=int(request.args(1)))
		z=db((db.Item.id == request.args(0))).select()
		y = z.first()
		z[0]['Rating'] = z[0]['Rating'] + int(request.args(1))
		#db(db.Item.id == request.args(0)).update(Rating+=int(request.args(1)))
	else:
		redirect(URL(listall))

def listall():
	x = db(db.Item.id>=0).select(orderby='Item.Rating DESC')
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
		redirect(URL(listall))
	return dict(form=form)

def delete():
	form = []
	if db((request.args(0)==db.Item.id) & (db.Item.User == auth.user_id) ).select():
		form = crud.delete(db.Item,request.args(0))
	else:
		redirect(URL(listall))
	return dict(form=form)

def list_cat():
	x = db((request.args(0)==db.Category.Name) & (db.Category.id == db.Item.Category)).select(orderby=db.Item.Rating) or redirect(URL('listall'))
	return dict(x=x)

def check_access():
    return True if auth.is_logged_in() else False

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    results = db(db.Category.id>0).select()
    posts=[]
    comments=[]
    if check_access():
    	posts = db(db.Item.User == auth.user_id).select()
#    redirect(URL("listall"))
    return dict(posts=posts,comments=comments,results=results)

def user():
    """
    exposes:
    http://..../[ap
    	print "here"p]/default/user/login
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
#    if form.process().accepted:
#    	db.auth_membership.insert(user_id=auth.user_id,group_id=4)
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

