import random
from sms_ir import SmsIr
from django.conf import settings

# ---------------------------------------------------------------------------
def creat_random_code(count):
    count-=1
    return random.randint(10**count,10**(count+1)-1)

#----------------------------------------------------------------------------
180833
def send_sms(number, code):
    try:
        sms_ir = SmsIr(api_key=settings.API_KEY_SMS1)
        result = sms_ir.send_verify_code(
            number=str(number),
            template_id=180833,
            parameters=[
                {
                    "name": "CODE",
                    "value": str(code)
                }
            ],
        )
        if result.status_code == 200:
            result_data = result.json()  
            if result_data.get("status"):
                print("پیامک با موفقیت ارسال شد.")
            else:
                print(f"خطا در ارسال پیامک: {result_data.get('message', 'اطلاعات بیشتر وجود ندارد.')}")
        else:
            print(f"خطا در ارسال پیامک: کد وضعیت HTTP: {result.status_code}")
    except Exception as e:
        print(f"خطا در ارسال پیامک: {e}")

# ----------------------------------------------------------------------------------
def send_sms2(number, message):
    sms_ir = SmsIr(api_key=settings.API_KEY_SMS2)
    try:
        response = sms_ir.send_sms(
            number=number,
            message=message,
            linenumber= 30007732003517
        )
        if response.status_code == 200:
            result = response.json()
            print(f"API Response: {result}")
            if result.get('status') == 1:
                return result
            else:
                print(f"Error in SMS API: {result.get('message', 'No error message')}")
                return None
        else:
            print(f"Request Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None






# def send_sms2(number, patient_name, time_date):
#     sms_ir = SmsIr('YrS1swqP7UTL0v4YPZeXJWlA08oHUqmCU2zmQ5XhNWMMrIac')
#     try:
#         response = sms_ir.send_verify_code(
#             number=number,
#             template_id=942413,
#             parameters=[
#                 {"name": "patient_name", "value": str(patient_name)},
#                 {"name": "time_date", "value": str(time_date)},
#             ],
#         )
#         if response.status_code == 200:
#             result = response.json()
#             print(f"API Response: {result}")
#             if result.get('status') == 1:
#                 return result
#             else:
#                 print(f"Error in SMS API: {result.get('message', 'No error message')}")
#                 return None
#         else:
#             print(f"Request Error: {response.status_code}, {response.text}")
#             return None
#     except Exception as e:
#         print(f"Exception: {e}")
#         return None


