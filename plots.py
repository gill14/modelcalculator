import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import interpolate
# Local File
from atomizationModel import AtomizationModel as am

class Plots():
    
    def static_params():
        # Cause I can't do it automagically
        upper_bound = 800
        # X
        _x = [0.1, 0.5, 0.9]
        x = np.linspace(0.1, 0.9, 50)
        # Y
        refs = [
            {'cat':'base', 'div':'BASE', 'y':[0,0,0], 'color':'#EE220C', 'abbreviation':'B', 'rank':0},
            {'cat':'Very Fine', 'div':'VF-F', 'y':[60, 134, 236], 'color':'#FF0000', 'abbreviation':'VF', 'rank':1},
            {'cat':'Fine', 'div':'F-M', 'y':[110,248,409], 'color':'#FEAE00', 'abbreviation':'F', 'rank':2},
            {'cat':'Medium', 'div':'M-C', 'y':[162,358, 584], 'color':'#FFF056', 'abbreviation':'M', 'rank':3},
            {'cat':'Coarse', 'div':'C-VC', 'y':[192,431,737], 'color':'#0076BA', 'abbreviation':'C', 'rank':4},
            {'cat':'Very Coarse', 'div':'VC-XC', 'y':[226,501,820], 'color':'#017100', 'abbreviation':'VC', 'rank':5},
            {'cat':'Extremely Coarse', 'div':'XC-UC', 'y':[303,659,1142], 'color':'#FFFFFF', 'abbreviation':'XC', 'rank':6},
            {'cat':'Ultra Coarse', 'div':'TOP', 'y':[upper_bound,upper_bound,upper_bound], 'color':'000000', 'abbreviation':'UC', 'rank':7}
        ]
        return x, _x, upper_bound, refs

    def plot2D(nozzles: list[tuple[str,am]]):
        # Set These Parameters
        flip_axes = True
        fill_color = True
        label_test_vals = True
        test_vals_list = []
        # test_vals = [175, 300, 600]
        for n in nozzles:
            name, model = n
            vf = model.volfracs()
            if vf[0]>0:
                test_vals_list.append(
                    [name, vf, model.dsc()]
                    )  
        # Make Backgound
        x, _x, upper_bound, refs = Plots.static_params()
        alpha = 0.85
        fig, ax = plt.subplots(nrows=1, ncols=1)
        patches = []
        for i, r in enumerate(refs):
            if i > 0:
                y1 = interpolate.pchip_interpolate(_x, refs[i-1]['y'], x)
                y2 = interpolate.pchip_interpolate(_x, r['y'], x)
                if flip_axes:
                    if fill_color:
                        ax.fill_betweenx(y=x, x1=y1, x2=y2, color=r['color'], alpha=alpha)
                    else:
                        _alpha = 1 if i< len(refs)-1 else 0
                        ax.plot(y2, x, color='#000000', alpha=_alpha)
                        ax.scatter(r['y'], _x, color='#000000', alpha=_alpha)
                        ax.text(y2[-1], x[-1]+.01, r['div'], fontsize=15, alpha=_alpha)
                else:
                    if fill_color:
                        ax.fill_between(x, y1, y2, color=r['color'], alpha=alpha)
                    else:
                        _alpha = 1 if i< len(refs)-1 else 0
                        ax.plot(x, y2, color='#000000', alpha=_alpha)
                        ax.scatter(_x, r['y'], color='#000000', alpha=_alpha)
                        ax.text(x[-1], y2[-1], '  '+r['div'], alpha=_alpha)

                patches.append(mpatches.Patch(color=r['color'], label=r['cat'], alpha=alpha))

        # Put some test points on it for examples (Uncomment as needed)
        for _test_vals in test_vals_list:
            name, test_vals, dsc = _test_vals
            if len(test_vals) == 3:
                _markersize = 5 if label_test_vals else 15
                if label_test_vals:
                    anch = -1
                    if test_vals[-1] > upper_bound:
                        if test_vals[-2] > upper_bound:
                            anch = -3
                        else:
                            anch = -2
                    ax.text(test_vals[anch] if flip_axes else _x[-1]+0.01, (_x if flip_axes else test_vals)[anch], (' ' if flip_axes else ' ')+name+' - '+dsc, fontsize=12 if flip_axes else 5, rotation=60 if flip_axes else 0, rotation_mode='anchor',
                        transform_rotates_text=False, in_layout=test_vals[anch]<upper_bound, color= "black" if anch==-1 else "white")
                #ax.plot(test_vals if flip_axes else _x, _x if flip_axes else test_vals, marker='X', color='white', markersize=_markersize+4, linewidth=4, clip_on=False, in_layout=False)
                ax.plot(test_vals if flip_axes else _x, _x if flip_axes else test_vals, marker='X', color='black', dashes=[4,4], gapcolor="white", markersize=_markersize, clip_on=False, in_layout=False)


        #Styling
        fig.set_facecolor('#D3D3D3')
        ax.set_facecolor('#FFFFFF')
        ax.margins(x=0,y=0)
        if flip_axes:
            ax.set_ylabel('Volume Fraction (Cumulative)', fontweight='bold')
            ax.set_yticks([0.1, 0.5, 0.9], ['DV0.1', 'VMD', 'DV0.9'])
            ax.set_xlabel('Droplet Size (microns)', fontweight='bold')
            ax.set_xticks(np.arange(0,upper_bound,100))
            ax.xaxis.get_major_ticks()[0].label1.set_visible(False)
            ax.set_xlim(0, upper_bound)
        else:
            ax.set_xlabel('Volume Fraction (Cumulative)', fontweight='bold')
            ax.set_xticks([0.1, 0.5, 0.9], ['DV0.1', 'VMD', 'DV0.9'])
            ax.set_ylabel('Droplet Size (microns)', fontweight='bold')
            ax.set_yticks(np.arange(0,upper_bound,100))
            ax.yaxis.get_major_ticks()[0].label1.set_visible(False)
        ax.grid(visible=flip_axes)
        legend_loc = 'lower right' if flip_axes else 'upper left'
        font_size = '10' if flip_axes else '10'
        if fill_color:
            ax.legend(handles=patches, fontsize=font_size, loc=legend_loc)
        #figwidth = 20 if flip_axes else 7
        #fig.set_figwidth(figwidth)
        return fig