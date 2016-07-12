#! /usr/bin/env python
import ROOT as rt
import os.path
import sys, glob, re
from array import *
from optparse import OptionParser

def getThyXsecDict():    
    thyXsecDict = {}
    xsecFiles = ['data/all_lowmass_lhc13TeV.txt','data/rsg_gg_lhc13TeV.txt','data/S8_13TeV_narrow.txt','data/string_total_13TeV.txt','data/axi_lhc13TeV_NLO.txt']
    
    for xsecFile in xsecFiles:
        moreThyModels = []
        f = open(xsecFile)
        for i,line in enumerate(f.readlines()):
            if line[0]=='#': continue
            line = line.replace('\n','')
            line = line.replace('\t','')
            line = line.replace('\r','')
            lineList = [l for l in line.split(" ") if l!='']
            
            if lineList[0]=='Mass':
                for l in lineList:
                    if l=='Mass': continue
                    thyXsecDict[l] = {}
                    moreThyModels.append(l)
            else:
                for j, thyModel in enumerate(moreThyModels):
                    thyXsecDict[thyModel][int(float(lineList[0]))] = float(lineList[j+1])
        f.close()

        thyXsecDict['AxigluonkNLO'] = {}
        for (mass,thyXsec) in thyXsecDict['Axigluon'].iteritems():
            thyXsecDict['AxigluonkNLO'][mass] = 1.08 * thyXsec
            
    return thyXsecDict


def file_key(filename):
    massPoint = re.findall("[0-9]+.000000",filename)
    gluinoMass    = massPoint[0]
    LSPMass  = massPoint[1]
    return float(gluinoMass)
    
def getHybridCLsArrays(directory, model, Box, bayes):
    if bayes:
        tfile = rt.TFile.Open("%s/xsecUL_MarkovChainMC_%s_%s.root"%(directory,model,Box))
    else:
        tfile = rt.TFile.Open("%s/xsecUL_Asymptotic_%s_%s.root"%(directory,model,Box))
    xsecTree = tfile.Get("xsecTree")
    
    gluinoMassArray = array('d')
    gluinoMassArray_er = array('d')
    observedLimit = array('d')
    observedLimit_er = array('d')
    expectedLimit = array('d')
    expectedLimit_minus1sigma = array('d')
    expectedLimit_plus1sigma = array('d')
    expectedLimit_minus2sigma = array('d')
    expectedLimit_plus2sigma = array('d')

    
    xsecTree.Draw('>>elist','','entrylist')
    elist = rt.gDirectory.Get('elist')
    entry = -1
    while True:
        entry = elist.Next()
        if entry == -1: break
        xsecTree.GetEntry(entry)

        gluinoMassArray.append(xsecTree.mass)
        gluinoMassArray_er.append(0.0)
        
        exec 'xsecULObs = xsecTree.xsecULObs_%s'%Box
        exec 'xsecULExp = xsecTree.xsecULExp_%s'%Box
        exec 'xsecULExpPlus = xsecTree.xsecULExpPlus_%s'%Box
        exec 'xsecULExpMinus = xsecTree.xsecULExpMinus_%s'%Box
        exec 'xsecULExpPlus2 = xsecTree.xsecULExpPlus2_%s'%Box
        exec 'xsecULExpMinus2 = xsecTree.xsecULExpMinus2_%s'%Box

            
            
        xsecULObs = xsecULObs
        xsecULExp = xsecULExp
        observedLimit.append(xsecULObs)#*crossSections[i])
        observedLimit_er.append(0.0)#*crossSections[i])

        expectedLimit.append(xsecULExp)#*crossSections[i])
        
            

        xsecULExpPlus = max(xsecULExpPlus,xsecULExp)
        xsecULExpMinus = min(xsecULExpMinus,xsecULExp)
        xsecULExpPlus2 = max(xsecULExpPlus2,xsecULExpPlus)
        xsecULExpMinus2 = min(xsecULExpMinus2,xsecULExpMinus)

        expectedLimit_minus1sigma.append(xsecULExp - xsecULExpMinus)#*crossSections[i])
        expectedLimit_plus1sigma.append(xsecULExpPlus - xsecULExp)#*crossSections[i])
        expectedLimit_minus2sigma.append(xsecULExp - xsecULExpMinus2)#*crossSections[i])
        expectedLimit_plus2sigma.append(xsecULExpPlus2 - xsecULExp)#*crossSections[i])
    

    return gluinoMassArray, gluinoMassArray_er, observedLimit, observedLimit_er, expectedLimit, expectedLimit_minus1sigma, expectedLimit_plus1sigma, expectedLimit_minus2sigma, expectedLimit_plus2sigma


