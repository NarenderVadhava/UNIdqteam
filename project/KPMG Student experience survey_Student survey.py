import pandas as pd
import numpy as np
import datetime
import re
import os
import streamlit as st

output_file = "output.txt" 

def write_to_output(data,output_file):
    with open(output_file, 'a+', encoding='utf-8') as f:
        f.write('\n' + str(data))


###################################################################################

## Single Punch Function-> quest="variable Name"; arguments="stub labels in list"
## sprsp('D1',['Yes','No']) : To check either response from list only

def sprsp(quest, arguments):
    if df.loc[record, quest] not in arguments:
        write_to_output(
            f'\nError in {quest} variable: invalid value at RespID-{df.loc[record, unique_identifier]} as {df.loc[record, quest]}',
            output_file)


###################################################################################

## Multi Punch Function-> quests="variable Names in list"; arguments="stub labels in list"
## mprsp(['Q30_1','Q30_2','Q30_3','Q30_4'],['Strongly agree','Somewhat agree','Somewhat disagree','Strongly disagree'])
## To check for responses from "arguments" to each variable
## checking for min/max or atleast one responses.
## quests=[]
## arguments'Performed on par','Significantly outperformed','Significantly underperformed','Somewhat outperformed','Somewhat underperformed'=[]

def mprsp(quests, arguments):
    Responses_All = []
    i_cat = 0
    for x in quests:
        Responses_All.append(df.loc[record, x])
        if df.loc[record, x] not in arguments:
            write_to_output(
                f'\nError in {x} variable: invalid value at RespID-{df.loc[record, unique_identifier]} as {df.loc[record, x]}',
                output_file)
        elif df.loc[record, x] in arguments:
            i_cat = i_cat + 1
    if len(Responses_All) == 0 or len(Responses_All) > i_cat:
        write_to_output(
            f'\nResponses error in {quests} variables: invalid values at RespID-{df.loc[record, unique_identifier]}',
            output_file)


###################################################################################

## Multi Punch Function-> quests="variable Names in list"; arguments="stub labels in list"; null_arg="Null labels in list"
## mprsp_null(['Q30_1','Q30_2','Q30_3','Q30_4'],['Strongly agree','Somewhat agree','Somewhat disagree','Strongly disagree'], ['Not selected'])
## To check for responses from "arguments" to each variable
## checking for min/max or atleast one responses.
## quests=[]
## arguments'Performed on par','Significantly outperformed','Significantly underperformed','Somewhat outperformed','Somewhat underperformed'=[]
## null_arg =['Not selected', 'NaN', '', '0']

