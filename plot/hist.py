#!/usr/bin/env python
import sys
import numpy as np
import matplotlib
import pylab
import random
from optparse import OptionParser

from matplotlib import rcParams
rcParams['font.family'] = 'Arial'

parser = OptionParser()

parser.add_option("-t",
                  "--title",
                  dest="title",
                  help="Title")

parser.add_option("-x",
                  "--xlabel",
                  dest="xlabel",
                  help="X axis label")

parser.add_option("-y",
                  "--ylabel",
                  dest="ylabel",
                  help="Y axis label")

parser.add_option("-o",
                  "--output_file",
                  dest="output_file",
                  help="Data file")

parser.add_option("-b",
                  "--bins",
                  dest="bins",
                  type="int",
                  default=10,
                  help="Number of fins")

parser.add_option("--x_max",
                  dest="max_x",
                  type="float",
                  help="Max x value")


parser.add_option("--x_min",
                  dest="min_x",
                  type="float",
                  help="Min x value")

parser.add_option("--y_max",
                  dest="max_y",
                  type="float",
                  help="Max y value")


parser.add_option("--y_min",
                  dest="min_y",
                  type="float",
                  help="Min y value")


parser.add_option("-c",
                  "--column",
                  dest="col",
                  type="int",
                  default="0",
                  help="Column in the data")

parser.add_option("-d",
                  "--delim",
                  dest="delim",
                  default="\t",
                  help="Field delimiter")

parser.add_option("-l",
                  "--ylog",
                  action="store_true",default=False,
                  dest="ylog",
                  help="Field delimiter")

parser.add_option("--x_sci",
                  action="store_true",default=False,
                  dest="x_sci",
                  help="Use scientific notation for x-axis")

parser.add_option("--y_sci",
                  action="store_true",default=False,
                  dest="y_sci",
                  help="Use scientific notation for y-axis")

parser.add_option("--width",
                  dest="width",
                  type="int",
                  default=5,
                  help="Figure width")

parser.add_option("--height",
                  dest="height",
                  type="int",
                  default=5,
                  help="Figure height")

parser.add_option("--black",
                  action="store_true", 
                  default=False,
                  dest="black",
                  help="black background")



(options, args) = parser.parse_args()
if not options.output_file:
    parser.error('Output file not given')

Y=[]
for l in sys.stdin:
    a = l.rstrip().split(options.delim)
    if len(a) == 1:
        if len(a[options.col]) != 0 :
            Y.append(float(a[options.col]))

matplotlib.rcParams.update({'font.size': 12})
#fig = matplotlib.pyplot.figure(figsize=(10,5),dpi=300)

#fig = matplotlib.pyplot.figure(figsize=(options.width,options.height),dpi=300)

if options.black:
    fig = matplotlib.pyplot.figure(\
            figsize=(options.width,options.height),\
            dpi=300,\
            facecolor='black')
else:
    fig = matplotlib.pyplot.figure(\
            figsize=(options.width,options.height),\
            dpi=300)



fig.subplots_adjust(wspace=.05,left=.01,bottom=.01)

x_max = max(Y)
x_min = min(Y)

if options.max_x:
    x_max = options.max_x
if options.min_x:
    x_min = options.min_x

#ax = fig.add_subplot(1,1,1)
if options.black:
    ax = fig.add_subplot(1,1,1,axisbg='k')
else:
    ax = fig.add_subplot(1,1,1)



ax.hist(Y,options.bins,log=options.ylog,align='mid',\
        histtype='bar', rwidth=1)

if options.max_x:
    ax.set_xlim(xmax=options.max_x)
if options.min_x:
    ax.set_xlim(xmin=options.min_x)
if options.max_y:
    ax.set_ylim(ymax=options.max_y)
if options.min_y:
    ax.set_ylim(ymin=options.min_y)

#ax.set_ylim([0,10])

if options.x_sci:
    formatter = matplotlib.ticker.ScalarFormatter()
    formatter.set_powerlimits((-2,2))
    ax.xaxis.set_major_formatter(formatter)

if options.y_sci:
    formatter = matplotlib.ticker.ScalarFormatter()
    formatter.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(formatter)


    #ax.plot(range(len(Y)),Y,options.line_style,color='black', linewidth=1)
#else:
    #ax.plot(X,Y,options.line_style,color='black', linewidth=1)

#if options.logy:
    #ax.set_yscale('log')

#if ((options.max_y) and (options.min_y)):
    #ax.set_ylim(float(options.min_y),float(options.max_y))

#if len(X) != 0:
    #ax.set_xticks([float(x) for x in X])
    #ax.set_xticklabels

if options.xlabel:
    ax.set_xlabel(options.xlabel)

if options.ylabel:
    ax.set_ylabel(options.ylabel)

if options.title:
    ax.set_title(options.title)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

if options.black:
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.title.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')



#matplotlib.pyplot.savefig(options.output_file,bbox_inches='tight')
if options.black:
    matplotlib.pyplot.savefig(options.output_file,bbox_inches='tight',\
            facecolor=fig.get_facecolor(),\
              transparent=True)
else:
    matplotlib.pyplot.savefig(options.output_file,bbox_inches='tight')
