import os, sys
from os import path

if sys.argv[1] != '':
    getTxt = '.txt' in sys.argv[1]
    if getTxt == True:
        txtFile = sys.argv[1].replace("\\", "/")
        epFolder = txtFile.rstrip('.txt')
        epName = os.path.basename(epFolder)

        #read .txt and save it to variable
        openTxt = open(txtFile, mode = 'r')
        txtContent = openTxt.readlines()
        openTxt.close()

        if not path.isdir(epFolder):
            os.makedirs(epFolder)
        
        for each in txtContent: 
            if not path.isdir(epFolder + '/' + epName + '_' + each.rstrip('\n')):
                if each.rstrip():    #make sure blank lines are skipped
                    os.makedirs(epFolder + '/' + epName + '_' + each.rstrip('\n'))
                    os.makedirs(epFolder + '/' + epName + '_' + each.rstrip('\n') + '/' + 'footage')

        os.startfile(epFolder)
