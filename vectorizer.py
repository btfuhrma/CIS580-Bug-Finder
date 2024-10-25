import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class vectorizor():
    
    # Initialize class with the report file and the source code directory
    def __init__(self, reportFile, sourceCodeDirectory):
        self.reportFile = reportFile
        self.sourceCodeDirectory = sourceCodeDirectory
        self.sourceCodeFiles = []
        self.reportVector = None
        self.codeVectors = None
        self.similarities = None

        return

    # Get list of source code file names
    def getSourceFileNames(self):
        for root, dirs, files in os.walk(self.sourceCodeDirectory):
            for file in files:
                if file not in self.sourceCodeFiles:
                    self.sourceCodeFiles.append(file)
        
        return
        
    def vectorize(self):
        self.getSourceFileNames()
        skVectorizor = TfidfVectorizer(stop_words='English')
        self.reportVector = skVectorizor.fit_transform(self.reportFile)
        self.codeVectors = skVectorizor.fit_transform(self.sourceCodeFiles)
        return
    
    def cosineSimilarity(self):
        self.vectorize()
        self.similarities = cosine_similarity(self.reportVector, self.codeVectors)
        return
    
    def getClosestFile(self):
        self.cosineSimilarity()
        index = self.similarities.argmax()
        closestFile = self.sourceCodeFiles[index]
        closestScore = self.similarities[index]
        return closestFile, closestScore