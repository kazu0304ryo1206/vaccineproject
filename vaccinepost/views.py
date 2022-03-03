from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import PlaceModel,CalendarModel,TimeModel,CustomUser,RegisterModel
from django.db import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required

year = int(2021)
month = int(12)
capacity = 2
time_num = TimeModel.objects.all().count()

def loginview(request):
    global user
    user = ""
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data'] 
        user = authenticate(request,username=username_data,password=password_data)
        if user is not None:
            login(request,user)
            return redirect('select')
        else:
            return render(request,'login.html',{'error':'このユーザ―は登録されていません'})
    return render(request,'login.html')    

@login_required
def selectview(request):
    global decision_place,decision_day,decision_time,selected_user,user,place_d,selected_num,place_d,time_d,calendar_d
    selected_num = 0
    register_list = RegisterModel.objects.filter(username=user)
    register = [i.username for i in register_list]
    if user in register:
        selected_user = 1
        decision_place = [i.place for i in register_list][0]
        decision_day = [i.day for i in register_list][0]
        decision_time = [i.time for i in register_list][0]
        place_d = PlaceModel.objects.get(place=decision_place)
        time_d = TimeModel.objects.get(time=decision_time)
        calendar_d = CalendarModel.objects.get(day=decision_day)
    else:
        selected_user = 0    
        decision_place = ""
        decision_day = ""
        decision_time = ""
    return render(request,'select.html',{'selected_user':selected_user,'decision_day':decision_day,\
    'decision_time':decision_time,'decision_place':decision_place,})

@login_required
def placeview(request):
    place = PlaceModel.objects.all()
    place_list = [i.place for i in place]
    place_list2 =[]
    if decision_day != "" and selected_user == 0:
        for i in place_list:
            each_place_d = PlaceModel.objects.get(place=i)
            num = RegisterModel.objects.filter(place__place=i,day__day=decision_day,time__time=decision_time).count()
            place_list2.append([i,num])
    else:
        for i in place_list:
            num = 0
            place_list2.append([i,num])
    return render(request,'place.html',{'place_list2':place_list2,'capacity':capacity,'selected_user':selected_user,\
    'decision_day':decision_day,'decision_time':decision_time,'decision_place':decision_place})

@login_required
def calendarview(request):
    year_month = str(year) + '/' + str(month) + '/'
    day_list = CalendarModel.objects.filter(day__contains = year_month)
    days = [date.day for date in day_list]
    empty_day = []
    full_day = []
    few_day = []
    days = [int(day[day.rfind('/')+1:]) for day in days]
    for j in range(len(day_list)):
        if decision_place == "":
            days_list =RegisterModel.objects.filter(day=day_list[j]).count()
            if days_list >= capacity * len(day_list) * time_num:
                full_day.append(days[j])
            elif days_list >= capacity * len(day_list) * time_num / 2:
                few_day.append(days[j])
            else:
                empty_day.append(days[j])
        else:
            days_list = RegisterModel.objects.filter(place__place=decision_place,day=day_list[j]).count()
            if days_list >= capacity * time_num:
                full_day.append(days[j])
            elif days_list >= capacity * time_num /2:
                few_day.append(days[j])
            else:
                empty_day.append(days[j])
    #calendar--------------------------------------
    import calendar
    import math
    day = calendar.monthrange(year,month)
    first_day = day[0] 
    end_day = day[1]
    total_day = first_day + end_day + 1
    rownum = math.ceil(total_day/7)
    total= []
    day_list = 1
    for i in range(rownum):
        if i == 0:
            for i in range(7):
                if i < first_day +1 :
                    total.append("-")
                else:
                    total.append(day_list)
                    day_list += 1
            total.append('#')
        else:
            for i in range(7):
                if day_list <= end_day:
                    total.append(day_list)
                    day_list += 1
                else:
                    total.append("-")
            total.append('#')
    return render(request,'calendar.html',{'total':total,'month':month,\
    'year':year,'days':days,'empty_day':empty_day,'full_day':full_day,'few_day':few_day,'selected_user':selected_user,\
    'decision_day':decision_day,'decision_time':decision_time,'decision_place':decision_place})

@login_required
def last_monthview(request):
    global year,month
    if month != 1:
        month = month - 1
    else:
        month = 12
        year -= 1
    return redirect('calendar')

