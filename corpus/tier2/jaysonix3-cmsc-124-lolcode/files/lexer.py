from copy import deepcopy
import re


ARITHMETHIC_kw = [
  'K_SUM_OF',
  'K_DIFF_OF',
  'K_PRODUKT_OF',
  'K_QUOSHUNT_OF',
  'K_MOD_OF',
  'K_BIGGR_OF',
  'K_SMALLR_OF'
]

BOOLEAN_kw = [
  'K_BOTH_OF',
  'K_EITHER_OF',
  'K_WON_OF',
  'K_NOT',
  'K_ANY_OF',
  'K_ALL_OF'
]

TYPE_kw = [
  'NUMBAR',
  'NUMBR',
  'YARN',
  'TROOF',
  'BUKKIT',
]
# dictionary of keywords, literals, identfiers
regex_dict = {
  'K_HAI': r'HAI',
  'K_KTHXBYE': r'KTHXBYE',
  'cmnt': r'BTW (.*)',  # finds BTW and subsequent characters
  #   'K_BTW': r'BTW',
  'K_OBTW': r'OBTW',
  'K_TLDR': r'TLDR',
  'K_I_HAS_A': r'I HAS A',
  'K_ITZ': r'ITZ',
  'K_R': r'R',
  'K_SUM_OF': r'SUM OF',
  'K_DIFF_OF': r'DIFF OF',
  'K_PRODUKT_OF': r'PRODUKT OF',
  'K_QUOSHUNT_OF': r'QUOSHUNT OF',
  'K_MOD_OF': r'MOD OF',
  'K_BIGGR_OF': r'BIGGR OF',
  'K_SMALLR_OF': r'SMALLR OF',
  'K_BOTH_OF': r'BOTH OF',
  'K_EITHER_OF': r'EITHER OF',
  'K_WON_OF': r'WON OF',
  'K_NOT': r'NOT',
  'K_ANY_OF': r'ANY OF',
  'K_ALL_OF': r'ALL OF',
  'K_MKAY':r'MKAY',
  'K_BOTH_SAEM': r'BOTH SAEM',
  'K_DIFFRINT': r'DIFFRINT',
  'K_SMOOSH': r'SMOOSH',
  'K_MAEK': r'MAEK',
  'K_AN': r'AN',
  'K_GTFO': r'GTFO',
  'K_IS_NOW_A': r'IS NOW A',
  'K_VISIBLE': r'VISIBLE',
  'K_GIMMEH': r'GIMMEH',
  'K_O_RLY': r'O RLY\?',
  'K_YA_RLY': r'YA RLY',
  'K_MEBBE': r'MEBBE',
  'K_NO_WAI': r'NO WAI',
  'K_OIC': r'OIC',
  'K_WTF': r'WTF\?',
  'K_OMG': r'OMG',
  'K_OMGWTF': r'OMGWTF',
  'K_IM_IN_YR': r'IM IN YR',
  'K_UPPIN': r'UPPIN',
  'K_NERFIN': r'NERFIN',
  'K_YR': r'YR',
  'K_TIL': r'TIL',
  'K_WILE': r'WILE',
  'K_IM_OUTTA_YR': r'IM OUTTA YR',
  'NUMBAR': r'(-?\d+\.(\d+)?)',
  'NUMBR': r'(-?\d+)',
  'YARN': r'"([^"]*)"',
  'TROOF': r'(WIN|FAIL)',
  'TYPE': r'(NUMBR|NUMBAR|YARN|TROOF|BUKKIT)',
  'varident': r'([A-Za-z][A-Za-z\d\_]*)',
  'funcident': r'([A-Za-z][A-Za-z\d\_]*)',
  'loopident': r'([A-Za-z][A-Za-z\d\_]*)',
  'linebreak': r'\n',
  'space': r'\s(\s*)',
  'special_char': r'[@_!#$%^&*()<>?/\|}{~:.,]',
}


def file_read():
  file = open("sample/comp.lol", 'r')
  read = file.read().split("\n")
  file.close()
  return read


