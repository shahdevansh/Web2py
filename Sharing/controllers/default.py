# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
def findItem(itemName):
    import urllib2
    import bs4
    itemName.replace(" ", "+")
    link = 'http://www.flipkart.com/search/a/all?query= {0}&vertical=all&dd=0&autosuggest[as]=off&autosuggest[as-submittype]=entered&autosuggest[as-grouprank]=0&autosuggest[as-overallrank]=0&autosuggest[orig-query]=&autosuggest[as-shown]=off&Search=%C2%A0&otracker=start&_r=YSWdYULYzr4VBYklfpZRbw--&_l=pMHn9vNCOBi05LKC_PwHFQ--&ref=a2c6fadc-2e24-4412-be6a-ce02c9707310&selmitem=All+Categories'.format(
        itemName)
    r = urllib2.Request(link, headers={"User-Agent": "Python-urlli~"})
    try:
        response = urllib2.urlopen(r)
    except:
        print "Internet connection error"
        return
    thePage = response.read()
    soup = bs4.BeautifulSoup(thePage)

    firstBlockSoup = soup.find('div', attrs={'class': 'product-unit'})
    if not firstBlockSoup:
        firstBlockSoup = soup.find('div', attrs={'class': 'size1of4 fk-medium-atom unit'})
        if not firstBlockSoup:
            print "Item Not Found"
            return

    print "Item found"
    return

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
    
    
@auth.requires_login()
def get_email():

  import facebook
    
  token = request.vars.Token
  if token:
    graph = facebook.GraphAPI(token)
    profile = graph.get_object("me")
    my_name = profile['name']
    my_id= profile['id']
    friends = graph.get_connections("me", "friends")
    friend_list_name = [friend['name'] for friend in friends['data']]
    friend_list_id = [friend['id'] for friend in friends['data']]
    k=len(friend_list_id)
    l=len(friend_list_name)
    y=auth.user.id
    db.Friend_list.user_id.default=y
    for x in range(0,k):
       l=db((db.Friend_list.id>0)&(db.Friend_list.user_id==y)&(db.Friend_list.friend_id==friend_list_id[x])).select()
       if l:
            enter=0;
       else :
            enter =1;
       if enter==1:
          db.Friend_list.insert(user_id=y,my_name=my_name,my_id=my_id,friend_name=friend_list_name[x],friend_id=friend_list_id[x])
    session.flash=T("Friend list updated")      
   #redirect(URL('contact_list'))    
    #print profile['email']
#print friend_list
  else:
     session.flash=T("Please Login First")      
     redirect(URL('auth_login')) 
     
  return locals()


def get_access_token():
    import facebook
    fb_app_id='590824174294171'
    fb_app_secret='caeab1e64171c79677117604083c5723'
    get_app_access_token(fb_app_id, fb_app_secret)


def fb_login():
    return locals()
   
def new():
    return locals()




def fb1():
    return locals()

@auth.requires_login()
def auth_login():
    return locals()


@auth.requires_login()
def contact_list():
    y=auth.user.id
    l=db((db.Friend_list.id>0)&(db.Friend_list.user_id==y)).select(db.Friend_list.friend_name)
    return locals()
