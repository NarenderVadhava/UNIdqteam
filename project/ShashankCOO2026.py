
import pandas as pd
import numpy as np
import datetime
import re


###################################################################################
def write_to_output(data, output_file):
    with open(output_file, 'a+', encoding='utf-8') as f:
        f.write('\n')
        f.writelines(data)


output_file = 'output.txt'


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
## mprsp_null(['Q30_1','Q30_2','Q30_3','Q30_4'],['Strongly agree','Somewhat agree','Somewhat disagree','Strongly disagree'], ['Not Selected'])
## To check for responses from "arguments" to each variable
## checking for min/max or atleast one responses.
## quests=[]
## arguments'Performed on par','Significantly outperformed','Significantly underperformed','Somewhat outperformed','Somewhat underperformed'=[]
## null_arg =['Not Selected', 'NaN', '', '0']

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
            f'\nResponses error in {quests} variables: All values are null/Not Selected at RespID-{df.loc[record, unique_identifier]}',
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
            if j == 'Not Selected':
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
        if df.loc[record, quest] not in ['Not Selected', '', None, 'nan']:
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
        if df.loc[record, x] in [None, '', np.nan, 'Not Selected']:
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
## ignoreargument=[]    (list of all possible responses as "Not Selected")
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


def rank_check_low(quests, rank_list, total_rank):
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


def rank_check_max(quests, rank_list, max_num):
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
            if j == 'Not Selected':
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
            f'\nResponses error in {quests} variables: All values are null/Not Selected at RespID-{df.loc[record, unique_identifier]}',
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
            f'\nResponses error in {quests} variables: All values are null/Not Selected at RespID-{df.loc[record, unique_identifier]}',
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
            if j == 'Not Selected':
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


df = (pd.read_excel(
    r"C:\Users\Sharmash\PycharmProjects\ COO survey for coding\07 api\IBM 2025 COO survey for coding_Interim_Data(N=900)_(07-April-2025)_V4_Excel.xlsx",
    header=1
    , sheet_name='WithValueAsLabels', na_filter=False))

df = df.replace(np.nan, '', regex=True)

total_comp = df.shape[0]
unique_identifier = "respid"
run_time = datetime.datetime.now().strftime("%Y-%m-%d %I-%M-%S %p")
write_to_output(f'\n\n------------------Total Completes: {total_comp} @ {run_time} \n\n', output_file)

