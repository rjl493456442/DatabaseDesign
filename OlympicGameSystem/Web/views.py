#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from models import *
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import logout
from datetime import datetime
def convertNationality(nationality):
    if nationality == 'CN':
        return "中国"
def convertProvince(province):
    if province == 'zj':
        return "浙江"
    if province == 'sx':
        return "山西"
    if province == 'sd':
        return "山东"
    if province == 'hb':
        return "湖北"
    if province == 'sh':
        return "上海"
    if province == 'bj':
        return "北京"


@login_required
def index(request):
    username = request.user.username
    dt = datetime.now()
    u = request.user
    teams = Team.objects.all()
    teams = sorted(teams, reverse = True)
    comlist = CompetitionEvent.objects.all()
    a_myself_event_today = []
    j_myself_event_today = []
    if u.p_user.category == 2:
        a_comlist = Attend.objects.filter(athlete = u.p_user.athlete)
        #athlete
        for itm in a_comlist:
            if itm.event.date.year == dt.year and itm.event.date.month == dt.month and itm.event.date.day == dt.day:
                a_myself_event_today.append(itm)
    if u.p_user.category == 3:

        mcomlist = CompetitionEvent.objects.filter(major_judge = u.p_user.judge)
        scomlist = CompetitionEvent.objects.filter(second_judge = u.p_user.judge)
        tcomlist = CompetitionEvent.objects.filter(third_judge = u.p_user.judge)

        for itm in mcomlist:
            if itm.date.year == dt.year and itm.date.month == dt.month and itm.date.day == dt.day:
                j_myself_event_today.append(itm)
        for itm in scomlist:
            if itm.date.year == dt.year and itm.date.month == dt.month and itm.date.day == dt.day:
                j_myself_event_today.append(itm)
        for itm in tcomlist:
            if itm.date.year == dt.year and itm.date.month == dt.month and itm.date.day == dt.day:
                j_myself_event_today.append(itm)

    TodayEvent = []
    for itm in comlist:
        if itm.date.year == dt.year and itm.date.month == dt.month and itm.date.day == dt.day:
            TodayEvent.append(itm)
    TodayEvent = sorted(TodayEvent, key = lambda x:x.date)
    return render_to_response('index.html',locals())
@login_required
def search(request):
    if request.method == "POST":
        event_name = request.POST['select_event']
        e = CompetitionEvent.objects.filter(event_name = event_name)
        for itm in e:
            print itm
        world_grade = 100000
        com_grade = 100000
        for itm in e:
            print itm.best_grade
            if itm.best_grade is not None and itm.best_grade < world_grade:
                world_grade = itm.best_grade
        com = Competition.objects.get(pk = request.POST['select_com'])
        print com
        for itm in e:
            if itm.com_grade is not None and itm.com_grade < com_grade and itm.competiton == com:
                print "Exist"
                com_grade = itm.com_grade
        print "World Best %s comBest %s" % (world_grade, com_grade)
    else:
        event = CompetitionEvent.objects.all()
        events = []
        world_best = []
        competition_best = []
        flag = True
        for itm in event:
            flag = True
            for entry in events:
                if entry.event_name == itm.event_name:
                   flag = False
                   break
            if flag ==  True:
                events.append(itm)
        competitions = Competition.objects.all()
    u = request.user
    return render_to_response('search.html',locals())
