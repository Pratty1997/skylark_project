from bottle import request,static_file,run,route,redirect,response
import update_records as ur
import json
import login

a=ur.Add_Data()
u=login.User()


root_dir='/home/skylark/'

@route('/')
def home(filename='index.html'):
    response.set_cookie('logged_in','')
    return static_file(filename,root=root_dir)

@route('/register')
def show_register(filename='register.html'):
    return static_file(filename,root=root_dir)

@route('/register',method="POST")
def register():
    email=request.forms.get('email')
    name=request.forms.get('name')
    password=request.forms.get('password')
    if(u.add_user(name,email,password)==200):
        response.set_cookie('logged_in','true')
        redirect('/')
    else:
        redirect('/login')

@route('/add')
def add_data():
    logged_in=request.get_cookie('logged_in')
    print(logged_in)
    if(logged_in=="true"):
        filename='data.html'
    else:
        filename='login2.html'
    return static_file(filename,root=root_dir)

@route('/login')
def show_login(filename='login.html'):
    return static_file(filename,root=root_dir)


@route('/login',method="POST")
def login():
    email=request.forms.get('email')
    password=request.forms.get('password')
    if(u.login(email,password)==200):
        response.set_cookie('user',email)
        response.set_cookie('logged_in',"true")
        redirect('/')


@route('/add',method="POST")
def add():
    year=request.forms.get('year')
    host=request.forms.get('host')
    resp=a.add_new(year,host)
    if(resp==200):
        return "REQUEST RECEIVED."
    else:
        return "An Error occurred, please try again."

@route('/new_data',method="POST")
def new_data():
    host=request.forms.get('host')
    host=host.upper()
    year=request.forms.get('year')
    if(year.isnumeric()):
        year=int(year)
        if(a.add_new(year,host)==200):
            return "Your request has been received, we'll add it once it is verified."
            
    else:
        return "The year that you entered was invalid."
@route('/wins')
def best_records(filename='best_records.html'):
    return static_file(filename,root=root_dir)

@route('/caf')
def caf(filename='caf.jpg'):
    return static_file(filename,root=root_dir)

@route('/most_goals')
def most_goals(filename='most_goals.html'):
    return static_file(filename,root=root_dir)

@route('/goal')
def goal(filename='goal.jpg'):
    return static_file(filename,root=root_dir)

@route('/least_goals')
def least_goals(filename='least_goals.html'):
    return static_file(filename,root=root_dir)

@route('/missed')
def missed(filename='missed.jpg'):
    return static_file(filename,root=root_dir)

@route('/get_data')
def send():
    data_r=a.send_data()
    data={'val':data_r}
    return json.dumps(data)

@route('/cup/<year>')
def show_cup(year):
    response.set_cookie('year',year)
    year=a.find_record(year)
    data="<b>Year:</b> "+str(year['_id'])+'<br><br>'+'<b>Hosted by:</b> '+year['host']+'<br><br>'+"<b>Winner: </b>"+year['winner']+'<br><br>'+"<b>Runner Up:</b> "+year['runnerup']+'<br><br>'+"<b>Third Place:</b> "+year['third']
    return data

@route('/country/<country>')
def show_country(country):
    response.set_cookie('country',country)
    found=a.find_by_country(country)
    data="<h1>"+country+"</h1>............................................................................................................................<br><br>"
    for i in found:
        data+='<b>Year: </b>'+str(i['_id'])+"<br><br><b>Winner: </b>"+i['winner']+"<br><br><b>Runner up: </b>"+i['runnerup']+"<br><br><b>Third: </b>"+i['third']+"<br>............................................................................................................................<br>"
    return data
run(host='31.220.52.15')
