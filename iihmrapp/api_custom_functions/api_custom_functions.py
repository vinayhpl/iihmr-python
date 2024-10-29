import json,datetime
from django.conf import settings
from django.db import connection
import mysql.connector
from iihmrapp.models import *
import logging
import mysql.connector
import traceback
import os
#fucntion to check the requested json is valid or not 
def json_validation(json_data):
    try:
        #checking the json_data is having the parameters or not 
        if json.loads(json_data)!=None:
            return True
        else:
            return False
    except Exception as e:
        error_log_insert(str(json.dumps(json_data)),'','','','','1','1','1')
        # sonar-ignore
        UpdateQTable('',str(json.dumps(json_data)),'','','','','1','1','1') # nosonar
    return False
    # except Exception as e:
    #     error_log_insert(str(json.dumps(json_data))),'','','','','1','1','1')
    #     UpdateQTable('',str(json.dumps(json_data))),'','','','','1','1','1')

# Function to insert the error into the database
def error_log_insert(error_json, Qid, formcode, spName, method_name, error_severity, error_status, error_code):
    error_log_upload_sql = "CALL sp_error_log_detials(%s, %s, %s, %s, %s, %s, %s, %s)"
    values_need_to_insert = (error_json, Qid, formcode, spName, method_name, error_severity, error_status, error_code)
    result = Query_execution(error_log_upload_sql, values_need_to_insert)  # Corrected function name to Query_execution
    return result

# Function to check the api key is valid or not
def apikey_validation(json_data):
    #checking the api key from the json data
    try:
        # getting the jason data and fetching the api key from the request
        api_key_from_request = json_data['ApiKey']
        # Checking if the API key matches the expected value
        if api_key_from_request == 'kavin':
            return True
        else:
            return False
    except:
        return False

