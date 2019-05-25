import xlrd
import mysql.connector
from datetime import datetime
from datetime import timedelta
import os

original_sheets_path = 'D:\Projects\Process Mining\OBS_Visualization\data_2017\\'
file_name = 'Service Transition Performance Report - Week 14.xls'
for roots, dirs, files in os.walk(original_sheets_path):
    for f in files:
     #if int(f[45:47]) > 20:
        file_name = f
        print(file_name)
        OB_field_name = ['OrderRef', 'Max Send for Sign_Cust Sign', 'First LVO', 'Last LVO', 'GAD', 'SIO Rcvd',
                         'Country', 'DLT1a', 'DLT1b1', 'DLT1b2', 'DLT1c']

        Cut_field_name = ['Order Ref', 'SESAM CSO', 'SESAM CAV', 'Eqpt Order Date (last)', 'Shipment Rqsted on',
                          'Ship Date', 'Eqpt Delivery Date', 'Install Order', 'Installation Original',
                          'Actual Install', 'AT Cmpltion Date', 'SAT Cmpltion', 'First Gold C&R', 'GOLD SRF2 Delivered'
            , 'LDM', 'LDM Team', 'LDM Region', 'Original Order Ref', 'Cust Name', 'Cust Code'
            , 'CUT on', 'SDM', 'CMP PRODUCT NAME', 'SDM Team', 'RFS', 'RFB in SESAM', 'SCN Issue Date', 'SDM MSC',
                          'Status', 'LTC', 'POCM', 'POCM Team', 'POCM MSC', 'DLT2', 'DLT3a1', 'DLT3a2', 'DLT3b1',
                          'DLT3b2', 'DLT3b3', 'DLT3b4', 'DLT3d', 'DLT3e', 'DLT4a', 'DLT4b']

        process_names = ['DLT1a', 'DLT1b1', 'DLT1b2', 'DLT1c', 'DLT2', 'DLT3a1', 'DLT3a2', 'DLT3b1', 'DLT3b2',
                         'DLT3b3', 'DLT3b4', 'DLT3d', 'DLT3e', 'DLT4a', 'DLT4b']

        cnx = mysql.connector.connect(user='root', password='admin',
                                      host='127.0.0.1',
                                      database='orders_info')
        cursor = cnx.cursor()
        cursor.execute("select id,num_fields from dlt_order_detail")
        order_details = dict(cursor.fetchall())


        def is_float(x):
            try:
                float(x)
                return True
            except ValueError:
                return False


        def is_date(x):
            try:
                datetime.strptime(str(x), '%d-%m-%Y')
                return True
            except ValueError:
                return False


        def read_excel_sheet():  # read  excel sheet file
            excel_sheet = xlrd.open_workbook(original_sheets_path + file_name)
            return excel_sheet


        def extract_ob_cut_data(excel_sheet):  # get the OB and Cut data sheets from excel sheet file
            data_sheet = {}
            data_sheet['OBData_read'] = excel_sheet.sheet_by_name('OB Data')
            data_sheet['CUTData_read'] = excel_sheet.sheet_by_name('CUT Data')
            return data_sheet


        filter_index = {}


        def field_index(data_Fields, sheet_data):  # get columns index at OB and Cut Data Sheet
            data_indx = {}
            equal_list = ['SDM', 'LDM', 'RFS', 'LTC', 'POCM', 'SDM MSC', 'SDM Team', 'LDM Region', 'LDM Team',
                          'Country', 'DLT1a']
            row_field = data_Fields.row_values(0)
            for header in range(0, len(sheet_data)):
                for col_indx in range(0, data_Fields.ncols):
                    if row_field[col_indx] == 'New Release':
                        filter_index['New Release'] = col_indx
                    if sheet_data[header] in equal_list and sheet_data[header] == row_field[col_indx]:
                        data_indx[sheet_data[header]] = col_indx
                        break
                    elif sheet_data[header] in row_field[col_indx] and sheet_data[header] not in equal_list:
                        if row_field[col_indx] == 'Status':
                            filter_index['Status'] = col_indx
                        data_indx[sheet_data[header]] = col_indx
                        break
            return data_indx


        update_detail_row_data = {}
        insertion_dlts_row_data = {}
        update_dlts_row_data = {}


        def get_rows_data(data_Fields, data_index, list_dict):  # get Data Fields for each row
            filter_col_indx = filter_index['New Release'] if len(data_index) == len(OB_data_indx) else filter_index[
                'Status']
            filter_value = '1.0' if len(data_index) == len(OB_data_indx) else 'CUT'
            print(str(filter_col_indx) + "  " + str(filter_value))
            for rows in range(2, data_Fields.nrows):
                row_data = data_Fields.row_values(rows)
                details_dict = {}
                dlts_dict = {}
                details_dict.setdefault('num_fields', 0)
                key = ''
                num_field = 0
                date = datetime(year=1899, month=12, day=30)
                not_equal_list = ['Original Order Ref', 'Cust Code', 'LTC', 'POCM', 'POCM Team', 'POCM MSC']
                if str(row_data[filter_col_indx]) == str(filter_value):
                    for k, v in data_index.items():
                        if k == 'OrderRef' or k == 'Order Ref':
                            key = str(row_data[v]).split('.')[0]
                        elif k in process_names:  # for DLTs row fields
                            dlts_dict[k] = str(row_data[v]).split('.')[0]
                        else:  # check if Data Field is Float represnting Date
                            if k not in not_equal_list and is_float(row_data[v]) and float(row_data[v]) > 1:
                                new_date = date + timedelta(days=int(row_data[v]))
                                details_dict[k] = new_date.strftime("%d-%m-%Y")
                                num_field = (num_field + 1) if ((str(row_data[v]) != '' and
                                                                 str(details_dict[k]) != '0'))else num_field
                            else:  # check if Data Field is str
                                details_dict[k] = str(row_data[v]).split('.')[0]
                                num_field = (num_field + 1) if ((str(row_data[v]) != '' and
                                                                 str(details_dict[k]) != '0'))else num_field

                    details_dict['num_fields'] = num_field
                    if details_dict.get(str('CUT on'), 'not') != 'not':
                        dlts_dict['CUT on'] = details_dict['CUT on']

                    if order_details.get(str(key), 'not') != 'not':  # Update data (fields exist at DB)
                        if len(details_dict) == (len(Cut_field_name) - 11) and update_detail_row_data.get(str(key),
                                                                                                          "not") == 'not' \
                                and int(order_details[key]) < 7:
                            details_dict['num_fields'] += int(order_details[key])
                            update_detail_row_data[key] = details_dict
                            update_dlts_row_data[key] = dlts_dict

                    elif list_dict.get(str(key), "not") != 'not' and len(list_dict[key]) != len(
                            details_dict) and list_dict[key][
                        'num_fields'] < 7:  # Update data (OB fields and Cut fields at the same excel week)
                        details_dict['num_fields'] += list_dict[key]['num_fields']
                        list_dict[key].update(details_dict)
                        insertion_dlts_row_data[key].update(dlts_dict)

                    else:  # New id data fields record
                        list_dict[key] = details_dict
                        insertion_dlts_row_data[key] = dlts_dict
            return list_dict


        excel_sheet = read_excel_sheet()
        data_sheet = extract_ob_cut_data(excel_sheet)

        OB_data_indx = field_index(data_sheet['OBData_read'], OB_field_name)

        Cut_data_indx = field_index(data_sheet['CUTData_read'], Cut_field_name)

        insert_rows_data = get_rows_data(data_sheet['OBData_read'], OB_data_indx, {})
        insert_rows_data = get_rows_data(data_sheet['CUTData_read'], Cut_data_indx, insert_rows_data)

        print(str(len(insert_rows_data)) + " insertion Details and DLTs records")
        print(str(len(update_detail_row_data)) + " Update Details and DLTs records")

        OB_length = len(OB_field_name) - 4  # 4 according to num of DLT1
        Cut_length = len(Cut_field_name) - 11  # 11 according to num of DLTs at CUT sheet
        full_fields_length = OB_length + Cut_length

        param_value = ''
        for j in range(full_fields_length):
            param_value += '%s, '
        param_value = param_value[:-2]

        insert_query = ("INSERT INTO dlt_order_detail "
                        "(id,num_fields,customer_signature, first_LVO, last_LVO, GAD, SIO, Country,CSO,  CAV,equipment_order,"
                        "shipment_requested, shipment_date, equipment_delivery,install_order, install_request,"
                        "actual_install,AT_completion,  SAT_completion,GOLD_CR, SRF, LDM, LDM_team, LDM_region,  Gold_ref,"
                        "CustomerName, CustomerCode, CUTDate,SDM, CMP_ProductName,"
                        "SDM_Team,RFS, RFB, SCN, SDM_MSC,Status,LTC,"
                        "POCM, POCM_Team, POCM_MSC)"
                        "VALUES ( " + param_value + " );")


        def insert_details_data_fields():
            rows_field_values = []
            field_values = [None] * full_fields_length
            count = 0
            for SESAM_Ref, fields in insert_rows_data.items():
                field_values[0] = SESAM_Ref
                field_values[1] = fields['num_fields']
                indx = 2 if (len(fields) <= OB_length or len(fields) > Cut_length) else (OB_length + 1)
                for k, field_val in fields.items():
                    if k == 'num_fields':
                        continue
                    if field_val != '' and field_val != '0':
                        if is_date(field_val):
                            field_values[indx] = datetime.strptime(field_val, '%d-%m-%Y')
                        else:
                            field_values[indx] = field_val
                    indx += 1

                rows_field_values.append(tuple(field_values))
                field_values = [None] * full_fields_length
                count += 1

                if count % 1000 == 0:
                    cursor.executemany(insert_query, rows_field_values)
                    cnx.commit()
                    rows_field_values = []

            if len(insert_rows_data) > 0:
                cursor.executemany(insert_query, rows_field_values)
                cnx.commit()


        update_query = ("""
           UPDATE dlt_order_detail
           SET num_fields=%s, CSO=%s, CAV=%s, equipment_order=%s, shipment_requested=%s,
           shipment_date=%s, equipment_delivery=%s,install_order=%s, install_request=%s,
           actual_install=%s,AT_completion=%s,SAT_completion=%s,GOLD_CR=%s, SRF=%s, LDM=%s, LDM_team=%s, LDM_region=%s,  Gold_ref=%s,
           CustomerName=%s, CustomerCode=%s, CUTDate=%s,SDM=%s, CMP_ProductName=%s,
           SDM_Team=%s,RFS=%s, RFB=%s, SCN=%s, SDM_MSC=%s,Status=%s,LTC=%s,
           POCM=%s, POCM_Team=%s, POCM_MSC=%s
           WHERE id=%s""")


        def update_details_data_fields():
            rows_field_values = []
            field_values = []
            count = 0
            for SESAM_Ref, fields in update_detail_row_data.items():
                for k, field_val in fields.items():
                    if field_val == '' or field_val == '0':
                        field_values.append(None)
                    else:
                        if is_date(field_val):
                            field_values.append(datetime.strptime(field_val, '%d-%m-%Y'))
                        else:
                            field_values.append(field_val)
                field_values.append(SESAM_Ref)
                rows_field_values.append(tuple(field_values))
                field_values = []
                count += 1
                if count % 1000 == 0:
                    cursor.executemany(update_query, rows_field_values)
                    cnx.commit()
                    rows_field_values = []

            if len(update_detail_row_data) > 0:
                cursor.executemany(update_query, rows_field_values)
                cnx.commit()


        param_value = ''
        for j in range(len(process_names) + 2):
            param_value += '%s, '
        param_value = param_value[:-2]

        insert_dlt_query = ("INSERT INTO dlt_order_days "
                            "(id,dlt1a,dlt1b1,dlt1b2,dlt1c,dlt2,dlt3a1,dlt3a2,dlt3b1"
                            ",dlt3b2,dlt3b3,dlt3b4,dlt3d,dlt3e,dlt4a,dlt4b,CUTDate)"
                            "VALUES ( " + param_value + " );")


        def insert_dlt_data_fields():
            rows_field_values = []
            field_values = [None] * (len(process_names) + 2)
            count = 0
            for SESAM_Ref, fields in insertion_dlts_row_data.items():
                field_values[0] = SESAM_Ref
                indx = 1 if (len(fields) <= 4 or len(fields) > 12) else 5
                for k, field_val in fields.items():
                    if field_val != '' and field_val != '0':
                        if is_date(field_val):
                            field_values[indx] = datetime.strptime(field_val, '%d-%m-%Y')
                        else:
                            field_values[indx] = field_val
                    indx += 1

                rows_field_values.append(tuple(field_values))
                field_values = [None] * (len(process_names) + 2)
                count += 1

                if count % 1000 == 0:
                    cursor.executemany(insert_dlt_query, rows_field_values)
                    cnx.commit()
                    rows_field_values = []

            if len(insertion_dlts_row_data) > 0:
                cursor.executemany(insert_dlt_query, rows_field_values)
                cnx.commit()


        update_dlt_query = ("""UPDATE dlt_order_days
                            SET dlt2=%s,dlt3a1=%s,dlt3a2=%s,dlt3b1=%s
                            ,dlt3b2=%s,dlt3b3=%s,dlt3b4=%s,dlt3d=%s,dlt3e=%s,dlt4a=%s,dlt4b=%s,CUTDate=%s
                            WHERE id=%s""")


        def update_dlt_data_fields():
            rows_field_values = []
            field_values = []
            count = 0
            for SESAM_Ref, fields in update_dlts_row_data.items():
                for k, field_val in fields.items():
                    if field_val != '' and field_val != '0':
                        if is_date(field_val):
                            field_values.append(datetime.strptime(field_val, '%d-%m-%Y'))
                        else:
                            field_values.append(field_val)
                    else:
                        field_values.append(None)

                field_values.append(str(SESAM_Ref))
                rows_field_values.append(tuple(field_values))
                field_values = []
                count += 1
                if count % 1000 == 0:
                    cursor.executemany(update_dlt_query, rows_field_values)
                    cnx.commit()
                    rows_field_values = []

            if len(update_dlts_row_data) > 0:
                cursor.executemany(update_dlt_query, rows_field_values)
                cnx.commit()


        insert_details_data_fields()
        update_details_data_fields()
        insert_dlt_data_fields()
        update_dlt_data_fields()

        cursor.close()
        cnx.close()
        print('Done Insertion')
