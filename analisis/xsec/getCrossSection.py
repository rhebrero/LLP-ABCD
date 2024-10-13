import os
import json
import argparse
json_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json')

def get_xsec_pb(filename, mass):
    """
    Given a filename.json and the SUSY mass, return the "xsec_pb" field in [pb] from one of the json files in json/*
    matching the filename.
    """
    xsec_pb = None
    # json_directory = 'json/' # hardcoded 
    for file in os.listdir(json_directory):
        if file.endswith('.json') and file.startswith(filename):
            with open(os.path.join(json_directory, file)) as f:
                data = json.load(f)
    
    xsec_pb = data['data'][str(int(mass))]['xsec_pb']
    return xsec_pb

def get_weight(filename, mass, eventsSample, luminosity):
    """
    Given a signal model determined by the json filename and the mass, it returns the corresponding weight given a number of
    generated events and an integrated luminosity in pb
    """
    weight = 0 
    xsec_pb = get_xsec_pb(filename, mass)
    weight = luminosity *  1000 * xsec_pb / eventsSample  # corresponding weight for the given signal model
    print('Signal xsec: ', xsec_pb,'pb')
    return weight

if __name__ == "__main__":
    # testing the function
    parser = argparse.ArgumentParser(description="get a SUSY cross section.")

    parser.add_argument('--doSMuon'          , dest='doSMuon'        , action='store_true'      , help='SMuon signal samples')
    parser.add_argument('--doSTop'           , dest='doSTop'         , action='store_true'      , help='STop  signal samples')
    parser.add_argument('--doSTau'           , dest='doSTau'         , action='store_true'      , help='STau  signal samples')
    parser.add_argument('--mass'             , dest='mass'           , default=100, type=int  , help='mass of Squark or Slepton')
    parser.add_argument('--luminosity'       , dest='luminosity'     , default=-1, type=float   , help='luminosity in fb-1 (36.6 fb-1 in 2022, 28.09 fb-1 in 2023)')
    parser.add_argument('--eventsSample'     , dest='eventsSample'   , default=-1, type=int     , help='number of generated events to compute the weight')

    args = parser.parse_args()

    dic_json = {}
    # so far only 13600 GeV cross sections available
    if args.doSMuon == True: 
        dic_json["selectron_LL"] = "pp13600_sleptons_1000011_-1000011_NNLL.json" # largest cross-section
        dic_json["selectron_RR"] = "pp13600_sleptons_2000011_-2000011_NNLL.json" # subleading process

    if args.doSTau == True: 
        dic_json["stau_1"] = "pp13600_sleptons_1000015_-1000015_NNLL.json"

    if args.doSTop == True: 
        dic_json["stop"] = "pp13600_stopsbottom_NNLO+NNLL.json"

    for keys in dic_json:
        filename = dic_json[keys]
        pretty_name = keys
        xsec_pb = get_xsec_pb(filename, args.mass)
        xsec_fb = xsec_pb * 1000

        print("Process = {pretty_name}, json = {filename}, mass= {args.mass} GeV: {xsec_pb} pb".format(**locals()))
        print("Cross section (13.6 TeV): {xsec_pb} pb or {xsec_fb} fb".format(**locals()))

        if args.luminosity > 0:
            nevents = xsec_fb * args.luminosity 
            print("Nevent produced after produced after {args.luminosity} fb-1: {nevents} ".format(**locals()))
            if args.eventsSample > 0:
                weight = get_weight(filename, args.mass, args.eventsSample, args.luminosity)
                print("   if a sample has {args.eventsSample} generated events, then the weight is: {weight} ".format(**locals()))