def getSignificanceArrays(directory, model, Box):
    tfile = rt.TFile.Open("%s/xsecUL_ProfileLikelihood_%s_%s.root"%(directory,model,Box))
    xsecTree = tfile.Get("xsecTree")
    
    gluinoMassArray = array('d')
    gluinoMassArray_er = array('d')
    observedLimit = array('d')
    observedLimit_er = array('d')
    expectedLimit = array('d')
    expectedLimit_minus1sigma = array('d')
    expectedLimit_plus1sigma = array('d')
    expectedLimit_minus2sigma = array('d')
    expectedLimit_plus2sigma = array('d')

    
    xsecTree.Draw('>>elist','','entrylist')
    elist = rt.gDirectory.Get('elist')
    entry = -1
    while True:
        entry = elist.Next()
        if entry == -1: break
        xsecTree.GetEntry(entry)

        gluinoMassArray.append(xsecTree.mass)
        gluinoMassArray_er.append(0.0)
        
        exec 'xsecULObs = xsecTree.xsecULObs_%s'%Box
        exec 'xsecULExp = xsecTree.xsecULExp_%s'%Box
        exec 'xsecULExpPlus = xsecTree.xsecULExpPlus_%s'%Box
        exec 'xsecULExpMinus = xsecTree.xsecULExpMinus_%s'%Box
        exec 'xsecULExpPlus2 = xsecTree.xsecULExpPlus2_%s'%Box
        exec 'xsecULExpMinus2 = xsecTree.xsecULExpMinus2_%s'%Box

            
            
        xsecULObs = xsecULObs
        xsecULExp = xsecULExp
        observedLimit.append(xsecULObs)#*crossSections[i])
        observedLimit_er.append(0.0)#*crossSections[i])

        expectedLimit.append(xsecULExp)#*crossSections[i])
        
            

        xsecULExpPlus = max(xsecULExpPlus,xsecULExp)
        xsecULExpMinus = min(xsecULExpMinus,xsecULExp)
        xsecULExpPlus2 = max(xsecULExpPlus2,xsecULExpPlus)
        xsecULExpMinus2 = min(xsecULExpMinus2,xsecULExpMinus)

        expectedLimit_minus1sigma.append(xsecULExp - xsecULExpMinus)#*crossSections[i])
        expectedLimit_plus1sigma.append(xsecULExpPlus - xsecULExp)#*crossSections[i])
        expectedLimit_minus2sigma.append(xsecULExp - xsecULExpMinus2)#*crossSections[i])
        expectedLimit_plus2sigma.append(xsecULExpPlus2 - xsecULExp)#*crossSections[i])
    

    return gluinoMassArray, gluinoMassArray_er, observedLimit, observedLimit_er, expectedLimit, expectedLimit_minus1sigma, expectedLimit_plus1sigma, expectedLimit_minus2sigma, expectedLimit_plus2sigma
    