# Function to check the all the required parameters are available in the json data or not
def parameters_validation(json_data, parameters_of):
    try:
        # Define required parameters based on the specified type
        if parameters_of == 'web_login':
            required_parameters = ['userid', 'password', 'synceddatetime', 'FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']
        elif parameters_of == 'user_master':
            required_parameters = ['login_role_code', 'login_user_id', 'user_date_of_joining', 'user_assigned_role_code', 'user_assigned_role_name', 'user_reg_username', 'user_reg_age', 'user_reg_gender_name', 'user_reg_mobile_nu', 'user_reg_email_id', 'user_reg_user_id', 'user_reg_user_pass']
        elif parameters_of == 'work_location_mappings':
            required_parameters = ['work_map_state_code', 'work_map_state', 'work_map_district_code', 'work_map_district', 'work_map_block_code', 'work_map_block', 'work_map_shc_code', 'work_map_shc', 'work_map_panchayat_code', 'work_map_panchayat', 'work_map_village_code', 'work_map_village', 'work_map_anganwadi_code', 'work_map_anganwadi', 'FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']
        elif parameters_of == 'web_create_state':
                required_parameters = ['state_name','synceddatetime','FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']
        elif parameters_of == 'web_create_district':
                required_parameters = ['state_swid','state_code','state_name','district_code','district_name','synceddatetime', 'FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']
        elif parameters_of == 'web_create_block':
                required_parameters = ['state_swid','state_code','state_name','district_swid','district_code','district_name','block_name','synceddatetime','FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']      
        elif parameters_of == 'web_create_shc':
                required_parameters = ['state_swid','state_code','state_name','district_swid','district_code','district_name','block_swid','block_code','block_name','shc_code','shc_name','synceddatetime','FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']    
        elif parameters_of == 'web_create_panchayat':
                required_parameters = ['state_swid','state_code','state_name','district_swid','district_code','district_name','block_swid','block_code','block_name','shc_swid','shc_code','shc_name','panchayat_code','panchayat_name','synceddatetime','FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']           
        elif parameters_of == 'web_create_village':
                required_parameters = ['state_swid','state_code','state_name','district_swid','district_code','district_name','block_swid','block_code','block_name','shc_swid','shc_code','shc_name','panchayat_swid','panchayat_code','panchayat_name','village_code','village_name','synceddatetime','FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']
        elif parameters_of == 'web_create_state':
            required_parameters = ['state_name', 'synceddatetime', 'FormCode', 'ApiKey', 'AppTypeNo', 'AppVersion']
        elif parameters_of =='get_state':
           required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='get_district':
            required_parameters = ['role_id','userid','state_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='get_block':
            required_parameters = ['role_id','userid','state_code','district_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='get_shc':
            required_parameters = ['role_id','userid','state_code','district_code','block_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='get_panchayat':
            required_parameters = ['role_id','userid','state_code','district_code','block_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='get_village':
            required_parameters = ['role_id','userid','state_code','district_code','block_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='get_role_details_and_mapping_location':
            required_parameters = ['login_role_id','login_userid','role_code','role_name','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']      
        elif parameters_of =='get_all_roles':
            required_parameters = ['login_id','log_userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']     
        elif parameters_of =='WebRegerdUserMaster_ViewAll':
            required_parameters = ['login_role_code','login_user_id','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']        
        elif parameters_of =='create_group_master':
            required_parameters = ['login_id','login_user_id','village_name','group_name','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']            
        elif parameters_of =='create_session_master':
            required_parameters = ['login_id','login_user_id','session_name','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']  
        elif parameters_of =='create_school_master':
            required_parameters = ['login_id','login_user_id','district_code','district_name','block_code','block_name','panchayat_code','panchayat_name','village_code','village_name','school_UDISE_id','school_name','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='get_all_state_geo_location':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='attendance_insert':
            required_parameters = ['synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_group_master_data':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_school_master_data':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_session_master_data':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_village_master_data':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_attendence_panachayata_data':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_attendence_panachayata_data':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_attendence_village_data':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_adoleascent_data':
            required_parameters = ['role_id','userid','panchayat_code','village_code','group_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='retrieve_group_list_all':
            required_parameters = ['role_id','userid','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='all_group_adoleacesnt_list_group_wise':
            required_parameters = ['role_id','userid','group_swid','group_number','group_lead_name','session_swid','session_code','session_name','attend_date','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='update_new_attendence':
            required_parameters = ['synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']    
        elif parameters_of =='bc_section_01_sync_data':
            required_parameters = ['synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']    
        elif parameters_of =='get_all_groups_info':
            required_parameters = ['role_id','userid','village_code','village_name','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']    
        elif parameters_of =='trn_tbl_fc_mpr_section':
            required_parameters = ['role_id','form_id','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']    
        elif parameters_of =='mpr_sections_status':
            required_parameters = ['role_id','fld_month_id','fld_month_name','fld_year_id','fld_year','fld_date','fld_fc_user_id','fld_fc_user_name','fld_fc_mpr_status','fld_fc_remarks','fld_bc_user_id','fld_bc_user_name','fld_bc_mpr_status','fld_bc_remarks','fld_po_user_id','fld_po_user_name','fld_po_mpr_status','fld_po_remarks','fld_state_po_user_id','fld_state_po_user_name','fld_state_po_mpr_status','fld_state_po_remarks','fld_data_source', 'fld_login_user_id','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion',]    
        elif parameters_of =='geo_location_mpr':
            required_parameters = ['login_user_id','FormCode','ApiKey','AppTypeNo','AppVersion','synceddatetime']
        elif parameters_of =='total_count_of_adolescents_agewise':
            required_parameters = ['role_id','login_user_id','month_id','year_id','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion'] 
        elif parameters_of =='trn_tbl_fc_mpr_section_6':
            required_parameters = ['synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion'] 
        elif parameters_of =='mpr_staus_check_and_display':
            required_parameters = ['role_id','userid','month_id','year_id','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='fc_section2':
            required_parameters = ['ApiKey' ,'AppTypeNo' ,'AppVersion' ,'FormCode' ,'synceddatetime']
        elif parameters_of =='fc_section3':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section4':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section5':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section6':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section7':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section8':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section9':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section10':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section11':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section12':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section13':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section14':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section15':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section16':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_section17':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
            # 'role_id' ,'mpr_id' ,'name_of_fc' ,'state_swid' ,'state_code' ,'state_name' ,'district_swid' ,'district_code' ,'district_name' ,'block_swid' ,'block_code' ,'block_name' ,'panchayat_swid' ,'panchayat_name' ,'panchayat_code' ,'village_swid' ,'village_code' ,'village_name' ,'month_id' ,'month_name' ,'mpr_year_id' ,'mpr_year' ,'date_of_ahwd' ,'ahwd_place_id' ,'ahwd_place_name' ,'hsc_swid' ,'hsc_code' ,'hsc_name' ,'gender_id' ,'gender_name' ,'num_ado_part_10_to_14_years' ,'num_ado_part_15_to_19_years' ,'num_bmi_service_rec_10_to_14_years' ,'num_bmi_service_rec_15_to_19_years' ,'num_hbtest_service_rec_10_to_14_years' ,'num_hbtest_service_rec_15_to_19_years' ,'num_ttshot_service_rec_10_to_14_years' ,'num_ttshot_service_rec_15_to_19_years' ,'num_couns_service_rec_10_to_14_years' ,'num_couns_service_rec_15_to_19_years' ,'num_ref_service_rec_10_to_14_years' ,'num_ref_service_rec_15_to_19_years','data_source' ,'loggedin_user_id' ,
        elif parameters_of =='retrive_comm_bind_web':
            required_parameters = ['bind_type_code','bind_type_name','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='shc_realted_data_for_sections':
            required_parameters = ['role_id','login_user_id','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='panachayat_realted_data_for_sections':
            required_parameters = ['role_id','login_user_id','shc_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='village_realated_data_for_sections':
            required_parameters = ['role_id','login_user_id','shc_code','panchayat_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='shool_realted_data':
            required_parameters = ['panchayat_code','block_code','synceddatetime','FormCode','ApiKey','AppTypeNo','AppVersion']
        elif parameters_of =='trn_tbl_fc_mpr_section_4a':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='trn_tbl_fc_mpr_section_4b':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_fc_section5_insert':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='show_related_school_master_mpr_section':
            required_parameters = ['panchayat_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='update_new_attendence':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime','DbVersion']
        elif parameters_of =='retrive_adolescents_girls_fc_10':
            required_parameters = ['loggedin_user_id','gender_id','panchayat_code','village_code','data_source']            
        elif parameters_of =='at_risk_adolescents_list_fc_17':
            required_parameters = ['loggedin_user_id','village_code','data_source']            
        elif parameters_of =='list_of_adolescents_for_login_id':
            required_parameters = ['loggedin_user_id','data_source','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_mpr_remarks':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_latest_mpr_section_data':
            required_parameters = ['login_role_id','login_user_id','month_id','year_id','mpr_id','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='assing_only_one_village_to_one_fc':
            required_parameters = ['login_role_id','loggedin_user_id','state_code','district_code','block_code','shc_code','panchayat_code','village_code','data_source','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']    
        elif parameters_of =='check_the_attendence_befor_entering_mpr':
            required_parameters = ['login_user_id','month_id','year_id','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']    
        elif parameters_of =='mpr_bc_section_01_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_bc_section_02_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_bc_section_03_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_bc_section_04_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_bc_section_05_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_bc_section_06_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_bc_section_07_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_bc_section_08_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']        
        elif parameters_of =='update_register_user_detials':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_mpr_submit':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='bc_mpr_submit':   
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='po_mpr_submit':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_po_section_01_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_po_section_02_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_po_section_03_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_po_section_04_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_po_section_05_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='mpr_po_section_06_sync_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_all_section_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_cumulative_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='bc_all_section_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_bc_cumulative_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='fc_bc_po_cumulative_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_belowed_user_data':
            required_parameters = ['role_id','userid','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_belowed_bc_user_data':
            required_parameters = ['role_id','userid','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_panchayat_for_bc':
            required_parameters = ['role_code','bc_user_id','block_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_list_of_villages_for_bc':
            required_parameters = ['role_code','block_code','panchayat_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_list_of_groups_for_bc':
            required_parameters = ['role_code','block_code','panchayat_code','village_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_list_of_adolescents_bc':
            required_parameters = ['role_code','block_code','panchayat_code','village_code','group_code','gender_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='retrive_block_list_for_po':
            required_parameters = ['role_code','po_user_id','state_code','district_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='retrive_panchayat_list_for_po':
            required_parameters = ['role_code','po_user_id','state_code','district_code','block_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='retrive_village_list_for_po':
            required_parameters = ['role_code','po_user_id','state_code','district_code','block_code','panchayat_code','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_admin_graph':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='table_view_get_admin_graph':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='admin_community_engagement':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='table_view_admin_community_engagement':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='cb_re_enrolment_birth_marriage_registration_sec_3':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='graph_view_suppo_supervision_met_attended_sec4':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='sess_monit_sheet_summ_report':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='retrieve_po_users_submitted_mpr':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='po_all_section_data':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='admin_fc_raw_data_download':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='admin_bc_raw_data_download':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='admin_po_raw_data_download':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='admin_attendance_raw_data_download':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='user_profile_details_list_on_role_id':
            required_parameters = ['ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='check_sec_10_adolesect_stauts':
            required_parameters = ['adolesce_sw_id','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        elif parameters_of =='get_mpr_sect_status_by_month':
            required_parameters = ['mpr_id','month_id','year_id','ApiKey','AppTypeNo','AppVersion','FormCode','synceddatetime']
        
        # Add more elif blocks for other parameter types if needed
        # Check if all required parameters are present in json_data
        if all(param in json_data.get(parameters_of, {}) for param in required_parameters):
                return True
        # Check if all required parameters are present at the top level of json_data
        keys_from_json = json_data.keys()
        for key in required_parameters:
            if key not in keys_from_json:
                return False
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

    
# Function to get the version code based on the api
def web_service_code(api_name):
    try:
        predefined_codes = {          
            "get_mpr_sect_status_by_month": "313"
        }
        if api_name != '' and api_name in predefined_codes:
            return predefined_codes[api_name]
        else:
            raise ValueError(f"Unknown React web service code for API: {api_name}")
    except:
        return False

# Funtion to get the staed procedure name based on the table name
def sp_name_from_table_name(table_name):
    try:
        sp_predefined_dictionary ={
        "tbl_mobile_login_details" : "sp_mobile_login_details",
        "tbl_mobile_version_details" : "sp_mobile_version_detials",
        "tbl_mobile_exception" : "sp_mobile_exception",
        } 
        if table_name in sp_predefined_dictionary:
            return sp_predefined_dictionary[table_name]
        else:
            return table_name
    except:
        return False

# Function to return the data in the dictionary format
def getting_data_in_dictionary_format(sql_query):
    try:
        # Establish a database connection
        mydb = mysql.connector.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            passwd=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )
        # Fetching the data with column names from the database
        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return result
        # # Convert result to a JSON string
        # result_json = json.dumps(result)
        # return result_json
    except mysql.connector.Error as err:
        # Handle any database errors here
        print(f"Error: {err}")
        return None
    finally:
        # Close the database connection in the 'finally' block to ensure it's always closed
        if mydb.is_connected():
            mydb.close()

# function to insert the Qtable data into the database
def inserQtable_data(WSFormCode,jsonData,receivedDate,syncDateTime):
    cursor = connection.cursor()
    Qid = ''
    sql = "call sp_q_mobile_detials(%s,%s,%s,%s)"
    values_need_to_insert = (WSFormCode,jsonData,receivedDate,syncDateTime)
    result = cursor.execute(sql,values_need_to_insert)
    if result != None and result != 0:
        Qid = cursor.fetchone()[0]
    else:
        Qid =''
    return Qid

def save_uploaded_image(image_file, folder):
    # Create the target directory if it doesn't exist
    target_directory = os.path.join(settings.MEDIA_ROOT, folder)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    # Get the file name and extension
    file_name = image_file.name
    file_extension = file_name.split('.')[-1]
    # Generate a unique file name
    unique_file_name = file_name  # Replace this with your own logic for generating unique names if needed
    # Build the file path
    file_path = os.path.join(target_directory, unique_file_name)
    # Save the image file
    with open(file_path, 'wb') as file:
        for chunk in image_file.chunks():
            file.write(chunk)
    # Return the file path relative to the media root
    return os.path.join(folder, unique_file_name)

# function to update the Qtable data into the database
def UpdateQTable(FormCode,valid,stringResponse,IsFullyProcessed,IsPartiallyProcessed,ReturnStatus,ApiKey,AppTypeNo,AppVersion,Qid):
    sql_to_update_q_table = """
        UPDATE trn_tbl_q_mobile_detials
        SET
            fld_form_code = %s,
            fld_is_json_valid = %s,
            fld_returned_json_text = %s,
            fld_is_fully_processed = %s,
            fld_is_partially_processed = %s,
            fld_return_status = %s,
            fld_returned_datetime = NOW(3),
            fld_process_time = TIMEDIFF(NOW(3), fld_server_rec_datetime),
            fld_api_key = %s,
            fld_app_type_no = %s,
            fld_app_version = %s
        WHERE fld_q_id = %s
    """
    values_to_update_q_table = (FormCode, valid, stringResponse, IsFullyProcessed, IsPartiallyProcessed, ReturnStatus, ApiKey, AppTypeNo, AppVersion, Qid)
    cursor = connection.cursor()
    result = cursor.execute(sql_to_update_q_table,values_to_update_q_table)
    if result != None and result != '':
        return True

# Function to get the current date time in the format of yyyy-mm-dd hh:mm:ss
def current_date_time_in_format():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to execute the query
def Query_execution(query,parameters):
    cursor = connection.cursor()
    if parameters!='':
        result = cursor.execute(query,parameters)
    else:
        result = cursor.execute(query)
    return result

# Function to excecute and return the result
def Query_data_fetch(query,parameters):
    cursor = connection.cursor()
    if parameters!='':
        result = cursor.execute(query,parameters)
    else:
        result = cursor.execute(query)
    
    result = cursor.fetchall()
    return result

def check_dependent_roles(reporting_role_code, reporting_role_name):
    dependent_roles = {
        "FC": ["BC"],
        "BC": ["PO"],
        "PO": ["SPO"],
        "SPO": ["State Head"],
        "State Head": ["Central Head"]
        # Add more dependent roles as needed
    }
    if reporting_role_name in dependent_roles:
        for dependent_role in dependent_roles[reporting_role_name]:
            try:
                # Check if dependent role exists in master_tbl_user
                sql_query = (f"SELECT COUNT(*) AS count FROM master_tbl_user WHERE fld_role_code = %s AND fld_role_name = %s")
                params = (reporting_role_code, reporting_role_name)
                cursor = connection.cursor()
                cursor.execute(sql_query, params)
                result_json = cursor.fetchone()
                result = json.dumps(result_json)
                if not result or result[0] == 0:
                    logging.error(f"For creating the {reporting_role_name} role, the {dependent_role} role must exist. Please create the {dependent_role} role and come back.")
                    return False
            except Exception as e:
                logging.error(f"Error checking dependent roles for {dependent_role}: {str(e)}")
                return False 
    return True

def new_getting_data_in_dictionary_format(sql_query, params):
    try:
        mydb = mysql.connector.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            passwd=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )
        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql_query, params)
            result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if mydb.is_connected():
            mydb.close()

def Generate_newUserId_get_nextUserid(user_assigned_role_code,state_id,district_id,block_id,role_name):
    try:
        # Your main code
        if user_assigned_role_code == "02":
            # Construct SQL query to retrieve the next available user ID
            sql_query = f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('CH', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user where fld_role_code = '02'"
            # Execute the SQL query to get the next user ID
            # cursor = connection.cursor()
            # cursor.execute(sql_query)
            # # Fetch the result
            # result = cursor.fetchone()
            result = getting_data_in_dictionary_format(sql_query)
            role_name ='CH'
            if result[0]['max_value'] is None:
                user_id = 'CH01'
                return user_id
            else:
                #new_userId = result[0]
                #user_id = role_name + str(new_userId)
                # new_userId = result[0]  # accessing the value associated with the 'user_id' key
                # user_id = str(role_name) + str(new_userId)
                # return user_id
                max_value = result[0]['max_value']  # Assuming 'max_value' is the key in the dictionary
                user_id =  role_name + str(max_value)
                return user_id  
        elif user_assigned_role_code == "03":
            # Construct SQL query to retrieve the next available user ID
            sql_query = f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('SH', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user where fld_role_code = '03'"
            # Execute the SQL query to get the next user ID
            # cursor = connection.cursor()
            # cursor.execute(sql_query)
            # # Fetch the result
            # result = cursor.fetchone()
            result = getting_data_in_dictionary_format(sql_query)
            role_name ='SH'
            if result[0]['max_value'] is None:
                user_id = str(state_id) + 'SH' + '01'
                return user_id
            else:
                # new_userId = result[0]
                # user_id = str(state_id) + str(role_name) + str(new_userId)
                # return user_id  
                max_value = result[0]['max_value']  # Assuming 'max_value' is the key in the dictionary
                user_id =  str(state_id) + role_name + str(max_value)
                return user_id  

        elif user_assigned_role_code == "04":
            # Construct SQL query to retrieve the next available user ID
            sql_query = f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('SPO', fld_user_id) + 3) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user where fld_role_code = '04'"
            result = getting_data_in_dictionary_format(sql_query)
            # Execute the SQL query to get the next user ID
            # cursor = connection.cursor()
            # cursor.execute(sql_query)
            # Fetch the result
            # result = cursor.fetchone()
            # new_user_id = result.first()
            role_name ='SPO'
            if result[0]['max_value'] is None:
                # user_id = str(state_id) + 'SPO' + '01'
                user_id = str(f"{state_id}{role_name}01")
                return user_id  
            else:
                # user_id = str(state_id) + str('SPO') + str(new_userId)
                max_value = result[0]['max_value']  # Assuming 'max_value' is the key in the dictionary
                user_id =  str(state_id)  + role_name + str(max_value)
                return user_id  
        elif user_assigned_role_code == "05":
            # Construct SQL query to retrieve the next available user ID
            sql_query = f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('PO', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user where fld_role_code = '05'"
            # Execute the SQL query to get the next user ID
            # cursor = connection.cursor()
            # cursor.execute(sql_query)
            # # Fetch the result
            # result = cursor.fetchone()
            result = getting_data_in_dictionary_format(sql_query)
            role_name ='PO'
            if result[0]['max_value'] is None:
                user_id = str(state_id) + 'PO' + '01'
                return user_id  
            else:
                # new_userId = result[0] 
                # user_id = str(state_id) + str(role_name) + str(new_userId)
                # return user_id    
                max_value = result[0]['max_value']  # Assuming 'max_value' is the key in the dictionary
                user_id =  str(state_id)  + role_name + str(max_value)
                return user_id  
        elif user_assigned_role_code == "06":
            # Construct SQL query to retrieve the next available user ID
            sql_query = f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('BC', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user where fld_role_code = '06'"
            # Execute the SQL query to get the next user ID
            # cursor = connection.cursor()
            # cursor.execute(sql_query)
            # # Fetch the result
            # result = cursor.fetchone()
            result = getting_data_in_dictionary_format(sql_query)
            role_name ='BC'
            if result[0]['max_value'] is None:
                user_id = str(district_id)+ 'BC' + '01'
                return user_id  
            else:
                # new_userId = result[0] 
                # user_id = str(district_id)+str(role_name) + str(new_userId)
                # return user_id
                max_value = result[0]['max_value']  # Assuming 'max_value' is the key in the dictionary
                user_id =  str(district_id)+str(role_name )+ str(max_value)
                return user_id      
        elif user_assigned_role_code == "07":
            # Construct SQL query to retrieve the next available user ID
            sql_query = f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('FC', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user where fld_role_code = '07'"
            # Execute the SQL query to get the next user ID
            # cursor = connection.cursor()
            # cursor.execute(sql_query)
            # # Fetch the result
            # result = cursor.fetchone()
            result =getting_data_in_dictionary_format(sql_query)
            role_name ='FC'
            if result[0]['max_value'] is None:
                user_id = str(block_id)+ 'FC' + '01'
                return user_id  
            else:
                # new_userId = result[0] 
                # user_id = str(block_id)+str(role_name)+str(new_userId)
                # return user_id   
                max_value = result[0]['max_value']  # Assuming 'max_value' is the key in the dictionary
                user_id =  str(block_id)+ str(role_name )+ str(max_value)
                return user_id
    except Exception as e:
        
        error_data = str(traceback.print_exc())
        error_data = traceback.format_exc()
        code_error = str(print("An error occurred:", error_data))
        # return_json = json.loads(json_body)
        success_info = {
            "status": "2",
            "error_message": str(e),
            "error_file": "views.py",
            "serverdatetime": current_date_time_in_format(),
        }
    return success_info

#     # Function to return the data in the dictionary format
# def getting_data_in_dictionary_format_userid(sql_query):
#     try:
#         # Establish a database connection
#         mydb = mysql.connector.connect(
#             host=settings.DATABASES['default']['HOST'],
#             user=settings.DATABASES['default']['USER'],
#             passwd=settings.DATABASES['default']['PASSWORD'],
#             database=settings.DATABASES['default']['NAME']
#         )
#         # Fetching the data with column names from the database
#         with mydb.cursor(dictionary=True) as cursor:
#             cursor.execute(sql_query)
#             result = cursor.fetchall()

#         # Fetching the data with column names from the database
#         with mydb.cursor(dictionary=True) as cursor:
#             cursor.execute(sql_query)
#             result = cursor.fetchall()
#         # Convert result to a JSON string
#         result_json = json.dumps(result)
#         return result_json
#     except mysql.connector.Error as err:
#         # Handle any database errors here
#         print(f"Error: {err}")
#         return None
#     finally:
#         # Close the database connection in the 'finally' block to ensure it's always closed
#         if 'mydb' in locals() and mydb.is_connected():
#             mydb.close()
# # sql_query = "SELECT * FROM master_tbl_role"
# # json_data = getting_data_in_dictionary_format_userid(sql_query)
# # # Convert data to JSON string
# # json_data_dumps = json.loads(json_data)
# # print(json_data_dumps)

# def Generate_newUserId_get_nextUserid(user_assigned_role_code, state_id, district_id, block_id, role_name):
#     try:
#         if user_assigned_role_code == "02":
#             sql_query = (f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('CH', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user WHERE fld_role_code = '02'")
#             result_json = getting_data_in_dictionary_format_userid(sql_query)
#             result_newID = json.loads(result_json)
#             role_name = 'CH'
#             if result_newID[0]['max_value'] is None:
#                 user_id = 'CH01'
#                 return user_id
#             else:
#                 max_value = result_newID[0]['max_value']
#                 user_id = f"{role_name}{max_value:02}"
#                 return user_id
#         elif user_assigned_role_code == "03":
#             sql_query = (f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('SH', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user WHERE fld_role_code = '03'")
#             result_json = getting_data_in_dictionary_format(sql_query)
#             result_newID = json.loads(result_json)
#             role_name = 'SH'
#             if result_newID[0]['max_value'] is None:
#                 user_id = f"{state_id}SH01"
#                 return user_id
#             else:
#                 max_value = result_newID[0]['max_value']
#                 user_id = f"{state_id}{role_name}{max_value:02}"
#                 return user_id
#         elif user_assigned_role_code == "04":
#             sql_query = (f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('SPO', fld_user_id) + 3) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user WHERE fld_role_code = '04'")
#             result_json = getting_data_in_dictionary_format_userid(sql_query)
#             result_newID = json.loads(result_json)
#             role_name = 'SPO'
#             if result_newID[0]['max_value'] is None:
#                 user_id = f"{state_id}{role_name}01"
#                 return user_id
#             else:
#                 max_value = result_newID[0]['max_value']
#                 user_id = f"{state_id}{role_name}{max_value:02}"
#                 return user_id
#         elif user_assigned_role_code == "05":
#             sql_query = (f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('PO', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user WHERE fld_role_code = '05'")
#             result_json = getting_data_in_dictionary_format_userid(sql_query)
#             result_newID = json.loads(result_json)
#             role_name = 'PO'
#             if result_newID[0]['max_value'] is None:
#                 user_id = f"{state_id}{role_name}01"
#                 return user_id
#             else:
#                 max_value = result_newID[0]['max_value']
#                 user_id = f"{state_id}{role_name}{max_value:02}"
#                 return user_id
#         elif user_assigned_role_code == "06":
#             sql_query = (f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('BC', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user WHERE fld_role_code = '06'")
#             result_json = getting_data_in_dictionary_format_userid(sql_query)
#             result_newID = json.loads(result_json)
#             role_name = 'BC'
#             if result_newID[0]['max_value'] is None:
#                 user_id = f"{district_id}{role_name}01"
#                 return user_id
#             else:
#                 max_value = result_newID[0]['max_value']
#                 user_id = f"{district_id}{role_name}{max_value:02}"
#                 return user_id
#         elif user_assigned_role_code == "07":
#             sql_query = (f"SELECT LPAD(MAX(CAST(SUBSTRING(fld_user_id, LOCATE('FC', fld_user_id) + 2) AS SIGNED))+1, 2, '0') AS max_value FROM master_tbl_user WHERE fld_role_code = '07'")
#             result_json = getting_data_in_dictionary_format_userid(sql_query)
#             result_newID = json.loads(result_json)
#             role_name = 'FC'
#             if result_newID[0]['max_value'] is None:
#                 user_id = f"{block_id}{role_name}01"
#                 return user_id
#             else:
#                 max_value = result_newID[0]['max_value']
#                 user_id = f"{block_id}{role_name}{max_value:02}"
#                 return user_id

#     except Exception as e:
       
#         error_data = str(traceback.print_exc())
#         error_data = traceback.format_exc()
#         code_error = str(print("An error occurred:", error_data))
#         # return_json = json.loads(json_body)
#         success_info = {
#             "status": "2",
#             "error_message": str(e),
#             "error_file": "views.py",
#             "serverdatetime": current_date_time_in_format(),
#         }
#     return success_info
