from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
# from django.conf import settings
from django.http import JsonResponse
import datetime
from django.db import transaction, connection
from iihmrapp.api_custom_functions import api_custom_functions
from iihmrapp.models import *
from datetime import datetime
# Create your views here.
def index(request):
    return render(request,'index.html')


# login for the web user based on the username and password method POST
@csrf_exempt    
def web_login(request):
    Qid = ''
    FormCode = ''
    valid = ''
    IsFullyProcessed = ''
    ReturnStatus = ''
    ReturnError_response = {}
    ReturnJson_response = {}
    stringResponse = ''
    ApiKey = ''
    AppTypeNo = ''
    AppVersion = ''
    receivedDate = api_custom_functions.current_date_time_in_format()
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            request_json_validation = api_custom_functions.json_validation(json_body)  # Validating the Json
            if request_json_validation:
                json_request = json.loads(json_body)
                apikey_validation = api_custom_functions.apikey_validation(json_request)  # Validation the apikey
                parameters_validation = api_custom_functions.parameters_validation(json_request, 'web_login')  # validation parameters
                webservice_code = api_custom_functions.web_service_code('web_login')  # getting the webservice code
                if request_json_validation and apikey_validation and parameters_validation and webservice_code != '':
                    userid = json_request['userid']
                    password = json_request['password']
                    synceddatetime = json_request['synceddatetime']
                    FormCode = json_request['FormCode']
                    ApiKey = json_request['ApiKey']
                    AppTypeNo = json_request['AppTypeNo']
                    AppVersion = json_request['AppVersion']
                    jsonData_database = str(json.dumps(json_request))
                    receivedDate = api_custom_functions.current_date_time_in_format()
                    Qid = api_custom_functions.inserQtable_data(FormCode, jsonData_database, api_custom_functions.current_date_time_in_format(), synceddatetime)
                    # if userid == 'admin'
                    query = f"SELECT * FROM master_tbl_user where fld_user_id='{userid}' and fld_password='{password}' and fld_is_active='1'"
                    cursor = connection.cursor()
                    cursor.execute(query)
                    result = cursor.fetchall()
                    login_user_data = api_custom_functions.getting_data_in_dictionary_format(f"SELECT * FROM master_tbl_user WHERE  fld_user_id='{userid}' AND fld_password = '{password}' AND fld_is_active=1")
                    # else:
                    #     query = f"SELECT * FROM master_tbl_user where fld_useri_id ={userid}' and fld_password={password}'"
                    if not result:
                        valid = 0
                        IsFullyProcessed = 0
                        IsPartiallyProcessed = 1                    
                        ReturnStatus = 2
                        ReturnJson_response = {
                            "status": ReturnStatus,
                            "responsemessage": "Failed",
                            "serverdatetime": api_custom_functions.current_date_time_in_format(),
                        }
                    else:
                        valid = 1
                        ReturnStatus = 1
                        IsFullyProcessed = 1
                        IsPartiallyProcessed = 0
                        ReturnJson_response = {
                            "status": '1',
                            "responsemessage": "Loged In Successfully",
                            "loged_in_details": login_user_data,
                            "serverdatetime": api_custom_functions.current_date_time_in_format(),
                        }
                    stringResponse = str(json.dumps(ReturnJson_response))
                    api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                                            ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                    return JsonResponse(ReturnJson_response)
                else:
                    if parameters_validation is False:
                        Json_response = json.dumps(json_body)
                        ReturnError_response = {
                            "error_level": "2",
                            "error_message": 'Parameter validation went wrong',
                            "error_file": "views.py",
                            "serverdatetime": api_custom_functions.current_date_time_in_format(),
                        }
                        stringResponse = str(json.dumps(ReturnError_response))
                        api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                                            ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                        api_custom_functions.error_log_insert(stringResponse, Qid, FormCode,
                                                        'sp_error_log_detials', 'web_login', '1', ReturnStatus, '1')
                    return JsonResponse(ReturnError_response)
            else:
                if not request_json_validation:
                    error_json = json.dumps(json_body)
                error_status = 4
                eroor_code = 4
                ReturnError_response = {
                    "error_level": "4",
                    "error_message": 'Invalid Json Request',
                    "error_file": "views.py",
                    "serverdatetime": api_custom_functions.current_date_time_in_format()
                }
                stringResponse = str(json.dumps(error_json))
                Qid = api_custom_functions.inserQtable_data(FormCode, error_json, api_custom_functions.current_date_time_in_format(), api_custom_functions.current_date_time_in_format())
                api_custom_functions.error_log_insert(str(json.dumps(error_json)), Qid, FormCode,'sp_error_log_detials', 'get_role_details_and_mapping_location', '1', error_status, eroor_code)
                api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                return JsonResponse(ReturnError_response)
    except Exception as e:
        valid = 1
        FormCode = json_request['FormCode'] if 'FormCode' in json_request else '' # Use get method to avoid KeyError
        ApiKey = json_request['ApiKey'] if 'FormCode' in json_request else ''
        AppTypeNo = json_request['AppTypeNo'] if 'AppType' in json_request else ''
        AppVersion = json_request['AppVersion'] if 'AppVersion' in json_request else ''
        IsFullyProcessed = 0
        IsPartiallyProcessed = 1
        ReturnStatus = 3

        # Construct error response
        ReturnError_response = {
            "error_level": "3",
            "error_message": str(e),
            "error_file": "views.py",
            "serverdatetime": api_custom_functions.current_date_time_in_format(),
        }
        stringResponse = str(json.dumps(ReturnError_response))

        # Log error details
        api_custom_functions.error_log_insert(stringResponse, Qid, FormCode,
                                            'sp_error_log_detials', 'web_login', '1', ReturnStatus, '1')
        api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                                          ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)

    # Return the constructed error response
    return JsonResponse(ReturnError_response)


