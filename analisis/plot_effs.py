import ROOT as rt
from Histogram import Histogram
import pdb
import matplotlib.pyplot as plt
from files import *
from GenSignalAnalisis import artif_signal



#---------------------------------------------------------------------

ctau = [0.1,1,10,100,1000,10000]

filename_100 = 'eff_data/datos_eficiencias_100GeV_2.txt'
with open(filename_100, "r") as f:
        ae_7_100 = []
        for x in f:
            if '#' in x[0]: continue
                
            x_split = x.split(",") 

            ae_7_100.append(float(x_split[7]))

filename_500 = 'eff_data/datos_eficiencias_500GeV_2.txt'
with open(filename_500, "r") as f:
        ae_7_500 = []
        for x in f:
            if '#' in x[0]: continue
                
            x_split = x.split(",")

            ae_7_500.append(float(x_split[7]))




def plot_eff(signal_Susy_mass, 
             mass,
             label, 
             alpha,
             figname=None, 
             close = False):
    
    sig_dicts = [] 
    tau = [0.1,1,10,100,1000,10000]
    ctau_label = ['1','10','100','1000','10000','100000']

    for i in range(len(signal_Susy_mass)): 
        # pdb.set_trace()
        sig_dicts.append({
                'file':signal_Susy_mass[i],
                'susy':'SMuon',
                'type':'signal',
                'mass':mass,
                'label':f"SMuon_{str(mass)}_{str(ctau_label[i])}"
        })


    effs = []
#     pdb.set_trace()

    for sig_dict in sig_dicts:
        eff = artif_signal(sig_dict, 100, 0, 700, var_name='d0sig', eff=True, data_lumi=4, extra_cond=str(mass))
        effs.append(eff)
                 
#     with open('/nfs/cms/rhebrero/work/analisis/eff_data/effs.txt', 'r') as f:
#         for eff in f:
#             effs.append(float(eff))

    plt.plot(tau, effs, alpha = alpha, label = label)
    if mass==100: plt.plot(tau, ae_7_100, alpha = alpha, label = 'Smuon 100 Gen')
    if mass==500: plt.plot(tau, ae_7_500, alpha = alpha, label = 'Smuon 500 Gen')

    plt.ylabel('signal eff')
    plt.xlabel('lifetime (cm)')
    plt.ylim(0,1)
    plt.xlim(0.1,10000)
    plt.semilogx()
    # plt.show()
    if close: 
        # plt.title('')
        plt.plot()
        plt.legend()
        plt.grid(True)
        plt.savefig('/nfs/cms/rhebrero/work/analisis/fig_effs/' + figname + '.png')
        plt.close()

# pdb.set_trace()

# plot_eff(signal_SMuon_100, 100, "SMuon_100 disp", 1, )
# plot_eff(signal_SMuon_100, 100, "SMuon_100 prompt", 1)
plot_eff(signal_SMuon_100, 100, "SMuon 100 Rec", 1, figname = 'SMuon_100_effs_rec_vs_gen_MoreCuts', close=True)
# plot_eff(signal_SMuon_500, 500, "SMuon 500 Rec", 1, figname = 'SMuon_500_effs_rec_vs_genCuts', close=True)




# plt.plot(tau, ae_7_100, label = 'SMuon_100 generador')

# plt.ylabel('signal eff')
# plt.xlabel('lifetime (cm)')
# plt.ylim(0,1)
# plt.xlim(0.1,10000)
# plt.semilogx()


# plot_eff(signal_STop_100, filters_signal_disp, "STop_100 dips", 1)
# plot_eff(signal_STop_100, filters_signal_prompt, "STop_100 prompt", 1)
# plot_eff(signal_STop_100, filters_signal, "STop_100", 1, figname='STop_100_rec', close=True)


