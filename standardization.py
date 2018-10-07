#!/usr/bin/env python

import re

import cnstnts

# sample input TEST
input_addr1 = '1'
input_addr2 = '1089 SUMMIT AVENUE'
input_city = 'JERSEY CITY'
input_state = 'NJ'
input_zip = '7307'


def parse_mailing_address(input_addr1, input_addr2, input_city,
                          input_state, input_zip):
    # input_addr = ''.join([input_addr1, ' ', input_addr2])

    # replace all punctuation marks with spaces
    #     except for periods, slashes, & hyphens surrounded by digits
    # https://pe.usps.com/text/pub28/28c2_007.htm
    # https://pe.usps.com/text/pub28/28c2_013.htm
    input_addr1 = re.sub(r'(^|[^\d])[\./-](?=$|[^\d])', r'\1 ', input_addr1)
    input_addr2 = re.sub(r'(^|[^\d])[\./-](?=$|[^\d])', r'\1 ', input_addr2)

    # replace consecutive whitespaces with a singular space
    # remove leading & trailing whitespace
    # convert to uppercase
    input_addr1 = ' '.join(input_addr1.split())
    input_addr2 = ' '.join(input_addr2.split())
    input_addr = '\n'.join([input_addr1, input_addr2]).upper()

    pa_nmbr, pa_pred, pa_name, pa_sufx, pa_posd, pa_pobx, sa_idnt, sa_addr, extra =
            parse_address(input_addr)

    ll_city = input_city.strip().upper()

    ll_stat = input_state.strip().upper()

    # split input zip as needed
    ll_zip5 = re.sub(r'[^\d-]', r'', input_zip)
    ll_zip5_hyphen_index = ll_zip5.find('-')
    if ll_zip5_hyphen_index != -1:
        if ll_zip5_hyphen_index < len(ll_zip5) - 1:
            ll_pls4 = ll_zip5[ll_zip5_hyphen_index + 1:]
        else:
            ll_pls4 = ''
        if len(ll_pls4) > 0 and len(ll_pls4) < 4:
            ll_pls4 = ll_pls4.zfill(4)
        elif len(ll_pls4) > 4:
            ll_pls4 = ll_pls4[-4:]
        ll_zip5 = ll_zip5[:ll_zip5_hyphen_index]
        if len(ll_zip5) > 0 and len(ll_zip5) < 5:
            ll_zip5 = ll_zip5.zfill(5)
        elif len(ll_zip5) > 5:
            ll_zip5 = ll_zip5[-5:]
    else:
        if len(ll_zip5) <= 5:
            ll_pls4 = ''
            ll_zip5 = ll_zip5.zfill(5)
        elif len(ll_zip5) <= 9:
            ll_pls4 = ll_zip5[-4:]
            ll_zip5 = ll_zip5[:-4].zfill(5)
        else:  # this should never happen, but if it does, read from the right
            ll_pls4 = ll_zip5[-4:]
            ll_zip5 = ll_zip5[-9:-4]

    return [pa_nmbr, pa_pred, pa_name, pa_sufx, pa_posd, pa_pobx,
            sa_idnt, sa_addr, extra, ll_city, ll_stat, ll_zip5, ll_pls4]


