---
layout: post
title: Creating a blog in 2012
---
[Permalink](http://ctrl68.wordpress.com/2012/10/20/making-your-own-ddns-with-django-and-appfog/ "Permalink to Making your own DDNS with Django and AppFog « CTRL 68")

# Making your own DDNS with Django and AppFog « CTRL 68

I love web-apps as the data is always in sync magically via the cloud, but sometimes I just need to access my computer via remote access to use some app, get some file or just to start downloading some torrents (shh) . Remember/Email/Evernote a changing WAN IP is tedious that is were a DDNS comes in. My previous and old Belkin router had a bunch of options for DDNSs fortunately one was free; unfortunately and unbelievable my new [Belkin N750 DB router][1] has only one option: [Dyn][2] which is not free ![:(][3] .

So I decide to make my own DDNS with [Django][4] and with a free PaaS.

The first decision was to select a PaaS and there are a lot of option currently; the list got narrowed because I needed a free PaaS for such a simple and small app that it is just for me. Some options were: [OpenShift][5] from Red Hat, [dotCloud][6] which looks pretty good but not so simple to use and never understand if is really free or not, and other thousand options that are paid and free. I choose [AppFog][7] because I recently read that they acquire Nodster (which I loved) and the service is **so simple** to use; just what I needed for this project.

The project consist on two parts; The first one is a Django server which stores previous IPs and acts as the DDNS domain and the second one is a python script that get the WAN IP and request the server to store it.

## 1. Django Server on AppFog

Create the app on AppFog (2 clicks via its web app), download the code via its CLI ([help][8]) and create a new Django app called *ddns*.

** NOTE**: AppFog currently runs Django 1.3.1 (current version is 1.4) be sure to look at the correct [tutorial/docs][9] on their site.

### 1.1 Create Django users on AppFog

Since it is not possible to do an SSH connection on AppFog (to run commands from the terminal to create the users to access the admin web interface; wow 3 to’s on a single phrase that needs to be some kind of record) the simplest solution I could find was to create the with a view and then access it  with a URL to create the user, and then change the password ![;)][10] :


    def createuser(request):
        if authenticate(username='daniel', password='pass') is not None:
            return HttpResponse("User already created ;)")
        try:
            user = User.objects.create_user('daniel', 'daniel@ctrl68.com', 'pass')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return HttpResponse("User created! :)")
        except:
            print sys.exc_info()[0]
            return HttpResponse("Couldnt' create user :(")


### 1.2 Models

Just one model to store the IPs by date:


    class IP(models.Model):
        IP = models.CharField(max_length=15)
        date = models.DateTimeField('date')

        def __unicode__(self):
            return u'%s @ %s' % (self.IP, self.date.ctime())

        class Meta:
            get_latest_by = "date"


### 1.3 Other Views:

index which does nothing, one to add new IP addresses available via POST or GET requests, and one to redirect to the latest IP.


    def index(request):
        template = loader.get_template('index.html')
        context = Context({
            'var': 0,
        })
        return HttpResponse(template.render(context))

    def addip(request):
        ip_txt = ""
        if request.method == 'GET':
            ip_txt = request.GET.get('ip')
        elif request.method == 'POST':
            ip_txt = request.POST.get('ip')
        try:
            if ip_txt != "" and ip_txt != None:
                ip = IP(IP=ip_txt, date=datetime.datetime.now())
                ip.save()
                ans = "IP %s added." % ip_txt
                return HttpResponse(ans)
            else:
                return HttpResponse("No IP.")
        except:
            return HttpResponse("Couldnt add %s to db." % ip_txt)

    def redirect(request):
        ip = IP.objects.latest('date')
        return HttpResponseRedirect(str("http://%s" % ip.IP))


### 1.4 Fix Django Admin on AppFog

The Django Admin on AppFog doesn’t load the CSS from static files correctly I found a solution that is probably not the best but for such a small project, well it is OK. On the main urls.py:


    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns %2B= staticfiles_urlpatterns()


[![How it looks on the admin interface][12]][12]
How it looks on the admin interface

## 2. Python Script

The other part is a python script which reads [this][12] page; a nice page that the people of [whatismyip.com][13] create to help automation processes like this one.

It makes a GET request to the Django app and also saves a file on [Dropbox][14] (before this I was using Dropbox as a temporally solution). All inside a while True with a sleep of 10 minutes.

[![Output from the script][16]][16]
Output from the script

### Conclusion

Thats it! Now I can access my PC from daniel-pc.aws.af.cm – no DDoS please ![:P][16]
I want to look more other PaaS solutions, mainly OpenShift, more coming soon.

Complete code is on [github][17].

### Like this:

Be the first to like this.

 [1]: http://www.belkin.com/us/p/P-F9K1103 "Belkin N750"
 [2]: http://dyn.com/dns/ "Dyn"
 [3]: http://s0.wp.com/wp-includes/images/smilies/icon_sad.gif?m=1129645325g
 [4]: https://www.djangoproject.com "Django"
 [5]: https://openshift.redhat.com/app/ "Open Shift"
 [6]: https://www.dotcloud.com/ "dotCloud"
 [7]: http://appfog.com "appfog"
 [8]: http://blog.appfog.com/getting-started-with-appfogs-command-line/ "AppFog CLI help"
 [9]: https://docs.djangoproject.com/en/1.3/intro/tutorial01/ "Django Tutorial"
 [10]: http://s1.wp.com/wp-includes/images/smilies/icon_wink.gif?m=1129645325g
 []: http://ctrl68.files.wordpress.com/2012/10/2012-10-20_22h07_15.png
 [12]: http://automation.whatismyip.com/n09230945.asp "WAN IP detector"
 [13]: http://whatismyip.com "whatismyip.com"
 [14]: http://dropbox.com "Dropbox"
 []: http://ctrl68.files.wordpress.com/2012/10/2012-10-20_22h06_431.png
 [16]: http://s2.wp.com/wp-includes/images/smilies/icon_razz.gif?m=1129645325g
 [17]: https://github.com/dfrodriguez143/django-ddns "Django DDNS on Github"