def mprsp_null(quests, arguments, null_arg):
    Responses_All = []
    i_cat = 0
    nu = 0
    for x in quests:
        Responses_All.append(df.loc[record, x])
        if df.loc[record, x] in null_arg or df.loc[record, x] in ['', None]:
            nu = nu + 1
        elif (df.loc[record, x] not in arguments) and (df.loc[record, x] not in null_arg):
            write_to_output(
                f'\nError in {x} variable: invalid value at RespID-{df.loc[record, unique_identifier]} as {df.loc[record, x]}',
                output_file)
        elif df.loc[record, x] in arguments:
            i_cat = i_cat + 1

    if len(Responses_All) == 0 or len(Responses_All) == nu:
        write_to_output(
            f'\nResponses error in {quests} variables: All values are null/Not selected at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    elif len(Responses_All) > (i_cat + nu):
        write_to_output(
            f'\nResponses error in {quests} variables: invalid responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)


#####################################################################################


## Blank check Function-> to check if input `element` is empty.
## Other than some special exclusions and inclusions,
## this function returns boolean result of Falsy check.

def is_empty(quest):
    if (isinstance(df.loc[record, quest], int) or isinstance(df.loc[record, quest], float)) and df.loc[
        record, quest] == 0:
        # Exclude 0 and 0.0 from the Falsy set.
        write_to_output(
            f'\nNull value check in {quest} variables: invalid numeric values at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    elif isinstance(df.loc[record, quest], str) and len(df.loc[record, quest].strip()) == 0:
        # Include string with one or more empty space(s) into Falsy set.
        return True
    elif isinstance(df.loc[record, quest], bool):
        # Exclude False from the Falsy set.
        write_to_output(
            f'\nNull value check in {quest} variables: value should be blank at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    else:
        # Falsy check.
        return False if df.loc[record, quest] else True


###################################################################################

def get_value(quest):  # which kind of question
    x = df.loc[record, quest]
    return x


def get_value_mprsp(quests):
    responses = []
    a = []
    b = ()  # why its in tuple
    for quest in quests:
        responses.append(df.loc[record, quest])
    b = (set(responses))
    a = list(b)
    for i in a:
        for j in a:
            if j == 'Not selected':
                a.remove(j)
    return a


# To check if variable is Null or not -> output is True/False

def is_null(quest):
    if df.loc[record, quest] is ['', None]:
        return True
    elif isinstance(df.loc[record, quest], str) and df.loc[record, quest].strip() == "":
        return True
    else:
        return False


###################################################################################
# To check if variable is Null or not
# nullcheck(['Q1'])

def nullcheck(quests):
    for quest in quests:
        if df.loc[record, quest] not in ['Not selected', '', None, 'nan']:
            write_to_output(
                f'\nNull value check in {quest} variables: value should be blank at RespID-{df.loc[record, unique_identifier]}',
                output_file)

        ###################################################################################


def isnull_list(quests):
    a = []
    for quest in quests:
        if df.loc[record, quest] is ['', None, 'nan', np.nan]:
            a.append('True')
        elif isinstance(df.loc[record, quest], str) and df.loc[record, quest].strip() == "":
            a.append('True')
        else:
            a.append('False')
    if len(set(a)) == 1:
        return True
    else:
        return False


def nullcheck_arg(quests, null_arg):
    for quest in quests:
        if df.loc[record, quest] not in null_arg:
            write_to_output(
                f'\nNull value check in {quest} variables: value should be null argument at RespID-{df.loc[record, unique_identifier]}',
                output_file)


##  Exclusive check-> To check the exclusive option with the list of statment as = quests but without exclusive one.
## *excl_arg has been used since we can have one/more exclusive options to consider.
## quests = ['P5_1','P5_2','P5_3','P5_4','P5_5','P5_6']
## arguments = ['Performed on par','Significantly outperformed','Significantly underperformed']
## excl_arg = 'P5_8','P5_7'  (all exclusive variables seperated by comma as *args)

def mprsp_excl(quests, arguments, *excl_arg):
    Responses_All = []
    Responses_exclusives = []
    i_cat = 0

    for x in quests:
        Responses_All.append(df.loc[record, x])
        if df.loc[record, x] not in arguments:
            write_to_output(
                f'\nError in {x} variable: invalid value at RespID-{df.loc[record, unique_identifier]} as {df.loc[record, quests]}',
                output_file)
        elif df.loc[record, x] in arguments:
            i_cat = i_cat + 1

    for arg in excl_arg:
        if df.loc[record, arg] in arguments:
            Responses_exclusives.append(df.loc[record, arg])

    if len(Responses_All) == 0 or len(Responses_All) > i_cat:
        write_to_output(
            f'\nResponses error in {quests} variables: invalid values at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    if len(Responses_All) > 0 and len(Responses_exclusives) > 0:
        write_to_output(
            f'\nResponses error in {excl_arg} {quests}  variables: exclusive values at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    if len(Responses_All) == 0 and len(Responses_exclusives) == 0:
        write_to_output(
            f'\nError in {excl_arg} {quests} variables: No responses / exclusive values at RespID-{df.loc[record, unique_identifier]}',
            output_file)

    ###################################################################################


## Straight liner - ""Categorical"" -> function to check if all responses to a list of variables are common/same.
## quests = []    (list of variables/questions)
## arguments = []    (list of all possible responses as list)

def sl_cat(quests, arguments):
    column_values = []
    for x in quests:
        if df.loc[record, x] in [None, '', np.nan, 'Not selected']:
            return None
        elif df.loc[record, x] in arguments:
            column_values.append(df.loc[record, x])
        else:
            write_to_output(
                f'\nError in {quests} variables: Responses are different at RespID-{df.loc[record, unique_identifier]}',
                output_file)

    unique_values = set(column_values)
    if len(unique_values) == 1:
        write_to_output(
            f'\nStraight liner: All values in {quests} variables are common at RespID-{df.loc[record, unique_identifier]}',
            output_file)


###################################################################################

## Straight liner - ""Numeric"" -> function to check if all numeric responses to a list of variables are common/same.
## quests =[]    (list of variables/questions)

def num_sl(quests):
    sum_of_values = 0
    a = []
    for x in quests:
        a.append(df.loc[record, x])
        sum_of_values += df.loc[record, x]
    average = sum_of_values / len(quests)
    straight_liner = all(df.loc[record, x] == average for x in quests)
    s = set(a)
    if straight_liner and len(s) == 1:
        write_to_output(
            f'\nStraight liner: All numbers in {quests} variables are common at RespID-{df.loc[record, unique_identifier]}',
            output_file
        )

    ###################################################################################


## SLrsp (Straight Liner responses) -> function to report if only common/same values are in multiple columns.
## columns_name = List of all columns.

def SLrsp(columns_name):
    column_values = []
    colCounts = 0
    for col in columns_name:
        if df.loc[record, col] not in [None, '', np.nan]:
            column_values.append(df.loc[record, col])
            colCounts += 1
    unique_values = set(column_values)

    if (len(unique_values) == 1) and (len(column_values) == colCounts):
        write_to_output(
            f'\nCommon value {unique_values} has been responsd with {columns_name} at RespID-{df.loc[record, unique_identifier]}',
            output_file)


###############################################################################

def single_cat(quests, arguments, count):
    c = 0
    for x in quests:
        if df.loc[record, x] == arguments:
            c += 1
    if c == count:
        return True
    else:
        return False


########################################################################################

def multi_cat(quests, arguments, count):
    c = 0
    for x in quests:
        if df.loc[record, x] == arguments:
            c += 1
    if c > count:
        return True
    else:
        return False


###################################################################################

def multi_cat_mprsp(quests, arguments, count):
    c = 0
    for x in quests:
        if df.loc[record, x] in arguments:
            c += 1
    if c > count:
        return True
    else:
        return False


##################################################################################

## Other - ""Closed Ended"" -> function to check the other variable and text box resp.
## quest = call for one question at a time.
## validarguments =[]    (list of all possible responses as list)
## ignoreargument=[]    (list of all possible responses as "Not selected")
## text_lenght -> keep this as 3 for defualt or can set as per need.

def has_numbers(inputString):
    return bool(re.search(r'\d', str(inputString)))


def other_CE(quest, validarguments, ignoreargument, quest_open, text_lenght):
    if df.loc[record, quest] in validarguments:
        if df.loc[record, quest_open] not in [None, '']:
            if (has_numbers(str(df.loc[record, quest_open])) == True):
                write_to_output(f'\nOther: {quest_open} have digits at RespID-{df.loc[record, unique_identifier]}',
                                output_file)
            elif (has_numbers(str(df.loc[record, quest_open])) == False):
                if len(''.join(df.loc[record, quest_open].split())) < text_lenght:
                    write_to_output(
                        f'\nOther: {quest_open} have charachters less than {text_lenght} at RespID-{df.loc[record, unique_identifier]}',
                        output_file)
        elif (df.loc[record, quest_open] in [None, '']):
            write_to_output(f'\nOther: {quest_open} is blank at RespID -{df.loc[record, unique_identifier]}',
                            output_file)
    elif df.loc[record, quest] in ignoreargument:
        if (df.loc[record, quest_open] not in [None, '']):
            write_to_output(
                f'\nOther: {quest_open} should be blank at RespID -{df.loc[record, unique_identifier]} as doesnt have valid punch',
                output_file)


###################################################################################

## Other - ""Open Ended"" -> function to check the other variable and text box resp.
## quests = call for one question at a time.
## text_lenght -> keep this as 3 for defualt or can set as per need.

def check_OE(quests, text_lenght):
    i = 1
    j = 0
    arr = []
    for obj in quests:
        if (i == 1):
            # print(df.loc[record,obj])
            if df.loc[record, obj] in [None, '', 'nan']:
                write_to_output(f'\n1st Other: {obj} is blank at RespID -{df.loc[record, unique_identifier]}',
                                output_file)
            elif df.loc[record, obj] not in [None, '', 'nan']:
                # if (has_numbers(str(df.loc[record, obj])) == True):
                #     write_to_output(f'\n1st Other: {obj} have digits at RespID-{df.loc[record, unique_identifier]}',
                #                     output_file)
                if isinstance(df.loc[record, obj], int):
                    return True
                if len(''.join(str(df.loc[record, obj]).split())) < text_lenght:
                    write_to_output(
                        f'\n1st Other: {obj} have charachters less than {text_lenght} at RespID-{df.loc[record, unique_identifier]}',
                        output_file)
        elif (i > 1):
            j = j + 1
            # if (has_numbers(str(df.loc[record, obj])) == True):
            #     write_to_output(f'\nOther: {obj} have digits at RespID-{df.loc[record, unique_identifier]}',
            #                     output_file)
            if df.loc[record, obj] not in [None, '', 'nan']:
                if len(''.join(df.loc[record, obj].split())) < text_lenght:
                    write_to_output(
                        f'\nOther: {obj} have charachters less than {text_lenght} at RespID-{df.loc[record, unique_identifier]}',
                        output_file)
        i = i + 1
        arr.append(df.loc[record, obj])

    if (j > 1) and (df.loc[record, quests[0]] in [None, '']):
        write_to_output(
            f'\nPre Open box: {quests[0]} is blank while other boxes have responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    if len(arr) != len(set(arr)):
        write_to_output(
            f'\nOthers - {quests[0]}: Unique responses issue found at RespID-{df.loc[record, unique_identifier]}',
            output_file)

    ###################################################################################


# numrsp('P2_1',1,100) -> To check the numeric response within min to max range only.

def numrsp(quest, minval, maxval):  # quest=question_name minval = minimum value maxval = maxvalue
    if df.loc[record, quest] not in [None, '', 'nan']:  # record = for i in data: i= record
        if (df.loc[record, quest] < minval):
            write_to_output(
                f'\n{quest}: Value {df.loc[record, quest]} is smaller than {minval} at RespID-{df.loc[record, unique_identifier]}',
                output_file)
        if (df.loc[record, quest] > maxval):
            write_to_output(
                f'\n{quest}: Value {df.loc[record, quest]} is greater than {maxval} at RespID-{df.loc[record, unique_identifier]}',
                output_file)
    elif df.loc[record, quest] in [None, '', 'nan']:
        write_to_output(
            f'\n{quest}: Value is Null at RespID-{df.loc[record, unique_identifier]} while should be a valid response.',
            output_file)


###################################################################################
# numrsp_any('P2_1',[1,100]) -> To check the numeric response within min to max range only.
# val_list -> To check the list of allowed numbers only not in Range.

def numrsp_any(quest, val_list):
    if df.loc[record, quest] not in [None, '', 'nan']:
        if (df.loc[record, quest] not in val_list):
            write_to_output(
                f'\n{quest}: Value {df.loc[record, quest]} is not per the required list {val_list} at RespID-{df.loc[record, unique_identifier]}',
                output_file)
    elif df.loc[record, quest] in [None, '', 'nan']:
        write_to_output(
            f'\n{quest}: Value is Null at RespID-{df.loc[record, unique_identifier]} while should be a valid response.',
            output_file)


###################################################################################
# # numrsp_mp(['P2_1', 'P2_2', 'P2_3'], 0, 100, 2) -> To check numeric response in a list of question within min to max range only.
# # tot_rsp


# def numrsp_mp(quests, minval, maxval, tot_rsp):
#     if df.loc[record, quest] not in [None, '', 'nan']:
#         if (df.loc[record, quest] < minval):
#             write_to_output(
#                 f'\n{quest}: Value {df.loc[record, quest]} is smaller than {minval} at RespID-{df.loc[record, unique_identifier]}',
#                 output_file)
#         if (df.loc[record, quest] > maxval):
#             write_to_output(
#                 f'\n{quest}: Value {df.loc[record, quest]} is greater than {maxval} at RespID-{df.loc[record, unique_identifier]}',
#                 output_file)
#     elif df.loc[record, quest] in [None, '', 'nan']:
#         write_to_output(
#             f'\n{quest}: Value is Null at RespID-{df.loc[record, unique_identifier]} while should be a valid response.',
#             output_file)

###################################################################################


# rank_check(quests,val_list) -> To check the Ranking responses within rank-list options.
# rank_list -> To check the list of allowed Ranks / numbers only not in Range.
# rank_check(['Q1_1','Q1_2','Q1_3','Q1_4'],['Rank1','Rank2','Rank3','Rank4'])

def rank_check(quests, rank_list):
    n = len(quests)
    validresponse = []
    for quest in quests:
        if df.loc[record, quest] not in [None, '', np.nan]:
            validresponse.append(df.loc[record, quest])

    if len(validresponse) == 0:
        write_to_output(f'\n{quests}: Ranking Value is missing at RespID-{df.loc[record, unique_identifier]} ',
                        output_file)
    elif len(validresponse) > 0:
        if len(set(validresponse)) != len(validresponse):
            write_to_output(f'\n{quests}: Ranked values have repeat at RespID-{df.loc[record, unique_identifier]} ',
                            output_file)
        if len(rank_list) != len(validresponse):
            write_to_output(
                f'\n{quests}: Ranking responses are missing per requirement at RespID-{df.loc[record, unique_identifier]} ',
                output_file)
        for i in validresponse:
            if i not in rank_list:
                write_to_output(
                    f'\n{quests}: Wrong rank response as per requirement at RespID-{df.loc[record, unique_identifier]} ',
                    output_file)

        ###################################################################################


def rank_check_Top(quests, rank_list, total_rank):
    n = len(quests)
    validresponse = []
    for quest in quests:
        if df.loc[record, quest] not in [None, '', np.nan]:
            validresponse.append(df.loc[record, quest])

    if len(validresponse) != total_rank:
        write_to_output(f'\n{quests}: Ranking Value is missing at RespID-{df.loc[record, unique_identifier]} ',
                        output_file)
    elif len(validresponse) == total_rank:
        if len(set(validresponse)) != len(validresponse):
            write_to_output(f'\n{quests}: Ranked values have repeat at RespID-{df.loc[record, unique_identifier]} ',
                            output_file)

        for i in validresponse:
            if i not in rank_list:
                write_to_output(
                    f'\n{quests}: Wrong rank response as per requirement at RespID-{df.loc[record, unique_identifier]} ',
                    output_file)

        ######################################################################################


def rank_check_min(quests, rank_list, min_num):
    n = len(quests)
    validresponse = []
    for quest in quests:
        if df.loc[record, quest] not in [None, '', np.nan]:
            validresponse.append(df.loc[record, quest])

    if len(validresponse) == 0:
        write_to_output(f'\n{quests}: Ranking Value is missing at RespID-{df.loc[record, unique_identifier]} ',
                        output_file)
    elif len(validresponse) >= min_num:
        if len(set(validresponse)) != len(validresponse):
            write_to_output(f'\n{quests}: Ranked values have repeat at RespID-{df.loc[record, unique_identifier]} ',
                            output_file)

        for i in validresponse:
            if i not in rank_list:
                write_to_output(
                    f'\n{quests}: Wrong rank response as per requirement at RespID-{df.loc[record, unique_identifier]} ',
                    output_file)

    ##############################################################################################################


def rank_check_upto_max(quests, rank_list, max_num):
    n = len(quests)
    validresponse = []
    for quest in quests:
        if df.loc[record, quest] not in [None, '', np.nan]:
            validresponse.append(df.loc[record, quest])

    if len(validresponse) == 0:
        write_to_output(f'\n{quests}: Ranking Value is missing at RespID-{df.loc[record, unique_identifier]} ',
                        output_file)
    elif len(validresponse) <= max_num and len(validresponse) > 0:
        if len(set(validresponse)) != len(validresponse):
            write_to_output(f'\n{quests}: Ranked values have repeat at RespID-{df.loc[record, unique_identifier]} ',
                            output_file)
    elif len(validresponse) > max_num:
        write_to_output(
            f'\n{quests}: Ranked values have exceeded from the maximum at RespID-{df.loc[record, unique_identifier]} ',
            output_file)

        for i in validresponse:
            if i not in rank_list:
                write_to_output(
                    f'\n{quests}: Wrong rank response as per requirement at RespID-{df.loc[record, unique_identifier]} ',
                    output_file)

    #############################################################################################################


# mustrsp(quest,rsplist) output is True/False
# quest -> Variable to check for condition
# rsplist -> List could have one or many responses/options per requirment.

def mustrsp(quest, rsplist):
    if df.loc[record, quest] in rsplist:
        return True
    elif df.loc[record, quest] not in rsplist:
        return False


def mustrsp_mprsp(quests, rsplist):
    count = []
    for quest in quests:
        if df.loc[record, quest] in rsplist:
            count.append('True')
        elif df.loc[record, quest] not in rsplist:
            count.append('False')
    if len(set(count)) == 1 and set(count) == {'True'}:
        return True


###################################################################################
# sumtotal(quests,totalvalue)
# quests -> [] -> list of all variables to consider for Sum
# totalvalue -> Value to match as total/sum for all variables

def sumtotal(quests, totalvalue):
    sumx = 0
    for quest in quests:
        if (df.loc[record, quest] == ''):
            df.loc[record, quest] = 0
        sumx = sumx + df.loc[record, quest]
    if sumx != totalvalue:
        write_to_output(
            f'\n{quests}: Sum should be {totalvalue} while it is {sumx} at RespID-{df.loc[record, unique_identifier]} ',
            output_file)


def sumupto(quests, maxval):
    sumx = 0
    for quest in quests:
        if (df.loc[record, quest] == ''):
            df.loc[record, quest] = 0
        sumx = sumx + df.loc[record, quest]
    if sumx > maxval:
        write_to_output(
            f'\n{quests}: Sum should be less than or equal to {maxval} while it is {sumx} at RespID-{df.loc[record, unique_identifier]} ',
            output_file)

    ########################### -Library- ########################################################


####req_rsp = to define the max valid responses to be allowed.

def mprsp_upto(quests, arguments, req_rsp):
    Responses_All = []
    for x in quests:
        Responses_All.append(df.loc[record, x])
    for i in Responses_All:
        for j in Responses_All:
            if j == 'Not selected':
                Responses_All.remove(j)
    if len(Responses_All) == 0 or len(Responses_All) > req_rsp and Responses_All in arguments:
        write_to_output(
            f'\nResponses error in {quests} variables: invalid number of responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)
        return False
    elif (len(Responses_All) <= req_rsp and Responses_All in arguments) and len(Responses_All) > 0:
        return True


def mprsp_null_count_upto(quests, arguments, null_arg, count):
    Responses_All = []
    i_cat = 0
    nu = 0
    for x in quests:
        Responses_All.append(df.loc[record, x])
        if df.loc[record, x] in null_arg:
            nu = nu + 1
        elif (df.loc[record, x] not in arguments) and (df.loc[record, x] not in null_arg):
            write_to_output(
                f'\nError in {x} variable: invalid value at RespID-{df.loc[record, unique_identifier]} as {df.loc[record, x]}',
                output_file)
        elif df.loc[record, x] in arguments:
            i_cat = i_cat + 1
    if count < i_cat:
        write_to_output(
            f'\nResponses error in {quests} variables: invalid responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)

    elif len(Responses_All) == 0 or len(Responses_All) == nu:
        write_to_output(
            f'\nResponses error in {quests} variables: All values are null/Not selected at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    elif len(Responses_All) > (i_cat + nu):
        write_to_output(
            f'\nResponses error in {quests} variables: invalid responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)


#     else:
#         write_to_output(
#             f'\nResponses error in {quests} variables: invalid number of responses at RespID-{df.loc[record, unique_identifier]}',
#             output_file)
#     elif Responses_All not in arguments:
#         write_to_output(
#             f'\nResponse error in {quests} variables: invalid response at RespID-{df.loc[record, unique_identifier]}',
#             output_file)

####req_rsp = to define the max valid responses to be allowed exactly.

def mprsp_null_count_exactly(quests, arguments, null_arg, count):
    Responses_All = []
    i_cat = 0
    nu = 0
    for x in quests:
        Responses_All.append(df.loc[record, x])
        if df.loc[record, x] in null_arg:
            nu = nu + 1
        elif (df.loc[record, x] not in arguments) and (df.loc[record, x] not in null_arg):
            write_to_output(
                f'\nError in {x} variable: invalid value at RespID-{df.loc[record, unique_identifier]} as {df.loc[record, x]}',
                output_file)
        elif df.loc[record, x] in arguments:
            i_cat = i_cat + 1

    if count != i_cat:
        write_to_output(
            f'\nResponses error in {quests} variables: invalid responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)

    elif len(Responses_All) == 0 or len(Responses_All) == nu:
        write_to_output(
            f'\nResponses error in {quests} variables: All values are null/Not selected at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    elif len(Responses_All) > (i_cat + nu):
        write_to_output(
            f'\nResponses error in {quests} variables: invalid responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)


def mprsp_exactly(quests, arguments, req_rsp):
    Responses_All = []
    for x in quests:
        Responses_All.append(df.loc[record, x])
    for i in Responses_All:
        for j in Responses_All:
            if j == 'Not selected':
                Responses_All.remove(j)
    if len(Responses_All) != req_rsp and Responses_All in arguments:
        write_to_output(
            f'\nResponses error in {quests} variables: invalid number of responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)
    elif len(Responses_All) == req_rsp and Responses_All in arguments:
        return True
    else:
        write_to_output(
            f'\nResponses error in {quests} variables: invalid responses at RespID-{df.loc[record, unique_identifier]}',
            output_file)
def run():
    global df, record, unique_identifier
    uploaded_file = st.file_uploader("Upload Excel", type=["xlsx", "xls"])
    if uploaded_file:
        if os.path.exists(output_file):
            os.remove(output_file)
        df = pd.read_excel(
            uploaded_file, 
            header=1,
            sheet_name='WithValueAsLabels',
            na_filter=False
        )
        df.replace(np.nan, '', regex=True)
        total_comp = df.shape[0]
        unique_identifier = "respid"
        run_time = datetime.datetime.now().strftime("%Y-%m-%d %I-%M-%S %p")
        write_to_output(f'\n\n------------------Total Completes: {total_comp} @ {run_time} \n\n',output_file)

        for record in range(0, total_comp):
            sprsp("Q1", [
                "Yes"
            ])
            sprsp("Q2", [
                "Public university",
                "Private non-profit university",
                "Private for-profit institution"
            ])
            sprsp("Q3", [
                "7,000 to 9,999 students",
                "10,000 to 19,999 students",
                "20,000 to 29,999 students",
                "30,000 or more students"
            ])
            sprsp("Q4", [
                "Undergraduate and graduate/postgraduate"
            ])
            sprsp("Q5", [
                "Full-time",
                "Part-time"
            ])
            sprsp("Q6", [
                "Undergraduate",
                "Graduate/professional student",
                "Other"
            ])
            if mustrsp("Q6",["Undergraduate"]):
                sprsp("Q6a", [
                    "First year",
                    "Second year",
                    "Third year",
                    "Fourth year",
                    "Fifth year or beyond"
                ])
            else:
                nullcheck(["Q6a"])
            sprsp("Q7", [
                "Woman",
                "Man",
                "Nonbinary",
                "Prefer not to answer"
            ])
            sprsp("Q8", [
                "US",
                "Canada",
                "UK",
                "France",
                "Germany",
                "Netherlands",
                "Ireland",
                "Saudi Arabia",
                "UAE",
                "Australia",
                "China",
                "Hong Kong (SAR), China",
                "Japan",
                "New Zealand",
                "Singapore",
                "India"
            ])
            sprsp("Q9", [
                "Yes",
                "No"
            ])
            sprsp("Q10", [
                "Humanities and social sciences",
                "Science, Technology, Engineering, and Mathematics",
                "Professional and applied fields"
            ])
            sprsp("Q11", [
                "Under 18",
                "18 to 21",
                "22 to 28",
                "29 to 36",
                "37 to 44",
                "45 to 60",
                "Over 60"
            ])
            sprsp("Q12", [
                "Yes",
                "No",
                "Unsure"
            ])
            sprsp("Q13", [
                "On-campus",
                "Online",
                "Hybrid (on-campus and online)",
                "Other"
            ])
            if mustrsp("Q13",["Other"]):
                check_OE(["Q13r4oe"],3)
            else:
                nullcheck(["Q13r4oe"])
            sprsp("Q14", [
                "Not at all important",
                "Slightly important",
                "Moderately important",
                "Considerably Important",
                "Very important"
            ])
            sprsp("noanswerQ15_n1",["None of the above","Not Selected"])
            if mustrsp("noanswerQ15_n1",["Not Selected"]):
                if mustrsp("Q15r28",[""]) == False:
                    mprsp(["Q15r1","Q15r2","Q15r3","Q15r4","Q15r5","Q15r6","Q15r7","Q15r8","Q15r9","Q15r10","Q15r11","Q15r12","Q15r13","Q15r14","Q15r15","Q15r16","Q15r17","Q15r18","Q15r19","Q15r20","Q15r21","Q15r22","Q15r23","Q15r24","Q15r25","Q15r26","Q15r27","Q15r28"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    sl_cat(["Q15r1","Q15r2","Q15r3","Q15r4","Q15r5","Q15r6","Q15r7","Q15r8","Q15r9","Q15r10","Q15r11","Q15r12","Q15r13","Q15r14","Q15r15","Q15r16","Q15r17","Q15r18","Q15r19","Q15r20","Q15r21","Q15r22","Q15r23","Q15r24","Q15r25","Q15r26","Q15r27","Q15r28"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    #### for each section 
                    sl_cat(["Q15r1","Q15r2","Q15r3","Q15r4","Q15r5","Q15r6","Q15r7","Q15r8"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    sl_cat(["Q15r9","Q15r10","Q15r11","Q15r12","Q15r13","Q15r14","Q15r15","Q15r16"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    sl_cat(["Q15r17","Q15r18","Q15r19","Q15r20","Q15r21","Q15r22","Q15r23","Q15r24","Q15r25","Q15r26","Q15r27"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    check_OE(["Q15r28oe"],3)
                else:
                    mprsp(["Q15r1","Q15r2","Q15r3","Q15r4","Q15r5","Q15r6","Q15r7","Q15r8","Q15r9","Q15r10","Q15r11","Q15r12","Q15r13","Q15r14","Q15r15","Q15r16","Q15r17","Q15r18","Q15r19","Q15r20","Q15r21","Q15r22","Q15r23","Q15r24","Q15r25","Q15r26","Q15r27"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    sl_cat(["Q15r1","Q15r2","Q15r3","Q15r4","Q15r5","Q15r6","Q15r7","Q15r8","Q15r9","Q15r10","Q15r11","Q15r12","Q15r13","Q15r14","Q15r15","Q15r16","Q15r17","Q15r18","Q15r19","Q15r20","Q15r21","Q15r22","Q15r23","Q15r24","Q15r25","Q15r26","Q15r27"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    #### for each section 
                    sl_cat(["Q15r1","Q15r2","Q15r3","Q15r4","Q15r5","Q15r6","Q15r7","Q15r8"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    sl_cat(["Q15r9","Q15r10","Q15r11","Q15r12","Q15r13","Q15r14","Q15r15","Q15r16"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    sl_cat(["Q15r17","Q15r18","Q15r19","Q15r20","Q15r21","Q15r22","Q15r23","Q15r24","Q15r25","Q15r26","Q15r27"],[
                                                            "Not important",
                                                            "Somewhat important",
                                                            "Very important"
                                                        ])
                    nullcheck(["Q15r28oe"])
            else:
                nullcheck(["Q15r1","Q15r2","Q15r3","Q15r4","Q15r5","Q15r6","Q15r7","Q15r8","Q15r9","Q15r10","Q15r11","Q15r12","Q15r13","Q15r14","Q15r15","Q15r16","Q15r17","Q15r18","Q15r19","Q15r20","Q15r21","Q15r22","Q15r23","Q15r24","Q15r25","Q15r26","Q15r27","Q15r28"])
                nullcheck(["Q15r28oe"])
            sprsp("Q16",[
                    "Very poor",
                    "Poor",
                    "Average",
                    "Good",
                    "Very good"
                ])
            mprsp_null_count_upto(["Q17r1","Q17r2","Q17r3","Q17r4","Q17r5","Q17r6","Q17r7","Q17r8","Q17r9","Q17r10","Q17r11","Q17r12","Q17r13","Q17r14"],[
                "Managing heavy workloads and higher academic expectations, often without clear guidance on what success looks like.",
                "Struggling with time management while juggling classes, ... extracurriculars, leading to missed deadlines and burnout.",
                "High levels of stress, anxiety, and depression that interfere with your concentration, sleep, and motivation.",
                "Underuse or limited access to counseling and wellness services, leaving issues like isolation and burnout unaddressed.",
                "Ongoing worry about tuition, housing, food, and other costs, especially for low income and first generation students.",
                "Needing to work significant hours while studying, which reduces time and energy for coursework.",
                "Navigating fragmented processes for aid, registration, and advising, often repeating information to multiple offices.",
                "Receiving confusing or inconsistent guidance on policies, deadlines, and degree requirements.",
                "Difficulty building friendships and community, with homesickness and loneliness common in the first year.",
                "Uncertainty about major, identity, and career direction, creating ongoing stress about the future.",
                "Confusing or unreliable digital platforms for registration, learning...leading to missed deadlines and errors.",
                "Poor integration across systems that forces students to reenter ... and check multiple portals to stay on top of tasks.",
                "Overcrowded, outdated, or inaccessible classrooms, libraries...that make it hard to focus or find a place to work.",
                "Limited, unreliable, or unsafe transportation, housing, and campus amenities that add daily friction to student life."
            ],["Not Selected"],5)
            mprsp(["Q18r1","Q18r2","Q18r3","Q18r4","Q18r5","Q18r6","Q18r7","Q18r8","Q18r9","Q18r10","Q18r11","Q18r12","Q18r13","Q18r14"],[
                "Agree",
                "Neutral",
                "Disagree"
            ])
            sl_cat(["Q18r1","Q18r2","Q18r3","Q18r4","Q18r5","Q18r6","Q18r7","Q18r8","Q18r9","Q18r10","Q18r11","Q18r12","Q18r13","Q18r14"],[
                "Agree",
                "Neutral",
                "Disagree"
            ])
            mprsp(["Q19r1","Q19r2","Q19r3","Q19r4","Q19r5"],[
                "Very poor",
                "Poor",
                "Average",
                "Good",
                "Excellent"
            ])
            sl_cat(["Q19r1","Q19r2","Q19r3","Q19r4","Q19r5"],[
                "Very poor",
                "Poor",
                "Average",
                "Good",
                "Excellent"
            ])
            sprsp("Q20r15",["None of the above","Not Selected"])
            if mustrsp("Q20r15",["Not Selected"]):
                mprsp_null(["Q20r1","Q20r2","Q20r3","Q20r4","Q20r5","Q20r6","Q20r7","Q20r8","Q20r9","Q20r10","Q20r11","Q20r12","Q20r13","Q20r14"],
                ["Improved academic success",
                "Increased motivation and engagement",
                "Ability to learn at my own pace",
                "More flexible learning options",
                "Clearer learning paths",
                "Stronger relationships with teachers",
                "Feeling more valued and understood",
                "Improved mental health and wellness",
                "Greater satisfaction with university experience",
                "Improved employability",
                "Greater preparation for life after school",
                "Better reputation for the university",
                "Greater efficiency and service quality",
                "Improved diversity, equity, and inclusion"],["Not Selected"])
            else:
                nullcheck_arg([["Q20r1","Q20r2","Q20r3","Q20r4","Q20r5","Q20r6","Q20r7","Q20r8","Q20r9","Q20r10","Q20r11","Q20r12","Q20r13","Q20r14"]])
        if os.path.exists(output_file):
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Output File",
                    data=f,
                    file_name="output.txt",
                    mime="text/plain"
                )

