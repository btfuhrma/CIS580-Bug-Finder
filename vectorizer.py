import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt_tab')
class Vectorizor():
    
    # Initialize class with the report file and the source code directory
    def __init__(self, reportFile, sourceCodeDirectory):
        self.reportFile = reportFile
        self.sourceCodeDirectory = sourceCodeDirectory
        self.sourceCodeContents = []
        self.sourceCodeFiles = []
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
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        stemmed_content = self.stem_text(content)
                        self.sourceCodeContents.append(stemmed_content)
                        self.sourceCodeFiles.append(file)
                        readList.append(file)
        
        return
    
    def stem_text(self, text):
        text = text.replace('_', ' ') # Separate snake case used
        stemmer = PorterStemmer()
        tokens = word_tokenize(text)
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return ' '.join(stemmed_tokens)

    def vectorize(self):
        self.getSourceContent()
        self.getReportContent()
        skVectorizor = TfidfVectorizer(stop_words='english')
        all_documents = [self.reportContents] + self.sourceCodeContents

        tfidf_matrix = skVectorizor.fit_transform(all_documents)

        self.reportVector = tfidf_matrix[0:1]
        self.codeVectors = tfidf_matrix[1:]
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
    
