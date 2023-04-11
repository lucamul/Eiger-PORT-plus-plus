import numpy as np

# parameters for plot
title_font = 20
axis_font = 18
tick_font = 16
title_info = {'fontsize': title_font,
            'fontweight' : "bold",
            'verticalalignment': 'baseline',
            'horizontalalignment': "center"}

marker_size = 13
line_width = 2.5
tick_font_inaxis = 10
haveGrid = False
showPlot = False
bar_width = 0.2
allBar = True
freshBar = True
plus = False
normalize = True
normalizer = "EIGER_PORT"
tp_label = "Throughput (ops/s)"
lat_label = "Latency (ms)"

algorithms = ["EIGER", "EIGER_PORT", "EIGER_PORT_PLUS_PLUS"]
saveTo = "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/plotting/plots/noplus/"
# edit this if you want to change the algorithms you can plot
if plus:
    algorithms = ["EIGER", "EIGER_PORT", "EIGER_PORT_PLUS", "EIGER_PORT_PLUS_PLUS"]
    saveTo = "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/plotting/plots/plus/"

if normalize:
    algorithms = ["EIGER_PORT", "EIGER_PORT_PLUS_PLUS"]
    saveTo = "/home/luca/ETH/Thesis/EIGERPORT++/Eiger-PORT-plus-plus/plotting/plots/normalized/"
    tp_label = "Normalized Throughput"
    lat_label = "Normalized Latency"
#algorithms = ["EIGER","EIGER_PORT", "EIGER_PORT_PLUS_PLUS"]
# save the images as pdfs here

if not allBar:
    saveTo = saveTo + "noBar/"
 
colors = {
    "EIGER": "#1f77b4",
    "EIGER_PORT": "#ff7f0e",
    "EIGER_PORT_PLUS": "#2ca02c",
    "EIGER_PORT_PLUS_PLUS": "#9467bd",
}

markers = {
    "EIGER": "o",
    "EIGER_PORT": "s",
    "EIGER_PORT_PLUS": "v",
    "EIGER_PORT_PLUS_PLUS": "x",
}

names = {
    "EIGER": "Eiger",
    "EIGER_PORT": "Eiger-PORT",
    "EIGER_PORT_PLUS": "Eiger-PORT+",
    "EIGER_PORT_PLUS_PLUS": "Eiger-PORT++",
}

# data freshness x_axis
staleness = [10,20,30,40,50,100,150,200,500,1000,3000]
staleness_string = []
for s in staleness:
    staleness_string.append(str(s))