def setstyle():
    # For the canvas:
    rt.gStyle.SetCanvasBorderMode(0)
    rt.gStyle.SetCanvasColor(rt.kWhite)
    rt.gStyle.SetCanvasDefH(400) #Height of canvas
    rt.gStyle.SetCanvasDefW(600) #Width of canvas
    rt.gStyle.SetCanvasDefX(0)   #POsition on screen
    rt.gStyle.SetCanvasDefY(0)
    
    # For the Pad:
    rt.gStyle.SetPadBorderMode(0)
    # rt.gStyle.SetPadBorderSize(Width_t size = 1)
    rt.gStyle.SetPadColor(rt.kWhite)
    rt.gStyle.SetPadGridX(False)
    rt.gStyle.SetPadGridY(False)
    rt.gStyle.SetGridColor(0)
    rt.gStyle.SetGridStyle(3)
    rt.gStyle.SetGridWidth(1)
    
    # For the frame:
    rt.gStyle.SetFrameBorderMode(0)
    rt.gStyle.SetFrameBorderSize(1)
    rt.gStyle.SetFrameFillColor(0)
    rt.gStyle.SetFrameFillStyle(0)
    rt.gStyle.SetFrameLineColor(1)
    rt.gStyle.SetFrameLineStyle(1)
    rt.gStyle.SetFrameLineWidth(1)
    
    # set the paper & margin sizes
    rt.gStyle.SetPaperSize(20,26)
    rt.gStyle.SetPadTopMargin(0.09)
    rt.gStyle.SetPadRightMargin(0.065)
    rt.gStyle.SetPadBottomMargin(0.15)
    rt.gStyle.SetPadLeftMargin(0.17)
    
    # use large Times-Roman fonts
    rt.gStyle.SetTitleFont(42,"xyz")  # set the all 3 axes title font
    rt.gStyle.SetTitleFont(42," ")    # set the pad title font
    rt.gStyle.SetTitleSize(0.06,"xyz") # set the 3 axes title size
    rt.gStyle.SetTitleSize(0.06," ")   # set the pad title size
    rt.gStyle.SetTitleSize(0.052,"y")   # set the pad title size
    rt.gStyle.SetTitleOffset(1.2,"y")   # set the pad title size
    rt.gStyle.SetLabelFont(42,"xyz")
    rt.gStyle.SetLabelSize(0.05,"xyz")
    rt.gStyle.SetLabelColor(1,"xyz")
    rt.gStyle.SetTextFont(42)
    rt.gStyle.SetTextSize(0.08)
    rt.gStyle.SetStatFont(42)
    
    # use bold lines and markers
    rt.gStyle.SetMarkerStyle(8)
    rt.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes
    
    #..Get rid of X error bars
    rt.gStyle.SetErrorX(0.001)
    
    # do not display any of the standard histogram decorations
    rt.gStyle.SetOptTitle(0)
    rt.gStyle.SetOptStat(0)
    rt.gStyle.SetOptFit(11111111)
    
    # put tick marks on top and RHS of plots
    rt.gStyle.SetPadTickX(1)
    rt.gStyle.SetPadTickY(1)
    
    ncontours = 999
    
    stops = [ 0.00, 0.34, 0.61, 0.84, 1.00 ]
    red =   [ 1.0,   0.95,  0.95,  0.65,   0.15 ]
    green = [ 1.0,  0.85, 0.7, 0.5,  0.3 ]
    blue =  [ 0.95, 0.6 , 0.3,  0.45, 0.65 ]
    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)
        
    npoints = len(s)
    rt.TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    rt.gStyle.SetNumberContours(ncontours)
   
    rt.gStyle.cd()
        

