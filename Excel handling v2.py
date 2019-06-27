# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 11:10:10 2019

@author: Austin
"""

import os
import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats
from collections import OrderedDict

root = Tk()
root.withdraw()
root.fileName = filedialog.askdirectory()
parentfolder = root.fileName


#folder is the tissue folder
def histPlot(series, folder, strain, label):
    plt.figure()
    ax = plt.gca()
    index = series.last_valid_index()
    if index == 0:
        ax.hist(series[0], bins = 100)
    elif index == None:
        ax.hist([0], bins = 100)
    else:
        ax.hist(series[0:index], bins = 100)
    ax.set_ylabel('Count')
    ax.set_xlabel(label+' intensity (au)')
    ax.set_title(strain+' '+label+' distribution')
    if label == 'mTFP/mCherry':
        if 'D1' in series.name:
        label = 'pHLIP_D1'+series.name
    plt.savefig(folder+'/'+strain+'_'+label+'.png')
    plt.close()
    

def barPlot(D1, D10, folder, strain, label):
        D1_mean = np.mean(D1)
        D10_mean = np.mean(D10)
        try:
            D1_max = np.max(D1)
        except:
            D1_max = 0
        try:
            D10_max = np.max(D10)
        except:
            D10_max = 0
        D1_std = np.std(D1)
        D10_std = np.std(D10)
        
        categories = ['D1', 'D10']
        x_pos = np.arange(len(categories))
        values = [D1_mean, D10_mean]
        error = [D1_std, D10_std]
        
        #pHLIP values
        plt.figure()
        ax = plt.gca()
        ax.bar(x_pos, values, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel(label)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categories)
        ax.set_title(strain+' '+label)
        if 'AF' in D1.name:
            plt.savefig(folder+'/'+strain+'_AF'+'.png')
        elif 'old' in D1.name and 'mTFP/mCherry' in label:
            plt.savefig(folder+'/'+strain+'_pHLIP_old'+'.png')
        elif 'mTFP/mCherry' in label:
            plt.savefig(folder+'/'+strain+'_pHLIP'+'.png')
        plt.close()

#Processes mTFP and mCherry D1 and D10, returns mTFP/mCherry for D1 and D10
def dayTables(mTFP_D1, mTFP_D10, mCherry_D1, mCherry_D10):
    if len(mTFP_D1) == 0 or len(mCherry_D1) == 0:
        D1 = [0]
    else:
        D1 = mTFP_D1/mCherry_D1
    
    if len(mTFP_D10) == 0 or len(mCherry_D10) == 0:
        D10 = [0]
    else:
        D10 = mTFP_D10/mCherry_D10
    
    #Removes any inf or nan values
    D1 = [x for x in D1 if str(x) != 'nan']
    D1 = [x for x in D1 if x != np.float64('inf')]
    D10 = [x for x in D10 if str(x) != 'nan']
    D10 = [x for x in D10 if x != np.float64('inf')]
    
    #calculates needed values for plotting
#    D1 = np.array(D1)
#    D10 = np.array(D10)
    return D1, D10

#series = folders within the directory, files = files within the directory
#both are lists
homefolder, tissues, files = next(os.walk(root.fileName))
for tissue in tissues:
    tissuefolder, strains, files = next(os.walk(homefolder+'/'+tissue))
    for strain in strains:
        strainfolder, days, files = next(os.walk(tissuefolder+'/'+strain))
        
        #create arrays to compile the dataframes between worm counts
        mTFPD1_array = [] 
        mCherryD1_array = []
        mTFPD10_array = [] 
        mCherryD10_array = []
        AFD1_array = []
        AFD10_array = []
        mTFPoldD1_array = [] 
        mCherryoldD1_array = []
        mTFPoldD10_array = [] 
        mCherryoldD10_array = []

        #adds the individual dataframes from dif worms to the same array
        #adds the individual dataframes from dif worms to the same array
        for day in days:
            os.chdir(strainfolder+'/'+day)
            if day[0:day.index(' ')] == 'D1':
                mTFPD1_array.append(pd.read_csv('mTFP_D1.csv'))
                mCherryD1_array.append(pd.read_csv('mCherry_D1.csv'))
                mTFPoldD1_array.append(pd.read_csv('mTFPold_D1.csv'))
                mCherryoldD1_array.append(pd.read_csv('mCherryold_D1.csv'))
                AFD1_array.append(pd.read_csv('AF_D1.csv'))
                
            elif day[0:day.index(' ')] == 'D10':
                mTFPD10_array.append(pd.read_csv('mTFP_D10.csv'))
                mCherryD10_array.append(pd.read_csv('mCherry_D10.csv'))
                mTFPoldD10_array.append(pd.read_csv('mTFPold_D10.csv'))
                mCherryoldD10_array.append(pd.read_csv('mCherryold_D10.csv'))
                AFD10_array.append(pd.read_csv('AF_D10.csv'))   
        
        #concats all the dataframes from dif worms to each other
        mTFP_D1 = pd.concat(mTFPD1_array, ignore_index = True)
        mTFP_D10 = pd.concat(mTFPD10_array, ignore_index = True)
        mCherry_D1 = pd.concat(mCherryD1_array, ignore_index = True)
        mCherry_D10 = pd.concat(mCherryD10_array, ignore_index = True)
        mTFPold_D1 = pd.concat(mTFPoldD1_array, ignore_index = True)
        mTFPold_D10 = pd.concat(mTFPoldD10_array, ignore_index = True)
        mCherryold_D1 = pd.concat(mCherryoldD1_array, ignore_index = True)
        mCherryold_D10 = pd.concat(mCherryoldD10_array, ignore_index = True)
        AF_D1 = pd.concat(AFD1_array, ignore_index = True)
        AF_D10 = pd.concat(AFD10_array, ignore_index = True)

        #get mTFP/mCherry D1 and D10 
        D1, D10 = dayTables(mTFP_D1.Mean, mTFP_D10.Mean, mCherry_D1.Mean, mCherry_D10.Mean)
        D1_old, D10_old = dayTables(mTFPold_D1.Mean, mTFPold_D10.Mean, mCherryold_D1.Mean,
                                    mCherryold_D10.Mean)
        
        data = pd.DataFrame(OrderedDict ({'mTFP_D1': mTFP_D1.Mean, 'mCherry_D1': mCherry_D1.Mean, 
                             'mTFPold_D1': mTFPold_D1.Mean, 'mCherryold_D1': mCherryold_D1.Mean,
                             'mTFP_D10': mTFP_D10.Mean, 'mCherry_D10': mCherry_D10.Mean,
                             'mTFPold_D10': mTFPold_D10.Mean, 'mCherryold_D10': mCherryold_D10.Mean,
                             'AF_D1': AF_D1.Mean, 'AF_D10': AF_D10.Mean, 'D1': pd.Series(D1), 'D10': pd.Series(D10),
                             'D1_old': pd.Series(D1_old), 'D10_old': pd.Series(D10_old)}))
        writer = pd.ExcelWriter(strainfolder+'/Aggregate.xlsx', engine='xlsxwriter')
        data.to_excel(writer, sheet_name = 'Sheet1')
        writer.save()
        
        
        keys = data.keys()

        for key in keys:
            if (key != 'D1' or key != 'D10' or key != 'D10_old' or key != 'D1_old'):
                histPlot(data[key], homefolder+'/'+tissue, strain, key)
        #Plots the new settings
        barPlot(data['D1'], data['D10'], homefolder+'/'+tissue, strain, 'mTFP/mCherry')
        histPlot(data['D1'], homefolder+'/'+tissue, strain, 'mTFP/mCherry')
        histPlot(data['D10'], homefolder+'/'+tissue, strain, 'mTFP/mCherry')
        
        #Plots the old settings
        barPlot(data['D1_old'], data['D10_old'], homefolder+'/'+tissue, strain, 'mTFP/mCherry')
        histPlot(data['D1_old'], homefolder+'/'+tissue, strain, 'mTFP/mCherry')
        histPlot(data['D10_old'], homefolder+'/'+tissue, strain, 'mTFP/mCherry')
        
        #Plots AF channel
        barPlot(data['AF_D1'], data['AF_D10'], homefolder+'/'+tissue, strain, 'AF')