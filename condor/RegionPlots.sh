
# python3 ABCD_plot.py --branch hasVtx --region A --pred --EraB
# python3 ABCD_plot.py --branch invMass --region A --pred --EraB
# python3 ABCD_plot.py --branch pt --region A --pred --EraB
# python3 ABCD_plot.py --branch d0sig --region A --pred --EraB
# python3 ABCD_plot.py --branch iso --region A --pred --EraB
# python3 ABCD_plot.py --branch DeltaR --region A --pred --EraB

python3 ABCD_plot.py --branch hasVtx --region A --pred --Zmass
python3 ABCD_plot.py --branch invMass --region A --pred --Zmass
python3 ABCD_plot.py --branch pt --region A --pred --Zmass
python3 ABCD_plot.py --branch d0sig --region A --pred --Zmass
python3 ABCD_plot.py --branch iso --region A --pred --Zmass
python3 ABCD_plot.py --branch DeltaR --region A --pred --Zmass

python3 ABCD_plot.py --branch hasVtx --region A --pred --SS
python3 ABCD_plot.py --branch invMass --region A --pred --SS
python3 ABCD_plot.py --branch pt --region A --pred --SS
python3 ABCD_plot.py --branch d0sig --region A --pred --SS
python3 ABCD_plot.py --branch iso --region A --pred --SS
python3 ABCD_plot.py --branch DeltaR --region A --pred --SS

# python3 GenSignalAnalisis.py --branch pt --mass 100
# python3 GenSignalAnalisis.py --branch pt --mass 500

# python3 GenSignalAnalisis.py --branch invMass --mass 100
# python3 GenSignalAnalisis.py --branch invMass --mass 500

# python3 GenSignalAnalisis.py --branch d0sig --mass 100
# python3 GenSignalAnalisis.py --branch d0sig --mass 500

# python3 GenSignalAnalisis.py --branch pt
# python3 GenSignalAnalisis.py --branch d0sig
# python3 GenSignalAnalisis.py --branch invMass

# python3 coef_evol.py --var invMass
# python3 coef_evol.py --var pt