if __name__ == '__main__':
    
    rt.gROOT.SetBatch()
    parser = OptionParser()
    parser.add_option('-b','--box',dest="box", default="CaloDijet",type="string",
                  help="box name")
    parser.add_option('-m','--model',dest="model", default="gg",type="string",
                  help="signal model name")
    parser.add_option('-d','--dir',dest="outDir",default="./",type="string",
                  help="Input/Output directory to store output")    
    parser.add_option('-l','--lumi',dest="lumi", default=1.,type="float",
                  help="integrated luminosity in fb^-1")
    parser.add_option('--signif',dest="doSignificance",default=False,action='store_true',
                  help="for significance instead of limit")
    parser.add_option('--bayes',dest="bayes",default=False,action='store_true',
                  help="for bayesian limits")
    parser.add_option('--no-sys',dest="noSys",default=False,action='store_true',
                  help="for no systematics limits")
    
    (options,args) = parser.parse_args()
    Box = options.box
    models = options.model.split('_')
    model = models[0]
    directory      = options.outDir

    box = Box.lower()
    
    thyXsecDict = getThyXsecDict() 
    thyModels = thyXsecDict.keys()

    thyModelsToDraw = []
    if options.model=='gg':
        if 'PF' in Box:
            thyModelsToDraw = ['S8']
        else:
            thyModelsToDraw = ['RSGravitonGG']            
    elif options.model=='qq':        
        if 'PF' in Box:
            thyModelsToDraw = ['AxigluonNLO','E6Diquark',"W'","Z'"]            
        else:
            thyModelsToDraw = ['AxigluonkNLO','E6Diquark',"W'","Z'"]            
    elif options.model=='qg':        
            thyModelsToDraw = ['String','q*']
    elif options.model=='gg_qq_gaus':
        thyModelsToDraw = ['AxigluonkNLO','E6Diquark',"W'","Z'",'RSGravitonGG']
    elif options.model=='gg_qg_qq':
        thyModelsToDraw = ['String','q*','AxigluonNLO','E6Diquark',"W'","Z'",'S8','RSGraviton']
    elif options.model=='gg_qg_qq_gaus':
        thyModelsToDraw = ['String','q*','AxigluonkNLO','E6Diquark',"W'","Z'",'S8','RSGravitonGG']

    lineStyle = {'RSGravitonGG':4,
                 'RSGraviton':4,
                 'Axigluon':3,
                 'AxigluonkNLO':3,
                 'AxigluonNLO':3,
                 'E6Diquark':9,
                 'S8':1,
                 "W'":5,
                 "Z'":6,       
                 "String":7,     
                 "q*":10,                  
                 }
        
    lineColor = {'RSGravitonGG':rt.kGray+1,
                 'RSGraviton':rt.kGray+1,
                 'Axigluon':rt.kBlue+1,
                 'AxigluonkNLO':rt.kBlue+1,
                 'AxigluonNLO':rt.kBlue+1,
                 'E6Diquark':rt.kOrange+2,
                 'S8':rt.kMagenta,
                 "W'":rt.kRed+1,
                 "Z'":rt.kBlue-1,
                 "String":rt.kTeal+1,     
                 "q*":rt.kBlack,       
                 'gg':rt.kGreen+1,
                 'qq':rt.kRed,
                 'qg':rt.kBlue,
                 'gaus':rt.kCyan+1
                 }
        
    markerStyle = {'gg':24,
                 'qq':20,
                 'qg':23,
                 'gaus':26
                 }
        
    legendLabel = {'RSGravitonGG':'RS graviton (gg#rightarrowG#rightarrowgg)',
                   'RSGraviton':'RS graviton',
                   'Axigluon': 'Axiguon/coloron',
                   'AxigluonkNLO': 'Axiguon/coloron (k_{NLO} = 1.08)',
                   'AxigluonNLO': 'Axiguon/coloron (NLO)',
                   'E6Diquark':'Scalar diquark',
                   'S8':'Color-octet scalar (k_{s}^{2} = 1/2)',
                   "W'": "W'",
                   "Z'": "Z'",
                    "String": "String",
                    "q*": "Excited quark",
                   'gg':'gg #rightarrow X #rightarrow jj',
                   'qq':'qq #rightarrow X #rightarrow jj',
                   'qg':'qg #rightarrow X #rightarrow jj',
                   'gaus':'Gaussian, 7% width'
                   }
    
    mass_xsec = {}
    sig_xsec = {}
    N_g_xsec = {}
    xsec_gr_nom = {}
    for thyModel in thyModelsToDraw:        
        mass_xsec[thyModel] = array('d')
        sig_xsec[thyModel] = array('d')
        for mg in sorted(thyXsecDict[thyModel].keys()):
            mass_xsec[thyModel].append(mg)
            sig_xsec[thyModel].append(thyXsecDict[thyModel][mg])
            
        N_g_xsec[thyModel] = len(mass_xsec[thyModel])
        xsec_gr_nom[thyModel] = rt.TGraph(N_g_xsec[thyModel], mass_xsec[thyModel], sig_xsec[thyModel])
        xsec_gr_nom[thyModel].SetMarkerSize(0)
        xsec_gr_nom[thyModel].SetLineWidth(2)
        xsec_gr_nom[thyModel].SetLineStyle(lineStyle[thyModel])
        xsec_gr_nom[thyModel].SetLineColor(lineColor[thyModel])

    setstyle()
    rt.gStyle.SetOptStat(0)
    c = rt.TCanvas("c","c",500,400)
    if options.doSignificance:
        c.SetLogy(0)
    else:        
        c.SetLogy()

    h_limit = rt.TMultiGraph()
    gr_observedLimit = {}
    gr_expectedLimit = {}
    gr_expectedLimit2sigma = {}
    gr_expectedLimit1sigma = {}
    gluinoMassArray = {}
    gluinoMassArray_er = {}
    observedLimit = {}
    observedLimit_er = {}
    expectedLimit = {}
    expectedLimit_minus1sigma = {}
    expectedLimit_plus1sigma = {}
    expectedLimit_minus2sigma = {}
    expectedLimit_plus2sigma = {}
    
    if options.doSignificance:
        h_limit.SetTitle(" ;Resonance Mass m_{X} [GeV];Local Significance n#sigma")
    else:
        h_limit.SetTitle(" ;Resonance Mass m_{X} [GeV];95% C.L. upper limit on #sigma B A [pb]")

    for model in models:
        if len(models)>1:
            directory =  options.outDir+'/%s'%model
        if options.doSignificance:
            gluinoMassArray[model], gluinoMassArray_er[model], observedLimit[model], observedLimit_er[model], expectedLimit[model], expectedLimit_minus1sigma[model], expectedLimit_plus1sigma[model], expectedLimit_minus2sigma[model], expectedLimit_plus2sigma[model] = getSignificanceArrays(directory, model, Box)
        else:        
            gluinoMassArray[model], gluinoMassArray_er[model], observedLimit[model], observedLimit_er[model], expectedLimit[model], expectedLimit_minus1sigma[model], expectedLimit_plus1sigma[model], expectedLimit_minus2sigma[model], expectedLimit_plus2sigma[model] = getHybridCLsArrays(directory, model, Box, options.bayes)
    
    
        nPoints = len(observedLimit[model])
    
        gr_observedLimit[model] = rt.TGraph(nPoints, gluinoMassArray[model], observedLimit[model])
        gr_observedLimit[model].SetMarkerColor(1)
        gr_observedLimit[model].SetMarkerStyle(22)
        gr_observedLimit[model].SetMarkerSize(0.6)
        gr_observedLimit[model].SetLineWidth(3)
        gr_observedLimit[model].SetLineColor(rt.kBlack)
        gr_observedLimit[model].SetMarkerStyle(20)
        if len(models)>1:
            gr_observedLimit[model].SetLineColor(lineColor[model])
            gr_observedLimit[model].SetMarkerStyle(markerStyle[model])
            gr_observedLimit[model].SetMarkerColor(lineColor[model])


        gr_expectedLimit[model] = rt.TGraph(nPoints, gluinoMassArray[model], expectedLimit[model])
        gr_expectedLimit[model].SetLineWidth(3)
        gr_expectedLimit[model].SetLineStyle(2)
        if len(models)>1:
            gr_expectedLimit[model].SetLineColor(lineColor[model])
    
        gr_expectedLimit2sigma[model] = rt.TGraphAsymmErrors(nPoints, gluinoMassArray[model], expectedLimit[model], gluinoMassArray_er[model], gluinoMassArray_er[model], expectedLimit_minus2sigma[model], expectedLimit_plus2sigma[model])
        gr_expectedLimit2sigma[model].SetLineColor(5)
        gr_expectedLimit2sigma[model].SetFillColor(5)
        gr_expectedLimit2sigma[model].SetFillStyle(1001)
    
        gr_expectedLimit1sigma[model] = rt.TGraphAsymmErrors(nPoints, gluinoMassArray[model], expectedLimit[model], gluinoMassArray_er[model], gluinoMassArray_er[model], expectedLimit_minus1sigma[model], expectedLimit_plus1sigma[model])

        gr_expectedLimit1sigma[model].SetLineColor(rt.kGreen-7)
        gr_expectedLimit1sigma[model].SetFillColor(rt.kGreen-7)

        if len(models)==1:
            h_limit.Add(gr_expectedLimit2sigma[model])
            h_limit.Add(gr_expectedLimit1sigma[model])
        h_limit.Add(gr_observedLimit[model])

        
    for thyModel in thyModelsToDraw:
        h_limit.Add(xsec_gr_nom[thyModel])
        
    h_limit.Draw("a3")
    if 'PF' in Box:
        h_limit.GetXaxis().SetLimits(1200,8000)
    else:
        h_limit.GetXaxis().SetLimits(500,1600)
    if options.doSignificance:
        h_limit.SetMaximum(4)
        h_limit.SetMinimum(0)
    else:
        if 'PF' in Box:
            h_limit.SetMaximum(100)
            h_limit.SetMinimum(1e-4)
        else:
            h_limit.SetMaximum(10000)
            h_limit.SetMinimum(1e-2)
            
    h_limit.Draw("a3")
    if options.doSignificance:
        h_limit.GetYaxis().SetNdivisions(405,True)
    
    for model in models:    
        if options.doSignificance:
            gr_observedLimit[model].SetMarkerStyle(21)
            gr_observedLimit[model].SetMarkerSize(0.6)
            gr_observedLimit[model].SetLineColor(rt.kRed)
            gr_observedLimit[model].SetMarkerColor(rt.kBlue)
            gr_observedLimit[model].Draw("lp SAME")
        else:
            gr_expectedLimit[model].Draw("c same")
            for thyModel in thyModelsToDraw:
                xsec_gr_nom[thyModel].Draw("c same")
            gr_observedLimit[model].Draw("lp SAME")
            
        gr_expectedLimit1sigma[model].SetLineStyle(2)
        gr_expectedLimit1sigma[model].SetLineWidth(3)
        gr_expectedLimit1sigma[model].SetLineColor(rt.kBlack)
        gr_expectedLimit2sigma[model].SetLineStyle(2)
        gr_expectedLimit2sigma[model].SetLineWidth(3)
        gr_expectedLimit2sigma[model].SetLineColor(rt.kBlack)
    
    l = rt.TLatex()
    l.SetTextAlign(11)
    l.SetTextSize(0.05)
    l.SetNDC()
    l.SetTextFont(62)
    l.DrawLatex(0.17,0.92,"CMS")
        
    l.SetTextFont(52)
    l.DrawLatex(0.26,0.92,"Preliminary")
    l.SetTextFont(42)
    #l.DrawLatex(0.65,0.92,"%.0f pb^{-1} (13 TeV)"%(options.lumi*1000))
    l.DrawLatex(0.68,0.92,"%.1f fb^{-1} (13 TeV)"%(options.lumi))
    
    if options.model=="gg":
        l.DrawLatex(0.3,0.8,"gg #rightarrow X #rightarrow jj")
    elif options.model=="qg":        
        l.DrawLatex(0.3,0.8,"qg #rightarrow X #rightarrow jj")
    elif options.model=="qq":
        l.DrawLatex(0.3,0.8,"qq #rightarrow X #rightarrow jj")
    elif options.model=="gaus":
        l.DrawLatex(0.24,0.8,"Gaussian, 7% width")

    #if options.bayes:
    #    if options.noSys:        
    #        l.DrawLatex(0.2,0.85,"Bayesian, no syst.")
    #    else:
    #        l.DrawLatex(0.2,0.85,"Bayesian, with syst.")
    #else:        
    #    if options.noSys:        
    #        l.DrawLatex(0.2,0.85,"Frequentist, no syst.")
    #    else:
    #        l.DrawLatex(0.2,0.85,"Frequentist, with syst.")

    if options.doSignificance:
        c.SetGridy()
        leg = rt.TLegend(0.55,0.79,0.92,0.87)
    else:        
        leg = rt.TLegend(0.55,0.68,0.92,0.87)
    
    leg.SetTextFont(42)
    leg.SetFillColor(rt.kWhite)
    leg.SetLineColor(rt.kWhite)

    if len(models)==1:
        if options.doSignificance:
            leg.AddEntry(gr_observedLimit[model], "Observed","lp")
        else:
            leg.AddEntry(gr_observedLimit[model], "Observed","lp")
        if not options.doSignificance:
            leg.AddEntry(gr_expectedLimit1sigma[model], "Expected #pm 1#sigma","lf")    
        if not options.doSignificance:
            leg.AddEntry(gr_expectedLimit2sigma[model], "Expected #pm 2#sigma","lf")
    else:
        for model in models:
            leg.AddEntry(gr_observedLimit[model], legendLabel[model],"lp")
            
    leg.Draw("SAME")
        
    if len(thyModelsToDraw)>0 and not options.doSignificance:        
        legThyModel = rt.TLegend(0.2,0.17,0.55,0.35)
        legThyModel.SetTextFont(42)
        legThyModel.SetFillColor(rt.kWhite)
        legThyModel.SetLineColor(rt.kWhite)
        for thyModel in thyModelsToDraw:
            legThyModel.AddEntry(xsec_gr_nom[thyModel], legendLabel[thyModel],'l')
        legThyModel.Draw("same")

        
    for model in models:    
        if options.doSignificance:
            gr_observedLimit[model].Draw("lp SAME")
        else:
            gr_expectedLimit[model].Draw("c same")
            for thyModel in thyModelsToDraw:
                xsec_gr_nom[thyModel].Draw("c same")
            gr_observedLimit[model].Draw("lp SAME")


    if 'PF' in Box:
        h_limit.GetXaxis().SetTitle('Resonance Mass m_{X} [TeV]')
        h_limit.GetXaxis().SetLabelOffset(1000)
        #h_fit_residual_vs_mass.GetXaxis().SetNoExponent()
        #h_fit_residual_vs_mass.GetXaxis().SetMoreLogLabels()    
        xLab = rt.TLatex()
        xLab.SetTextAlign(22)
        xLab.SetTextSize(0.05)
        xLab.SetTextFont(42)
        xLab.SetTextSize(0.05)
        if options.doSignificance:
            yOffset = -0.138
        else:
            yOffset = 6.5e-5
        for i in range(2,9):
            xLab.DrawLatex(i*1000, yOffset, "%i"%i)

    if options.doSignificance:
        c.SaveAs(options.outDir+"/signif_"+options.model+"_"+box+".pdf")
        c.SaveAs(options.outDir+"/signif_"+options.model+"_"+box+".C")
    else:
        if options.bayes:
            if options.noSys:
                c.SaveAs(options.outDir+"/limits_bayes_nosys_"+options.model+"_"+box+".pdf")
                c.SaveAs(options.outDir+"/limits_bayes_nosys_"+options.model+"_"+box+".C")
            else:
                c.SaveAs(options.outDir+"/limits_bayes_"+options.model+"_"+box+".pdf")
                c.SaveAs(options.outDir+"/limits_bayes_"+options.model+"_"+box+".C")
        else:
            if options.noSys:
                c.SaveAs(options.outDir+"/limits_freq_nosys_"+options.model+"_"+box+".pdf")
                c.SaveAs(options.outDir+"/limits_freq_nosys_"+options.model+"_"+box+".C")
            else:
                c.SaveAs(options.outDir+"/limits_freq_"+options.model+"_"+box+".pdf")
                c.SaveAs(options.outDir+"/limits_freq_"+options.model+"_"+box+".C")