# login for the web user based on the username and password method POST
@csrf_exempt    
def web_login(request):
    Qid = ''
    FormCode = ''
    valid = ''
    IsFullyProcessed = ''
    ReturnStatus = ''
    ReturnError_response = {}
    ReturnJson_response = {}
    stringResponse = ''
    ApiKey = ''
    AppTypeNo = ''
    AppVersion = ''
    receivedDate = api_custom_functions.current_date_time_in_format()
    try:
        if request.method == 'POST':
            json_body = request.body.decode('utf-8')
            request_json_validation = api_custom_functions.json_validation(json_body)  # Validating the Json
            if request_json_validation:
                json_request = json.loads(json_body)
                apikey_validation = api_custom_functions.apikey_validation(json_request)  # Validation the apikey
                parameters_validation = api_custom_functions.parameters_validation(json_request, 'web_login')  # validation parameters
                webservice_code = api_custom_functions.web_service_code('web_login')  # getting the webservice code
                if request_json_validation and apikey_validation and parameters_validation and webservice_code != '':
                    userid = json_request['userid']
                    password = json_request['password']
                    synceddatetime = json_request['synceddatetime']
                    FormCode = json_request['FormCode']
                    ApiKey = json_request['ApiKey']
                    AppTypeNo = json_request['AppTypeNo']
                    AppVersion = json_request['AppVersion']
                    jsonData_database = str(json.dumps(json_request))
                    receivedDate = api_custom_functions.current_date_time_in_format()
                    Qid = api_custom_functions.inserQtable_data(FormCode, jsonData_database, api_custom_functions.current_date_time_in_format(), synceddatetime)
                    # if userid == 'admin'
                    query = f"SELECT * FROM master_tbl_user where fld_user_id='{userid}' and fld_password='{password}' and fld_is_active='1'"
                    cursor = connection.cursor()
                    cursor.execute(query)
                    result = cursor.fetchall()
                    login_user_data = api_custom_functions.getting_data_in_dictionary_format(f"SELECT * FROM master_tbl_user WHERE  fld_user_id='{userid}' AND fld_password = '{password}' AND fld_is_active=1")
                    # else:
                    #     query = f"SELECT * FROM master_tbl_user where fld_useri_id ={userid}' and fld_password={password}'"
                    if not result:
                        valid = 0
                        IsFullyProcessed = 0
                        IsPartiallyProcessed = 1                    
                        ReturnStatus = 2
                        ReturnJson_response = {
                            "status": ReturnStatus,
                            "responsemessage": "Failed",
                            "serverdatetime": api_custom_functions.current_date_time_in_format(),
                        }
                    else:
                        valid = 1
                        ReturnStatus = 1
                        IsFullyProcessed = 1
                        IsPartiallyProcessed = 0
                        ReturnJson_response = {
                            "status": '1',
                            "responsemessage": "Loged In Successfully",
                            "loged_in_details": login_user_data,
                            "serverdatetime": api_custom_functions.current_date_time_in_format(),
                        }
                    stringResponse = str(json.dumps(ReturnJson_response))
                    api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                                            ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                    return JsonResponse(ReturnJson_response)
                else:
                    if parameters_validation is False:
                        Json_response = json.dumps(json_body)
                        ReturnError_response = {
                            "error_level": "2",
                            "error_message": 'Parameter validation went wrong',
                            "error_file": "views.py",
                            "serverdatetime": api_custom_functions.current_date_time_in_format(),
                        }
                        stringResponse = str(json.dumps(ReturnError_response))
                        api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                                            ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                        api_custom_functions.error_log_insert(stringResponse, Qid, FormCode,
                                                        'sp_error_log_detials', 'web_login', '1', ReturnStatus, '1')
                    return JsonResponse(ReturnError_response)
            else:
                if not request_json_validation:
                    error_json = json.dumps(json_body)
                error_status = 4
                eroor_code = 4
                ReturnError_response = {
                    "error_level": "4",
                    "error_message": 'Invalid Json Request',
                    "error_file": "views.py",
                    "serverdatetime": api_custom_functions.current_date_time_in_format()
                }
                stringResponse = str(json.dumps(error_json))
                Qid = api_custom_functions.inserQtable_data(FormCode, error_json, api_custom_functions.current_date_time_in_format(), api_custom_functions.current_date_time_in_format())
                api_custom_functions.error_log_insert(str(json.dumps(error_json)), Qid, FormCode,'sp_error_log_detials', 'get_role_details_and_mapping_location', '1', error_status, eroor_code)
                api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                return JsonResponse(ReturnError_response)
    except Exception as e:
        valid = 1
        FormCode = json_request['FormCode'] if 'FormCode' in json_request else '' # Use get method to avoid KeyError
        ApiKey = json_request['ApiKey'] if 'FormCode' in json_request else ''
        AppTypeNo = json_request['AppTypeNo'] if 'AppType' in json_request else ''
        AppVersion = json_request['AppVersion'] if 'AppVersion' in json_request else ''
        IsFullyProcessed = 0
        IsPartiallyProcessed = 1
        ReturnStatus = 3

        # Construct error response
        ReturnError_response = {
            "error_level": "3",
            "error_message": str(e),
            "error_file": "views.py",
            "serverdatetime": api_custom_functions.current_date_time_in_format(),
        }
        stringResponse = str(json.dumps(ReturnError_response))

        # Log error details
        api_custom_functions.error_log_insert(stringResponse, Qid, FormCode,
                                            'sp_error_log_detials', 'web_login', '1', ReturnStatus, '1')
        api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                                          ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)

    # Return the constructed error response
    return JsonResponse(ReturnError_response)


  
