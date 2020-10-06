# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
print('Python %s on %s' % (sys.version, sys.platform))


# Specify your specific content here
projectname = 'yqrgjm'
dcolName = 'dataset_name'
tcolName = 'original_output_name'  # the variable used for program names
dfileName = 'Dataset_.xls'
tfileName = 'TFLS_.xls' # the path of the tracking file
sheetIndex = 0  # which sheet will be used
path='c:/Users/zengzhanhua/Desktop/'  # the path of your output
# end of edit ######################################

import datetime
date = datetime.datetime.now().strftime('%b%d%Y')
date1 = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%b%d%Y')
print(date1)
# step1: read tracking

def read_tracking():
    import xlrd
    excel = xlrd.open_workbook(path+projectname+'/'+dfileName)
    table = excel.sheets()[sheetIndex]
    print('tracking line count:', table.nrows)
    names = table.row_values(0)
    keyIndex = -1
    for i in range(len(names)):
        if dcolName == names[i]:
            keyIndex = i
            break
    print(keyIndex)
    print(names)
    table_confs = {}
    for i in range(1, table.nrows):
        line = table.row_values(i)
        d = table_confs.get(line[keyIndex], {})
        for j in range(0, len(names)):
            if j == keyIndex:
                continue
            values = d.get(names[j].lower(), set())
            values.add(line[j])
            d[names[j].lower()] = values
        d[names[keyIndex].lower()] = set([line[keyIndex].lower()])
        d['study_number'] = {projectname}
        d['date1'] = {date1}
        d['date'] = {date}
        table_confs[line[keyIndex].lower()] = d
    return table_confs

table_confs = read_tracking()
# step2, replace the specified variable in the model
model_file=[]
import re
with open(path+projectname+'/model/demo_dataset.sas', 'r+') as f:
    model_file = f.readlines()
print("model file lines ", model_file)
for table_name in table_confs.keys():
    conf = table_confs.get(table_name)
    # print(conf_)
    # conf = conf_[0:conf_.rfind('-testdir')]
    write_lines = []
    for line in model_file:
        match = re.findall('\${(.*?)\}', line, flags=0)
        for word in match:
    # ********** keep format **********
            index = line.index('${' + word + '}')
            values = list(conf[word.lower()])

            print("key", word, "values ", values)
            tmp = line.replace('${' + word + '}', values[0])
            for x in range(1, len(values)):
                tmp += (' ' * index) +line[index:].replace('${' + word + '}'
, values[x])
            line = tmp
# **********end**********
# create SAS programs and write your code in
        write_lines.append(line)
    print("write table " + table_name)
    with open(path+projectname+'/program/adam/'+table_name+'.sas', 'w+') as write_table:
        write_table.writelines(write_lines)
print('end--------')


# TFLS

# step1: read tracking

def read_tracking():
    import xlrd
    excel = xlrd.open_workbook(path+projectname+'/'+tfileName)
    table = excel.sheets()[sheetIndex]
    print('tracking line count:', table.nrows)
    names = table.row_values(0)
    keyIndex = -1
    for i in range(len(names)):
        if tcolName == names[i]:
            keyIndex = i
            break
    print(keyIndex)
    print(names)
    table_confs= {}
    for i in range(1, table.nrows):
        line = table.row_values(i)
        d = table_confs.get(line[keyIndex], {})
        for j in range(0, len(names)):
            if j == keyIndex:
                continue
            values = d.get(names[j].lower(), set())
            values.add(line[j])
            d[names[j].lower()] = values
        d[names[keyIndex].lower()] = set([line[keyIndex]])
        d['study_number'] = {projectname}
        d['date1'] = {date1}
        d['date'] = {date}
        table_confs[line[keyIndex].lower()] = d
    return table_confs

table_confs = read_tracking()
# step2, replace the specified variable in the model
model_file = []
import re
for table_name in table_confs.keys():
    conf = table_confs.get(table_name)
    if conf['file_type'] == {'rtf'}:
        with open(path+projectname+'/model/demo.sas', 'r+') as f:
            model_file = f.readlines()
    else :
        with open(path+projectname+'/model/demo_pdf.sas', 'r+') as f:
            model_file = f.readlines()
            # print("model file lines ", model_file)    

    write_lines=[]
    for line in model_file:
        match = re.findall('\${(.*?)\}', line, flags=0)
        for word in match:
            # **********keep format**********
            index = line.index('${' + word + '}')
            values = list(conf[word.lower()])
    
            print("key", word, "values ", values)
            tmp = line.replace('${' + word + '}', values[0])
            for x in range(1, len(values)):
                tmp += (' ' * index) +line[index:].replace('${' + word + '}', values[x])
            line = tmp
    # ##############end#######################
    # create SAS programs and write your code in
        write_lines.append(line)
    print("write table " + table_name)
    with open(path+projectname+'/program/tfls/'+table_name+'.sas', 'w+') as write_table:
        write_table.writelines(write_lines)
print('end**********')
