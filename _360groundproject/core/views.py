from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from . import models
import datetime
from . import decorators






def register(request):
    if request.method == 'GET':
        return render(request, 'registration.html')
    elif request.method == 'POST':
        print ('Inside the post method')
        if request.POST['firstname']:
            if request.POST['lastname']:
                if request.POST['username']:
                    if request.POST['password']:
                        if request.POST['email']:
                            models.Calendar_users.objects.create(
                                first_name = request.POST['firstname'],
                                last_name = request.POST['lastname'],
                                date_of_account_creation = datetime.datetime.now(),
                                username = request.POST['username'],
                                password = request.POST['password'],
                                email = request.POST['email'],
                            )
                            request.session['status'] = 'logged_in'
                            request.session['username'] = request.POST['username']
                            return render(request, 'core/home.html')
                        else:
                            data = {
                                'firstname':request.POST['firstname'],
                                'lastname':request.POST['lastname'],
                                'username':request.POST['username'],
                                'password':request.POST['password'],
                                'emailerror':'* Please enter Email account'
                            }
                            return render(request, 'registration.html', {'data':data})
                    else:
                        data = {
                            'firstname':request.POST['firstname'],
                            'lastname':request.POST['lastname'],
                            'username':request.POST['username'],
                            'email':request.POST['email'],
                            'passworderror':'* Please enter password'
                        }
                        return render(request, 'registration.html', {'data':data})
                else:
                    data = {
                        'firstname':request.POST['firstname'],
                        'lastname':request.POST['lastname'],
                        'password':request.POST['password'],
                        'email':request.POST['email'],
                        'usernameerror':'* Please enter username',
                    }
                    return render(request, 'registration.html', {'data':data})
            else:
                data = {
                    'firstname':request.POST['firstname'],
                    'username':request.POST['username'],
                    'password':request.POST['password'],
                    'email':request.POST['email'],
                    'lastnameerror':'* Please enter lastname'
                }
                return render(request, 'registration.html', {'data':data})
        else:
            data = {
                'lastname':request.POST['lastname'],
                'username':request.POST['username'],
                'password':request.POST['password'],
                'email':request.POST['email'],
                'firstnameerror':'* Please enter first name'
            }
            return render(request, 'registration.html', {'data':data})






def log_in(request):
    if 'status' in request.session:
        if request.session['status'] == 'logged_in':
            username = request.session['username']
            user = models.Calendar_users.objects.get(username = username)
            events = models.Events_on_Calendar.objects.filter(created_by = user).reverse()
            allevents = []
            for event in events:
                single_event = {
                    'event_name':event.event_name,
                    'date_of_creation':event.date_of_creation,
                    'status':event.status,
                    'recurrence':event.recurrence,
                    'due_date':event.due_date,
                    'id':event.id,
                }
                allevents.append(single_event)
            return render(request, 'core/home.html', {'allevents':allevents})
        elif request.session['status'] == 'not_logged_in':
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                try:
                    x = models.Calendar_users.objects.get(username = username)
                    if x.password == password:
                        request.session['status'] = 'logged_in'
                        request.session['username'] = username
                        username = request.session['username']
                        user = models.Calendar_users.objects.get(username = username)
                        events = models.Events_on_Calendar.objects.filter(created_by = user).reverse()
                        allevents = []
                        for event in events:
                            single_event = {
                                'event_name':event.event_name,
                                'date_of_creation':event.date_of_creation,
                                'status':event.status,
                                'recurrence':event.recurrence,
                                'due_date':event.due_date,
                                'id':event.id,
                            }
                            allevents.append(single_event)
                        return render(request, 'core/home.html', {'allevents':allevents})
                    else:
                        errorpass = "* Password incorrect!"
                        error = {'username':username, 'errorpass':errorpass, 'password':password}   
                        return render(request, 'login.html', {'error':error})    
                except models.Calendar_users.DoesNotExist:
                    erroruser = "* Username doesn't exist!"
                    error = {'password':password, 'erroruser':erroruser, 'username':username}    
                    return render(request, 'login.html', {'error':error})             
            elif request.method == 'GET':
                return render(request, 'login.html')
    else:
        request.session['status'] = 'not_logged_in'
        return HttpResponseRedirect(reverse('log_in'))
    



