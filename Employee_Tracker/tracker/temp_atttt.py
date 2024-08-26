import re
import pdfplumber
import pandas as pd

class first_page_extractor:
    def __init__(self,input_file):
        self.input_path = input_file
        self.Lines_1 = None
        pages_data = []
        with pdfplumber.open(self.input_path) as pdf:
            num_of_pages = len(pdf.pages)
        if num_of_pages < 999:
            with pdfplumber.open(self.input_path) as pdf:
                pages_data = [page.extract_text() for page in pdf.pages[:2]]
            for page_data in pages_data:
                first_page_data = page_data
                break

            self.first_page_data_dict= {
                "Bill_Date": None,
                "AccountNumber": None,
                "foundation_account": None,
                "InvoiceNumber": None,
                "Billing_Name":None,
                "Billing_Address":None,
                "Remidence_Address":None}
            
        for line in first_page_data.splitlines():
            if line.startswith("Issue Date:"):
                self.first_page_data_dict["Bill_Date"] = line.split(": ")[-1]
            elif line.startswith("Account Number:"):
                self.first_page_data_dict["AccountNumber"] = line.split(": ")[-1]
            elif line.startswith("Foundation Account:"):
                self.first_page_data_dict["foundation_account"] = line.split(": ")[-1]
            elif line.startswith("Invoice:"):
                self.first_page_data_dict["InvoiceNumber"] = line.split(": ")[-1]

            self.first_page_data_dict['Billing_Name'] = re.search(r"^(.*?)\n", first_page_data).group(1)
            self.first_page_data_dict['Billing_Address'] = re.search(r"\n(.*?)\n", first_page_data).group(1)
            self.first_page_data_dict['Remidence_Address'] = "PO Box 6463 Carol Stream, IL 60197-646"

    def first_page_data_func(self):
        return self.first_page_data_dict
    def get_acc_info(self):
        return self.first_page_data_dict['AccountNumber']
    def get_bill_date_info(self):
        return self.first_page_data_dict['Bill_Date']

