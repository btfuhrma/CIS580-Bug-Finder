import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
import re
nltk.download('punkt_tab')
class Vectorizor:
    
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
        if not os.path.exists(self.reportFile):
            raise FileNotFoundError(f"The file '{self.reportFile}' was not found.")
        with open(self.reportFile ,'r') as f:
            content = f.read()
            if len(content) <= 0:
                raise Exception(f"The file '{self.reportFile}' is empty.")
            self.reportContents = self.stem_text(content)

    # Get list of source code file names
    def getSourceContent(self):
        if not os.path.exists(self.sourceCodeDirectory):
            raise FileNotFoundError(f"The directory '{self.sourceCodeDirectory}' was not found.")
        readList = []
        for root, dirs, files in os.walk(self.sourceCodeDirectory):
            for file in files:
                if file not in readList:
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        if len(content) <= 0:
                            readList.append(file)
                            pass
                        stemmed_content = self.stem_text(content)
                        self.sourceCodeContents.append(stemmed_content)
                        self.sourceCodeFiles.append(file)
                        readList.append(file)
        
        return
    
    def stem_text(self, text):
        text = text.replace('_', ' ') # Separate snake case when used
        text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)  # Separate camel case when used

        text = re.sub(r'\(\)', '', text)  # Remove paranthesis from methods
        text = re.sub(r'\(', ' ', text)   # Remove paranthesis from methods
        text = re.sub(r'\)', ' ', text)   # Remove paranthesis from methods
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
    