@decorators.require_login
@decorators.hx_request_only
def dashboard(request):
    username = request.session['username']
    user = models.Calendar_users.objects.get(username = username)
    events = models.Events_on_Calendar.objects.filter(created_by = user).reverse()
    allevents = []
    for event in events:
        single_event = {
            'event_name':event.event_name,
            'date_of_creation':event.date_of_creation,
            'status':event.status,
            'recurrence':event.recurrence,
            'due_date':event.due_date,
            'id':event.id,
        }
        allevents.append(single_event)
    return render(request, 'core/dashboard.html', {'allevents':allevents})






@decorators.require_login
@decorators.hx_request_only
def addevents(request):
    if request.method == 'POST':
        if request.POST['eventtype'] == 'onetime':
            if request.POST['eventname']:
                if request.POST['eventdate']:
                    event_name = request.POST['eventname']
                    event_date = datetime.datetime.strptime(request.POST['eventdate'], '%Y-%m-%d') 
                    event_date = event_date.date()
                    event_status = request.POST['eventstatus']
                    event_description = request.POST['event-description']
                    username = request.session['username']
                    user = models.Calendar_users.objects.get(username = username)
                    models.Events_on_Calendar.objects.create(
                        event_name = event_name,
                        event_description = event_description,
                        date_of_creation = datetime.datetime.now(),
                        status = event_status,
                        created_by = user,
                        recurrence = False,
                        due_date = event_date,
                    )
                    return render(request, 'core/eventadditionsuccessfull.html')
                else:
                    error = {
                        "eventname":request.POST['eventname'],
                        "eventnameordate":"* Please enter Event date !"
                    }
                    return render(request, 'core/onetimeeventform.html', {'error':error})
            else:
                error = {
                    "eventdate":request.POST['eventdate'],
                    "eventnameordate":"* Please enter the Event name !"
                }
                return render (request, 'core/onetimeeventform.html', {'error':error})
        elif request.POST['eventtype'] == 'recurring':
            pass
    elif request.method == 'GET':
        return render(request, 'core/eventadditionform.html')





@decorators.require_login
@decorators.hx_request_only
def editevent(request):
    if request.method == 'GET':
        event = models.Events_on_Calendar.objects.get(id = int(request.GET['id']))
        if event.recurrence == True:
            pass
        elif event.recurrence == False:
            data = {
                'event_name':event.event_name,
                'due_date':event.due_date,
                'status':event.status,
                'event_description':event.event_description,
                'id':event.id,
            }
            return render(request, 'core/editonetimeeventform.html', {'data':data})
    elif request.method == 'POST':
        if request.POST['eventtype'] == 'onetime':
            status = request.POST['eventstatus']
            id = request.POST['id']
            if request.POST['eventname']:
                if request.POST['eventdate']:
                    event_name = request.POST['eventname']
                    event_date = datetime.datetime.strptime(request.POST['eventdate'], '%Y-%m-%d') 
                    event_date = event_date.date()
                    event_status = request.POST['eventstatus']
                    event_description = request.POST['event-description']
                    event = models.Events_on_Calendar.objects.get(id = request.POST['id'])
                    event.event_name = event_name
                    event.due_date = event_date
                    event.status = event_status
                    event.event_description = event_description
                    event.save()
                    return render(request, 'core/eventeditsuccessful.html')
                else:
                    data = {
                        "event_name":request.POST['eventname'],
                        "eventnameordate":"* Please enter Event date !",
                        "status":status,
                        "id":id,
                    }
                    return render(request, 'core/editonetimeeventform.html', {'data':data})
            else:
                data = {
                    "due_date":request.POST['eventdate'],
                    "eventnameordate":"* Please enter the Event name !",
                    "status":status,
                    "id":id,
                }
                return render (request, 'core/editonetimeeventform.html', {'data':data})
        elif request.POST['eventtype'] == 'recurring':
            return HttpResponse()





@decorators.require_login
@decorators.hx_request_only
def deleteevent(request):
    id = request.GET['id']
    models.Events_on_Calendar.objects.get(id = int(id)).delete()
    return HttpResponseRedirect(reverse('dashboard'))





@decorators.require_login
@decorators.hx_request_only
def addeventsafterreg(request):
    return render(request, 'core/onetimeeventform.html')




