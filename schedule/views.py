from django.db.models import fields
from django.http import request, response
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView
from django.views.generic.edit import UpdateView
from schedule.models import TakuMember, UserModel, TakuModel, TakuDate, TakuSuke, PersonalSchedule
from time import monotonic

import calendar
import itertools
import datetime
import re


def scheduleIndex(request):
    userModel = UserModel.objects.all()
    takuModel = TakuModel.objects.all()
    takuDate = TakuDate.objects.all()
    takuMember = TakuMember.objects.all()
    users = []
    for i in userModel:
        users.append(i.userID)

    # for i in takuDate:
    #     print(i.date)
    
    calendar.setfirstweekday(6)
    hc = calendar.monthcalendar(2021,12)
    # print(hc)

    return render(request, 'schedule/index.html',{
        'userModel': userModel,
        'takuModel': takuModel,
        'takuDate': takuDate,
        'takuMember': takuMember,
        'users': users,
        'hc':hc})

'''
ユーザーのプロフィール画面
'''

'''
ユーザーの卓一覧表示
'''


'''
ユーザーのスケジュール確認画面
res = user,schedule_dict[{title,dates}],calenders
・今月の予定が見える(デフォ)
・指定した月の予定が見える
・複数月指定できる
・予定のタイトルが見える
・押すと予定の詳細が見える
'''
class UserView(TemplateView):
    template_name = 'schedule/userSchedule.html'

    def get(self,request,user):
        ## userの判別
        try:
            user_id = self.kwargs.get('user','ぬるぬるID')
            taku_model = TakuModel.objects.values('takuID','title').filter(userID=user_id)
        except:
            # userがGETできない場合
            # 「クエリを入力してね」か、リダイレクトか未定
            user_id = "ぬるぽ"
            taku_model = "ぬるぬるぽぽ"
            return redirect('/')

        ## ユーザーのスケジュールをschedule_dictに保存
        schedule_dict = []
        for tm in taku_model:
            tm_dates = TakuDate.objects.values('date').filter(takuID=tm.get('takuID'))
            dates = []
            for d in tm_dates:
                # dates[[2021,12,23],[2021,12,24],...]の形で保存
                dates.append([d.get('date').year,d.get('date').month,d.get('date').day])
            schedule_dict.append({'title':tm.get('title'), 'dates':dates})

        ## パーソナルスケジュールを保存
        ps_models = PersonalSchedule.objects.values('title','date').filter(user=user_id)
        ps_dict = []
        for ps in ps_models:
            ps_dates = re.findall(r'(\d{4})\D+(\d+)\D+(\d+)',ps.get('date'))
            dates = []
            for d in ps_dates:
                dates.append([int(d[0]),int(d[1]),int(d[2])])
            ps_dict.append({'title':ps.get('title'), 'dates': dates})
        


        ## カレンダー作成
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        num = 3
        calendar_arr = calender_method(year,month,num)

        response_data={
            'user_id': user_id,
            'schedule_dict': schedule_dict,
            'calendar_arr':calendar_arr,
            'ps_dict':ps_dict,
            'year': year,
            'month': month,
        }

        return render(request, 'schedule/userSchedule.html',response_data)
    
'''class UserViewに統合 削除予定
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
'''

# class UserTakuCreate(CreateView):
#     template_name = 'schedule/userTakuCreate.html'
#     model = TakuModel
#     fields = ('userID','title','charaURL')
#     success_url = reverse_lazy('scheduleIndex')

class PersonalScheduleCreate(CreateView):
    template_name = 'schedule/personalScheduleCreate.html'
    model = PersonalSchedule
    fields = ('user','title','member','date')
    success_url = reverse_lazy('scheduleIndex')

