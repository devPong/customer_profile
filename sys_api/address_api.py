from django.db import connections
from django.http import JsonResponse,HttpResponse
from datetime import datetime

def conn_fetchall(dataBase,q_txt):
    rawDatas = None
    with connections[dataBase].cursor() as cursor:
        cursor.execute(q_txt)
        rawDatas = cursor.fetchall()
    return rawDatas

def get_province_all(request):
    q_txt = '''
                     SELECT  c.code as "contactCode",
                            concat(c.name,' ',c.branch) as "contactName",
                            date_trunc('day', sc.create_time) as "date",
                            sc.state as "state",
                            sp."name" as "promotionName",
                            scm."type" as "earnType",
                            scm."name" as "earnName",
                            ai."number"  as "invoiceRef",
                            cvc."number"  as "createVoidRef",
                            ac."number"  as "adjustRef",
                           	so.id as "salesOrderId",
                            so.number as "ordernumber",
                            scm.price as "price",
                            count(sc.id)
                        from sale_coupon sc
                        left join contact c on  sc.contact_id = c.id
                        left join sale_promotion sp on  sc.promotion_id = sp.id
                        left join sale_coupon_master scm on sc.master_id = scm.id
                        left join account_invoice ai on cast(replace (sc.invoice_relate,'account.invoice,','') as int)  = ai.id 
                        left join create_void_coupon cvc  on cast(replace (sc.create_void_related ,'create.void.coupon,','') as int)  = cvc.id 
                        left join adjust_coupon ac on cast(replace (sc.adjust_create_related  ,'adjust.coupon,','') as int)  = ac.id 
                        left join sale_order so on cast(replace (sc.related_id ,'sale.order,','') as int)  = so.id
                        where
                            scm."type" = 'stamp'
                            and sc.create_time between '%s' and '%s'
                            and c.id  = %s
                        group by
                            c.code ,
                            concat(c.name,' ',c.branch),
                            date_trunc('day', sc.create_time),
                            sc .state,
                            sp."name" ,
                            scm."type",
                            scm."name",
                            ai."number"  ,
                            cvc."number" ,
                            ac."number" ,
                            scm.price ,
                            so.id,
                            so.number;'''  %(dateStart,dateEnd,contactID)
        # print (q_txt) 
        rawDatas = conn_fetchall(erpDB,q_txt)
        datas = []
        # so_datas_tmp = []
        for r_data in rawDatas:
            datas.append(  { 'contactCode' : r_data[0],
                    'contactName' : r_data[1],
                    'date' : r_data[2],
                    'state' : r_data[3],
                    'promotionName': r_data[4],
                    'earnType' : r_data[5],
                    'earnName' : r_data[6],
                    'invoiceRef' : r_data[7],
                    'createVoidRef' : r_data[8],
                    'adjustRef' : r_data[9],
                    'salesOrderId': r_data[10],
                    'salesOrderNumber': r_data[11],
                    'price' : r_data[12],
                    'stampAmount' : r_data[13]}
                )
            # if r_data[10] != None:
            #     so_datas_tmp.append(r_data[10])
        return datas#,so_datas_tmp