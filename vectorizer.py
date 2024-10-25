import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
class vectorizor():
    
    # Initialize class with the report file and the source code directory
    def __init__(self, reportFile, sourceCodeDirectory):
        self.reportFile = reportFile
        self.sourceCodeDirectory = sourceCodeDirectory
        self.sourceCodeContents = []
        self.reportContents = None
        self.reportVector = None
        self.codeVectors = None
        self.similarities = None

        return

    def getReportContent(self):
        with open(self.reportFile ,'r') as f:
            content = f.read()
            self.reportContents = self.stem_text(content)

    # Get list of source code file names
    def getSourceContent(self):
        readList = []
        for root, dirs, files in os.walk(self.sourceCodeDirectory):
            for file in files:
                if file not in readList:
                    with open(file, 'r') as f:
                        content = f.read()
                        stemmed_content = self.stem_text(content)
                        self.sourceCodeContents.append(stemmed_content)
                        readList.append(file)
        
        return
    
    def stem_text(self, text):
        stemmer = PorterStemmer()
        tokens = word_tokenize(text)
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return ' '.join(stemmed_tokens)

    def vectorize(self):
        self.getSourceContent()
        self.getReportContent()
        skVectorizor = TfidfVectorizer(stop_words='English')
        self.reportVector = skVectorizor.fit_transform(self.reportContents)
        self.codeVectors = skVectorizor.fit_transform(self.sourceCodeContents)
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
    

