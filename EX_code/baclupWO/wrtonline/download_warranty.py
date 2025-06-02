from ast import Not
import base64
from django import template
from django.template.defaultfilters import stringfilter
from io import BytesIO
import requests
import os
from PIL import Image, ImageFont, ImageDraw 
import textwrap
import datetime
from core.settings import API_Link

SITE_ROOT = os.path.abspath(os.path.dirname(__name__))
register = template.Library()


#ฟังก์ชันแปลงวันเดือนปีเป็นพ.ศ.ไปแสดง
def convert_date_to_thai_format(date_str):
    if not date_str:
        return None 
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        thai_year = date_obj.year + 543
        formatted_date = date_obj.strftime(f'%d/%m/{thai_year}')
        return formatted_date
    except ValueError:
        return None

def downloadWarannty(request):

    number_wrt = request.POST.get('number_wrt')
    brand_wrt = "lamina"
    
    api_url = API_Link + "/erp_get/wNumberChecker"
    data = {'number_wrt': number_wrt, 'brand_wrt': brand_wrt}
    response = requests.post(api_url, data=data)
    print(number_wrt)

    if response.status_code == 200:
        api_result = response.json()
        dataWRT = api_result['w_data']
        pro_code = dataWRT['product_code']
        # print(pro_code)
        cust_name = dataWRT['cust_name']
        cust_phone = dataWRT['cust_phone']
        cust_address = dataWRT['cust_address_full']
        cust_carbrand = dataWRT['cust_carbrand']
        cust_carmodel  = dataWRT['cust_carmodel']
        cust_liceseplateblack = dataWRT['cust_liceseplateblack']
        cust_vin = dataWRT['cust_vin']
        # cust_dateinstall = dataWRT['cust_install_date']
        # cust_warrant_exdate = dataWRT['cust_warrant_exdate']
        showroominstall_name = dataWRT['showroominstall_name']
        showroominstall_address = dataWRT['showroominstall_address']
        showroominstall_phone = dataWRT['showroominstall_phone']
        another_position = dataWRT['another_position']

        cust_dateinstall = convert_date_to_thai_format(dataWRT['cust_install_date'])
        cust_warrant_exdate = convert_date_to_thai_format(dataWRT['cust_warrant_exdate'])

        img = "http://172.17.1.56:8001/static/assets/img/WarrantyOnlineLamina.jpg"
        im = Image.open(requests.get(img, stream=True).raw)
        req = os.path.join(SITE_ROOT, 'static/assets/fonts/DB Adman X Bd.ttf')
        
        my_image = im.convert('RGB')
        image_editable = ImageDraw.Draw(my_image)
        font22 = ImageFont.truetype(BytesIO(open(req, "rb").read()), 22)
        font155 = ImageFont.truetype(BytesIO(open(req, "rb").read()), 155)

        # text(100,300) 100=ความยาว (เลขมากเลื่อนขวา เลขน้อยเลื่อนซ้าย) , 300=ความสูง (เลขมากจะเลื่อนลง เลขน้อยจะเลื่อนขึ้น)
        # Add text to image
        image_editable.text((2900,1650), str(number_wrt), (0, 0, 0), font=font155)
        custname = textwrap.fill(text=cust_name or '', width=100)
        
        image_editable.text((1350,2005), custname, (0, 0, 0), font=font155)
        
        if cust_dateinstall is not None:
            # anotherposition = textwrap.fill(text=another_position or '', width=70)
            anotherposition = textwrap.fill(text=another_position or '', width=60)
            dateinstall = textwrap.fill(text=cust_dateinstall or '', width=100)
            warrant_exdate = textwrap.fill(text=cust_warrant_exdate or '', width=100)
            carbrand = textwrap.fill(text=cust_carbrand or '', width=100)
            carmodel = textwrap.fill(text=cust_carmodel or '', width=100)
            liceseplateblack = textwrap.fill(text=cust_liceseplateblack or '', width=100)
            custvin = textwrap.fill(text=cust_vin or '', width=100)

            image_editable.text((750,2365), carbrand or '', (0, 0, 0), font=font155)
            image_editable.text((2405,2365), carmodel or '', (0, 0,  0), font=font155)
            image_editable.text((900,2720), liceseplateblack, (0, 0, 0), font=font155)
            image_editable.text((2600,2720), custvin or '', (0, 0, 0), font=font155)
            image_editable.text((710, 3255), anotherposition  or '', (0, 0, 0), font=font155)
            
            image_editable.text((2700,4545), dateinstall or '', (0, 0, 0), font=font155)
            image_editable.text((750, 4920), warrant_exdate or '', (0, 0, 0), font=font155)

        if showroominstall_name is not None:
            # showroominstall_address = textwrap.fill(text=showroominstall_address or '', width=55)
            showroominstall_address = textwrap.fill(text=showroominstall_address or '', width=60)
            image_editable.text((720, 3850), showroominstall_name or '', (0, 0, 0), font=font155)
            image_editable.text((720, 4020), showroominstall_address, (0, 0, 0), font=font155)
            image_editable.text((750, 4545), showroominstall_phone or '', (0, 0, 0), font=font155)
            
            
                                        
        buffered = BytesIO()
        my_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return "data:image/jpeg;base64," + img_str, {'img_str': img_str, 'number_wrt': number_wrt}
    else:
        api_result = {'error': 'Cannot fetch data from API'}