for record in range(0, total_comp):
    sprsp("D1",["Yes"])
    sprsp("D2",["Chief Operations Officer or equivalent","Chief Supply Chain Officer or equivalent"])
    sprsp("D3",["Automotive OEMs","Automotive Suppliers","Banking - Financial Markets","Banking - Retail / Consumer",
                "Banking - Wholesale / Business","Chemicals","Consumer Products","Consumer - Retail","Electronics",
                "Energy and Utilities","Government - Federal","Government - State / Provincial","Healthcare Payer",
                "Healthcare Provider","Industrial Products","Information technology services (incl. IT consulting)",
                "Insurance","Life Sciences / Pharmaceuticals","Manufacturing (excluding Industrial Products)",
                "Media and Entertainment","Petroleum (incl. Oil and Gas)","Telecommunications","Transportation","Travel"])
    sprsp("D4",["Australia","Brazil","Canada","Chile","China Mainland","Colombia","Denmark","Egypt",
                "France","Germany","Hong Kong","India","Indonesia","Ireland","Italy","Japan","Malaysia","Mexico","Netherlands",
                "Philippines","Qatar","Saudi Arabia"
        ,"Singapore","South Africa","South Korea","Spain","Sweden","Switzerland","Taiwan","Thailand","UAE","United Kingdom","United States"])
    if mustrsp("D3",["Government - Federal","Government - State / Provincial"])==False:
        sprsp("D5",["Publicly traded","Privately held"])
        nullcheck(["D5a"])
    else:
        nullcheck(["D5"])
        sprsp("D5a",["General public services (e.g., executive and legislative bodies, economic affairs, environmental policy and protection)"
            ,"Defense",
                     "Public order and safety (e.g., police and fire protection services, law courts, prisons)","Education",
                     "Social and citizen services (e.g., unemployment, housing, health)"])
    numrsp("D6",1,70)
    sprsp("D7",["Prefer not to respond","Female","Male","Non-binary"])
    numrsp("P1",250000000,650000000000)
    numrsp("P2_1",-100,1000)
    numrsp("P2_2",-100,1000)
    numrsp("P2_3",-100,1000)

    if mustrsp("D3",["Government - Federal","Government - State / Provincial"])==False:
        numrsp("P3_1", -100, 1000)
        numrsp("P3_2", -100, 1000)
        numrsp("P3_3", -100, 1000)
        num_sl(["P3_1","P3_2","P3_3"])
    else:
        nullcheck(["P3_1","P3_2","P3_3"])
    mprsp(["P4_1","P4_2","P4_3","P4_4","P4_5"],
          ["Significantly underperformed","Underperformed","Performed on par","Outperformed","Significantly outperformed"])
    sl_cat(["P4_1","P4_2","P4_3","P4_4","P4_5"],
          ["Significantly underperformed","Underperformed","Performed on par","Outperformed","Significantly outperformed"])
    mprsp(["P5_1","P5_2","P5_3","P5_4"],
          ["Significantly lagging","Lagging","No better / no worse","Leading","Significantly leading"])
    sl_cat(["P5_1","P5_2","P5_3","P5_4"],
          ["Significantly lagging","Lagging","No better / no worse","Leading","Significantly leading"])
    mprsp(["P6_1","P6_2"],["Ineffective","Somewhat effective","Moderately effective","Effective","Highly effective"])

    if mustrsp("D3", ["Government - Federal", "Government - State / Provincial"]) == False:
        mprsp_null_count_upto(["Q1_1_1","Q1_1_2","Q1_1_3","Q1_1_4","Q1_1_5","Q1_1_6","Q1_1_7","Q1_1_8","Q1_1_9","Q1_1_10","Q1_1_11","Q1_1_12","Q1_1_13","Q1_1_14","Q1_1_15"],
                              ["Customer/Constituent experience","Product and service innovation","Business model innovation","Forecast accuracy","Productivity or profitability/efficiency","Scalability of service delivery","Marketing and sales effectiveness","Diversity and inclusion","Environmental sustainability","Talent recruiting and retention","Supply chain performance","Market share growth","Technology modernization","Cybersecurity and data privacy","Ecosystems and partnerships"]
                              ,["Not selected"],5)
        mprsp_null_count_upto(["Q1_2_1","Q1_2_2","Q1_2_3","Q1_2_4","Q1_2_5","Q1_2_6","Q1_2_7","Q1_2_8","Q1_2_9","Q1_2_10","Q1_2_11","Q1_2_12","Q1_2_13","Q1_2_14","Q1_2_15"],
                              ["Customer/Constituent experience","Product and service innovation","Business model innovation"
                                  ,"Forecast accuracy","Productivity or profitability/efficiency","Scalability of service delivery"
                                  ,"Marketing and sales effectiveness","Diversity and inclusion","Environmental sustainability",
                               "Talent recruiting and retention","Supply chain performance","Market share growth","Technology modernization"
                                  ,"Cybersecurity and data privacy","Ecosystems and partnerships"],
                              ["Not selected"],5)
    else:
        mprsp_null_count_upto(
            ["Q1_1_1", "Q1_1_2", "Q1_1_3", "Q1_1_4", "Q1_1_5", "Q1_1_6", "Q1_1_7", "Q1_1_8", "Q1_1_9", "Q1_1_10",
             "Q1_1_11", "Q1_1_13", "Q1_1_14", "Q1_1_15"],
            ["Customer/Constituent experience", "Product and service innovation", "Business model innovation",
             "Forecast accuracy", "Productivity or profitability/efficiency", "Scalability of service delivery",
             "Marketing and sales effectiveness", "Diversity and inclusion", "Environmental sustainability",
             "Talent recruiting and retention", "Supply chain performance", "Market share growth",
             "Technology modernization", "Cybersecurity and data privacy", "Ecosystems and partnerships"]
            , ["Not selected"], 5)
        mprsp_null_count_upto(
            ["Q1_2_1", "Q1_2_2", "Q1_2_3", "Q1_2_4", "Q1_2_5", "Q1_2_6", "Q1_2_7", "Q1_2_8", "Q1_2_9", "Q1_2_10",
             "Q1_2_11", "Q1_2_13", "Q1_2_14", "Q1_2_15"],
            ["Customer/Constituent experience", "Product and service innovation", "Business model innovation",
             "Forecast accuracy", "Productivity or profitability/efficiency", "Scalability of service delivery",
             "Marketing and sales effectiveness", "Diversity and inclusion", "Environmental sustainability",
             "Talent recruiting and retention", "Supply chain performance", "Market share growth",
             "Technology modernization", "Cybersecurity and data privacy", "Ecosystems and partnerships"],
            ["Not selected"], 5)
        nullcheck(["Q1_1_12","Q1_2_12"])
    mprsp_null_count_upto(["Q2_1","Q2_2","Q2_3","Q2_4","Q2_5","Q2_6"],
                          ["Daily operational tasks","Unanticipated issues and crises","Ad hoc reporting demands",
                           "Compliance and regulatory obligations","Team leadership and management","Technology and process enhancement projects"],
                          ["Not selected"], 3)
    mprsp(["Q3_1","Q3_2","Q3_3","Q3_4","Q3_5","Q3_6"],
          ["Not at all confident","Minimally confident","Moderately confident","Very confident"])
    sl_cat(["Q3_1","Q3_2","Q3_3","Q3_4","Q3_5","Q3_6"],
          ["Not at all confident","Minimally confident","Moderately confident","Very confident"])
    mprsp(["Q4_1","Q4_2","Q4_3","Q4_4"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q4_1","Q4_2","Q4_3","Q4_4"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sprsp("Q5",["Decrease significantly","Decrease somewhat","Stay the same","Increase somewhat","Increase significantly"])
    mprsp(["Q6_1","Q6_2","Q6_3"],["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q6_1","Q6_2","Q6_3"],["Strongly disagree","Disagree","Agree","Strongly agree"])
    mprsp_null_count_upto(["Q7_1","Q7_2","Q7_3","Q7_4","Q7_5","Q7_6","Q7_7","Q7_8","Q7_9","Q7_10"],
                          ["Real-time data analytics and decision-making","Agile resource allocation","Automated and AI workflows",
                           "Scenario planning and AI-driven forecasting","Continuous process improvement",
                           "Cross-functional collaboration","Investment in modern technology, plant, and equipment","Supplier and partner ecosystem management",
                           "Change management and workforce development","Proactive risk identification"],["Not selected"],5)
    mprsp(["Q8_1","Q8_2","Q8_3","Q8_4"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q8_1","Q8_2","Q8_3","Q8_4"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    mprsp_null_count_upto(["Q9_1","Q9_2","Q9_3","Q9_4","Q9_5","Q9_6","Q9_7","Q9_8","Q9_9","Q9_10","Q9_11","Q9_12"],
                          ["Organizational structure","Processes and workflows","Performance metrics and KPIs","Technology and digital capabilities","Talent management and development","Risk management and resilience",
                           "Cross-functional collaboration and integration","Agility and adaptability","Stakeholder engagement and communication",
                           "Strategic alignment and execution","Ecosystem partnerships","Operational footprint and location strategy"],["Not selected"],6)
    mprsp_null_count_upto(["Q10_1","Q10_2","Q10_3","Q10_4","Q10_5","Q10_6","Q10_7","Q10_8","Q10_9","Q10_10","Q10_11","Q10_12"],
                          ["Limited budget / financial resources","Lack of expertise / knowledge","Inadequate technology",
                           "Insufficient or poorly integrated data","Resistance to change within our organization",
                           "Resistance to change outside our organization","Focus on short-term performance","Organizational silos / lack of collaboration",
                           "Lack of clear innovation strategy","Aversion to risk / disruption","Inefficient processes / governance","Regulatory constraints"]
                          ,["Not selected"],6)
    mprsp(["Q11_1","Q11_2","Q11_3","Q11_4","Q11_5","Q11_6","Q11_7","Q11_8","Q11_9","Q11_10","Q11_11","Q11_12","Q11_13","Q11_14","Q11_15"],
          ["Not investing","Experimenting","Piloting","Scaling","Fully scaled"])
    sl_cat(["Q11_1","Q11_2","Q11_3","Q11_4","Q11_5","Q11_6","Q11_7","Q11_8","Q11_9","Q11_10","Q11_11","Q11_12","Q11_13","Q11_14","Q11_15"],
          ["Not investing","Experimenting","Piloting","Scaling","Fully scaled"])

    for i in range (1,6):
        numrsp(f"Q12_{i}",-100,1000)
    num_sl(["Q12_1","Q12_2","Q12_3","Q12_4","Q12_5"])
    numrsp("Q13",0,100)
    mprsp_null_count_upto(["Q14_1","Q14_2","Q14_3","Q14_4","Q14_5","Q14_6","Q14_7","Q14_8","Q14_9","Q14_10"],
                          ["Complex integration","Technology did not meet business requirements","Insufficient talent and capabilities","Data-related challenges","Limited vendor capabilities",
                           "Inadequate program leadership","Flawed business case","Inadequate change management","Lack of executive sponsorship",
                           "Insufficient resources or budget"],["Not selected"],5)
    que=[]
    notqu=[]
    for i in range(1,11):
        if get_value(f"Q14_{i}") != "Not selected":
            que.append(f"Q15_{i}")

        else:
            notqu.append(f"Q15_{i}")
    #print(que)
    if len(que)>1:
        rank_check_max(que,["Rank 1","Rank 2","Rank 3","Rank 4","Rank 5"],5)
    else:
        nullcheck(que)
    nullcheck(notqu)

    mprsp(["Q16_1","Q16_2","Q16_3","Q16_4","Q16_5","Q16_6","Q16_7","Q16_8"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q16_1","Q16_2","Q16_3","Q16_4","Q16_5","Q16_6","Q16_7","Q16_8"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    mprsp(["Q17_1","Q17_2","Q17_3","Q17_4","Q17_5","Q17_6","Q17_7"],
          ["Not developed","Slightly developed","Moderately developed","Fully developed"])
    sl_cat(["Q17_1","Q17_2","Q17_3","Q17_4","Q17_5","Q17_6","Q17_7"],
          ["Not developed","Slightly developed","Moderately developed","Fully developed"])
    mprsp_null_count_upto(["Q18_1","Q18_2","Q18_3","Q18_4","Q18_5","Q18_6","Q18_7","Q18_8","Q18_9","Q18_10","Q18_11","Q18_12"],
                          ["Data siloes and lack of data integration","Unclear data ownership","Insufficient data governance processes"
                              ,"Data quality issues","Inadequate executive sponsorship","Unclear ROI / economic benefits"
                              ,"Technological barriers","Regulatory barriers","Inadequate skills and resources","Data privacy"
                              ,"Cybersecurity","Sourcing and accessing data"],["Not selected"],6)

    Qeig = []
    notqueig = []
    for i in range(1, 13):
        if get_value(f"Q18_{i}") != "Not selected":
            Qeig.append(f"Q19_{i}")
        else:
            notqueig.append(f"Q19_{i}")
    #print(Qeig)
    if len(Qeig)>1

        rank_check_max(Qeig, ["Rank 1", "Rank 2", "Rank 3", "Rank 4", "Rank 5","Rank 6"], 6)
    else:
        nullcheck(Qeig)
    nullcheck(notqueig)
    mprsp_null_count_upto(["Q20_1","Q20_2","Q20_3","Q20_4","Q20_5","Q20_6","Q20_7","Q20_8","Q20_9","Q20_10","Q20_11","Q20_12"],
          ["Rationalizing technology infrastructure and platforms","Scaling AI and automation across the enterprise",
           "Leveraging analytics for decision-making and cost optimization","Eliminating structural redundancies and inefficiencies",
           "Restructuring / reducing the workforce","Streamlining / optimizing supply chains",
           "Outsourcing non-core business functions / processes","Exiting low-margin / low-growth markets or business lines",
           "Divesting non-core assets","Reducing office / real-estate costs","Investing in energy-efficient technologies",
           "Renegotiating / reducing vendor spend"],["Not selected"],6)
    mprsp(["Q21_1","Q21_2"],["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q21_1","Q21_2"],["Strongly disagree","Disagree","Agree","Strongly agree"])
    mprsp(["Q22_1","Q22_2","Q22_3","Q22_4","Q22_5","Q22_6","Q22_7","Q22_8","Q22_9","Q22_10","Q22_11","Q22_12"],
          ["No risk","Little risk","Moderate risk","Critical risk"])
    sl_cat(["Q22_1","Q22_2","Q22_3","Q22_4","Q22_5","Q22_6","Q22_7","Q22_8","Q22_9","Q22_10","Q22_11","Q22_12"],
          ["No risk","Little risk","Moderate risk","Critical risk"])
    mprsp_null_count_upto(["Q23_1","Q23_2","Q23_3","Q23_4","Q23_5","Q23_6","Q23_7","Q23_8","Q23_9","Q23_10","Q23_11"],
                          ["Demand volatility","Increased costs (transportation, distribution, wages, and raw materials)",
                           "Transportation and logistics unavailability (e.g., ships, trucks, drivers)","Manufacturing and production interruptions",
                           "Supplier commitment deficiencies and slow response times","Natural disasters","Geopolitical instabilities",
                           "Technology issues (including cyber)",
                           "Regulatory changes","Quality control","Lack of visibility (inability to effectively track goods and materials)"],
                          ["Not selected"],5)

    Qtwenttfive = []
    notqtwenttfive = []
    for i in range(1, 12):
        if get_value(f"Q23_{i}") != "Not selected":
            Qtwenttfive.append(f"Q24_{i}")
        else:
            notqtwenttfive.append(f"Q24_{i}")
    #print(Qtwenttfive)

    mprsp(Qtwenttfive,["Not at all","Limited extent","Moderate extent","Great extent"])
    if len(Qtwenttfive)>2:
        #print(len(Qtwenttfive))
        sl_cat(Qtwenttfive,["Not at all","Limited extent","Moderate extent","Great extent"])

    mprsp_null_count_upto(["Q25_1","Q25_2","Q25_3","Q25_4","Q25_5","Q25_6"],
                          ["Improving workflows with automation and AI","Optimizing our supply chain","Creating value through procurement","Optimizing service delivery",
                           "Enhancing talent utilization",
                           "Improving decision-making through data analytics"],["Not selected"],3)
    mprsp(["Q26_1","Q26_2","Q26_3","Q26_4","Q26_5","Q26_6","Q26_7"],
          ["No impact","Minimal impact","Moderate impact","Significant impact","Transformational impact"])
    sl_cat(["Q26_1","Q26_2","Q26_3","Q26_4","Q26_5","Q26_6","Q26_7"],
          ["No impact","Minimal impact","Moderate impact","Significant impact","Transformational impact"])
    mprsp(["Q27_1","Q27_2","Q27_3","Q27_4","Q27_5","Q27_6","Q27_7"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q27_1","Q27_2","Q27_3","Q27_4","Q27_5","Q27_6","Q27_7"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    mprsp(["Q28_1","Q28_2","Q28_3","Q28_4","Q28_5","Q28_6","Q28_7","Q28_8"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q28_1","Q28_2","Q28_3","Q28_4","Q28_5","Q28_6","Q28_7","Q28_8"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])


    numrsp(f"Q29_1", 0, 100)

    if get_value("Q29_2")<get_value("Q29_3"):
        write_to_output(f' Q29_3 value is greater then Q29_2 RespID-{df.loc[record, unique_identifier]}',
                        output_file)
    else:
        numrsp(f"Q29_2", 0, 100)
    numrsp(f"Q29_3", 0, 100)
    num_sl(["Q29_1", "Q29_2", "Q29_3"])
    mprsp(["Q30_1","Q30_2","Q30_3","Q30_4","Q30_5","Q30_6","Q30_7"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q30_1","Q30_2","Q30_3","Q30_4","Q30_5","Q30_6","Q30_7"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    check_OE(["Q31"],3)
    mprsp(["Q32_1","Q32_2","Q32_3","Q32_4"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q32_1","Q32_2","Q32_3","Q32_4"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])

    mprsp(["Q33_1","Q33_2","Q33_3","Q33_4","Q33_5"],
          ["Strongly disagree", "Disagree", "Agree", "Strongly agree"])
    sl_cat(["Q33_1","Q33_2","Q33_3","Q33_4","Q33_5"],
          ["Strongly disagree", "Disagree", "Agree", "Strongly agree"])

    if mustrsp("D2",["Chief Operations Officer or equivalent"]):
        mprsp(["Q34_1", "Q34_2", "Q34_3", "Q34_5", "Q34_6", "Q34_7", "Q34_8", "Q34_9"],
              ["Not effective", "Somewhat effective", "Effective", "Very effective"])
        sl_cat(["Q34_1", "Q34_2", "Q34_3", "Q34_5", "Q34_6", "Q34_7", "Q34_8", "Q34_9"],
               ["Not effective", "Somewhat effective", "Effective", "Very effective"])
        nullcheck(["Q34_4"])
        mprsp_null_count_upto(
            ["Q35_1", "Q35_2", "Q35_3", "Q35_4", "Q35_6", "Q35_7", "Q35_8", "Q35_9", "Q35_10", "Q35_11",
             "Q35_12"],
            ["Chief Financial Officer (CFO) or equivalent",
             "Chief Information Officer (CIO) or equivalent",
             "Chief Technology Officer (CTO) or Chief Digital Officer (CDO) or equivalent",
             "Chief Data (or Analytics) Officer (CDO/CAO) or equivalent",
             "Chief Supply Chain Officer (CSCO) or equivalent",

             "Chief Human Resources (or Talent) Officer (CHRO) or equivalent",
             "Chief Marketing (or Customer or Communications) Officer (CMO) or equivalent",
             "Chief Sales (or Revenue) Officer or equivalent", "Chief AI Officer (CAIO) or equivalent",
             "Chief Information Security Officer (CISO) or equivalent",
             "Chief Risk (or Compliance) Officer (CRO/CCO) or equivalent",
             "Chief Innovation (or Transformation) Officer or equivalent"],
            ["Not selected"], 5)
        nullcheck(["Q35_5"])



    elif mustrsp("D2", ["Chief Supply Chain Officer or equivalent"]):
        mprsp(["Q34_1", "Q34_2", "Q34_3", "Q34_4", "Q34_6", "Q34_7", "Q34_8", "Q34_9"],
              ["Not effective", "Somewhat effective", "Effective", "Very effective"])
        sl_cat(["Q34_1", "Q34_2", "Q34_3", "Q34_4", "Q34_6", "Q34_7", "Q34_8", "Q34_9"],
               ["Not effective", "Somewhat effective", "Effective", "Very effective"])
        nullcheck(["Q34_5"])
        mprsp_null_count_upto(
            ["Q35_1", "Q35_2", "Q35_3", "Q35_4", "Q35_5", "Q35_7", "Q35_8", "Q35_9", "Q35_10", "Q35_11",
             "Q35_12"],
            ["Chief Financial Officer (CFO) or equivalent",
             "Chief Information Officer (CIO) or equivalent",
             "Chief Technology Officer (CTO) or Chief Digital Officer (CDO) or equivalent",
             "Chief Data (or Analytics) Officer (CDO/CAO) or equivalent",
             "Chief Operations Officer (COO) or equivalent",
             "Chief Human Resources (or Talent) Officer (CHRO) or equivalent",
             "Chief Marketing (or Customer or Communications) Officer (CMO) or equivalent",
             "Chief Sales (or Revenue) Officer or equivalent", "Chief AI Officer (CAIO) or equivalent",
             "Chief Information Security Officer (CISO) or equivalent",
             "Chief Risk (or Compliance) Officer (CRO/CCO) or equivalent",
             "Chief Innovation (or Transformation) Officer or equivalent"],
            ["Not selected"], 5)
        nullcheck(["Q35_6"])

    else:
        mprsp(["Q34_1", "Q34_2", "Q34_3", "Q34_4", "Q34_5", "Q34_6", "Q34_7", "Q34_8", "Q34_9"],
              ["Not effective", "Somewhat effective", "Effective", "Very effective"])
        sl_cat(["Q34_1", "Q34_2", "Q34_3", "Q34_4", "Q34_5", "Q34_6", "Q34_7", "Q34_8", "Q34_9"],
               ["Not effective", "Somewhat effective", "Effective", "Very effective"])
        mprsp_null_count_upto(
            ["Q35_1", "Q35_2", "Q35_3", "Q35_4", "Q35_5", "Q35_6", "Q35_7", "Q35_8", "Q35_9", "Q35_10", "Q35_11",
             "Q35_12"],
            ["Chief Financial Officer (CFO) or equivalent", "Chief Information Officer (CIO) or equivalent",
             "Chief Technology Officer (CTO) or Chief Digital Officer (CDO) or equivalent",
             "Chief Data (or Analytics) Officer (CDO/CAO) or equivalent",
             "Chief Operations Officer (COO) or equivalent", "Chief Supply Chain Officer (CSCO) or equivalent",
             "Chief Human Resources (or Talent) Officer (CHRO) or equivalent",
             "Chief Marketing (or Customer or Communications) Officer (CMO) or equivalent",
             "Chief Sales (or Revenue) Officer or equivalent", "Chief AI Officer (CAIO) or equivalent",
             "Chief Information Security Officer (CISO) or equivalent",
             "Chief Risk (or Compliance) Officer (CRO/CCO) or equivalent",
             "Chief Innovation (or Transformation) Officer or equivalent"],
            ["Not selected"], 5)


    mprsp(["Q36_1","Q36_2","Q36_3","Q36_4","Q36_5","Q36_6","Q36_7","Q36_8","Q36_9","Q36_10"],
          ["Today","In the next 12 months","In 13 to 24 months","No plan to adopt within the next 24 months"])
    sl_cat(["Q36_1","Q36_2","Q36_3","Q36_4","Q36_5","Q36_6","Q36_7","Q36_8","Q36_9","Q36_10"],
          ["Today","In the next 12 months","In 13 to 24 months","No plan to adopt within the next 24 months"])
    mprsp(["Q37_1","Q37_2","Q37_3","Q37_4","Q37_5"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    sl_cat(["Q37_1","Q37_2","Q37_3","Q37_4","Q37_5"],
          ["Strongly disagree","Disagree","Agree","Strongly agree"])
    numrsp("Q38",-100,500)























































