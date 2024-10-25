import os
from sklearn.feature_extraction.text import TfidfVectorizer

class vectorizor():
    
    # Initialize class with the report file and the source code directory
    def __init__(self, reportFile, sourceCodeDirectory):
        self.reportFile = reportFile
        self.sourceCodeDirectory = sourceCodeDirectory
        self.sourceCodeFiles = []
        self.reportVector = None
        self.codeVectors = None

        return

    # Get list of source code file names
    def getSourceFileNames(self):

        for root, dirs, files in os.walk(self.sourceCodeDirectory):
            for file in files:
                if file not in self.sourceCodeFiles:
                    self.sourceCodeFiles.append(file)
        
        return
        
    def vectorize(self, fileName):
        skVectorizor = TfidfVectorizer(stop_words='English')
        self.reportVector = skVectorizor.fit_transform(self.reportFile)
        self.codeVectors = skVectorizor.fit_transform(self.sourceCodeFiles)
    