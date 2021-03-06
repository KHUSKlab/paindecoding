# msbak, 2019. 09. 02.
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 20:58:38 2019

@author: msbak
"""

import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import pickle
import os
import random
from scipy import stats
import scipy

def msMinMaxScaler(matrix1):
    matrix1 = np.array(matrix1)
    msmin = np.min(matrix1)
    msmax = np.max(matrix1)
    
    return (matrix1 - msmin) / (msmax-msmin)

def mslinear_regression(x,y):
    x = np.array(x); y = np.array(y); 
    x = x[np.isnan(x)==0]; y = y[np.isnan(y)==0]
    
    n = x.shape[0]
    r = (1/(n-1)) * np.sum(((x - np.mean(x))/np.std(x)) * ((y - np.mean(y))/np.std(y)))
    m = r*(np.std(y)/np.std(x))
    b = np.mean(y) - np.mean(x)*m

    return m, b # bx+a

shortlist = []; longlist = []
def msGrouping_nonexclude(msdata): 
    df3 = pd.concat([pd.DataFrame(msdata[salineGroup,0:4]) \
                                  ,pd.DataFrame(msdata[highGroup + highGroup2,0:4]) \
                                  ,pd.DataFrame(msdata[midleGroup,0:4]) \
                                  ,pd.DataFrame(msdata[ketoGroup,0:4]) \
                                  ,pd.DataFrame(msdata[lidocainGroup,0:4])] \
                                  ,ignore_index=True, axis=1)
    
    df3 = np.array(df3)
    return df3

def msGrouping_pslOnly(psl): # psl만 처리
    psldata = np.array(psl)
    
    df3 = pd.DataFrame(psldata[shamGroup,0:3]) 
    df3 = pd.concat([df3, pd.DataFrame(psldata[pslGroup,0:3]), \
                     pd.DataFrame(psldata[adenosineGroup,0:3])], ignore_index=True, axis = 1)
        
    df3 = np.array(df3)
    
    return df3

def msGrouping_yohimbine(msdata):
    msdata = np.array(msdata)
    df3 = np.array(pd.concat([pd.DataFrame(msdata[salineGroup,1:4]) \
                                  ,pd.DataFrame(msdata[yohimbineGroup,1:4])] \
                                  ,ignore_index=True, axis=1))
    df3 = np.array(df3)
    return df3


try:
    savepath = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\'; os.chdir(savepath)
    gsync = 'D:\\mscore\\syncbackup\\google_syn\\'
except:
    try:
        savepath = 'D:\\painDecorder\\save\\tensorData\\'; os.chdir(savepath);
    except:
        try:
            savepath = 'C:\\Users\\skklab\\Google 드라이브\\save\\tensorData\\'; os.chdir(savepath);
        except:
            savepath = ''; # os.chdir(savepath);
print('savepath', savepath)
#

# var import
with open(gsync + 'mspickle.pickle', 'rb') as f:  # Python 3: open(..., 'rb')
    msdata_load = pickle.load(f)
    
FPS = msdata_load['FPS']
N = msdata_load['N']
bahavss = msdata_load['bahavss']
behavss2 = msdata_load['behavss2']
msGroup = msdata_load['msGroup']
msdir = msdata_load['msdir']
signalss = msdata_load['signalss']
    
highGroup = msGroup['highGroup']
midleGroup = msGroup['midleGroup']
lowGroup = msGroup['lowGroup']
salineGroup = msGroup['salineGroup']
restrictionGroup = msGroup['restrictionGroup']
ketoGroup = msGroup['ketoGroup']
lidocainGroup = msGroup['lidocaineGroup']
capsaicinGroup = msGroup['capsaicinGroup']
yohimbineGroup = msGroup['yohimbineGroup']
pslGroup = msGroup['pslGroup']
shamGroup = msGroup['shamGroup']
adenosineGroup = msGroup['adenosineGroup']
highGroup2 = msGroup['highGroup2']
CFAgroup = msGroup['CFAgroup']
chloroquineGroup = msGroup['chloroquineGroup']
itSalineGroup = msGroup['itSalineGroup']
itClonidineGroup = msGroup['itClonidineGroup']
ipsaline_pslGroup = msGroup['ipsaline_pslGroup']
ipclonidineGroup = msGroup['ipclonidineGroup']
gabapentinGroup = msGroup['gabapentinGroup']

msset = msGroup['msset']
msset2 = msGroup['msset2']
del msGroup['msset']; del msGroup['msset2']
msset_total = np.array(pd.concat([pd.DataFrame(msset), pd.DataFrame(msset2)], ignore_index=True, axis=0))

skiplist = restrictionGroup + lowGroup

fset = highGroup + midleGroup + yohimbineGroup + ketoGroup + highGroup2 
se3set = capsaicinGroup + pslGroup + shamGroup + adenosineGroup + CFAgroup + chloroquineGroup
pslset = pslGroup + shamGroup + adenosineGroup

def msGrouping_pain_vs_itch(msdata): # psl만 처리
    msdata = np.array(msdata)
    
    df3 = pd.DataFrame(msdata[highGroup,1]) 
    df3 = pd.concat([df3, pd.DataFrame(msdata[chloroquineGroup,1:3])], ignore_index=True, axis = 1)
    df3 = np.array(df3)
    
    return df3

grouped_total_list = []
keylist = list(msGroup.keys())
for k in range(len(keylist)):
    grouped_total_list += msGroup[keylist[k]]

def msacc(class0, class1, mslabel='None', figsw=False, fontsz=15, fontloc="lower right", legendsw=True):
    pos_label = 1; roc_auc = -np.inf; fig = None
    while roc_auc < 0.5:
        class0 = np.array(class0); class1 = np.array(class1)
        class0 = class0[np.isnan(class0)==0]; class1 = class1[np.isnan(class1)==0]
        
        anstable = list(np.ones(class1.shape[0])) + list(np.zeros(class0.shape[0]))
        predictValue = np.array(list(class1)+list(class0)); predictAns = np.array(anstable)
        #            
        fpr, tpr, thresholds = metrics.roc_curve(predictAns, predictValue, pos_label=pos_label)
        
        maxix = np.argmax((1-fpr) * tpr)
        specificity = 1-fpr[maxix]; sensitivity = tpr[maxix]
        accuracy = ((class1.shape[0] * sensitivity) + (class0.shape[0]  * specificity)) / (class1.shape[0] + class0.shape[0])
        roc_auc = metrics.auc(fpr,tpr)
        
        if roc_auc < 0.5:
            pos_label = 0
            
    if figsw:
        sz = 0.9
        fig = plt.figure(1, figsize=(7*sz, 5*sz))
        lw = 2
        plt.plot(fpr, tpr, lw=lw, label = (mslabel + ' ' + str(round(roc_auc,2))), alpha=1)
        plt.plot([0, 1], [0, 1], lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        if legendsw:
            plt.legend(loc="lower right", prop={'size': fontsz})
            
    return roc_auc, accuracy, fig


def nanex(array1):
    array1 = np.array(array1)
    array1 = array1[np.isnan(array1)==0]
    return array1

def msGrouping_base_vs_itch(msdata): # psl만 처리
    msdata = np.array(msdata)
    
    df3 = pd.DataFrame(msdata[salineGroup,:]) 
    df3 = pd.concat([df3, pd.DataFrame(msdata[chloroquineGroup,0:3])], ignore_index=True, axis = 1)
    df3 = np.array(df3)
    return df3

# 제외된 mouse 확인용, mouseGroup
mouseGroup = []
for i in list(msGroup.keys()):
    mouseGroup += msGroup[i]
print('현재 grouping된 mouse #...', len(set(mouseGroup)), '/', str(N))
      
# long, short separate
#msshort = 42; mslong = 97; 
bins = 10

t4 = np.zeros((N,5)); movement = np.zeros((N,5))
for SE in range(N):
    for se in range(5):
        t4[SE,se] = np.mean(signalss[SE][se])
        movement[SE,se] = np.mean(bahavss[SE][se]>0) # binaryzation or not
        # 개별 thr로 relu 적용되어있음. frame은 signal과 syn가 다름
                    
        # In[] model1 load
if False:
    savepath = 'D:\\mscore\\syncbackup\\google_syn\\model1\\'               
    project_list = []

    project_list.append(['model1_roiroi_formalin_1', 100, None])

    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + '.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw3 = pickle.load(f)
                testsw3_mean[SE,:,ix] = testsw3[SE,:]
    model1 = np.nanmean(testsw3_mean, axis=2)
    

# In[] Formalin CV-- model2 (AI)
 
if True:
    savepath = 'D:\\mscore\\syncbackup\\google_syn\\model2\\'               
    project_list = []

    project_list.append(['foramlin_only_1', 100, None])
    project_list.append(['foramlin_only_2', 200, None]) 
    project_list.append(['foramlin_only_3', 300, None]) 
    project_list.append(['foramlin_only_4', 400, None])
    project_list.append(['foramlin_only_5', 500, None]) 
  
    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + '.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw3 = pickle.load(f)
                testsw3_mean[SE,:,ix] = testsw3[SE,:]
    model2 = np.nanmean(testsw3_mean, axis=2)
    
# In Formalin CV-- model2 - mean (AA)
 
if True:
    savepath = 'D:\\mscore\\syncbackup\\google_syn\\model2\\'               
    project_list = []

    project_list.append(['foramlin_only_1', 100, None])
    project_list.append(['foramlin_only_2', 200, None]) 
    project_list.append(['foramlin_only_3', 300, None]) 
    project_list.append(['foramlin_only_4', 400, None])
    project_list.append(['foramlin_only_5', 500, None]) 
  
    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + 'mean.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw3 = pickle.load(f)
                testsw3_mean[SE,:,ix] = testsw3[SE,:]
    model2_mean = np.nanmean(testsw3_mean, axis=2)
    
# In Formalin CV-- model2_roi_roi (II)
 
if True:
    savepath = 'D:\\mscore\\syncbackup\\google_syn\\model2-roi\\'               
    project_list = []

    project_list.append(['model2_roitraining_1', 100, None])

    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + '.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw3 = pickle.load(f)
                testsw3_mean[SE,:,ix] = testsw3[SE,:]
    model2roi_roi = np.nanmean(testsw3_mean, axis=2)
    
# In Formalin CV-- model2_roi_eman (IA)
 
if True:
    savepath = 'D:\\mscore\\syncbackup\\google_syn\\model2-roi\\'               
    project_list = []

    project_list.append(['model2_roitraining_1', 100, None])

    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + 'mean.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw3 = pickle.load(f)
                testsw3_mean[SE,:,ix] = testsw3[SE,:]
    model2roi_mean = np.nanmean(testsw3_mean, axis=2)  
                
    # In[] PSL용 load - model3
if True:
    t = 10
    testsw3_mean = np.zeros((N,5,t)); testsw3_mean[:] = np.nan         
    for i in range(t):
        path1 = 'D:\\mscore\\syncbackup\\google_syn\\model3\\'
        path2 = 'fset + baseonly + CFAgroup + capsaicinGroup_0.69_0415_t' + str(i) + '.h5'
        path3 = path1+ path2
        
        if os.path.isfile(path3):
            with open(path3, 'rb') as f:  # Python 3: open(..., 'rb')
                testsw3 = pickle.load(f)
                testsw3_mean[:testsw3.shape[0],:,i] = testsw3
    model3 = np.nanmean(testsw3_mean, axis=2)
    
    
        # In[] model4 load
if False:
    savepath = 'D:\\mscore\\syncbackup\\google_syn\\model4\\'               
    project_list = []

    project_list.append(['model4_roiroi_formalin_cap_cfa_1', 100, None])

    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + '.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw3 = pickle.load(f)
                testsw3_mean[SE,:,ix] = testsw3[SE,:]
    model4 = np.nanmean(testsw3_mean, axis=2)
    
        # In[] model5 load
if True:
    savepath = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\result\\'               
    project_list = []

    project_list.append(['model5_1', 100, None])

    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw5_mean = np.zeros((N,5,len(model_name))); testsw5_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + '.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw5 = pickle.load(f)
                testsw5_mean[SE,:,ix] = testsw5[SE,:]
    model5 = np.nanmean(testsw5_mean, axis=2)
   
# In[] raw test (구버전) - with model3
    
if True:
    thr = 0.5
    savepath = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\result\\0331_CFA_selection\\exp_raw\\'               
    project_list = range(10)

    model3_mean_overtime = []; [model3_mean_overtime.append([]) for u in range(N)]
    for i in range(N):
        [model3_mean_overtime[i].append([]) for u in range(5)]
        
    for SE in range(N):
        for se in range(5):
            matrixsave=[]
            for i in range(len(project_list)):
                loadpath_mean = savepath + 'PSL_result_' + str(SE) + '_' + str(project_list[i]) + '.pickle' 
                if os.path.isfile(loadpath_mean):
                    with open(loadpath_mean, 'rb') as f:  # Python 3: open(..., 'rb')
                        PSL_result_save = pickle.load(f)
                        
                    binum = len(PSL_result_save[SE][se])
                    if binum == 0: continue          
                    ROInum = len(PSL_result_save[SE][se][0])
                    
                    binROI_matrix = np.zeros((ROInum, binum)); binROI_matrix[:] = np.nan
                    
                    for col in range(binum):
                        for row in range(ROInum):
                            binROI_matrix[row,col] = PSL_result_save[SE][se][col][row][0][1]
                    matrixsave.append(np.array(binROI_matrix))
            matrixsave = np.array(matrixsave)
                            
            model3_mean_overtime[SE][se] = np.mean(matrixsave, axis=0)
            print(SE, se, model3_mean_overtime[SE][se].shape)

                        
    # heatmatplot
    
    nonpains2 = []
    nonpains2.append(np.mean(model3_mean_overtime[167][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[168][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[173][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[173][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[75][0] > thr, axis=0)[:55]) # 5
    nonpains2.append(np.mean(model3_mean_overtime[76][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[85][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[87][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[88][0] > thr, axis=0)[:55])
    nonpains2.append(np.mean(model3_mean_overtime[94][1] > thr, axis=0)[:55]) # 10
    nonpains2 = np.array(nonpains2)
    
    pains = []
    pains.append(np.mean(model3_mean_overtime[71][1] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[72][2] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[73][1] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[73][2] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[75][1] > thr, axis=0)) # 5
    pains.append(np.mean(model3_mean_overtime[76][1] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[85][2] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[87][1] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[88][1] > thr, axis=0))
    pains.append(np.mean(model3_mean_overtime[94][1] > thr, axis=0)) # 10
    pains = np.array(pains)[:,:55]
    
    nonpains = []
    nonpains.append(np.mean(model3_mean_overtime[167][2] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[168][2] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[172][2] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[173][2] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[174][2] > thr, axis=0)) # 5
    nonpains.append(np.mean(model3_mean_overtime[175][2] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[177][1] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[178][1] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[179][1] > thr, axis=0))
    nonpains.append(np.mean(model3_mean_overtime[180][1] > thr, axis=0)) # 10
    nonpains = np.array(nonpains)[:,:55]
    
    inter = np.ones((1,55))
    msplot = np.concatenate((nonpains2, inter, pains, inter, nonpains), axis=0) 
    
    plt.imshow(msplot, cmap='hot')
    
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)
    
    plt.colorbar()

# In[] label 재정렬 movement 
t4 = np.zeros((N,5)); movement = np.zeros((N,5))
for SE in range(N):
    for se in range(5):
        t4[SE,se] = np.mean(signalss[SE][se])
        movement[SE,se] = np.mean(bahavss[SE][se]>0) # binaryzation or not
    
target = np.array(movement)
for SE in range(N):
    if SE in [141,142,143]:
        target[SE,1:3] = target[SE,3:5] 
        target[SE,1:3] = np.nan
        
    if SE in [146,149,158,159]:
        target[SE,3:] = np.nan

movement = target     
movement_filter = np.array(movement)
        
# In[]
# target = np.array(model3); fsw=True
def dict_gen(target, msset=None, legendsw=None):
    if msset is None:
        print('set mssset')
        pass
    
    target = np.array(target)
    print(target.shape, movement_filter.shape)
    
    if msset in ['psl'] and False:
        print('movement > 0.5 filter')
        ix = np.where(movement_filter[:,0] > 0.5)[0]
        target[ix,:] = np.nan
        
    # subset 평균처리        
    subset_mean = np.zeros((N,5)); subset_mean[:] = np.nan
    for SE in range(N):
        if SE in np.array(msset_total)[:,0]:
            settmp = np.array(msset_total)[np.where(np.array(msset_total)[:,0]==SE)[0][0],:]
            subset_mean[SE,:] = np.nanmean(target[settmp,:],axis=0)
    #        print('set averaging', settmp)
        elif SE not in np.array(msset_total).flatten(): 
            subset_mean[SE,:] = target[SE,:]
            
    for SE in range(N):
        if SE in [141,142,143]:
            subset_mean[SE,3:5] = subset_mean[SE,1:3]
            subset_mean[SE,1:3] = np.nan
    
    # grouping
    high0 = nanex(subset_mean[highGroup+highGroup2,0])
    high1 = nanex(subset_mean[highGroup+highGroup2,1])
    
    midle0 = nanex(subset_mean[midleGroup,0])
    midle1 = nanex(subset_mean[midleGroup,1])
    
    keto0 = nanex(subset_mean[ketoGroup,0])
    keto1 = nanex(subset_mean[ketoGroup,1])
    
    lido0 = nanex(subset_mean[lidocainGroup,0])
    lido1 = nanex(subset_mean[lidocainGroup,1])
    
    saline0 = nanex(subset_mean[salineGroup,0])
    saline1 = nanex(subset_mean[salineGroup,1])
    
    cap0 = nanex(subset_mean[capsaicinGroup,0])
    cap1 = nanex(subset_mean[capsaicinGroup,1])
    
    CFA0 = nanex(subset_mean[CFAgroup,0])
    CFA1 = nanex(subset_mean[CFAgroup,1])
    CFA2 = nanex(subset_mean[CFAgroup,2])
    
    sham0 = nanex(subset_mean[shamGroup,0])
    sham1 = nanex(subset_mean[shamGroup,1])
    sham2 = nanex(subset_mean[shamGroup,2])
           
    psl0 = nanex(subset_mean[pslGroup,0])
    psl1 = nanex(subset_mean[pslGroup,1])
    psl2 = nanex(subset_mean[pslGroup,2])
    
    
#    ipsaline_pslGroup
    
    ipsaline0 = nanex(subset_mean[ipsaline_pslGroup,0])
    ipsaline1 = nanex(subset_mean[ipsaline_pslGroup,1])
    ipsaline2 = nanex(subset_mean[ipsaline_pslGroup,2])
    ipsaline3 = nanex(subset_mean[ipsaline_pslGroup,3])
    ipsaline4 = nanex(subset_mean[ipsaline_pslGroup,4])
    
    ipclonidine0 = nanex(subset_mean[ipclonidineGroup,0])
    ipclonidine1 = nanex(subset_mean[ipclonidineGroup,1])
    ipclonidine2 = nanex(subset_mean[ipclonidineGroup,2])
    ipclonidine3 = nanex(subset_mean[ipclonidineGroup,3])
    ipclonidine4 = nanex(subset_mean[ipclonidineGroup,4])

    
    gaba120_0 = nanex(np.mean(subset_mean[[164,165,166],0:2], axis=1))
    gaba120_1 = nanex(subset_mean[[177,179],2]) # psl_d3, GB/VX_i.p._120m 
    gaba120_2 = nanex(np.mean(subset_mean[[164,165,166],2:4], axis=1)) # psl_d10, GB/VX_i.p._120m 
    
    
    gaba30_0 = nanex(subset_mean[[167,168,172,174,177,179,182], 0])
    gaba30_0 = np.concatenate((gaba30_0, [np.nanmean(subset_mean[181,0:2])]), axis=0)
    add = np.mean(subset_mean[[185,186],0:2], axis=1)
    gaba30_0 = np.concatenate((gaba30_0, add), axis=0)     
    
    gaba30_1 = nanex(subset_mean[[167,168], 1]) # GB/VX (d3)
    gaba30_1 = np.concatenate((gaba30_1, nanex(subset_mean[[172,174], 2])), axis=0)  # GB/VX (d3)
    gaba30_1 = np.concatenate((gaba30_1, nanex(subset_mean[[177,179], 1])), axis=0)  # GB/VX (d3)
    add = np.nanmean(subset_mean[181, [2,3]])
    gaba30_1 = np.concatenate((gaba30_1, [add]), axis=0)
    add = np.nanmean(subset_mean[182, [1,2]])
    gaba30_1 = np.concatenate((gaba30_1, [add]), axis=0)
    
    
    gaba30_2 = nanex(subset_mean[[167,168], 2]) # lidocaine (d2)
    gaba30_2 = np.concatenate((gaba30_2, nanex(subset_mean[[172,174], 3])), axis=0)  # lidocaine (d2)
    
    gaba30_3 = nanex(np.mean(subset_mean[[169,170,171],0:2], axis=1)) # GB/VX (d10~)
    gaba30_3 = np.concatenate((gaba30_3, [np.mean(subset_mean[176,0:2])]), axis=0) 
    add = np.mean(subset_mean[[183,184],0:2], axis=1)
    gaba30_3 = np.concatenate((gaba30_3, add), axis=0)
    add = np.mean(subset_mean[[185,186],2:4], axis=1)
    gaba30_3 = np.concatenate((gaba30_3, add), axis=0) 
    
    gaba30_4 = nanex(np.mean(subset_mean[[169,170,171],2:4], axis=1)) # lidocaine (d10~)
    
    scsalcine = nanex(subset_mean[[172,174], 1])
    
    itsaline0 = nanex(subset_mean[itSalineGroup,0])
    itsaline1 = nanex(subset_mean[itSalineGroup,1])
    itsaline2 = nanex(subset_mean[itSalineGroup,2])
    
    itclonidine0 = nanex(subset_mean[itClonidineGroup,0])
    itclonidine1 = nanex(subset_mean[itClonidineGroup,1])
    itclonidine2 = nanex(subset_mean[itClonidineGroup,2])
    

    if msset == 'formalin':
        name=''
        pain = np.concatenate((high1, midle1), axis=0)
        nonpain = np.concatenate((high0, midle0, saline0, saline1), axis=0)
        roc_auc, _, _ = msacc(nonpain, pain, mslabel= name + ', AUC:', figsw=True, legendsw=legendsw)
        
        base_merge = np.concatenate((saline0, saline1), axis=0)
        Aprism = pd.concat([pd.DataFrame(base_merge), pd.DataFrame(high0), pd.DataFrame(high1) \
                                       , pd.DataFrame(midle0), pd.DataFrame(midle1) \
                                       , pd.DataFrame(keto0), pd.DataFrame(keto1)
                                       , pd.DataFrame(lido0), pd.DataFrame(lido1)] \
                                       , ignore_index=True, axis=1)
        
    elif msset == 'capcfa':
        base_merge = np.concatenate((saline0, saline1), axis=0)
        name=''
        pain = np.concatenate((cap1, CFA1, CFA2), axis=0)
        nonpain = base_merge
        roc_auc, _, _ = msacc(nonpain, pain, mslabel= name + ', AUC:', figsw=True, legendsw=legendsw)
        
        Aprism = pd.concat([pd.DataFrame(base_merge), pd.DataFrame(cap1), pd.DataFrame(CFA1) \
                                       , pd.DataFrame(CFA2)], ignore_index=True, axis=1)
        
    elif msset == 'psl':
        name=''
        pain = np.concatenate((psl1, psl2), axis=0)
        nonpain = np.concatenate((psl0, sham0, sham1, sham2), axis=0)
        roc_auc, _, _ = msacc(nonpain, pain, mslabel= name + ', AUC:', figsw=True, legendsw=legendsw)
        
        base_merge = np.concatenate((sham0, psl0, ipsaline0, ipclonidine0), axis=0)
        psl3_merge = np.concatenate((psl1, ipsaline1, ipclonidine1), axis=0)
        psl10_merge = np.concatenate((psl2, ipsaline3, ipclonidine3), axis=0)

        Aprism = [[], [], [], []]
        
        # base, sham, psl
        Aprism[0] = pd.concat([pd.DataFrame(base_merge), pd.DataFrame(sham1), pd.DataFrame(psl3_merge), \
                            pd.DataFrame(sham2), pd.DataFrame(psl10_merge)], \
                            ignore_index=True, axis=1)
        
        # psl+ipsaline, psl+ipclonidine, psl+ipGB/VX
        base_merge = np.concatenate((ipsaline0, ipclonidine0, gaba120_0, gaba30_0), axis=0)
        Aprism[1] = pd.concat([pd.DataFrame(base_merge), pd.DataFrame(ipsaline2), pd.DataFrame(ipsaline4), pd.DataFrame(ipclonidine2), \
                    pd.DataFrame(ipclonidine4), pd.DataFrame(gaba120_1), pd.DataFrame(gaba30_1), pd.DataFrame(gaba30_3), pd.DataFrame(gaba30_2), \
                    pd.DataFrame(gaba30_4), pd.DataFrame(scsalcine)], \
                    ignore_index=True, axis=1)
        
        # psl+itsaline, psl+itclonidine
        base_merge = np.concatenate((itsaline0, itclonidine0), axis=0)
        Aprism[2] = pd.concat([pd.DataFrame(base_merge), pd.DataFrame(itsaline1), pd.DataFrame(itclonidine1), \
              pd.DataFrame(itsaline2), pd.DataFrame(itclonidine2)],ignore_index=True, axis=1)
        
        # base, sham, psl(psl+ipsaline), psl+GB/VX
        base_merge = np.concatenate((sham0, psl0, ipsaline0, gaba30_0, gaba120_0), axis=0)
  
        Aprism[3] = pd.concat([pd.DataFrame(base_merge), \
              pd.DataFrame(sham1), pd.DataFrame(psl3_merge), pd.DataFrame(gaba30_1), pd.DataFrame(gaba120_1), \
              pd.DataFrame(sham2), pd.DataFrame(psl10_merge), pd.DataFrame(gaba30_3), pd.DataFrame(gaba120_2)],ignore_index=True, axis=1)
        

    return Aprism

# In[]

#model1_dict = dict_gen(model1)
#model3_dict = dict_gen(model3)
#model4_dict = dict_gen(model4)

#fsw=True
#model2_dict = dict_gen(model2)
#model2mean_dict = dict_gen(model2_mean)
#model2roi_roi_dict = dict_gen(model2roi_roi)
#model2roi_mean_dict = dict_gen(model2roi_mean)

#### formalin pain
legendsw = True
if False:
    Aprism_foramlin_pain = dict_gen(model2, msset='formalin', legendsw=True)
    _ = dict_gen(model2_mean, msset='formalin', legendsw=True)
    _ = dict_gen(model2roi_roi, msset='formalin', legendsw=True)
    _ = dict_gen(model2roi_mean, msset='formalin', legendsw=True)
    
    # formalin movement
    Aprism_foramlin_movement = dict_gen(movement, msset='formalin', legendsw=True)
    
    # capcfa pain
    Aprism_capcfa_pain = dict_gen(model2, msset='capcfa', legendsw=legendsw)
    _ = dict_gen(model2_mean, msset='capcfa', legendsw=legendsw)
    _ = dict_gen(model2roi_roi, msset='capcfa', legendsw=legendsw)
    _ = dict_gen(model2roi_mean, msset='capcfa', legendsw=legendsw)
#    _ = dict_gen(model5, msset='capcfa', legendsw=legendsw)
    savepath2 = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\psl_visualization\\'
    plt.savefig(savepath2 + 'capcfa_roc', dpi=1000)#
    
    # capcfa movement
    Aprism_capcfa_movement = dict_gen(movement, msset='capcfa', legendsw=True)


legendsw = True
Aprism_psl_pain = dict_gen(model2, msset='psl', legendsw=legendsw)
_ = dict_gen(model2_mean, msset='psl', legendsw=legendsw)
_ = dict_gen(model2roi_roi, msset='psl', legendsw=legendsw)
_ = dict_gen(model2roi_mean, msset='psl', legendsw=legendsw)
savepath2 = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\psl_visualization\\'
plt.savefig(savepath2 + 'psl_roc', dpi=1000)#

_ = dict_gen(model2, msset='psl', legendsw=legendsw)
_ = dict_gen(model5, msset='psl', legendsw=legendsw)
Aprism_psl_pain3 = dict_gen(model3, msset='psl', legendsw=legendsw)
plt.savefig(savepath2 + 'psl_roc_models', dpi=1000)#

# psl movement
legendsw = True
Aprism_psl_movement = dict_gen(movement, msset='capcfa', legendsw=legendsw)
#Aprism_psl_movement = dict_gen(movement, msset='psl', legendsw=True)
savepath2 = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\psl_visualization\\'
plt.savefig(savepath2 + 'capcfa_movement_roc', dpi=1000)#

legendsw = True
_ = dict_gen(model5, msset='psl', legendsw=legendsw)
_ = dict_gen(model5, msset='capcfa', legendsw=True)
# In[]
import os
os.sys.exit()

# In[]
# In[] cerebellum _ capsaicin
picklesavename = 'D:\\mscore\\syncbackup\\paindecoder\\save\\tensorData\\msGroup_ksh_bRNN.pickle'
with open(picklesavename, 'rb') as f:  # Python 3: open(..., 'wb')
    cerebellum_capsaicin = pickle.load(f)
    
pain = cerebellum_capsaicin[:7,1]
nonpain = np.concatenate((cerebellum_capsaicin[7:,:].flatten(), cerebellum_capsaicin[:7,0], cerebellum_capsaicin[:7,2]),axis=0)
roc_auc, _, _ = msacc(nonpain, pain, mslabel='AUC:', figsw=True)
plt.savefig(savepath2 + 'cerebellum_ROC.png', dpi=1000)


# In[] itch vs non-itch
if True:
    savepath = 'D:\\mscore\\syncbackup\\save\\tensorData\\result\\'    
    project_list = []

    project_list.append(['20200308_itch_vs_before', 111, None])
    project_list.append(['20200308_itch_vs_before2', 222, None])
    project_list.append(['20200308_itch_vs_before3', 333, None])

    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    for ix, p in enumerate(model_name):
        for SE in range(N):
            
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'testsw3_' + str(SE) + '.pickle'
            if os.path.isfile(loadpath5):
                with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                    testsw3 = pickle.load(f)
                testsw3_mean[SE,:,ix] = testsw3[SE,:]
    model_itch_vs_nonitch = np.nanmean(testsw3_mean, axis=2)
    
    pain = model_itch_vs_nonitch[chloroquineGroup,1]
    
    tmp1 = model_itch_vs_nonitch[chloroquineGroup,0]
    tmp2 = model_itch_vs_nonitch[salineGroup,1].flatten()
    nonpain = np.concatenate((tmp1, tmp2), axis=0)
    
#    nonpain = np.array(model_itch_vs_nonitch[chloroquineGroup,0])

    roc_auc, _, _ = msacc(nonpain, pain, mslabel='AUC:', figsw=True)
    
    # saline inter를 사용할이유가?
    # saline을 모두 빼고, ROC 및 본 그래프 수정


    
# In[] itch vs pain
if False:
    savepath = 'D:\\mscore\\syncbackup\\save\\tensorData\\result\\'    
    project_list = []

    project_list.append(['20200302_painitch_1', 100, None])
    project_list.append(['20200302_painitch_2', 200, None]) 
    project_list.append(['20200302_painitch_3', 300, None]) # acc_thr 증가
    project_list.append(['20200302_painitch_4', 400, None])

    model_name2 = project_list 
                 
    model_name = np.array(model_name2)
    testsw3_mean = np.zeros((N,5,len(model_name))); testsw3_mean[:] = np.nan
    

    ## 
    for ix, p in enumerate(model_name):
        for SE in range(N):          
            loadpath5 = savepath + p[0] + '\\exp_raw\\' + 'PSL_result_' + str(SE) + '.pickle'
            if os.path.isfile(loadpath5):
                sessionNum = 5
    
                for se in range(sessionNum):
                    with open(loadpath5, 'rb') as f:  # Python 3: open(..., 'rb')
                        PSL_result_save = pickle.load(f)
                    PSL_result_save2 = np.array(PSL_result_save[SE][se]) # [BINS][ROI][bins] # BINS , full length 넘어갈때, # bins는 full length 안에서
                    if type(PSL_result_save2) == np.ndarray:
                        if len(PSL_result_save2) != 0:
                            testsw3_mean[SE,se,i] = np.nanmean(PSL_result_save2[:,:,:,1])
                            if np.isnan(np.mean(PSL_result_save2[:,:,:,1])):
                                print('nan')
        model_itch_vs_pain = np.nanmean(testsw3_mean, axis=2)
        
        a1 = model_itch_vs_pain[highGroup,1]
        model_itch_vs_pain[highGroup2,1]
        a2 = model_itch_vs_pain[chloroquineGroup,1]           
        
    # rawdata 직접 load
if True:
    loadpath = 'D:\\mscore\\syncbackup\\save\\tensorData\\result\\20200302_painitch_1\\rawdata.xlsx'
    df1 = np.array(pd.read_excel(loadpath))
        
    pain = df1[:,0]
    nonpain = df1[:,1]
    roc_auc, _, _ = msacc(nonpain, pain, mslabel='', figsw=True)
    plt.savefig(savepath2 + 'itch_vs_pain_ROC.png', dpi=1000)


legendsw = True

pain = cerebellum_capsaicin[:7,1]
nonpain = np.concatenate((cerebellum_capsaicin[7:,:].flatten(), cerebellum_capsaicin[:7,0], cerebellum_capsaicin[:7,2]),axis=0)
roc_auc, _, _ = msacc(nonpain, pain, mslabel='Cerebellum, pain vs non-pain, AUC:', \
                      figsw=True, fontsz=12, fontloc="lower right", legendsw=legendsw)

pain = model_itch_vs_nonitch[chloroquineGroup,1]
nonpain = np.concatenate((model_itch_vs_nonitch[salineGroup,:2].flatten(), model_itch_vs_nonitch[chloroquineGroup,0]),axis=0)
roc_auc, _, _ = msacc(nonpain, pain, mslabel='S1, itch vs non-itch, AUC:', \
                      figsw=True, fontsz=12, fontloc="lower right", legendsw=legendsw)

# itch vs pain
pain = df1[:,0]
nonpain = df1[:,1]
roc_auc, _, _ = msacc(nonpain, pain, mslabel='S1, itch vs pain, AUC:', \
                      figsw=True, fontsz=12, fontloc="lower right", legendsw=legendsw)

plt.savefig(savepath2 + 'etc_ROC_HR.png', dpi=1000)









