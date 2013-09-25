# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all 
#ed services (none by default)
#########################################################################
def rateaproject():
    "rate any existing project"
    form1=SQLFORM(db.Rate)
    avg=0
    print "ok"
    form2 = SQLFORM.factory(
           Field('Query','reference Project',requires=IS_IN_DB(db,'Project.id','Project.Name')))
    if form1.process().accepted:
        response.flash = 'Rated!'
   #     return dict(form=form,form2=form2,avg=avg)
    elif form2.process().accepted:
        no=0
        i=0
        rows = db(db.Rate.Project == form2.vars.Query).select(db.Rate.rating)
        for row in rows:
            no=no+row['rating']
            i=i+1
        try:
            avg=no/i
        except:
            avg=0
    #    return dict(form=form,form2=form2,avg=avg)
    return dict(form1=form1,form2=form2,avg=avg)
    
def comments():
    "comment any project"
    rows=[]
    form1=SQLFORM(db.Comment)
    form2 = SQLFORM.factory(
           Field('Query','reference Project',requires=IS_IN_DB(db,'Project.id','Project.Name')))
    if form1.process().accepted:
        response.flash = 'Commented!'
   #     return dict(form=form,form2=form2,avg=avg)
    elif form2.process().accepted:
        rows=db(db.Comment.Project==form2.vars.Query).select(db.Comment.ALL)
    return dict(form1=form1,form2=form2,rows=rows)

def seeproject():
    text=request.args(0) or redirect('index.html')
    print text
    rows=db(db.Project.Name==text).select(db.Project.ALL)
    return dict(rows=rows)
    
def email(form):
    a=request.application
    b=form.vars.file
    mail.send(to='sweetdevansh@gmail.com',
              subject='file shared by %s' % auth.user.email,
              message='http://web2py.com/%s/default/download/%s' % (a,b))

@auth.requires_login()
def editdepartment():
     "edit an existing client"
     this_page = db.department(request.args(0)) or redirect(URL('institutes'))
     form = crud.update(db.Institutes, this_page,
     next = URL('institutes'))
     return dict(form=form)
     
@auth.requires_login()
def editstudent():
     "edit an existing client"
     this_page = db.StudentPersonal(auth.user_id)
     form = crud.update(db.StudentPersonal,this_page)
     next = URL('students.html')
     return dict(form=form)
#@auth.requires_login()   
def editproject():
     "edit an existing project"
     this_page = db.Project(request.args(0)) or 1
     row=db(db.Project.id==this_page).select(db.Project.ALL)
     db.archive.insert(Name=this_page,ZipFile=row[0].ZipFile)
     form = crud.update(db.Project, this_page, onaccept=auth.archive)
     return dict(form=form)
     
@auth.requires_login()   
def joiner():
    form = SQLFORM.factory(
           Field('Query', requires=IS_IN_DB(db,'Project.id','Project.Name')))
    if form.process().accepted:
        response.flash = 'Done..'
        session.Query = form.vars.Query
        db.Request.insert(StudentName=auth.user_id,ProjectName=form.vars.Query)
    return dict(form=form)
    
def approve2():
    rows=db(db.Request.id==int(request.vars(0))).select(db.Request.ALL)
    db.StuProject.insert(ProjectName=rows[0]['ProjectName'],StudentName=rows[0]['StudentName'])
    return dict(rows=rows)
    
@auth.requires_login()              
def approve():
    if db.auth_user[auth.user.id]['typ']!='faculty':
        redirect('index.html')
    rows=db((db.Project.Owner==auth.user.id) & (db.Request.ProjectName==db.Project.id)).select(db.Request.ALL)
    return dict(rows=rows)
def seearchive():
    this_page = request.args(0) or redirect(URL('institutes'))
    result=db((db.archive.Name==db.Project.id) & (db.Project.id==this_page)).select(db.archive.ALL)
    arg=this_page
    return dict(result=result,arg=arg)
      
def search():
    import re
    new=request.get_vars
    result=[]
    query = new['s']
    rows=db().select(db.Project.ALL)
    query=re.compile(query)
    for row in rows:
        if re.search(query,row['Name']):
                result.append(row)
    return dict(result=result)
    
