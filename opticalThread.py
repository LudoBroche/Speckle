from threading import Thread
import spytIO
import corrections as corr
import OpticalFlow
import os



def createFolder(folder):
    if not (os.path.exists(folder)):
        os.mkdir(folder)


class OpticalFlowSolverThread(Thread):
    def __init__(self, dictio,listOfProjections,outputFolder):
        Thread.__init__(self)
        self.dictionaryOfExperiment = dictio
        self.listOfProjection=listOfProjections
        self.output=outputFolder
        self.createFolders()

    def createFolders(self):
        self.dxFolder = self.output + '/dx/'
        self.dyFolder = self.output + '/dy/'
        self.phiFolder = self.output + '/phi/'
        self.phiLarkin = self.output + '/phiLarkin/'
        self.phiKottler = self.output + '/phiKottler/'

        createFolder(self.dxFolder)
        createFolder(self.dyFolder)
        createFolder(self.phiFolder)
        createFolder(self.phiLarkin)
        createFolder(self.phiKottler)

    def saveResult(self,res,projNumber):
        dx = res['dx']
        dy = res['dy']
        phi = res['phi']
        phi2 = res['phi2']
        phi3 = res['phi3']
        txtProj = '%4.4d' % projNumber
        spytIO.saveEdf(dx, self.dxFolder+'/dx_' + txtProj + '.edf')
        spytIO.saveEdf(dy.real, self.dyFolder+'/dy_' + txtProj + '.edf')
        spytIO.saveEdf(phi.real, self.phiFolder+'/phi_' + txtProj + '.edf')
        spytIO.saveEdf(phi2.real, self.phiLarkin+'/phiLarkin_' + txtProj + '.edf')
        spytIO.saveEdf(phi3.real, self.phiKottler+'/phiKottler' + txtProj + '.edf')



    def run(self):
        projectionFiles = self.dictionaryOfExperiment['projections']
        referenceFilename = self.dictionaryOfExperiment['references'][0]
        Ir = spytIO.openImage(referenceFilename)
        for numeroProjection in self.listOfProjection:
            numeroProjection = int(numeroProjection)
            print('Processing ' + str(numeroProjection))
            projectionFileName=projectionFiles[numeroProjection]
            Is=spytIO.openImage(projectionFileName)
            result = OpticalFlow.processOneProjection(Is, Ir)
            self.saveResult(result, numeroProjection)


class multiTomoOpticalFlowSolver(Thread):

    def __init__(self, listOfDictionaries,listOfProjections,outputFolder):
        Thread.__init__(self)
        self.listOfDictionnaries = listOfDictionaries
        self.listOfProjection=listOfProjections
        self.output=outputFolder
        self.createFolders()

    def createFolders(self):
        self.dxFolder = self.output + '/dx/'
        self.dyFolder = self.output + '/dy/'
        self.phiFolder = self.output + '/phi/'
        self.phi2Folder = self.output + '/phiKottler/'
        self.phi3Folder = self.output + '/phiLarkin/'

        createFolder(self.dxFolder)
        createFolder(self.dyFolder)
        createFolder(self.phiFolder)
        createFolder(self.phi2Folder)
        createFolder(self.phi3Folder)

    def run(self):
        for numeroProjection in self.listOfProjection:
            numeroProjection=int(numeroProjection)
            print('Processing '+str(numeroProjection))
            projectionFiles = []
            referencesFiles = []
            darkFieldFiles = []
            for dict in self.listOfDictionnaries:
                projectionFiles.append(dict['projections'][numeroProjection])
                referencesFiles.append(dict['references'][0])
                darkFieldFiles.append(dict['darkField'])


            print(projectionFiles)

            Is = spytIO.openSeq(projectionFiles)
            Ir = spytIO.openSeq(referencesFiles)
            #df = spytIO.openSeq(darkFieldFiles)
            #Is, Ir = corr.registerImagesBetweenThemselves(Is, Ir)
            result = OpticalFlow.processProjectionSet(Is, Ir)

            dx = result['dx']
            dy = result['dy']
            phi = result['phi']
            phi2 = result['phi2']
            phi3 = result['phi3']

            textProj='%4.4d'%numeroProjection
            spytIO.saveEdf(dx.real, self.dxFolder + '/dx_' + textProj + '.edf')
            spytIO.saveEdf(dy.real, self.dyFolder + '/dy_' + textProj + '.edf')
            spytIO.saveEdf(phi.real, self.phiFolder + '/phi_' + textProj + '.edf')
            spytIO.saveEdf(phi2.real, self.phi2Folder + '/phiKottler_' + textProj + '.edf')
            spytIO.saveEdf(phi3.real, self.phi3Folder + '/phiLarkin_' + textProj + '.edf')






