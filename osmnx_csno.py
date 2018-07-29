import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import pandas as pd

places_v = {# Vojvodina
            'Subotica'         : 'Subotica City, Serbia',
            'Sombor'           : 'Sombor City, Serbia',
            'Apatin'           : 'Apatin Municipality, Serbia',
            'Senta'            : 'Senta, Serbia',
            'Novi Sad'         : 'Novi Sad, Serbia',
            'Kikinda'          : 'Kikinda, Serbia',
            'Kula'             : 'Kula Municipality, Serbia',
            'Bačka Topola'     : 'Backa Topola Municipality, Serbia',
            'Zrenjanin'        : 'Zrenjanin, Serbia',
            'Sremski Karlovci' : 'Sremski Karlovci Municipality',
            'Sremska Mitrovica': 'Sremska Mitrovica City, Serbia',
            'Vršac'            : 'Vrsac Municipality, Serbia',
            'Pančevo'          : 'Pancevo City, Serbia',
            'Inđija'           : 'Indjija Municipality, Serbia',
            'Kovin'            : 'Kovin Municipality, Serbia',
            'Bela Crkva'       : 'Bela Crkva Municipality, Serbia'}

places_c = {# Central Serbia and Belgrade
            'Beograd'    : 'Belgrade, Serbia',
            'Šabac'      : 'Sabac, Serbia',
            'Smederevo'  : 'Smederevo City, Serbia',
            'Požarevac'  : 'Pozarevac, Serbia',
            'Valjevo'    : 'Valjevo City, Serbia',
            'Kragujevac' : 'Kragujevac, Serbia',
            'Kraljevo'   : 'Kraljevo, Serbia',
            'Kruševac'   : 'Krusevac City, Serbia',
            'Jagodina'   : 'Jagodina, Serbia',
            'Užice'      : 'Uzice City, Serbia',
            'Čačak'      : 'Cacak, Serbia',
            'Neogtin'    : 'Negotin, Serbia',
            'Zaječar'    : 'Zajecar, Serbia',
            'Bor'        : 'Bor Municipality, Serbia',
            'Ivanjica'   : 'Ivanjica, Serbia',
            'Paraćin'    : 'Paracin, Serbia',
            'Ćuprija'    : 'Cuprija, Serbia'}

places_s = {# South Serbia
            'Niš'          : 'Nis, Serbia',
            'Pirot'        : 'Pirot, Serbia',
            'Dimitrovgrad' : 'Dimitrovgrad Municipality, Serbia',
            'Leskovac'     : 'Leskovac, Serbia',
            'Vranje'       : 'Vranje, Serbia',
            'Kuršumlija'   : 'Kursumlija, Serbia',
            'Bosilegrad'   : 'Bosilegrad, Serbia',
            'Medveđa'      : 'Medvedja, Serbia',
            'Preševo'      : 'Presevo Municipality, Serbia',
            'Bujanovac'    : 'Bujanovac, Serbia'}

places_n = {# Novi Pazar region
            'Novi Pazar' : 'Novi Pazar, Serbia',
            'Sjenica'    : 'Sjenica, Serbia',
            'Tutin'      : 'Tutin, Serbia',
            'Prijepolje' : 'Prijepolje, Serbia',
            'Raška'      : 'Raska Municipality, Serbia',
            'Nova Varoš' : 'Nova Varos, Serbia',
            'Priboj'     : 'Priboj, Serbia'}

places_k = {# Kosovo
            'Priština'           : 'Pristina, Kosovo',
            'Kosovska Mitrovica' : 'Municipality of Mitrovica, Kosovo',
            'Prizren'            : 'Municipality of Prizren, Kosovo',
            'Peć'                : 'District of Peja, Kosovo',
            'Uroševac'           : 'Municipality of Ferizaj, Kosovo',
            'Gnjilane'           : 'Municipality of Gjilan, Kosovo',
            'Đakovica'           : 'Municipality of Gjakova, Kosovo'}

places_usa = {# For testing
              'Atlanta'       : 'Atlanta, GA, USA',
              'Boston'        : 'Boston, MA, USA',
              'Buffalo'       : 'Buffalo, NY, USA',
              'Charlotte'     : 'Charlotte, NC, USA',
              'Chicago'       : 'Chicago, IL, USA',
              'Cleveland'     : 'Cleveland, OH, USA',
              'Dallas'        : 'Dallas, TX, USA',
              'Houston'       : 'Houston, TX, USA',
              'Denver'        : 'Denver, CO, USA',
              'Detroit'       : 'Detroit, MI, USA',
              'Las Vegas'     : 'Las Vegas, NV, USA',
              'Los Angeles'   : {'city':'Los Angeles', 'state':'CA', 'country':'USA'},
              'Manhattan'     : 'Manhattan, NYC, NY, USA',
              'Miami'         : 'Miami, FL, USA',
              'Minneapolis'   : 'Minneapolis, MN, USA',
              'Orlando'       : 'Orlando, FL, USA',
              'Philadelphia'  : 'Philadelphia, PA, USA',
              'Phoenix'       : 'Phoenix, AZ, USA',
              'Portland'      : 'Portland, OR, USA',
              'Sacramento'    : 'Sacramento, CA, USA',
              'San Francisco' : {'city':'San Francisco', 'state':'CA', 'country':'USA'},
              'Seattle'       : 'Seattle, WA, USA',
              'St Louis'      : 'St. Louis, MO, USA',
              'Tampa'         : 'Tampa, FL, USA',
              'Washington'    : 'Washington, DC, USA'}