def detect_tokens(text):
  keys = list(regex_dict.keys())  # keys of regex_dict
  values = list(regex_dict.values())  # values of regex_dict
  arr = []  # 2D array
  #   line_cnt = 1
  for line in text:  # iterate each element in text
    arr2 = []  # array containing tuples
    # if line_cnt < 10:
    #     print("0"+str(line_cnt), line)
    # else:
    #     print(line_cnt, line)
    while line:  # while line is not empty
      #   print("current line", line)
      for i in values:  # iterate each element in values
        pos = values.index(i)  # get the index of i
        kkey = keys[pos]  # get the corresponding key of i
        z = re.match(i,
                     line)  # look for the first occurence of regex(i) in line
        # print(z)
        if z:  #if z is not empty
          # print(z.group())
          if z.group().startswith(
              'BTW'
          ):  # case for BTW; convert each line after BTW to cmnt lexeme
            temp = z.group().split()  # return each string store in temp
            arr2.append(
              ('K_BTW', temp[0]))  # append string BTW as keyword K_BTW
            temp.remove(temp[0])  # remove string BTW
            temp_string = ""  # declare empty string
            for i in range(len(temp)):  # iterate each element in temp
              if i + 1 == len(temp):  # if in last element of temp
                temp_string = temp_string + temp[
                  i]  # concatenate to temp_string with no space
              else:
                temp_string = temp_string + temp[
                  i] + " "  # concatenate to temp_string with space
            arr2.append(
              ('cmnt', temp_string))  # append temp_string as keyword cmt
          # STRING DELIMITER AND LITERAL
          elif z.group().startswith('"'):
            temp = z.group().replace('"', '')
            arr2.append(('str_delim', '"'))
            arr2.append(('str_literal', temp))
            arr2.append(('str_delim', '"'))
          else:
            arr2.append((kkey, z.group()))  # append z.group() as kkey
          # print(z.group())
          line = line.replace(z.group(), '',
                              1)  # remove first occurence of z.group in line
        else:
          continue
    arr2 = [x for x in arr2 if x[0] != 'space']  # remove space keyword
    arr2.append(('newline', '\n'))
    # print(arr2)
    arr.append(arr2)  # append arr2 to arr
    # arr = [x for x in arr if x] # uncomment to remove arrays without regex kineme
    # line_cnt += 1
    # print(arr)

  temp_arr = deepcopy(arr)
  obtw_idx = []
  tldr_idx = []
  multiline_idx = []
  multiline = []
  #   print(temp_arr)
  del_cnt = 0
  for x in temp_arr:
    if x:
      if x[0][0] == 'K_OBTW':
        idx = temp_arr.index(x)
        temp_arr.remove(temp_arr[idx])
        obtw_idx.append(idx + del_cnt)
        del_cnt += 1
      elif x[0][0] == "K_TLDR":
        idx = temp_arr.index(x)
        temp_arr.remove(temp_arr[idx])
        tldr_idx.append(idx + del_cnt)
        del_cnt += 1

#   print(obtw_idx)
#   print(tldr_idx)

  if len(obtw_idx) == len(tldr_idx):
    for i in range(len(obtw_idx)):
      temp_multi = tldr_idx[i] - obtw_idx[i] - 1
      multiline_idx.append(temp_multi)

#   print(multiline_idx)

  for i in range(len(multiline_idx)):
    for j in range(multiline_idx[i]):
      multiline.append(j + 1 + obtw_idx[i])


#   print(multiline)

  for i in range(len(arr)):
    for j in multiline:
      if i == j:
        temp_string = ""
        for k in range(len(arr[i])):
          if k + 1 == len(arr[i]):
            temp_string = temp_string + arr[i][k][1]
          else:
            temp_string = temp_string + arr[i][k][1] + " "
        # print(temp_string)
        temp_tuple = ('multi_cmnt', temp_string)
        arr_to_add = [temp_tuple]
        arr[i] = arr_to_add

  return list((arr))  # return


def create_tok(tokens):
  tok = []
  for i in range(len(tokens)):  # print tokens per line
    for j in range(len(tokens[i])):
      if tokens[i][j][0] != 'multi_cmnt' and tokens[i][j][0] != 'cmnt':
        tok.append(list(tokens[i][j]))
  # print(tok)
  return tok


def main():
  text = file_read()
  # print(text, "\n\n\n\n")
  ret = detect_tokens(text)  # call function, returns a 2D array
  # print(ret)
  printtok = create_tok(ret)
  return ret

if __name__ == '__main__':
    main()
