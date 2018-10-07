#!/usr/bin/env python

import re

import cnstnts

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
    # input_addr = re.sub(r'(^|[^\d])[\./-](?=$|[^\d])', r'\1 ', input_addr)

    # replace consecutive whitespaces with a singular space
    # remove leading & trailing whitespace
    # convert to uppercase
    input_addr1 = ' '.join(input_addr1.split())#.upper()
    input_addr2 = ' '.join(input_addr2.split())#.upper()
    input_addr = '\n'.join([input_addr1, input_addr2]).upper()
    # input_addr = ' '.join([input_addr1.split(), input_addr2.split()]).upper()
    # input_addr = ' '.join(input_addr.split()).upper()

    # addr1_list = parse_address(input_addr1)
    # addr2_list = parse_address(input_addr2)
    addr_list = parse_address(input_addr, '', '', '', '', '', '', '', '', '')

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


# uses new lines to separate unsorted values while parsing
def parse_address(input_addr_line,
                  pa_nmbr, pa_pred, pa_name, pa_sufx, pa_posd, pa_pobx,
                  sa_idnt, sa_addr, extra):

    # search for PO Box substrings

    if pa_pobx == '':
        # search for PO Box from the beginning of the string
        loc_pa_pobx = re.finditer(r'(?#^|[\s])([pP][^\S\n]*[oO][^\S\n]*[bB][^\S\n]*[oO][^\S\n]*[xX])[^\S\n]*(\d+)', input_addr_line)
        for m in loc_pa_pobx:
            pa_pobx = ''.join(['PO Box ', m.group(2)])
            input_addr_line = ''.join([input_addr_line[:m.start(1)].strip(), '\n', input_addr_line[m.end():].strip()])

    # search for secondary address indicators

    if sa_idnt == '':
        loc_sa_idnt_range = []
        for sa_idnt_range in set(
                cnstnts.ABBR_SA_IDNT_RANGE.values()).union(
                cnstnts.ABBR_SA_IDNT_RANGE.keys()):
            sa_idnt_range_index = input_addr_line.rfind(sa_idnt_range)
            if sa_idnt_range_index != -1:
                loc_sa_idnt_range.append([sa_idnt_range_index, sa_idnt_range])
        if loc_sa_idnt_range != []:
            loc_sa_idnt_range = max(loc_sa_idnt_range)
        loc_sa_idnt_norng = []
        for sa_idnt_norng in set(
                cnstnts.ABBR_SA_IDNT_NORNG.values()).union(
                cnstnts.ABBR_SA_IDNT_NORNG.keys()):
            sa_idnt_norng_index = input_addr_line.rfind(sa_idnt_norng)
            if sa_idnt_norng_index != -1:
                loc_sa_idnt_norng.append([sa_idnt_norng_index, sa_idnt_norng])
        if loc_sa_idnt_norng != []:
            loc_sa_idnt_norng = max(loc_sa_idnt_norng)
        if loc_sa_idnt_range != []:
            sa_idnt = input_addr_line[loc_sa_idnt_range[0]], input_addr_line[loc_sa_idnt_range[0] + len(loc_sa_idnt_range[1])]]
            loc_sa_addr = re.finditer(r'(?#^|\s*)(\w+)(?#$|\s*)', input_addr_line[input_addr_line[loc_sa_idnt_range[0] + len(loc_sa_idnt_range[1])]:].strip())
            for m in loc_sa_addr:
                sa_addr = m.group(1)
                input_addr_line = ''.join([input_addr_line[:m.start(1)].strip(), '\n', input_addr_line[m.end(1):].strip()])
        elif loc_sa_idnt_norng != []:
            sa_idnt = input_addr_line[loc_sa_idnt_norng[0]], input_addr_line[loc_sa_idnt_norng[0] + len(loc_sa_idnt_norng[1])]]
            sa_addr = ''
            input_addr_line = ''.join([input_addr_line[:loc_sa_idnt_norng[0]].strip(), '\n', input_addr_line[loc_sa_idnt_norng[0] + len(loc_sa_idnt_norng[1]):].strip()])

    # search for street name suffixes

    if pa_sufx == '':
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


    # if none of these are found, assume bulk of string is primary address with a missing suffix

    return [pa_nmbr, pa_pred, pa_name, pa_sufx, pa_posd, pa_pobx,
            sa_idnt, sa_addr, extra]


# https://pe.usps.com/text/pub28/28c2_009.htm
def create_standardized_address(pa_nmbr, pa_pred, pa_name, pa_sufx,
                                pa_posd, sa_idnt, sa_addr, extra,
                                ll_city, ll_stat, ll_zip5, ll_pls4):
    return ''
