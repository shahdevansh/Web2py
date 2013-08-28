# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T('Music, on you mind!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Devansh Shah <devansh.shah@students.iiit.ac.in>'
response.meta.description = 'Music Recommender!'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Built on Web2Py'
response.meta.copyright = 'Copyright 2013'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu+=[
        (SPAN('Let it Play!',_style='color:red'),False, None, [
                (T('Check these out:'),False,URL('admin','default','site')),
                (T('This App'),False,URL('admin','default','design/%s' % app), [
                        (T('Controller'),False,
                         URL('admin','default','edit/%s/controllers/%s.py' % (app,ctr))),
                        (T('View'),False,
                         URL('admin','default','edit/%s/views/%s' % (app,response.view))),
                        (T('Layout'),False,
                         URL('admin','default','edit/%s/views/layout.html' % app)),
                        (T('Stylesheet'),False,
                         URL('admin','default','edit/%s/static/css/web2py.css' % app)),
                        (T('DB Model'),False,
                         URL('admin','default','edit/%s/models/db.py' % app)),
                        (T('Menu Model'),False,
                         URL('admin','default','edit/%s/models/menu.py' % app)),
                        (T('Database'),False, URL(app,'appadmin','index')),
                        (T('Errors'),False, URL('admin','default','errors/' + app)),
                        (T('About'),False, URL('admin','default','about/' + app)),
                        ]),
                ('web2py.com',False,'http://www.web2py.com', [
                        (T('Songs'),False,'http://www.web2py.com/examples/default/download'),
                        (T('Movies'),False,'http://www.web2py.com/examples/default/support'),
                        (T('Artists'),False,'http://web2py.com/demo_admin'),
                        (T('Ratings!'),False,'http://web2py.com/examples/default/examples'),
                        (T('FAQ'),False,'http://web2py.com/AlterEgo')
                        ]),
                (T('Documentation'),False,'http://www.web2py.com/book', [
                        (T('Preface'),False,'http://www.web2py.com/book/default/chapter/00'),
                        (T('Introduction'),False,'http://www.web2py.com/book/default/chapter/01'),
                        (T('Python'),False,'http://www.web2py.com/book/default/chapter/02'),
                        (T('Overview'),False,'http://www.web2py.com/book/default/chapter/03'),
                        (T('The Core'),False,'http://www.web2py.com/book/default/chapter/04'),
                        (T('The Views'),False,'http://www.web2py.com/book/default/chapter/05'),
                        (T('Database'),False,'http://www.web2py.com/book/default/chapter/06'),
                        (T('Forms and Validators'),False,'http://www.web2py.com/book/default/chapter/07'),
                        (T('Email and SMS'),False,'http://www.web2py.com/book/default/chapter/08'),
                        (T('Access Control'),False,'http://www.web2py.com/book/default/chapter/09'),
                        (T('Services'),False,'http://www.web2py.com/book/default/chapter/10'),
                        (T('Ajax Recipes'),False,'http://www.web2py.com/book/default/chapter/11'),
                        (T('Components and Plugins'),False,'http://www.web2py.com/book/default/chapter/12'),
                        (T('Deployment Recipes'),False,'http://www.web2py.com/book/default/chapter/13'),
                        (T('Other Recipes'),False,'http://www.web2py.com/book/default/chapter/14'),
                        (T('Buy this book'),False,'http://stores.lulu.com/web2py'),
                        ]),
                (T('Catch me on :'),False, None, [
                        (T('Facebook'),False,'facebook.com/theboyinatux'),
                        (T('Twitter'),False,'http://twitter.com/theboyinatux'),
                        (T('Quora'),False,'https://www.quora.com/Devansh-Shah-2'),
                        ]),
                (T('Plugins'),False,None, [
                        ('plugin_wiki',False,'http://web2py.com/examples/default/download'),
                        (T('Other Plugins'),False,'http://web2py.com/plugins'),
                        (T('Layout Plugins'),False,'http://web2py.com/layouts'),
                        ])
                ]
         )]
_()