def projects():
    result=[]
    form = SQLFORM.factory(
        Field('Query', requires=IS_NOT_EMPTY()))
    rows=db(db.Project.id>0).select(db.Project.ALL)
    if form.process().accepted:
        response.flash = 'Results..'
        session.Query = form.vars.Query
        import re
        re.compile(session.Query)
        rows=db().select(db.Project.ALL)
        for row in rows:
            if re.search(session.Query,row['Name']):
                result.append(row)
        return dict(result=result,rows=rows,form=form)
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form,result=result,rows=rows)
@auth.requires_login()   
def update():
    if auth.user.typ=='student':
        n = db((db.auth_user.id==auth.user.id)).select(db.auth_user.ALL)
        m=n[0]['id']
        form1=SQLFORM(db.auth_user, record = m)
        return dict(form1=form1)
    elif auth.user.typ=='faculty':
        n = db((db.auth_user.id==auth.user.id) & (db.auth_user.id == db.StudentPersonal.Name)).select(db.StudentPersonal.ALL)
        m=n[0]['id']
        form1=SQLFORM(db.StudentPersonal, record = m,
        deletable = False, linkto = None,
        upload = None, fields = None, labels = None,
        col3 = {}, submit_button = 'Update',
        delete_label = 'Check to delete:',
        showid = False, readonly = False,
        comments = True, keepopts = [],
        ignore_rw = False, record_id = None,
        formstyle = 'table3cols',
        buttons = ['submit'], separator = ': ',
        **attributes)
        return dict(form1=form1)
@auth.requires_login()           
def faculty():
    result=[]
    form = SQLFORM.factory(
        Field('Query', requires=IS_NOT_EMPTY()))
    rows=db((db.auth_user.id>0)&(db.auth_user.typ=="faculty")).select(db.auth_user.ALL)
    if form.process().accepted:
        response.flash = 'Searching..'
        session.Query = form.vars.Query
        result=db((db.auth_user.first_name==session.Query) & (db.auth_user.typ=="faculty")).select(db.auth_user.ALL)
        return dict(result=result,rows=rows,form=form)
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form,result=result,rows=rows)

def students():
    result={}
    form = SQLFORM.factory(
        Field('Query', requires=IS_NOT_EMPTY()))
    rows=db((db.auth_user.id>0)&(db.auth_user.typ=="student")).select(db.auth_user.ALL)
    if form.process().accepted:
        response.flash = 'Searching..'
        session.Query = form.vars.Query
        result=db((db.auth_user.first_name==session.Query) & (db.auth_user.typ=="student")).select(db.auth_user.ALL)
        return dict(result=result,form=form,rows=rows)
    elif form.errors:
        response.flash = 'form has errors'
        return dict(result=result)
    return dict(form=form,result=result,rows=rows)

def institutes():
    result=[]
    form = SQLFORM.factory(
        Field('Query', requires=IS_NOT_EMPTY()))
    rows=db((db.Institutes.id>0)).select(db.Institutes.ALL)
    if form.process().accepted:
        response.flash = 'Searching..'
        session.Query = form.vars.Query
        import re
        re.compile(session.Query)
        rows=db().select(db.Institutes.ALL)
        for row in rows:
            if re.search(session.Query,row['Name']):
                result.append(row)
        return dict(result=result,rows=rows,form=form)
    elif form.errors:
        response.flash = 'form has errors'
        return dict(result=result)
    return dict(form=form,result=result,rows=rows)

def organizations():
    pass
@auth.requires_login()              
def Addproject():
    form=SQLFORM(db.Project)
    return dict(form=form)
    
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "XSeed Rocks!"
    form=crud.create(db.item,onaccept=email,message='Message Sent, thanks you!')
    return dict(message=T('Welcome to XSeed!'),form=form)
def login():
    form=Auth.login(auth,next='/XSeed/default/index')
    return dict(form=form)

def register():
    form=Auth.register(auth)
    auth.settings.login_after_registration = True
    auth.settings.registration_requires_approval = False
    if form.process().accepted:
        session.typ = form.vars.typ
        if session.typ=="student":
            db.auth_membership.insert(user_id=auth.user_id,group_id=1)
            db.StudentPersonal.insert(Name=form.vars.first_name + " " + form.vars.last_name,Age=18,Address=form.vars.Address,Phone=form.vars.Phone,Image=form.vars.Image)
        elif session.typ=="faculty":
            db.auth_membership.insert(user_id=auth.user_id,group_id=2)
        elif session.typ=="organization":
            db.auth_membership.insert(user_id=auth.user_id,group_id=3)
        redirect('/XSeed/default/index')
        response.flash('Account created')
    return dict(form=form)

def user():
    if request.args(0) == 'login':
        redirect('/XSeed/default/login')
    elif request.args(0) == 'register':
        redirect('/XSeed/default/register')
    form=auth()
    if form.validate() :
        session.typ = form.vars.typ
        if session.typ=="student":
            db.auth_membership.insert(user_id=auth.user_id,group_id=1)
            print "inserting"
            db.StudentPersonal.insert(Name=form.vars.first_name + " " + form.vars.last_name,Age=18,Address=form.vars.Address,Phone=form.vars.Phone,Image=form.vars.Image)
        elif session.typ=="faculty":
            db.auth_membership.insert(user_id=auth.user_id,group_id=2)
        elif session.typ=="organization":
            db.auth_membership.insert(user_id=auth.user_id,group_id=3)
        redirect('/XSeed/default/index')
    return dict(form=form)
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