class PersonalScheduleUpdate(UpdateView):
    template_name = 'schedule/personalScheduleUpdate.html'
    model = PersonalSchedule
    fields = ('user','title','member','date')
    success_url = reverse_lazy('scheduleIndex')

    def get(self,request,pk):
        ps = PersonalSchedule.objects.get(pk=pk)
        user = ps.user
        title = ps.title
        members = re.findall(r'\w+',ps.member)
        dates_date = re.findall(r'(\d{4})\D+(\d+)\D+(\d+)',ps.date)
        dates = []
        for d in dates_date:
            dates.append([int(d[0]),int(d[1]),int(d[2])])

        ## カレンダー作成
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        num = 1
        calendar_arr = calender_method(year,month,num)

        response_data={
            'user':user,
            'title': title,
            'members': members,
            'dates': dates,
            'pk': pk,
            'calendar_arr':calendar_arr,
        }
        return render(request, 'schedule/personalScheduleUpdate.html',response_data)

    def post(self,request,pk):
        print(request.POST)
        ps = PersonalSchedule.objects.get(pk=pk)
        user = ps.user
        title = ps.title
        members = re.findall(r'\w+',ps.member)
        dates_date = re.findall(r'(\d{4})\D+(\d+)\D+(\d+)',ps.date)
        dates = []
        for d in dates_date:
            dates.append([int(d[0]),int(d[1]),int(d[2])])
        if request.POST.get('title'):
            title = request.POST.get('title')
            ps.title = title
            ps.save()
        if request.POST.get('member'):
            members.append(request.POST.get('member'))
            ps.member = members
            ps.save()
        if request.POST.get('date'):
            add_dates = re.findall(r'(\d{4})\D+(\d+)\D+(\d+)',request.POST.get('date'))
            if add_dates:
                for d in add_dates:
                    dates.append([int(d[0]),int(d[1]),int(d[2])])
                ps.date = dates
                ps.save()
            else:
                dates.append("形式エラー:")
                dates.append(request.POST.get('date'))

        if request.POST.get('delete'):
            post_date = re.findall(r'(\d{4})\D+(\d+)\D+(\d+)',request.POST.get('delete'))
            del_date = []
            del_date.append([int(post_date[0][0]),int(post_date[0][1]),int(post_date[0][2])])
            try:
                dates.remove(del_date[0])
                ps.date = dates
                ps.save()
            except:
                print("error")
                
        ## カレンダー作成
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        num = 1
        if request.POST.get('nowyear'):
            year = int(request.POST.get('nowyear'))
        if request.POST.get('nowmonth'):
            month = int(request.POST.get('nowmonth'))
        if request.POST.get('updown')=='>':
            month += 1
        if request.POST.get('updown')=='<':
            month -= 1
            if month <= 0:
                year -= 1
        calendar_arr = calender_method(year,month,num)

        response_data={
            'user': user,
            'title': title,
            'members': members,
            'dates': dates,
            'pk': pk,
            'calendar_arr':calendar_arr,
        }
        print(dates)
        print(calendar_arr)
        return render(request, 'schedule/personalScheduleUpdate.html',response_data)




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
        month = request.POST.get('month')
    print(year)
    print(month)
    
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


'''
class ScheduleView(TemplateView):
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    
    def get(self, request):
        try:
            # スケジュールを見たい人のIDを取ってくる
            user = request.GET['user']
            takusukeModel = TakuSuke.objects.get(takusukeID=user)
        except:
            # IDがなかった場合orデータがなかった場合
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

    def post(self, request):
        postdata = {}
        if request.POST.get('year'):
            year = request.POST.get('year')
            postdata = {'year':year}
        if request.POST.get('month'):
            month = request.POST.get('month')
        if request.POST.get('user'):
            member.append(request.POST.get('user'))
            takusukeModel.member = member
            takusukeModel.save()
        if request.POST.get('title'):
            title = request.POST.get('title')
        if request.POST.get('submitDate'):
            submit_date.append(request.POST.get('submitDate'))


        return render(request, 'schedule/takusuke.html',postdata)
'''

# '''
def calender_method(year,month,num):
    calendar_arr = []
    c_month = month
    c_year = year
    c = calendar.Calendar(firstweekday=6)
    for i in range(num):
        c_month += i
        if c_month > 12:
            c_month %= 12
            c_year += 1
        if c_month <= 0:
            c_month = 12
        base_calendar_datetime = c.monthdatescalendar(c_year,c_month)
        month_arr = []
        for week in base_calendar_datetime:
            week_arr = []
            for day in week:
                week_arr.append([day.year,day.month,day.day])
            month_arr.append(week_arr)
        calendar_arr.append(month_arr)
    
    return calendar_arr
# '''