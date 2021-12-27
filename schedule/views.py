from time import monotonic
from django.shortcuts import redirect, render
import calendar
import itertools
import datetime
import re
from schedule.models import TakuMember, UserModel, TakuModel, TakuDate, TakuSuke

def scheduleIndex(request):
    userModel = UserModel.objects.all()
    takuModel = TakuModel.objects.all()
    takuDate = TakuDate.objects.all()
    takuMember = TakuMember.objects.all()
    users = []
    for i in userModel:
        users.append(i.userID)

    for i in takuDate:
        print(i.date)
    
    calendar.setfirstweekday(6)
    hc = calendar.monthcalendar(2021,12)
    print(hc)

    return render(request, 'schedule/index.html',{
        'userModel': userModel,
        'takuModel': takuModel,
        'takuDate': takuDate,
        'takuMember': takuMember,
        'users': users,
        'hc':hc})




def userSchedule(request,pk):
    user = pk
    takuList = TakuModel.objects.values('takuID','title').filter(userID=user)
    taku = []
    for t in takuList:
    #     print(t)
        date = TakuDate.objects.values('date').filter(takuID=t.get('takuID'))
        dates = []
        for d in date:
            dtDate = d.get('date')
            dates.append([dtDate.month,dtDate.day])
        dates
        taku.append([t.get('title'),dates])
    
    impDate = []
    for t in taku:
        impDate.append(t[1])
    
    impDate = list(itertools.chain.from_iterable(impDate))
    print(impDate)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    c = calendar.Calendar(firstweekday=6)
    base_calendar_datetime = c.monthdatescalendar(year,month)
    base_calendar = []
    for week in base_calendar_datetime:
        weekArr = []
        for day in week:
            weekArr.append([day.month, day.day])
        base_calendar.append(weekArr)
    
    print(taku)
    resData = {
        'user': user,
        'taku': taku,
        'imp': impDate,
        'year': year,
        'month': month,
        'bc': base_calendar,
    }
    return render(request, 'schedule/userSchedule.html',resData)

def takusukeIndex(request):
    if request.POST.get('title'):
        # takusuke = TakuSuke.objects.create(title=request.POST.get('title'))
        takusuke = TakuSuke(title=request.POST.get('title'))
        takusuke.save()
        print(takusuke.takusukeID)
        try:
            print("トライ")
            return redirect('./'+str(takusuke.takusukeID))
        except:
            print("えくせぷと")
            return redirect('../pk')
    return render(request, 'schedule/takusukeIndex.html')

# def takusukeCreate(request,title):
#     takusuke = TakuSuke.objects.create(title=title)
#     return takusuke(request,takusuke.pk)

def takusuke(request,pk):
    # 年月の取得
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if request.POST.get('year'):
        year = request.POST.get('year')
    if request.POST.get('month'):
        year = request.POST.get('month')
    
    # title,memberの取得
    try:
        takusukeModel = TakuSuke.objects.get(takusukeID=pk)
    except:
        print("なんかミスった")
        return redirect('./')
    title = ""
    member = []
    submit_date = []
    try:
        tModel = TakuSuke.objects.values('title','member','submitDate').filter(takusukeID=pk)
        title = tModel[0]['title']
        memberTxt = tModel[0]['member']
        member = re.findall(r'\w+',memberTxt)
        submitDateTxt = tModel[0]['submitDate']
        submit_date = re.findall(r'\d+,\d+',submitDateTxt)
        print(submit_date)

    except:
        print(takusukeModel)
    if request.POST.get('delete','user'):
        try:
            member.remove(request.POST.get('user'))
            takusukeModel.member = member
            takusukeModel.save()
        except:
            print("delete error")
    if request.POST.get('user'):
        member.append(request.POST.get('user'))
        takusukeModel.member = member
        takusukeModel.save()
    if request.POST.get('title'):
        title = request.POST.get('title')
    if request.POST.get('submitDate'):
        submit_date.append(request.POST.get('submitDate'))
    member = dict.fromkeys(member)

    users = []
    for user in member:
        taku = TakuModel.objects.values("takuID").filter(userID=user)
        userDates = []
        for t in taku:
        #     print(t)
            takuDate = TakuDate.objects.values("date").filter(takuID=t.get('takuID'))
            userDate = []
            for tDate in takuDate:
                # dateTxt = str(bDate.get("date").month) +"/"+ str(bDate.get("date").day)
                userDate.append([tDate.get("date").month,tDate.get("date").day])
            # bDate = batuDate.get("date")
            userDates.append(userDate)
        userDates = list(itertools.chain.from_iterable(userDates))
        users.append({'user':user,'date':userDates})
    
    impossible_date = []
    for u in users:
        impossible_date.append(u.get('date'))
    impossible_date = list(itertools.chain.from_iterable(impossible_date))
    
    # カレンダー
    c = calendar.Calendar(firstweekday=6)
    base_calendar_datetime = c.monthdatescalendar(year,month)
    base_calendar = []
    for week in base_calendar_datetime:
        weekArr = []
        for day in week:
            weekArr.append([day.month, day.day])
        base_calendar.append(weekArr)
    

    resData = {
        'pk': pk,
        'year': year,
        'month': month,
        'member': member,
        'users': users,
        'bc': base_calendar,
        'title': title,
        'impossible': impossible_date,
        'submit_date': submit_date,
    }
    return render(request, 'schedule/takusuke.html',resData)