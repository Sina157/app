from flask import Flask, render_template, request , jsonify
import Db
import requests
import jdatetime
from pytz import timezone

DaysOfWeek = {
    "Saturday":"شنبه","Sunday":"یکشنبه","Monday":"دوشنبه","Tuesday":"سه‌شنبه","Wednesday":"چهارشنبه","Thursday":"پنجشبه","Friday":"جمعه"
}
Months = {
    "1":"فروردین","2":"اردیبهشت","3":"خرداد","4":"تیر","5":"مرداد","6":"شهریور","7":"مهر","8":"آبان","9":"آذر","10":"دی","11":"بهمن","12":"اسفند"
}

def SendMessageToTelegramDirect(Message):
    requests.get("https://api.telegram.org/bot6744041909:AAE-DQD8TuJpVAWZv0UDKL3_8YAcJetblmU/sendmessage?chat_id=-1001946865397&text="+Message)

def SendMessageToTelegramIndirect(Message):
    settings = {
        "UrlBox": "https://api.telegram.org/bot6744041909:AAE-DQD8TuJpVAWZv0UDKL3_8YAcJetblmU/sendmessage?chat_id=-1001946865397&text="+Message,
        "MethodList": "POST"
    }
    req = requests.post(
        "https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", settings)
    return req


app = Flask(__name__ , template_folder=".")


def SendToTelegram(f1 , f2 , f3 , visited , submited , id):
    message = f"""
    کاربر شماره: {id}
    کد اشتراکی دریافتی از ادمین:
    {f1}
    کد انتخاب شده:
    {f2}
    تاریخ و زمان رسید:
    {f3}
    """
    if submited > 1:
        now = jdatetime.datetime.now(timezone('Asia/Tehran'))
        day = DaysOfWeek.get(now.strftime("%A")) 
        time = now.strftime("%H:%M")  
        Month = Months.get(now.strftime("%m"))
        DayOfMonth = now.strftime("%d") 
        message += f"""
        کاربر تکراری هست هشدار🔴
        {visited} بار وارد سایت شده 
        {submited} بار فیلد هارو پر کرده 
        {time} {day} {DayOfMonth} {Month} 
        """
    SendMessageToTelegramIndirect(message)

@app.route('/', methods=['GET', 'POST'])
def form_page():
    Ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 
    IsFromIran = True  # For Debug
    # IsFromIran = requests.get(f"https://geolocation-db.com/json/{Ip}&position=true").json().get("country_name") == "Iran"
    if not IsFromIran:
        return "<h1>برای استفاده از سرویس فیلترشکن خود را خاموش کنید</h1>" 
    try:
        data = jsonify(request.json).get_json()
        Scode = data.get('SecretCode')
        if request.method == 'POST' and len(Scode) == 32:
            Field1 = data.get('Field1')
            Field2 = data.get('Field2')
            Field3 = data.get('Field3')
            Db.AddOrUpdate(Ip , Scode)
            User = Db.GetUserByIP(Ip)
            SendToTelegram(Field1,Field2,Field3,User[1],User[2],User[0])
            return "Ok"
    finally:
        Db.onVisitEvent(Ip)
        return render_template('form.html')

if __name__ == '__main__':
    app.run()
