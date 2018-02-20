#!/usr/bin/env python
import subprocess, argparse

__author__  = "Jeff White [karttoon] @noottrak"
__email__   = "karttoon@gmail.com"
__version__ = "1.0.3"
__date__    = "20FEB2018"

# Adjust paths as necessary for pcregrep

def check_matches(pcre, matched):

    try:
        match_check = ((subprocess.check_output(["/usr/local/bin/pcregrep '%s' %s" % (pcre, args.url)], shell=True)).strip()).split("\n")
    except:
        match_check = []

    for url in match_check:
        if url not in matched[pcre]["m"]:
            matched[pcre]["m"].append(url)

    return matched

def check_nonmatches(pcre, matched):

    try:
        match_check = ((subprocess.check_output(["/usr/local/bin/pcregrep -v '%s' %s" % (pcre, args.url)], shell=True)).strip()).split("\n")
    except:
        match_check = []

    for url in match_check:
        if url not in matched[pcre]["u"]:
            matched[pcre]["u"].append(url)

    return matched

def print_match(pcre, value, type, matched):

    print "\n[-] %s [-]\n" % value

    for url in matched[pcre]["%s" % type]:
        print url

    return

def print_unmatch(matched, url_list):

    print "\n[+] NO HITS [+]\n"

    match = []

    for pcre in matched:
        for url in matched[pcre]["m"]:
            match.append(url)

    for url in url_list:
        if url not in match:
            print url

    return

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Check URLs against RH PCREs.")
    parser.add_argument("-p", "--pcre",help="Roadhouse PCRE file.",metavar='<RH_pcre_file>', required=True)
    parser.add_argument("-u", "--url", help="URL file.", metavar='<url_file>', required=True)
    parser.add_argument("-r", "--reverse", help="Print non-matching URLs per section.", action="store_true")
    parser.add_argument("-s", "--show", help="Print matching URLs.", action="store_true")
    parser.add_argument("-n", "--nonmatch", help="Print all non-matching URLs at end.", action="store_true")
    args = parser.parse_args()

    pcre_list = []
    url_list  = []
    matched   = {}

    rh_pcre = open(args.pcre, "r")
    for entry in rh_pcre:
        pcre_list.append(entry)

    url_count = 0
    with open(args.url) as url_file:
        for url in url_file:
            url_list.append(url.strip())
            url_count += 1

    for entry in pcre_list:
        if not entry.startswith("#"):
            pcre = entry.split("\t")[0].strip()
            matched[pcre] = {"m":[],"u":[]}
            try:
                comment = entry.split("\t")[1].strip()
            except:
                comment = "No comments"

            matched = check_matches(pcre, matched)

            match_count = len(matched[pcre]["m"])

            if match_count >= 1:

                print "\n[+] FOUND [+]\n\nCount: %d/%d\nComment: %s\nPCRE: %s" % (match_count, url_count, comment, pcre)

                if args.show:

                    print_match(pcre, "MATCH", "m", matched)

                if args.reverse:

                    matched = check_nonmatches(pcre, matched)

                    print_match(pcre, "NON-MATCH", "u", matched)

    if args.nonmatch:

        print_unmatch(matched, url_list)

    print ""