def reverse_bearing(x):
    return x + 180 if x < 180 else x - 180

def count_and_merge(n, bearings):
    n = n * 2
    bins = np.arange(n + 1) * 360 / n
    count, _ = np.histogram(bearings, bins=bins)
    count = np.roll(count, 1)
    return count[::2] + count[1::2]

def polar_plot(ax, bearings, n=36, title=''):
    bins = np.arange(n + 1) * 360 / n
    count = count_and_merge(n, bearings)
    _, division = np.histogram(bearings, bins=bins)
    frequency = count / count.sum()
    division = division[0:-1]
    width = 2 * np.pi / n

    ax.set_theta_zero_location('N')
    ax.set_theta_direction('clockwise')

    x = division * np.pi / 180
    bars = ax.bar(x, height=frequency, width=width, align='center', bottom=0,
                  zorder=2, color='#003366', edgecolor='k', linewidth=0.5, alpha=0.7)
    ax.set_ylim(top=frequency.max())

    title_font = {'family':'Century Gothic', 'size':24, 'weight':'bold'}
    xtick_font = {'family':'Century Gothic', 'size':10, 'weight':'bold', 'alpha':1.0, 'zorder':3}
    ytick_font = {'family':'Century Gothic', 'size': 9, 'weight':'bold', 'alpha':0.2, 'zorder':3}

    ax.set_title(title.upper(), y=1.05, fontdict=title_font)

    ax.set_yticks(np.linspace(0, max(ax.get_ylim()), 5))
    yticklabels = ['{:.2f}'.format(y) for y in ax.get_yticks()]
    yticklabels[0] = ''
    ax.set_yticklabels(labels=yticklabels, fontdict=ytick_font)

    xticklabels = ['N', '', 'E', '', 'S', '', 'W', '']
    ax.set_xticklabels(labels=xticklabels, fontdict=xtick_font)
    ax.tick_params(axis='x', which='major', pad=-2)

def get_bearings(places, weight_by_length=False):
    bearings = {}
    for place in sorted(places.keys()):
        query = places[place]
        G = ox.graph_from_place(query, network_type='drive')
        Gu = ox.add_edge_bearings(ox.get_undirected(G))
        if weight_by_length:
            city_bearings = []
            for u, v, k, d in Gu.edges(keys=True, data=True):
                city_bearings.extend([d['bearing']] * int(d['length']))
            b = pd.Series(city_bearings)
            bearings[place] = pd.concat([b, b.map(reverse_bearing)]).reset_index(drop='True')
        else:
            b = pd.Series([d['bearing'] for u, v, k, d in Gu.edges(keys=True, data=True)])
            bearings[place] = pd.concat([b, b.map(reverse_bearing)]).reset_index(drop='True')
    return bearings

def print_plots(places, title, file_name):
    bearings = get_bearings(places)
    n = len(places)
    ncols = int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))
    figsize = (ncols * 5, nrows * 5)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, subplot_kw={'projection':'polar'})

    for ax, place in zip(axes.flat, sorted(places.keys())):
        polar_plot(ax, bearings[place].dropna(), title=place)

    suptitle_font = {'family':'Century Gothic', 'fontsize':40, 'fontweight':'normal', 'y':1.07}
    fig.suptitle(title, **suptitle_font)
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.35)
    fig.savefig(file_name, dpi=120, bbox_inches='tight')
    plt.close()

ox.config(log_console=True, use_cache=True)
plot_title_base = 'City Street Network Orientation '
print_plots(places_usa, plot_title_base + 'USA', 'img/usa.png')
print_plots(places_v, plot_title_base + 'Vojvodina', 'img/vojvodina.png')
print_plots(places_c, plot_title_base + 'Central Serbia', 'img/central.png')
print_plots(places_s, plot_title_base + 'South Serbia', 'img/south.png')
print_plots(places_n, plot_title_base + 'Novi Pazar region', 'img/np.png')
print_plots(places_k, plot_title_base + 'Kosovo', 'img/kosovo.png')