@csrf_exempt
def admin_raw_data_download(request):
     if request.method == 'POST':
        ouputjson = {}
        Qid = ''
        formcode = ''
        valid = 0
        IsFullyProcessed = 0
        IsPartiallyProcessed = 1                    
        ReturnStatus = 2
        ReturnError_response = {}
        ReturnJson_response = {}
        stringResponse = ''
        ApiKey = ''
        AppTypeNo = ''
        AppVersion = ''
        FormCode = ''
        try:
            json_body = request.body
            request_json_validation = api_custom_functions.json_validation(json_body) # Validating the Json is valid or not
            if request_json_validation == True: # if the json is valid
                Json_request = json.loads(request.body)
                apikey_validation = api_custom_functions.apikey_validation(Json_request) # Validation the
                parameters_validation = api_custom_functions.parameters_validation(Json_request, 'admin_bc_raw_data_download') # validation th
                webservice_code = api_custom_functions.web_service_code('admin_bc_raw_data_download')  # getting the webservice code
                # if the json is valid and parameters and valid and webservice code is not empty
            if apikey_validation == True and parameters_validation == True and webservice_code !='':
                Json_request = json.loads(request.body)
                datetime_obj_to_str_array = ['fld_sys_inserted_datetime','fld_form_start_time','fld_form_end_time']
                # get the json data
                Json_request = json.loads(request.body)
                login_user_id=Json_request['login_user_id']
                request_tables = Json_request['request_tables']
                synceddatetime = Json_request['synceddatetime']
                jsonData_database = str(json.dumps(Json_request))
                Qid = api_custom_functions.inserQtable_data(webservice_code,jsonData_database,api_custom_functions.current_date_time_in_format(),synceddatetime)
                for tablenames in request_tables:
                    ouputjson[tablenames] = []
                    max_rn = request_tables[tablenames]
                    master_or_transaction_tbl = tablenames.split('_')[0]
                    if tablenames == "trn_tbl_chornic_illnesses": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_chornic_illnesses where fld_is_active='1';""")
                    elif tablenames == "trn_tbl_diabets": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_diabets where fld_is_active='1'; """)
                    elif tablenames == "trn_tbl_diet_and_nutrition": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_diet_and_nutrition where fld_is_active='1'; """)
                    elif tablenames == "trn_tbl_family_details": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_family_details where fld_is_active='1';""")
                    elif tablenames == "trn_tbl_gi_house_hold_detail": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_gi_house_hold_detail where fld_is_active='1';""")  
                    elif tablenames == "trn_tbl_health_problem": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_health_problem where fld_is_active='1';""")    
                    elif tablenames == "trn_tbl_hh_consent_form": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_hh_consent_form where fld_is_active='1';""")
                    elif tablenames == "trn_tbl_hospitalization": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_hospitalization where fld_is_active='1';""") 
                    elif tablenames == "trn_tbl_hypertension": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_hypertension where fld_is_active='1';""") 
                    elif tablenames == "trn_tbl_respondent_detail_form": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_respondent_detail_form where fld_is_active='1';""") 
                    elif tablenames == "trn_tbl_standred_of_living": 
                        # table_published_check = f"SELECT * FROM master_tbl_state "
                        table_data = api_custom_functions.getting_data_in_dictionary_format(f"""SELECT * FROM trn_tbl_standred_of_living where fld_is_active='1';""")    
                    for table_data_dict in table_data: 
                        # check the datetime_obj_to_str_array is in the table_data_dict or not
                        if datetime_obj_to_str_array:
                            for datetime_obj_to_str in datetime_obj_to_str_array:
                                # check the datetime_obj_to_str is in the table_data_dict or not
                                if datetime_obj_to_str in table_data_dict:
                                    # convert the datetime object to string
                                    table_data_dict[datetime_obj_to_str] = str(table_data_dict[datetime_obj_to_str])
                        ouputjson[tablenames].append(table_data_dict)
                # convertin the ouputjson to json
                valid = 1
                ReturnStatus = 1
                IsFullyProcessed = 1
                IsPartiallyProcessed = 0
                Json_response = {
                    "status": "1",
                    "responsemessage": ouputjson,
                    "serverdatetime": str(api_custom_functions.current_date_time_in_format())
                }
                stringResponse = str(json.dumps(Json_response))
                api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                return JsonResponse(Json_response)
            else:
                if request_json_validation == True:
                    Json_request = json.dumps(json.loads(request.body), default=str) # convert the json to string
                else:
                    Json_request = request.body # getting the json data
                Qid = api_custom_functions.inserQtable_data(webservice_code,str(Json_request),api_custom_functions.current_date_time_in_format(),'')
                Json_response ={
                "error_level": "2",
                "error_message": 'Invalid Json Request',
                "error_file": "views.py",
                "serverdatetime": api_custom_functions.current_date_time_in_format()
                }
                api_custom_functions.error_log_insert(str(Json_response),Qid,'','','admin_bc_raw_data_download','1','1','2')
                api_custom_functions.UpdateQTable('',str(json.dumps(Json_response)),'0','0','1','2','','','','','',Qid)
            return JsonResponse(Json_response)
        except Exception as e:
            if request_json_validation == True:
                Json_request = json.dumps(json.loads(request.body))
            else:
                Json_request = request.body
            # Qid = api_custom_functions.inserQtable_data(webservice_code,str(Json_request),api_custom_functions.current_date_time_in_format(),'')
            error_json ={
                "error_level": "1",                                     
                "error_message": str(e),
                "error_file": "views.py",
                "serverdatetime": api_custom_functions.current_date_time_in_format()
                }
            api_custom_functions.error_log_insert(str(json.dumps(error_json)),Qid,'','','admin_bc_raw_data_download','1','1','1')
            api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
        return HttpResponse(json.dumps(error_json), content_type="application/json")
     