class Att:
    def __init__(self, input_file):
        self.input_path = input_file
        self.Lines_1 = None

        print('start')
        pages_data = []
        with pdfplumber.open(self.input_path) as pdf:
            num_of_pages = len(pdf.pages)
        if num_of_pages < 999:
            with pdfplumber.open(self.input_path) as pdf:
                pages_data = [page.extract_text() for page in pdf.pages]
            flag = len(pages_data) - 1
            str_con = str(flag)
            for page_data in pages_data:
                if f"Page: 1 of {str_con}" in page_data:
                    first_page_data = page_data
                    break
            try:
                self.billing_name = re.search(r"^(.*?)\n", first_page_data).group(1)
                self.Billing_Address = re.search(r"\n(.*?)\n", first_page_data).group(1)
                self.Remidence_Addresss = "PO Box 6463 Carol Stream, IL 60197-646"
            except:
                self.billing_name ='NA'
                self.Billing_Address = 'NA'
                self.Remidence_Addresss = "PO Box 6463 Carol Stream, IL 60197-646"

            total_text = ''.join(pages_data)
            pattern =  r"Group (\d+)\n(\d+) Devices?\nMonthly charges (\w+ \d+ - \w+ \d+)\n1\. (.+) \$([\d.]+)"
            matches = re.findall(pattern, total_text)
            self.plan_price_list = []
            if matches:
                for match in matches:
                    plan_price_dict = {}
                    group_no = match[0]
                    plan = match[3]
                    chrages = match[4]
                    plan_price_dict['Group_Number'] = group_no
                    plan_price_dict['Plans'] = plan
                    plan_price_dict['Monthly_Charges'] = chrages
                    self.plan_price_list.append(plan_price_dict)

            data = ''
            for text in pages_data:
                data += "\n" + text
                match_news = re.search(r"News you can use", data)
                match_usage = re.search(r"Detailed usage", data)

                if match_news or match_usage:
                    print(match_news.group() if match_news else match_usage.group())
                    break

            self.data = data
            print('end')
        else:
            print('badiwali')

            data = ''
            for page_num in range(num_of_pages):
                with pdfplumber.open(self.input_path) as pdf:
                    page = pdf.pages[page_num]
                    text = page.extract_text()
                    data = data + "\n" + text
                    
        self.data = data

    def plan_and_price(self):
        return self.plan_price_list

    def data_manage_part1(self):
        Lines = []
        data_1 = self.data
        lines = data_1.split('\n')
        for line in lines:
            match = re.search(
                r'(\d{3}.\d{3}.\d{4}) (.+?|.+? \b\d+\b) (\d+|\d+\,\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-)',
                line)
            if match:
                Lines.append({'Wireless_number': 'NA' if match.group(1) == '-' else match.group(1),
                              'User_name': 'NA' if match.group(2) == '-' else match.group(2),
                              'Page Number': 'NA' if match.group(3) == '-' else match.group(3),
                              'Activity since last bill': 'NA' if match.group(4) == '-' else match.group(4),
                              'Monthly charges Plan': 'NA' if match.group(5) == '-' else match.group(5),
                              'Monthly charges Equipment': 'NA' if match.group(6) == '-' else match.group(6),
                              'Monthly charges Add-ons': 'NA' if match.group(7) == '-' else match.group(7),
                              'Company fees & surcharges': 'NA' if match.group(8) == '-' else match.group(8),
                              'Government fees & taxes': 'NA' if match.group(9) == '-' else match.group(9),
                              'Billing_Name':self.billing_name,
                              'Billing_Address':self.Billing_Address,
                              'Remidence_Addresss':self.Remidence_Addresss,
                              'Total': 'NA' if match.group(10) == '-' else match.group(10)})
            else:
                match = re.search(
                    r'(\d{3}.\d{3}.\d{4}) (.+?|.+? \b\d+\b) (\d+|\d+\,\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-)',
                    line)
                if match:
                    Lines.append({'Wireless_number': 'NA' if match.group(1) == '-' else match.group(1),
                                  'User_name': 'NA' if match.group(2) == '-' else match.group(2),
                                  'Page Number': 'NA' if match.group(3) == '-' else match.group(3),
                                  'Activity since last bill': 'NA' if match.group(4) == '-' else match.group(4),
                                  'Monthly charges': 'NA' if match.group(5) == '-' else match.group(5),
                                  'Company fees & surcharges': 'NA' if match.group(6) == '-' else match.group(6),
                                  'Government fees & taxes': 'NA' if match.group(7) == '-' else match.group(7),
                                  'Billing_Name':self.billing_name,
                                  'Billing_Address':self.Billing_Address,
                                  'Remidence_Addresss':self.Remidence_Addresss,
                                  'Total': 'NA' if match.group(8) == '-' else match.group(8)})
            match = re.search(
                r'(^Group \d+) (\d+|\d+\,\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-)',
                line)
            if match:
                Lines.append({'Wireless_number': 'NA', 'User_name': 'NA' if match.group(1) == '-' else match.group(1),
                              'Page Number': 'NA' if match.group(2) == '-' else match.group(2),
                              'Activity since last bill': 'NA' if match.group(3) == '-' else match.group(3),
                              'Monthly charges Plan': 'NA' if match.group(4) == '-' else match.group(4),
                              'Monthly charges Equipment': 'NA' if match.group(5) == '-' else match.group(5),
                              'Monthly charges Add-ons': 'NA' if match.group(6) == '-' else match.group(6),
                              'Company fees & surcharges': 'NA' if match.group(7) == '-' else match.group(7),
                              'Government fees & taxes': 'NA' if match.group(8) == '-' else match.group(8),
                              'Billing_Name':self.billing_name,
                              'Billing_Address':self.Billing_Address,
                              'Remidence_Addresss':self.Remidence_Addresss,
                              'Total': 'NA' if match.group(9) == '-' else match.group(9)})
            else:
                match = re.search(
                    r'(^Group \d+) (\d+|\d+\,\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+|\-)',
                    line)
                if match:
                    Lines.append(
                        {'Wireless_number': 'NA', 'User_name': 'NA' if match.group(1) == '-' else match.group(1),
                         'Page Number': 'NA' if match.group(2) == '-' else match.group(2),
                         'Activity since last bill': 'NA' if match.group(3) == '-' else match.group(3),
                         'Monthly charges': 'NA' if match.group(4) == '-' else match.group(4),
                         'Company fees & surcharges': 'NA' if match.group(5) == '-' else match.group(5),
                         'Government fees & taxes': 'NA' if match.group(6) == '-' else match.group(6),
                         'Billing_Name':self.billing_name,
                         'Billing_Address':self.Billing_Address,
                         'Remidence_Addresss':self.Remidence_Addresss,
                         'Total': 'NA' if match.group(7) == '-' else match.group(7)})
        self.Lines_1 = Lines
        return Lines

    def geo_member(self):
        unique = set()
        pool = None
        lines = self.data.split('\n')
        for line in lines:
            if line.startswith('Pooling detail'):
                break
            match = re.match(r'^Group (\d+)$', line)
            if match:
                user_name = match.group(1)
                if user_name not in unique:
                    unique.add(user_name)

            if re.compile(
                    r'\b\d{3}\.\d{3}\.\d{4}\b.*\$\d+\.\d{2}\b|\bGroup \d+ \d+ - \$\d+\.\d{2}(- \$\d+\.\d{2})*\b|(?:\bGroup (\d+) (\d+) - \$\d+\.\d{2} - - - - \$\d+\.\d{2}\b|\bGroup (\d+) (\d+) \$\d+\.\d{2} \$\d+\.\d{2} - - \$\d+\.\d{2} \$\d+\.\d{2} \$\d+\.\d{2}\b|Group \d+ \d+ -\$[\d.]+(?: - - - - - -\$[\d.]+)*)').search(
                line):
                items = line.split()
                target_index = None
                if items[0] == 'Group':
                    unique.add(items[1])
        gro_member = []
        uniques = set()
        line_re = re.compile(r'\b\d{3}\.\d{3}\.\d{4}\b.*\$\d+\.\d{2}\b')
        pool = None
        check = 0
        lines = self.data.split('\n')
        for line in lines:
            if check == 1:
                break
            if line.startswith('Pooling detail'):
                pool = 'Data Pool: Mobile Select - Pooled'

            match = re.search(r'Total for Mobile Select - Pooled', line)
            if match:
                check = 1
                break
            match = re.search(r'Group (\d+)', line)
            if match:
                user_name = match.group(1)
                if user_name not in unique:
                    uniques.add(user_name)
            match = re.search(r'Subtotal for Group (\d+)', line)
            if match:
                user_name = None
            if line_re.search(line):
                items = line.split()
                if user_name:
                    gro_member.append({'Group Number': user_name, 'Wireless_number': items[0]})
                if pool:
                    gro_member.append({'Group Number': pool, 'Wireless_number': items[0]})
        return gro_member

    def geo_members(self):
        dataset = []
        gro_members = []
        current_section = None
        lines = self.data.split('\n')
        for i, line in enumerate(lines):
            match = re.search(r"Total for Group (\d+) \$([\d.]+)|Total for Group (\d+) -\$(-?\d+\.\d{2})", line)
            if match:
                current_section = 'Group Plan Cost'
                itemss = line.split()
                gro_name = itemss[-2]
                gro_cost = float(str(itemss[-1]).replace('$', ''))

            match = re.search(r"^Total usage", line)
            if match:
                if dataset:
                    mem_cost = '$' + str(round(gro_cost / float(len(dataset)), 2))
                    # print(mem_cost)
                    for datas in dataset:
                        gro_members.append({'Group Wireless_number': datas, 'Group Number': gro_name,
                                            'Group': mem_cost.replace('$-', '-$')})
                    dataset = []
                current_section = None

            match = re.search(r"(^\d{3}\.\d{3}\.\d{4})\s+([A-Z]+(?:\s+[A-Z]+)*)", line)
            if match:
                if current_section:
                    dataset.append(match.group(1))

        return gro_members

    def data_manage_part2(self):
        result = []
        phone_number = None
        current_section = None
        name = None
        
        data_2 = self.data
        lines = data_2.split('\n')
        note = None
        check = 0
        self.Lines_1 = self.data_manage_part1()
        gro_member = self.geo_member()
        gro_members = self.geo_members()
        for i, line in enumerate(lines):
            match = re.search(r"^News you can use", line)
            if match:
                break

            match = re.search(r"^Detailed usage", line)
            if match:
                break

            match = re.search(r"Issue Date: ([A-Za-z]{3} \d{2}, \d{4})", line)
            if match:
                issue_date = match.group(1)

            match = re.search(r"Account Number: (\d+)", line)
            if match:
                account_number = match.group(1)

            match = re.search(r"Invoice: (\d+)X(\d{8})", line)
            if match:
                invoice = match.group(1) + '-' + match.group(2)

            match = re.search(r"Foundation Account: (\d+)", line)
            if match:
                foundation = match.group(1)

            match = re.search(r"Ph\[\[([\d]+o[\d]+)\|\| ne, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            match = re.search(r"Ph\[\[([\d]+o[\d]+)\|\|ne, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            match = re.search(r"We\[\[([\d]+a[\d]+)\|\| rable, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            match = re.search(r"We\[\[([\d]+a[\d]+)\|\|rable, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            match = re.search(r"Co\[\[([\d]+n[\d]+)\|\| nected Device, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            match = re.search(r"Co\[\[([\d]+n[\d]+)\|\|nected Device, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            match = re.search(r"Ta\[\[(\w+)\|\| let, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            match = re.search(r"Ta\[\[(\w+)\|\|let, ([\d]{3}\.[\d]{3}\.[\d]{4})", line)
            if match:
                phone_number = match.group(2)
                name = lines[i + 1]

            if re.search(r"Monthly charges", line):
                current_section = 'Monthly charges'
                check = 1
                note = None
            elif re.search(r"Company fees & surcharges", line):
                current_section = 'Company fees & surcharges'
                check = 1
                note = None
            elif re.search(r"Government fees & taxes", line):
                current_section = 'Government fees & taxes'
                note = None
            elif re.search(r"Other Activity", line):
                current_section = 'Other Activity'
                note = 'One-time charge'
            elif re.search(r"(\w+\s\d{2}): (\w+)", line):
                current_section = 'Other Activity'
                note = 'Service change'
            elif re.search(r'Total for \d{3}\.\d{3}\.\d{4}', line):
                current_section = None

            for line_data in self.Lines_1:
                if phone_number:
                    if line_data.get('Wireless_number') == phone_number:
                        try:
                            line_plan = float(
                                str(line_data.get('Monthly charges Plan')).replace('$', '').replace('NA', '0'))
                            if line_plan > 0:
                                status = 'Active'
                            else:
                                status = 'Inactive'
                        except:
                            line_plan = float(str(line_data.get('Monthly charges')).replace('$', '').replace('NA', '0'))
                            if line_plan > 0:
                                status = 'Active'
                            else:
                                status = 'Inactive'

            if current_section == ('Monthly charges' and check == 1) or (
                    current_section == 'Company fees & surcharges' and check == 1):
                check = 0
                for gro_data in gro_members:
                    if gro_data.get('Group Wireless_number') == phone_number:
                        gro_phone = gro_data.get('Group Wireless_number')
                        data_news1 = gro_data.get('Group Number')
                        mem_cost = gro_data.get('Group')
                        result.append({'Foundation_Account': foundation if foundation else 'NA', 'Account_number': str(account_number),
                                       'Group_Number': data_news1, 'User_name': name, 'Wireless_number': phone_number,
                                       'User_Email': None, 'Status': status, 'Cost_Center': None,
                                       'Account_Charges_and_Credits': None, 'Item_Category': 'Monthly_charges',
                                       'Item_Description': 'Plan_Allocation', 'Charges': mem_cost,'Note': None})
            match = re.search(
                r'(\d+\.) (.*?) (\-\$\d+\.\d+|\-\$\.\d+|\$\d+\.\d+|\$\.\d+|\$[0-9,]+\.\d+|\-\$[0-9,]+\.\d+)',
                line)
            if match:
                if re.search(r'Total for ', line):
                    continue

                if current_section and name:
                    for gro_data1 in gro_member:
                        if gro_data1.get('Wireless_number') == phone_number:
                            gro_phone = gro_data1.get('Wireless_number')
                            data_news1 = gro_data1.get('Group Number')

                    if gro_phone == phone_number:
                        result.append({'Foundation_Account': foundation if foundation else 'NA', 'Account_number': str(account_number),
                                       'Group_Number': data_news1, 'User_name': name, 'Wireless_number': phone_number,
                                       'User_Email': None, 'Status': status, 'Cost_Center': None,
                                       'Account_Charges_and_Credits': None, 'Item_Category': current_section,
                                       'Item_Description': match.group(2), 'Charges': match.group(3),
                                       'Note': note if note != None else None})
                    else:
                        result.append(
                            {'Foundation_Account': foundation if foundation else 'NA', 'Account_number': str(account_number),
                             'Group Number': None,
                             'User_name': name, 'Wireless_number': phone_number, 'User_Email': None, 'Status': status,
                             'Cost Center': None, 'Account_Charges_and_Credits': None, 'Item_Category': current_section,
                             'Item_Description': match.group(2), 'Charges': match.group(3),'Note': note if note != None else None})
        return result
    
    def to_csv(self, List_data):
        df = pd.DataFrame(List_data)
        return df

def get_first_page_data(uploaded_file):
    obj = first_page_extractor(uploaded_file)
    first_dict = obj.first_page_data_func()
    first_df = pd.DataFrame(first_dict,index=[0])
    return first_df
import os
def process_all(uploaded_file):
    try:
        data_list = Att(uploaded_file)
        x = data_list.plan_and_price()
        z = data_list.data_manage_part1()
        correct_charge_df = data_list.to_csv(z)
        plan_price_df = data_list.to_csv(x)
        a = data_list.geo_member()
        b = data_list.geo_members()
        y = data_list.data_manage_part2()
        intital_df = data_list.to_csv(y)
        final_df = pd.merge(intital_df,plan_price_df,on='Group_Number',how='inner')
        unique_df = final_df.drop_duplicates(subset='Wireless_number')
        correct_charge_df.rename(columns={'Total':'Charges'},inplace=True)
        unique_df = correct_charge_df
        filtered_df = correct_charge_df[correct_charge_df['User_name'].str.contains('Group')]
        final_df = final_df.append(filtered_df[['User_name', 'Charges']], ignore_index=True)
        final_df['ECPD Profile ID'] = 'NA'
        unique_df['ECPD Profile ID'] = 'NA'
        final_df['User ID'] = 'NA'
        unique_df['User ID'] = 'NA'
        new_columns = ['Data Usage (KB)','Data Usage (MB)','Voice Roaming','Messaging Roaming','Data Roaming (KB)','Data Roaming (MB)','Data Roaming (GB)','Usage_and_Purchase_Charges','Equipment_Charges','Surcharges_and_Other_Charges_and_Credits','Taxes_Governmental_Surcharges_and_Fees','Third_Party_Charges_includes_Tax','Total_Charges','Voice_Plan_Usage','Messaging_Usage','Data Usage(GB)']
        for y in new_columns:
            unique_df[y] = 0
            final_df[y] = 0
        final_df.rename(columns={'Plans':"Your Calling Plans"},inplace=True)
        unique_df.rename(columns={'Plans':"Your Calling Plans"},inplace=True)
        unique_df.drop('Page Number',axis=1)
        unique_df.rename(columns={'Monthly charges Plan':'Monthly Charges','Monthly charges Equipment':'Equipment Charges','Company fees & surcharges':'Surcharges and Credits','Government fees & taxes':'Taxes, Governmental Surcharges and Fees',},inplace=True)
        return final_df,unique_df
    except Exception as e:
        print(e)
        return None
    
file = r'D:/project/ATT Bills/mob_1016_287235992973_20231113_R.pdf'
process_all(file)