@decorators.require_login
@decorators.hx_request_only
def editcomplete(request):
    return HttpResponseRedirect(reverse('dashboard'))





@decorators.require_login
@decorators.hx_request_only
def changeform(request):
    print (request.GET['eventtype'])
    if request.GET['eventtype'] == 'onetime':
        return render(request, 'core/onetimeeventform.html')
    elif request.GET['eventtype'] == 'recurring':
        return render(request, 'core/recurringeventform.html')





@decorators.require_login
@decorators.hx_request_only
def changerecurrenceform(request):
    if request.GET['recurrencetype'] == 'standard_recurrence':
        return render(request, 'core/standardrecurrenceform.html')
    elif request.GET['recurrencetype'] == 'interval_patterns':
        return render(request, 'core/intervalpatternsform.html')
    elif request.GET['recurrencetype'] == 'weekdays':
        return render(request, 'core/weekdaysform.html')
    elif request.GET['recurrencetype'] == 'relative_date_pattern':
        return render(request, 'core/relativedatepatternform.html')
    




@decorators.require_login
@decorators.hx_request_only
def addrecurringevent(request):
    if request.method == 'POST':
        if request.POST['recurssiontype'] == 'standardrecurrence':
            pass
        elif request.POST['recurssiontype'] == 'intervalpatterns':
            pass
        elif request.POST['recurssiontype'] == 'weekdays':
            print ('This is ljfailjefijlsijf')
            if request.POST['eventname']:
                print('INSIDE')
                if request.POST['days_of_week'] == "":
                    data = {
                        'dayerror':'* Enter a valid day',
                        'eventname':request.POST['eventname'],
                        'eventdescription':request.POST['eventdescription'],
                    }
                    return render(request, 'core/weekdaysform.html', {'data':data})
                else:
                    user = models.Calendar_users.objects.get(username = request.session['username'])
                    eventname = request.POST['eventname']
                    status = request.POST['eventstatus']
                    description = request.POST['eventdescription']
                    day = request.POST['days_of_week']
                    newevent =  models.Events_on_Calendar.objects.create(
                        event_name = eventname,
                        event_description = description,
                        date_of_creation = datetime.datetime.now(),
                        status = request.POST['eventstatus'],
                        created_by = user,
                        recurrence = True,
                    )
                    models.Recurring_Events.objects.create(
                        Event = newevent,
                        recurrence_type = 'Weekday_selection',
                        recurring_time = {'recurringtime':request.POST['days_of_week']},
                    )
                    message = {
                        'message':'Event registered',
                    }
                    return render(request, 'core/weekdaysform.html', {'message':message})
            else:
                data = {
                    'nameerror':'* Enter Event name',
                    'eventdescription':request.POST['eventdescription'],
                }
                return render(request, 'core/weekdaysform.html', {'data':data})
        elif request.POST['recurssiontype'] == 'relativedatepatterns':
            pass
    elif request.method == 'GET':
        return HttpResponse()





@decorators.require_login
@decorators.hx_request_only
def profile(request):
    return render(request, 'core/profile.html')