# remove sorted fields from the address and
# use new lines to separate remaining unsorted fields while parsing
def parse_address(input_addr_line):

    # search for PO Box substrings

    loc_pa_pobx = re.finditer(r'(?#^|[\s])([pP][^\S\n]*[oO][^\S\n]*[bB][^\S\n]*[oO][^\S\n]*[xX])[^\S\n]*(\d+)', input_addr_line)
    for m in loc_pa_pobx:
        pa_pobx = ''.join(['PO Box ', m.group(2)])
        input_addr_line = ''.join([input_addr_line[:m.start(1)].strip(), '\n', input_addr_line[m.end():].strip()])

    # search for secondary address indicators

    loc_sa_idnt_range = []
    for sa_idnt_range in set(
            cnstnts.ABBR_SA_IDNT_RANGE.values()).union(
            cnstnts.ABBR_SA_IDNT_RANGE.keys()):
        # search from the end of the address
        sa_idnt_range_index = input_addr_line.rfind(sa_idnt_range)
        if sa_idnt_range_index != -1:
            loc_sa_idnt_range.append([sa_idnt_range_index, sa_idnt_range])
    if loc_sa_idnt_range != []:
        loc_sa_idnt_range = max(loc_sa_idnt_range)
        # works because python compares sequences lexicographically
        # https://dbader.org/blog/python-min-max-and-nested-lists
    loc_sa_idnt_norng = []
    for sa_idnt_norng in set(
            cnstnts.ABBR_SA_IDNT_NORNG.values()).union(
            cnstnts.ABBR_SA_IDNT_NORNG.keys()):
        # search from the end of the address
        sa_idnt_norng_index = input_addr_line.rfind(sa_idnt_norng)
        if sa_idnt_norng_index != -1:
            loc_sa_idnt_norng.append([sa_idnt_norng_index, sa_idnt_norng])
    if loc_sa_idnt_norng != []:
        loc_sa_idnt_norng = max(loc_sa_idnt_norng)
        # works because python compares sequences lexicographically
        # https://dbader.org/blog/python-min-max-and-nested-lists
    if loc_sa_idnt_range != []:
        sa_idnt = input_addr_line[loc_sa_idnt_range[0]:
                                  loc_sa_idnt_range[0] +
                                  len(loc_sa_idnt_range[1])]
        loc_sa_addr = re.finditer(r'^\s*(\w+)(?#$|\s*)', input_addr_line[input_addr_line[loc_sa_idnt_range[0] + len(loc_sa_idnt_range[1])]:])
        for m in loc_sa_addr:
            sa_addr = m.group(1)
            input_addr_line = ''.join([input_addr_line[:loc_sa_idnt_norng[0]].strip(), '\n', input_addr_line[loc_sa_idnt_norng[0] + len(loc_sa_idnt_norng[1]) + m.end(1):].strip()])
    elif loc_sa_idnt_norng != []:
        sa_idnt = input_addr_line[loc_sa_idnt_norng[0]:loc_sa_idnt_norng[0] + len(loc_sa_idnt_norng[1])]
        sa_addr = ''
        input_addr_line = ''.join([input_addr_line[:loc_sa_idnt_norng[0]].strip(), '\n', input_addr_line[loc_sa_idnt_norng[0] + len(loc_sa_idnt_norng[1]):].strip()])

    # what's left is probably just primary address fields

    # search for street name suffixes

    loc_pa_sufx = []
    for pa_sufx in set(
            cnstnts.ABBR_PA_SUFX.values()).union(
            cnstnts.ABBR_PA_SUFX.keys()):
        # search from the end of the address
        pa_sufx_index = input_addr_line.rfind(pa_sufx)
        if pa_sufx_index != -1:
            loc_pa_sufx.append([pa_sufx_index, pa_sufx])
    if loc_pa_sufx != []:
        loc_pa_sufx = max(loc_pa_sufx)
        # works because python compares sequences lexicographically
        # https://dbader.org/blog/python-min-max-and-nested-lists

    # if no street name suffixes found, assume no postdirectionals in address

    # if postdirectionals exist, they can be to the right of the street name suffix

    # dump any remaining text to the right of the postdirectional to `extra`

    # the street number should be all the way at the left

    # if predirectionals exist, they can be to the right of the street number

    # what remains between the predirectional and the suffix should be the street name

    # dump any remaining text to the left of the street number into `extra`

    return [pa_nmbr, pa_pred, pa_name, pa_sufx, pa_posd, pa_pobx,
            sa_idnt, sa_addr, extra]


# returns a string formatted acceptably for USPS standards
def create_standardized_address(pa_nmbr, pa_pred, pa_name, pa_sufx,
                                pa_posd, pa_pobx, sa_idnt, sa_addr, extra,
                                ll_city, ll_stat, ll_zip5, ll_pls4):
    ret_str = ''
    if pa_pobx != '':
        ''.join([ret_str, pa_pobx, '\n'])
    if pa_nmbr != '':
        ''.join([ret_str, pa_nmbr, ' '])
    if pa_pred != '':
        ''.join([ret_str, pa_pred, ' '])
    if pa_name != '':
        ''.join([ret_str, pa_name, ' '])
    if pa_sufx != '':
        ''.join([ret_str, pa_sufx, ' '])
    if pa_posd != '':
        ''.join([ret_str, pa_posd, ' '])
    if sa_idnt != '':
        ''.join([ret_str, pa_nmbr, ' '])
    if extra != '':
        ''.join([extra, ' '])
    ''.join([ret_str, '\b\n'])
    if ll_city != '':
        ''.join([ret_str, ll_city, ' '])
    if ll_stat != '':
        ''.join([ret_str, ll_stat, ' '])
    if ll_zip5 != '':
        ''.join([ret_str, ' ', ll_zip5, '-'])
        # because USPS prefers two spaces between the state and zip
        # https://pe.usps.com/text/pub28/28c2_009.htm
    if ll_pls4 != '':
        ''.join([ret_str, ll_pls4])
    return ret_str