@login_required
def eventdetail(request,id):
    if request.method == "POST":
        try:
            comEvent = CompetitionEvent.objects.get(pk = id)
            attendid = request.POST['attendid']
            grade = request.POST['grade']
            rank = request.POST['rank']
            print rank
            a = Attend.objects.get(pk = attendid)
            a.grade = float(grade)
            a.rank = rank
            print a.grade
            print type(a.grade)
            # update World Best && Competition Best
            updateComLst = CompetitionEvent.objects.filter(event_name = comEvent.event_name)
            for itm in updateComLst:
                if itm.best_grade > a.grade:
                    print "Update"
                    itm.best_grade = a.grade
                    itm.save()
            for itm in updateComLst:
                if itm.competiton == comEvent.competiton and itm.com_grade > a.grade:
                    itm.com_grade = a.grade
                    itm.save()

            if a.rank == '1' and comEvent.level == 2 and comEvent.event_category != 2:
                a.athlete.n_gold = a.athlete.n_gold + 1
                a.athlete.save()
                at = a.athlete.at_athlete.all()[0]
                at.team.n_gold = at.team.n_gold + 1
                at.team.save()
            elif a.rank == '2' and comEvent.level == 2 and comEvent.event_category != 2:
                a.athlete.n_silver = a.athlete.n_silver + 1
                a.athlete.save()
                at = a.athlete.at_athlete.all()[0]
                at.team.n_silver = at.team.n_silver + 1
                at.team.save()
            elif a.rank == '3' and comEvent.level == 2 and comEvent.event_category != 2:
                a.athlete.n_bronze = a.athlete.n_bronze + 1
                a.athlete.save()
                at = a.athlete.at_athlete.all()[0]
                at.team.n_silver = at.team.n_silver + 1
                at.team.save()
            a.status = 2
            a.save()
            if comEvent.level == 0 and int(a.rank) <= 8 and comEvent.event_category != 2:
                p = CompetitionEvent.objects.filter(competiton = comEvent.competiton,level = 1, event_name = comEvent.event_name)
                if len(p) == 0:
                    p = CompetitionEvent(competiton = comEvent.competiton,level = 1,event_name = comEvent.event_name,event_category = comEvent.event_category,status = 0,date = datetime.now())
                    p.save()
                xxx = CompetitionEvent.objects.filter(competiton = comEvent.competiton, level = 1, event_name = comEvent.event_name)
                attendlocal = Attend(athlete = a.athlete,event = xxx[0],isAll = False,status = 0)
                attendlocal.save()
            if comEvent.level == 1 and int(a.rank) <= 8 and comEvent.event_category != 2:
                p = CompetitionEvent.objects.filter(competiton = comEvent.competiton,level = 2, event_name = comEvent.event_name)
                if len(p) == 0:
                    p = CompetitionEvent(competiton = comEvent.competiton,level = 2,event_name = comEvent.event_name,event_category = comEvent.event_category,status = 0,date = datetime.now())
                    p.save()
                xxx = CompetitionEvent.objects.filter(competiton = comEvent.competiton, level = 2, event_name = comEvent.event_name)
                attendlocal = Attend(athlete = a.athlete,event = xxx[0],isAll = False,status = 0)
                attendlocal.save()

        except:
            a = CompetitionEvent.objects.get(pk = id)
            status = request.POST['optionsRadios']
            print status
            if status == 'option1':
                a.status = 0
            elif status == 'option2':
                a.status = 1
            else:
                a.status = 2
            a.save()
        return HttpResponseRedirect("")
    else:
        event = CompetitionEvent.objects.get(pk = id)
        attendlist = event.a_event.all()
        athletes = []
        for itm in attendlist:
            athletes.append(itm.athlete)
    u = request.user
    return render_to_response('eventdetail.html',locals())
@login_required
def alldetail(request):
    all_event = CompetitionEvent.objects.filter(event_category = 2)
    for itm in all_event:
        print itm
    athletes = Athlete.objects.all()
    dist = {}
    for itm in athletes:
        info = []
        for q in all_event:
            eventlst = Attend.objects.filter(athlete = itm, event = q)
            if len(eventlst) > 0:
                info.append(eventlst[0])
        if len(info) > 0 and len(info) <= 3:
            dist[itm] = info
    u = request.user
    return render_to_response("alldetail.html",locals())
@login_required
def team(request):
    teams = Team.objects.all()
    u =request.user
    return render_to_response("team.html",locals())
@login_required
def teamdetail(request,id):
    team = Team.objects.get(pk = id)
    atlist = team.at_team.all()
    athletes = []
    for itm in atlist:
        athletes.append(itm.athlete)
    u = request.user
    return render_to_response("teamdetail.html",locals())
@login_required
def eventedit(request):
    if request.method == "POST":
        event_id =  request.POST['events']
        nmajor_judge = request.POST['major_judge']
        print nmajor_judge
        major_judge = Judge.objects.filter(name = nmajor_judge)
        print "DEBUG"
        njudges = request.POST.getlist("judges")
        judges = []
        for itm in njudges:
            judges.append(Judge.objects.filter(name = itm)[0])
        athletes = request.POST.getlist("athletes")
        for itm in athletes:
            print itm
        if len(judges) != 2:
            pass
        else:
            e = CompetitionEvent.objects.get(pk = event_id)
            e.a_event.status = 1
            e.status = 1
            e.major_judge = major_judge[0]
            e.second_judge = judges[0]
            e.third_judge = judges[1]
            e.save()
            ath = []
            for itm in athletes:
                ath.append(Athlete.objects.filter(name = itm)[0])
            for itm in ath:
                p = itm.a_athlete.all()
                for i in p:
                    i.status = 1
                    i.save()
            return HttpResponseRedirect("/eventedit/")
    else:
        u = request.user
        events = CompetitionEvent.objects.filter(status = 0)
        dist = {}
        for itm in events:
            ath = []
            for p in itm.a_event.all():
                ath.append(p.athlete)
            dist[itm] = ath
        judges = Judge.objects.all()
    return render_to_response("eventEdit.html", locals())
@login_required
def eventdate(request):
    if request.method == "POST":
        pass
    else:
        b_eventlist = CompetitionEvent.objects.filter(status = 0)
        i_eventlist = CompetitionEvent.objects.filter(status = 1)
        a_eventlist = CompetitionEvent.objects.filter(status = 2)
        b_attend = Attend.objects.filter(status = 0)
        i_attend = Attend.objects.filter(status = 1)
        a_attend = Attend.objects.filter(status = 2)
    u =request.user
    return render_to_response("eventdate.html",locals())
