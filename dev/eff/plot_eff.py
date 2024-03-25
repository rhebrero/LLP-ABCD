import matplotlib.pyplot as plt
import pickle
import json
import numpy as np
import pandas as pd
def plot(eff_100,eff_500,output, savefig=True, ax : plt.Axes = None, label = ''):
    if ax is None:
        fig, ax = plt.subplots(1,1)
    else:
        fig = ax.get_figure()
        
    ax.plot(ctau,eff_100,label=' '.join([label,'100 GeV']))
    ax.plot(ctau,eff_500,label=' '.join([label,'500 GeV']))
    ax.legend()
    fig.suptitle(output)
    ax.set_xscale('log')
    ax.set_ylabel('Efficiency')
    ax.set_ylim(0,1)
    ax.set_xlabel(r'c$\tau$ (cm)')
    ax.grid(True)
    fig.show()
    if savefig:
        fig.savefig(f'/nfs/cms/martialc/Displaced2024/llp/dev/eff/figs/{output}.png')
        plt.close(fig)
    return ax


signal = 'STop'
# signal = 'SMuon'




d0_list = [0.1,0.01]
do_plot = False

# Plot for each
for i, d0 in enumerate(d0_list):
    
    D0Min = str(d0).replace('.','p')
    
    with open(f'/nfs/cms/martialc/Displaced2024/llp/dev/eff/{signal}_D0Min_{D0Min}__1e0_1e5.eff','rb') as file:
        eff_dict = pickle.load(file)
        


    ctau = np.array(list(eff_dict['total']['data'].keys()))/10



    # Eficiencia total
    eff_100 = np.array(list(eff_dict['total']['100'].values()))
    eff_500 = np.array(list(eff_dict['total']['500'].values()))
    
    ax_total_eff = plot(eff_100,eff_500,f'{signal}_total_D0Min_{D0Min}', label = signal)


    # Eficiencia de los cortes
    eff_selection = pd.DataFrame(eff_dict['selection'])
    eff_Min2D = eff_selection[['100','500']].applymap(lambda x: x['+2Displaced'])
    eff_Min2G = eff_selection[['100','500']].applymap(lambda x: x['+2Good'])
    eff_D0Min = eff_selection[['100','500']].applymap(lambda x: x[f'MinD0_{D0Min}'])
    
    ax_Min2Good = plot(eff_Min2G['100'],  eff_Min2G['500'],       f'{signal}_Min2Good_D0Min_{D0Min}', label = signal)
    
    ax_Min2Displaced = plot(eff_Min2D['100'],  eff_Min2D['500'],       f'{signal}_Min2Displaced_D0Min_{D0Min}', label = signal)

    ax_D0Min = plot(eff_D0Min['100'],  eff_D0Min['500'],       f'{signal}_D0Min_{D0Min}', label = signal)


ax_total_eff        = None
ax_Min2Good         = None
ax_Min2Displaced    = None
ax_D0Min            = None
# Plot comparison
for i, d0 in enumerate(d0_list):
    if (i == (len(d0_list) - 1)): do_plot = True
    D0Min = str(d0).replace('.','p')
    label = ' '.join([signal,D0Min])
    
    with open(f'/nfs/cms/martialc/Displaced2024/llp/dev/eff/{signal}_D0Min_{D0Min}__1e0_1e5.eff','rb') as file:
        eff_dict = pickle.load(file)
        


    ctau = np.array(list(eff_dict['total']['data'].keys()))/10



    # Eficiencia total
    eff_100 = np.array(list(eff_dict['total']['100'].values()))
    eff_500 = np.array(list(eff_dict['total']['500'].values()))
    
    
    ax_total_eff = plot(eff_100,eff_500,f'{signal}_total_comp',savefig=do_plot, ax = ax_total_eff, label = label)

    # Eficiencia de los cortes
    eff_selection = pd.DataFrame(eff_dict['selection'])
    eff_Min2D = eff_selection[['100','500']].applymap(lambda x: x['+2Displaced'])
    eff_Min2G = eff_selection[['100','500']].applymap(lambda x: x['+2Good'])
    eff_D0Min = eff_selection[['100','500']].applymap(lambda x: x[f'MinD0_{D0Min}'])
    
    
    ax_Min2Good         = plot(eff_Min2G['100'],  eff_Min2G['500'],       f'{signal}_Min2Good_D0Min_comp',  savefig = do_plot,  ax = ax_Min2Good,       label = label)
    ax_Min2Displaced    = plot(eff_Min2D['100'],  eff_Min2D['500'],       f'{signal}_Min2Displaced_comp',   savefig = do_plot,  ax = ax_Min2Displaced,  label = label)
    ax_D0Min            = plot(eff_D0Min['100'],  eff_D0Min['500'],       f'{signal}_D0Min_comp',           savefig = do_plot,  ax = ax_D0Min,          label = label)