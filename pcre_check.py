#!/usr/bin/env python
import subprocess, argparse

__author__  = "Jeff White [karttoon] @noottrak"
__email__   = "karttoon@gmail.com"
__version__ = "1.0.1"
__date__    = "31MAY2017"

# Adjust paths as necessary for pcregrep

def check_matches(pcre):

    match_check = ((subprocess.check_output(["/opt/local/bin/pcregrep '%s' %s" % (pcre, args.url)], shell=True)).strip()).split("\n")

    for url in match_check:
        if url not in matched[pcre]["m"]:
            matched[pcre]["m"].append(url)

    return

def check_nonmatches(pcre):

    match_check = ((subprocess.check_output(["/opt/local/bin/pcregrep -v '%s' %s" % (pcre, args.url)], shell=True)).strip()).split("\n")

    for url in match_check:
        if url not in matched[pcre]["u"]:
            matched[pcre]["u"].append(url)

    return

def print_match(pcre, value, type):

    print "\n[-] %s [-]\n" % value

    for url in matched[pcre]["%s" % type]:
        print url

    return

def print_unmatch():

    print "\n[+] NO HITS [+]\n"

    for pcre in matched:
        for url in matched[pcre]["m"]:

            try:
                url_list.remove(url)
            except:
                pass

    for url in url_list:
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
            try:
                pcre = entry.split("\t")[0].strip()
                matched[pcre] = {"m":[],"u":[]}
                try:
                    comment = entry.split("\t")[1].strip()
                except:
                    comment = "No comments"

                check_matches(pcre)

                match_count = len(matched[pcre]["m"])

                if match_count >= 1:

                    print "\n[+] FOUND [+]\nCount: %d/%d\nComment: %s\nPCRE: %s" % (match_count, url_count, comment, pcre)

                    if args.show:

                        print_match(pcre, "MATCH", "m")

                    if args.reverse:

                        check_nonmatches(pcre)

                        print_match(pcre, "NON-MATCH", "u")

            except:
                continue

    if args.nonmatch:

        print_unmatch()

    print ""




