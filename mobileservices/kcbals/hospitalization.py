from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
from mobileservices.api_custome_functions import api_custome_functions
from iihmrapp.models import *
from django.db.models import Max
from django.db.models import Q
import string
import random
from django.forms.models import model_to_dict

@csrf_exempt
def hospitalizations_insert_ajax(request):
    Qid = ''
    FormCode = ''  # Initialize FormCode variable outside of the try block
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
    try:
        cursor = connection.cursor()
        if request.method == 'POST':
            # Define request_json_validation here
            json_body = request.body.decode('utf-8')
            request_json_validation = api_custome_functions.json_validation(json_body)
            # If the JSON is valid
            if request_json_validation:
                Json_request = json.loads(json_body)
                apikey_validation = api_custome_functions.apikey_validation(Json_request)
                parameters_validation = api_custome_functions.parameters_validation(Json_request, 'syncData')
                web_service_code = api_custome_functions.webservice_code('syncData')
                receivedDate = api_custome_functions.current_date_time_in_format()
            # If JSON, API key, parameters are valid, and webservice code is not empty
            if request_json_validation and apikey_validation and parameters_validation and web_service_code !='':
                Json_request = json.loads(json_body)
                result_array = []
                synceddatetime = Json_request ['synceddatetime']
                FormCode = Json_request ['formcode']
                ApiKey = Json_request ['apikey']
                AppTypeNo = Json_request ['apptypeno']
                AppVersion = Json_request ['appversion']
                # Insert data into Qtable
                Qid = api_custome_functions.inserQtable_data(FormCode, json.dumps(Json_request), receivedDate, synceddatetime)
                # Check if the State is already exists or not
                if "trn_tbl_hospitalization" in Json_request:
                    hospitalization_data = Json_request["trn_tbl_hospitalization"]
                    for hospitalization in hospitalization_data:
                        fld_rf_id = hospitalization['fld_rf_id'] 
                        fld_state_swid = hospitalization['fld_state_swid'] 
                        fld_state_code = hospitalization['fld_state_code'] 
                        fld_state_name = hospitalization['fld_state_name'] 
                        fld_district_swid = hospitalization['fld_district_swid'] 
                        fld_district_code = hospitalization['fld_district_code'] 
                        fld_district_name = hospitalization['fld_district_name'] 
                        fld_taluk_swid = hospitalization['fld_taluk_swid'] 
                        fld_taluk_code = hospitalization['fld_taluk_code'] 
                        fld_taluk_name = hospitalization['fld_taluk_name'] 
                        fld_block_sw_Id = hospitalization['fld_block_sw_Id']
                        fld_block_code = hospitalization['fld_block_code']
                        fld_block_name = hospitalization['fld_block_name']
                        fld_panchyt_swid = hospitalization['fld_panchyt_swid'] 
                        fld_panchyt_code = hospitalization['fld_panchyt_code'] 
                        fld_panchyt_name = hospitalization['fld_panchyt_name'] 
                        fld_phc_swid = hospitalization['fld_phc_swid'] 
                        fld_phc_code = hospitalization['fld_phc_code'] 
                        fld_phc_name = hospitalization['fld_phc_name'] 
                        fld_hsc_hwc_swid = hospitalization['fld_hsc_hwc_swid'] 
                        fld_hsc_hwc_code = hospitalization['fld_hsc_hwc_code'] 
                        fld_hsc_hwc_name = hospitalization['fld_hsc_hwc_name'] 
                        fld_village_swid = hospitalization['fld_village_swid'] 
                        fld_village_code = hospitalization['fld_village_code'] 
                        fld_village_name = hospitalization['fld_village_name'] 
                        fld_hh_id = hospitalization['fld_hh_id'] 
                        fld_member_swid = hospitalization['fld_member_swid'] 
                        fld_member_id = hospitalization['fld_member_id'] 
                        fld_name = hospitalization['fld_name']
                        fld_num_hospit_event = hospitalization['fld_num_hospit_event']
                        fld_recent_hospi_illns_detals = hospitalization['fld_recent_hospi_illns_detals'] 
                        fld_recent_hosptl_name_id = hospitalization['fld_recent_hosptl_name_id'] 
                        fld_recent_hosptl_name_name = hospitalization['fld_recent_hosptl_name_name'] 
                        fld_hospital_any_other_specify = hospitalization['fld_hospital_any_other_specify'] 
                        fld_totl_amnt_spnt_hosptlzn = hospitalization['fld_totl_amnt_spnt_hosptlzn'] 
                        fld_arrang_money_id = hospitalization['fld_arrang_money_id'] 
                        fld_arrang_money_name = hospitalization['fld_arrang_money_name'] 
                        fld_arrang_any_other_specify = hospitalization['fld_arrang_any_other_specify'] 
                        fld_did_covr_expnd_helth_schm_id = hospitalization['fld_did_covr_expnd_helth_schm_id'] 
                        fld_did_covr_expnd_helth_schm_name = hospitalization['fld_did_covr_expnd_helth_schm_name'] 
                        fld_name_schme = hospitalization['fld_name_schme'] 
                        fld_data_source = hospitalization['fld_data_source'] 
                        fld_loggedin_user_id  = hospitalization['fld_loggedin_user_id'] 
                        fld_is_full_form_completed_form = hospitalization['fld_is_full_form_completed_form'] 
                        fld_form_start_time = hospitalization['fld_form_start_time'] 
                        fld_form_end_time = hospitalization['fld_form_end_time']  
                        fld_app_version = hospitalization['fld_app_version']
                        fld_date_of_interview = hospitalization['fld_date_of_interview']   
                        fld_interviewer_name = hospitalization['fld_interviewer_name']
                        
                        
                        
                        query = "CALL sp_hospitalization(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"#46
                        values_need_to_insert = (fld_rf_id,fld_state_swid,fld_state_code,fld_state_name,fld_district_swid,fld_district_code,fld_district_name,fld_taluk_swid,fld_taluk_code,fld_taluk_name,fld_block_sw_Id,fld_block_code,fld_block_name,fld_panchyt_swid,fld_panchyt_code,fld_panchyt_name,fld_phc_swid,fld_phc_code,fld_phc_name,fld_hsc_hwc_swid,fld_hsc_hwc_code,fld_hsc_hwc_name,fld_village_swid,fld_village_code,fld_village_name,fld_hh_id,fld_member_swid,fld_member_id,fld_name,fld_num_hospit_event,fld_recent_hospi_illns_detals,fld_recent_hosptl_name_id,fld_recent_hosptl_name_name,fld_hospital_any_other_specify,fld_totl_amnt_spnt_hosptlzn,fld_arrang_money_id,fld_arrang_money_name,fld_arrang_any_other_specify,fld_did_covr_expnd_helth_schm_id,fld_did_covr_expnd_helth_schm_name,fld_name_schme,Qid,fld_data_source,fld_loggedin_user_id,fld_is_full_form_completed_form,fld_form_start_time,fld_form_end_time,fld_app_version,fld_date_of_interview,fld_interviewer_name) 
                        result = cursor.execute(query, values_need_to_insert)
                       

                    if result == True:
                        Json_response = {
                            "staus": 'True',
                            "Qid":Qid
                        }
                       
                    
                        return JsonResponse(Json_response)
                    else:
                         Json_response = {
                            "staus": 'False',
                            "Qid":Qid
                        }
                         return JsonResponse(Json_response)
                stringResponse=json.dumps(Json_response)
                api_custome_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                                    ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
                # FormCode,valid,stringResponse,IsFullyProcessed,IsPartiallyProcessed,ReturnStatus,ApiKey,qId
                return JsonResponse(Json_response)
            else:
                        if request_json_validation is False:  # If the JSON is valid
                            Json_request = json.dumps(json.loads(json_body),default=str) # Convert the JSON data to a string
                            Json_request = json_body  # Get the JSON data
                            Qid = api_custome_functions.inserQtable_data(FormCode, str(Json_request),
                            api_custome_functions.current_date_time_in_format(), '')
                            Json_response = {
                            "error_level": "2",
                            "error_message": 'Invalid Json Request',
                            "error_file": "views.py",
                            "serverdatetime": current_date
                            }
                        return JsonResponse(Json_response)
    except Exception as e:
        Json_response = {
            "error_level": "1",
            "error_message": str(e),
            "error_file": "views.py",
            "serverdatetime": api_custome_functions.current_date_time_in_format()
        }
        api_custome_functions.error_log_insert(str(json.dumps(Json_response)), Qid, FormCode, '', 'attendance_master', '1', '1','1')
        api_custome_functions.UpdateQTable(FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed,
                        ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
    return JsonResponse(Json_response)   

