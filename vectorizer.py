import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
import re

nltk.download('punkt_tab')

class Vectorizor:
    def __init__(self, reportFile, sourceCodeDirectory):
        self.reportFile = reportFile
        self.sourceCodeDirectory = sourceCodeDirectory
        self.sourceCodeFiles = self.load_source_code_files()  # Load file names
        self.sourceCodeContents = self.load_source_code_contents()  # Load contents
        self.reportContents = self.load_report()  # Load report contents
        self.reportVector = None
        self.codeVectors = None
        self.similarities = None

    def load_report(self):
        try:
            with open(self.reportFile, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("Report file not found!")
            return None

    def load_source_code_files(self):
        try:
            return os.listdir(self.sourceCodeDirectory)
        except FileNotFoundError:
            print("Source code directory not found!")
            return []

    def load_source_code_contents(self):
        contents = []
        for file_name in self.sourceCodeFiles:
            file_path = os.path.join(self.sourceCodeDirectory, file_name)
            try:
                with open(file_path, 'r') as file:
                    contents.append(file.read())
            except FileNotFoundError:
                print(f"Source code file {file_name} not found!")
        return contents

    def stem_text(self, text):
        text = text.replace('_', ' ')  # Separate snake case when used
        text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)  # Separate camel case when used
        text = re.sub(r'[\(\)]', ' ', text)  # Remove parentheses from methods
        stemmer = PorterStemmer()
        tokens = word_tokenize(text)
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return ' '.join(stemmed_tokens)

    def vectorize(self):
        self.sourceCodeContents = [self.stem_text(content) for content in self.sourceCodeContents]
        self.reportContents = self.stem_text(self.reportContents)
        skVectorizor = TfidfVectorizer(stop_words='english')
        all_documents = [self.reportContents] + self.sourceCodeContents

        tfidf_matrix = skVectorizor.fit_transform(all_documents)
        self.reportVector = tfidf_matrix[0:1]
        self.codeVectors = tfidf_matrix[1:]

    def cosineSimilarity(self):
        self.vectorize()
        self.similarities = cosine_similarity(self.reportVector, self.codeVectors)

    def get_all_similarities(self):
        self.cosineSimilarity()
        return self.similarities[0].tolist(), self.sourceCodeFiles  # Returning scores and file names


    def getClosestFile(self):
        self.cosineSimilarity()
        index = self.similarities.argmax()
        closestFile = self.sourceCodeFiles[index]
        closestScore = self.similarities[0][index]  # Access the score correctly
        return closestFile, closestScore

if __name__ == "__main__":
    report_file = "report.txt"
    source_code_directory = "source_code"
    vectorizor = Vectorizor(report_file, source_code_directory)

    if os.path.exists(report_file) and os.path.exists(source_code_directory):
        # Get all similarity scores for the source code files
        similarities, files = vectorizor.get_all_similarities()
        for file, score in zip(files, similarities):
            print(f"File: {file}, Similarity Score: {score}")

        # Get the closest file based on the highest similarity score
        closest_file, closest_score = vectorizor.getClosestFile()
        print(f"Closest file: {closest_file}, Similarity score: {closest_score}")
    else:
        if not os.path.exists(report_file):
            print("Report file does not exist.")
        if not os.path.exists(source_code_directory):
            print("Source code directory does not exist.")

