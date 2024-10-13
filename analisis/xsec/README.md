# Instruction

The folder `json` contains the cross sections at 13 and 13.6 TeV for various processes, from: https://github.com/fuenfundachtzig/xsec

To produce the cross section plots, run the following command:

```bash
# produces various xsec and nsignal events plots
./all_SUSY_plots.py
```

One can run a specific cross section plot (or in terms of number of signal events with)

```bash
# example for slepton
python3 python plot_xsecs_from_json.py --sqrt 13.6 --slepton --xmin 1 --xmax 1500
```

One can also get numberically cross sections, weights and number of signal events for various proceses

```bash
# examples
python3 getCrossSection.py --doSMuon --mass 500 
python3 getCrossSection.py --doSTau --mass 500 
python3 getCrossSection.py --doSTop --mass 500 

# now with luminosity and eventsSample 
python getCrossSection.py --doSMuon --mass 500 --luminosity 36 --eventsSample 20000
```