# Update new apk in the folder as well as in the database to provide the new Mobile Updated APK version to the client 
@csrf_exempt
def admin_IIHMR_mobile_apk_upload(request):
    Qid = ''
    FormCode = ''
    valid = ''
    IsFullyProcessed = ''
    IsPartiallyProcessed = ''
    ReturnStatus = ''
    ReturnError_response = {}
    ReturnJson_response = {}
    stringResponse = ''
    ApiKey = ''
    AppTypeNo = ''
    AppVersion = ''
    receivedDate = api_custom_functions.current_date_time_in_format()
    if request.method == 'POST':
        try:
            # Check if the 'apk' file is present in the request
            if 'apk' not in request.FILES:
                return JsonResponse({'error': 'APK file not provided.'}, status=400)
            webservice_code = api_custom_functions.web_service_code('admin_IIHMR_mobile_apk_upload')  # getting the webservice code
            synced_datetime = api_custom_functions.current_date_time_in_format()
            rf_id = ''  # Initialize rf_id as empty string
            folder = 'IIHMR_mobile_apk_uploads'  # Replace with the desired folder name for APKs
            apk_file = request.FILES['apk']
            fldmobversioncode = request.POST.get('fld_mob_version_code')
            fldmobversionname = request.POST.get('fld_mob_version_name')
            remark = request.POST.get('remarks')
            # Create a dictionary to hold the data
            jsonData_database = {
                "apk_file": apk_file.name,
                "fld_mob_version_code": fldmobversioncode,
                "fld_mob_version_name": fldmobversionname,
                "remarks": remark
            }
            # Convert the dictionary to a JSON string
            jsonData_database_str = json.dumps(jsonData_database)
            Qid = api_custom_functions.inserQtable_data(webservice_code,jsonData_database_str,receivedDate,synced_datetime)
            # Validate that all required fields are provided
            if not all([fldmobversioncode, fldmobversionname, remark]):
                Json_response = {
                    "status": "2",
                    "responsemessage": f"Please Update the mobile version code and mobile version_name and remakrs",
                    "serverdatetime": receivedDate
                }
                stringResponse = str(json.dumps(Json_response))
                api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
            checks = [
                (master_trn_updatecheck.objects.filter(fld_mob_version_code=fldmobversioncode).exists(), f"Version code {fldmobversioncode} already exists, please change it."),
                (master_trn_updatecheck.objects.filter(fld_mob_version_name=fldmobversionname).exists(), f"Version name {fldmobversionname} already exists, please change it."),
                (master_trn_updatecheck.objects.filter(fld_file_name=apk_file).exists(), f"File name {apk_file} already exists, please change it.")
            ]
            for exists, message in checks:
                if exists:
                    Json_response = {
                        "status": "3",
                        "responsemessage": message,
                        "serverdatetime": receivedDate
                    }
                    stringResponse = json.dumps(Json_response)
                    api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed, ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                    return JsonResponse(Json_response)                
            cursor = connection.cursor()
            fldfilename = apk_file.name  # Save the file name, not the file object
            # Save the uploaded APK file
            # Insert data into Q table (assuming this function handles its own database operations)
            Qid = api_custom_functions.inserQtable_data(webservice_code, apk_file, api_custom_functions.current_date_time_in_format(), synced_datetime)
            # Execute stored procedure
            query = "CALL sp_updatecheck(%s, %s, %s, %s, %s)"
            values_need_to_insert = (rf_id, fldmobversioncode, fldmobversionname, fldfilename, remark)
            cursor.execute(query, values_need_to_insert)
            file_path = api_custom_functions.save_uploaded_image(apk_file, folder)
            # Update Q table with additional information           
            api_custom_functions.UpdateQTable(FormCode,valid,stringResponse,IsFullyProcessed,IsPartiallyProcessed,ReturnStatus,ApiKey,AppTypeNo,AppVersion,Qid)
            if file_path:
                FormCode = webservice_code,
                valid = 1,
                IsFullyProcessed=1,
                IsPartiallyProcessed=1,
                ReturnStatus=1,
                ApiKey = 'kavin',
                AppTypeNo='Mobile_apk',
                AppVersion = fldmobversioncode, 
                Json_response = {
                    "status": "1",
                    "responsemessage": f"IIHMR Mobile APK updated successfully.[file_path {file_path}]",
                    "serverdatetime": receivedDate
                }
                stringResponse = str(json.dumps(Json_response))
                api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                return JsonResponse(Json_response)
            else:
                FormCode = webservice_code,
                valid = 2,
                IsFullyProcessed= 2,
                IsPartiallyProcessed=1,
                ReturnStatus=2,
                ApiKey = 'kavin',
                AppTypeNo='Mobile_apk',
                AppVersion = fldmobversioncode, 
                Json_response = {
                    "status": "4",
                    "responsemessage": f"IIHMR Mobile APK updation not successful.Please try again",
                    "serverdatetime": receivedDate
                }
                stringResponse = str(json.dumps(Json_response))
                api_custom_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                return JsonResponse(Json_response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)