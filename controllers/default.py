# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
def about():
	return locals()
def contact():
	return locals()

@auth.requires_login()
def addquestion():
	if auth.user_id != 1:
		return dict(form="No Donut for you!")
	form = crud.create('Trivia')
	return dict(form=form)

@auth.requires_login()
def updatequestion():
	if auth.user_id != 1:
		return dict(form="No Donut for you!")
	no = int(request.args(0))
	form = crud.update('Trivia',no)
	return dict(form=form)

def ranklist():
	x = db(db.auth_user.id > 0).select(orderby = 'auth_user.Points DESC')
	return dict(x=x)

@auth.requires_login()
def solved():
	x = db((db.Done.User == auth.user_id) & (db.Done.Question == db.Trivia.id)).select(orderby=db.Done.Question)
	return dict(x=x)

@auth.requires_login()
def question():
	no=request.args(0)
	no = int(no)
	if auth.user_id == None:
		redirect(URL('landing'))
	if len(db((db.Level.Level == no) & (db.Level.User == auth.user_id)).select()) != 0 or no == 0:
		questions = []
		x = db((db.Trivia.Level == no) & ((db.Done.User == auth.user_id) & (db.Done.Question == db.Trivia.id))).select(db.Trivia.ALL)
		y = db(db.Trivia.Level == no).select()
		for i in y:
			if i not in x:
				questions.append(i)
		return dict(questions = questions)
	else:
		session.flash = "You are yet to reach that level yet!"
		redirect(URL('landing'))

@auth.requires_login()
def think():
	#Perform validation here
	no = int(request.vars.qno)
	if len(db((db.Level.Level == db.Trivia.Level) & (db.Trivia.id == no) & (db.Level.User == auth.user_id)).select()) > 0 or len(db((db.Trivia.id == no) & (db.Trivia.Level == 0)).select()) > 0:
		x = db(db.Trivia.id == no).select()
	else:
		x = []
		session.flash = "No Donot for you kiddo!"
		redirect(URL('landing'))
	return dict(x=x)

@auth.requires_login()
def landing():
	y = db(db.Level.User == auth.user_id).select(distinct=True)
	return dict(y=y)

@auth.requires_login()
def checkans():
	try:
		ans = int(request.vars.ans)
		qno = int(request.vars.Qno)
	except:
		qno = int(request.vars.Qno)
		session.flash = 'Invalid answer. Please enter a positive integer'
		redirect(URL('think',vars={'qno':qno}))
	if len(db((db.Done.User == auth.user_id) & (db.Done.Question == qno)).select()) > 0:
		response.flash = "You've already attempted this question"
		z = db(db.Trivia.id == qno).select(distinct=True)
		return dict(z=z,done=True)
	x = db((db.Trivia.id == qno) & (db.Trivia.Answer == ans)).select()
	if  len(x) == 0:
		session.flash = 'Wrong answer. But You can do it!'
		redirect(URL('think',vars={'qno':qno,'wrong':True}))
	#	z = db(db.Level.User == auth.user_id).select(distinct=True)
	#	response.flash = "I think you can do it!"
	#	return dict(z=z,done=False)
	else:
		db.Done.insert(User=auth.user.id,Question=qno)
		y = db((db.Done.User == auth.user.id) & (db.auth_user.id == db.Done.User)).select(db.auth_user.ALL).first()
		ans = int(y['Points'])+100
		db(db.auth_user.id == auth.user.id).update(Points=str(ans))
		if len(y) >= 2 and len(db((db.Level.User == auth.user_id) & (db.Level.Level == 1)).select()) == 0:
			session.flash = "Congratulations, Level 1 unlocked!"
			db.Level.insert(User=auth.user_id,Level=1)
		elif len(y) >= 5 and len(db((db.Level.User == auth.user_id) & (db.Level.Level == 2)).select()) == 0:
			session.flash = "Congratulations, Level 2 unlocked!"
			db.Level.insert(User=auth.user_id,Level=2)
		elif len(y) >= 10 and len(db((db.Level.User == auth.user_id) & (db.Level.Level == 3)).select()) == 0:
			session.flash = "Congratulations, Level 3 unlocked!"
			db.Level.insert(User=auth.user_id,Level=3)
		elif len(y) >= 15 and len(db((db.Level.User == auth.user_id) & (db.Level.Level == 4)).select()) == 0:
			session.flash = "Congratulations, Level 4 unlocked!"
			db.Level.insert(User=auth.user_id,Level=4)			
		z = db(db.Trivia.id == qno).select(distinct=True)
		return dict(z=z,done=True)

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Cut the Gordian Knot!"
    return dict(message=T('What is Gordian Knot?'))

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