@login_required
def next_monthview(request):
    global year,month
    if month != 12:
        month += 1
    else:
        month = 1
        year += 1
    return redirect('calendar')

@login_required
def timeview(request):
    time_list = TimeModel.objects.all() 
    time_count_list=[]
    if decision_place != "":
        for i in time_list:
            time_count = RegisterModel.objects.filter(place=place_d,day=calendar_d,time=i).count()
            time_count_list.append([i,int(time_count)])
    else:
        for i in time_list:
            time_count = (RegisterModel.objects.filter(day=calendar_d,time=i).count())
            time_count = int(time_count)/2
            time_count_list.append([i,int(time_count)])
    return render(request,'time.html',{'time_count_list':time_count_list,'capacity':capacity,'selected_user':selected_user,\
    'decision_day':decision_day,'decision_time':decision_time,'decision_place':decision_place})

@login_required
def decisionview(request,i):###calendar
    global decision_day,calendar_d,selected_num
    selected_num += 1
    if selected_user == 1:
        return redirect('time')
    else:
        decision_day = str(year) +'/' + str(month) + '/' + str(i)
        calendar_d = CalendarModel.objects.get(day=decision_day)
        return redirect('time')

@login_required
def decision2view(request,time):###time
    global decision_place,decision_time,time_d,selected_num,selected_user
    selected_num += 1
    if selected_user == 1 and selected_num == 3:
        return redirect('confirm')
    elif selected_user ==1 and selected_num != 3:
        return redirect('place')
    elif selected_num ==3 :
        decision_time = time
        time_d = TimeModel.objects.get(time=decision_time)
        return redirect('confirm')
    else:
        return redirect('place')

@login_required
def decision3view(request,i):###place
    global decision_place,decision_time,place_d,selected_num,selected_user
    selected_num += 1
    print('i:',i)
    if selected_user == 1 and selected_num ==3:
        return redirect('confirm')
    elif selected_user == 1 and selected_num !=3:
        return redirect('calendar')
    elif selected_user == 0 and selected_num ==3:
        decision_place = i
        return redirect('confirm')
    else:
        decision_place = i
        place_d = PlaceModel.objects.get(place=decision_place)
        return redirect('calendar')

@login_required
def decision4view(request):###confirm
    if decision_place != "":
        if decision_day != "" and decision_time != "":
            RegisterModel.objects.create(username=user,day=calendar_d,time=time_d,place=place_d,check='0')
        else:
            return redirect('calendar')    
    else:
        return redirect('place')        
    return redirect('login')

@login_required
def confirmview(request):
    user_count = RegisterModel.objects.filter(username=user).count()
    return render(request,'confirm.html',{'decision_day':decision_day,\
    'decision_time':decision_time,'decision_place':decision_place,'selected_user':selected_user})

@staff_member_required
def login2view(request):
    global user
    user = ""
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data'] 
        user = authenticate(request,username=username_data,password=password_data)
        if user is not None:
            login(request,user)
            return redirect('select2')
        else:
            return render(request,'login.html',{'error':'このユーザ―は登録されていません'})
    return render(request,'login.html')    

@login_required
@staff_member_required
def select2view(request):
    object_list = RegisterModel.objects.all()
    each_object = [i for i in object_list]
    data = [] 
    aitems = ['id','place','ymd','time','name']
    for i in range(len(each_object)):
        data.append(str(each_object[i].id))
        data.append(str(each_object[i].place))
        data.append(str(each_object[i].day))
        data.append(str(each_object[i].time))
        data.append(str(each_object[i].username))
        data.append('#')
    print('aitems:',aitems)
    print('data:',data)
    return render(request,'select2.html',{'data':data,'aitems':aitems})

@login_required
@staff_member_required
def decision5view(request,i):
    object_list = RegisterModel.objects.all()
    if id =='id':
        num=0
    elif i=='place':
        num = 1
    elif i =='ymd':
        num=2
    elif i=='time':
        num=3
    else:
        num=4
    data = [[str(ii.id),str(ii.place),str(ii.day),str(ii.time),str(ii.username),'#'] for ii in object_list]
    data.sort(reverse=False,key=lambda x:x[num])
    data2 = sum(data,[])
    aitems = ['id','place','ymd','time','name']

    return render(request,'select2.html',{'data':data2,'aitems':aitems})