@login_required
def eventapply(request):
    if request.method == "POST":
        try:
            selectItm = request.POST.getlist('selectItem')
            isAll = request.POST.get('isallEvent',"")
            bAll = False
            if isAll == 'true':
                bAll = True
            for itm in selectItm:
                print itm
                attend = Attend(athlete = request.user.p_user.athlete,event = CompetitionEvent.objects.get(pk = itm), isAll = bAll,status = 0)
                attend.save()
            return HttpResponseRedirect('/eventapply/')
        except:
            print "DEBUG"
    else:
        u =request.user
        events = CompetitionEvent.objects.filter(status = 0)
    return render_to_response('eventapply.html', locals())

def userprofile(request, username):
    ulist = User.objects.filter(username = username)
    u = ''
    if len(ulist) > 0:
        u = ulist[0]
    if u == '':
        #todoi
        pass
    else:
        try:
            uname = u.p_user.name
            uage = u.p_user.age
            uheight = u.p_user.height
            uweight = u.p_user.weight
            unationality = u.p_user.nationality.Country
            uprovince = u.p_user.province.Province
            unationality = convertNationality(unationality)
            uprovince = convertProvince(uprovince)
            ucategory = u.p_user.category
            nsex = u.p_user.sex
            if nsex == 0:
                usex = '男'
            else:
                usex = '女'
            #common = 0
            #leader = 1
            #athlete = 2
            #judge = 3
            if ucategory == 2:
                g_num = u.p_user.athlete.n_gold
                s_num = u.p_user.athlete.n_silver
                t_num = u.p_user.athlete.n_bronze
                print g_num ,s_num,t_num
                b_eventlist = u.p_user.athlete.a_athlete.filter(status = 0)
                i_eventlist = u.p_user.athlete.a_athlete.filter(status = 1)
                a_eventlist = u.p_user.athlete.a_athlete.filter(status = 2)
            elif ucategory == 1:
                pass
            elif ucategory == 3:
                #judge
                print u.p_user.name
                majorlist = u.p_user.judge.CE_majorJudge.all()
                secondlist = u.p_user.judge.CE_secondJudge.all()
                thirdlist = u.p_user.judge.CE_thirdJudge.all()
            else:
                pass
        except:
            pass
    return render_to_response('personDetail.html',locals())
def login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username','')
            password = request.POST.get('pass','')
            print username, password
            user = auth.authenticate(username = username, password = password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect("/index/")
            else:
                #todo
                print "User not Exist"
        except:
            print "Error Keyword"
    elif request.method == 'GET':
        pass
    else:
        pass
    return render_to_response('login.html')
def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
def register(request):
    if request.user.is_authenticated():
        logout(request)
    if request.method == 'POST':
        for key,value in request.POST.items():
            print "%s--%s" % (key,value)
        try:
            uusername = request.POST['username']
            passwd = request.POST['pass']
            email = request.POST['email']
            u =  User.objects.create_user(uusername,email,passwd)
            u.save()
            uprovince = request.POST['province']
            uweight = request.POST['weight']
            uname = request.POST['uname']
            uage = request.POST['age']
            usex = request.POST['sex']
            indexsex = 0
            if usex == 'female':
                indexsex = 1
            unationality = request.POST['nationality']
            uheight = request.POST['height']
            ucategory = request.POST['category']
            ulevel = request.POST['level']
            numlevel = 0
            if ulevel == 'primary':
                numlevel = 0
            elif ulevel == 'secondary':
                numlevel = 1
            else:
                numlevel = 2
            n = Nationality.objects.get_or_create(Country = unationality)
            prv = Province.objects.get_or_create(Province = uprovince)
            if ucategory == "athlete":
                #athlete
                p = Athlete(user = u,nationality = n[0], province = prv[0], name = uname , sex = indexsex, age = uage, height = uheight, weight = uweight, level = numlevel, category = 2)
                p.save()
                team_instance = Team.objects.get_or_create(nationality = n[0], province = prv[0])
                at = AthleteTeam(team = team_instance[0],athlete = p)
                at.save()
            elif ucategory == "leader":
                #office
                p = Leader(user = u,nationality = n[0], province = prv[0], name = uname , sex = indexsex, age = uage, height = uheight, weight = uweight, level = numlevel,category = 1)
                p.save()
            elif ucategory == "judge":
                #judge
                p = Judge(user = u,nationality = n[0], province = prv[0], name = uname , sex = indexsex, age = uage, height = uheight, weight = uweight, level = numlevel,category = 3)
                p.save()
            else:
                #common people
                p = Person(user = u,nationality = n[0], province = prv[0], name = uname , sex = indexsex, age = uage, height = uheight, weight = uweight,category = 0)
                p.save()
            return HttpResponseRedirect("/index/")
        except:
            #todo
            print "Error"
    elif request.method == 'GET':
        pass
    else:
        pass
    return render_to_response('register.html')
# Create your views here.