@decorators.require_login
@decorators.hx_request_only
def changeusername(request):
    if request.method == 'GET':
        username = request.session['username']
        try:
            user = models.Calendar_users.objects.get(username = username)
            data = {
                "id":user.id,
            }
            return render(request, 'core/changeusername.html', {'data':data})
        except models.Calendar_users.DoesNotExist:
            pass
    elif request.method == 'POST':
        username = request.session['username']
        try:
            user = models.Calendar_users.objects.get(username = username)
            if request.POST['prevpassword']:
                if request.POST['prevusername']:
                    if request.POST['newusername']:
                        if user.password != request.POST['prevpassword']:
                            data = {
                                "prevpassword":request.POST["prevpassword"],
                                "prevusername":request.POST["prevusername"],
                                "newusername":request.POST["newusername"],
                                "prevpassworderror":"* Previous password is incorrect",
                            }
                            return render(request, "core/changeusername.html", {'data':data})
                        else:
                            if user.username != request.POST['prevusername']:
                                data = {
                                    "prevpassword":request.POST["prevpassword"],
                                    "prevusername":request.POST["prevusername"],
                                    "newusername":request.POST["newusername"],
                                    "prevusernameerror":"* Previous username is incorrect",
                                }
                                return render(request, "core/changeusername.html", {'data':data})
                            else:
                                try:
                                    models.Calendar_users.objects.get(username = request.POST['newusername'])
                                    data = {
                                        "prevpassword":request.POST["prevpassword"],
                                        "prevusername":request.POST["prevusername"],
                                        "newusername":request.POST["newusername"],
                                        "newusernameerror":"* Username already exists.",
                                    }
                                    return render(request, "core/changeusername.html", {'data':data})
                                except models.Calendar_users.DoesNotExist:
                                    user.username = request.POST['newusername']
                                    user.save()
                                    request.session['username'] = request.POST['newusername']
                                    return HttpResponseRedirect(reverse('profile'))
                    else:
                        data = {
                            "prevpassword":request.POST["prevpassword"],
                            "prevusername":request.POST["prevusername"],
                            "newusername":request.POST["newusername"],
                            "newusernameerror":"* Enter new username",
                        }
                        return render(request, "core/changeusername.html", {'data':data})
                else:
                    data = {
                        "prevpassword":request.POST["prevpassword"],
                        "prevusername":request.POST["prevusername"],
                        "newusername":request.POST["newusername"],
                        "prevusernameerror":"* Enter previous username",
                    }
                    return render(request, "core/changeusername.html", {'data':data})
            else:
                data = {
                    "prevpassword":request.POST["prevpassword"],
                    "prevusername":request.POST["prevusername"],
                    "newusername":request.POST["newusername"],
                    "prevpassworderror":"* Enter previous password",
                }
                return render(request, "core/changeusername.html", {'data':data})
        except models.Calendar_users.DoesNotExist:
            pass





@decorators.require_login
@decorators.hx_request_only
def changepassword(request):
    if request.method == 'GET':
        username = request.session['username']
        try:
            user = models.Calendar_users.objects.get(username = username)
            data = {
                "id":user.id,
            }
            return render(request, 'core/changepassword.html', {'data':data})
        except models.Calendar_users.DoesNotExist:
            pass
    elif request.method == 'POST':
        username = request.session['username']
        try:
            user = models.Calendar_users.objects.get(username = username)
            if request.POST['prevpassword']:
                if request.POST['prevusername']:
                    if request.POST['newpassword']:
                        if user.password != request.POST['prevpassword']:
                            data = {
                                "prevpassword":request.POST["prevpassword"],
                                "prevusername":request.POST["prevusername"],
                                "newpassword":request.POST["newpassword"],
                                "prevpassworderror":"* Previous password is incorrect",
                            }
                            return render(request, "core/changepassword.html", {'data':data})
                        else:
                            if user.username != request.POST['prevusername']:
                                data = {
                                    "prevpassword":request.POST['prevpassword'],
                                    "prevusername":request.POST['prevusername'],
                                    "newpassword":request.POST['newpassword'],
                                    "prevusernameerror":"* Previous username is incorrect"
                                }
                                return render(request, "core/changepassword.html", {'data':data})
                            else:
                                user.password = request.POST['newpassword']
                                user.save()
                                return HttpResponseRedirect(reverse('profile'))
                    else:
                        data = {
                            "prevpassword":request.POST["prevpassword"],
                            "prevusername":request.POST["prevusername"],
                            "newpassword":request.POST["newpassword"],
                            "newpassworderror":"* Enter new password",
                        }
                        return render(request, "core/changepassword.html", {'data':data})
                else:
                    data = {
                        "prevpassword":request.POST["prevpassword"],
                        "prevusername":request.POST["prevusername"],
                        "newpassword":request.POST["newpassword"],
                        "prevusernameerror":"* Enter previous username",
                    }
                    return render(request, "core/changepassword.html", {'data':data})
            else:
                data = {
                    "prevpassword":request.POST["prevpassword"],
                    "prevusername":request.POST["prevusername"],
                    "newpassword":request.POST["newpassword"],
                    "prevpassworderror":"* Enter previous password",
                }
                return render(request, "core/changepassword.html", {'data':data})
        except models.Calendar_users.DoesNotExist:
            pass





@decorators.require_login
def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('log_in'))