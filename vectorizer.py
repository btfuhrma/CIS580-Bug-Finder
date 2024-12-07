import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import re

nltk.download('punkt')
nltk.download('wordnet')

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
            sourceCodeFiles = []
            for root, dirs, files in os.walk(self.sourceCodeDirectory):
                for file in files:
                    if file not in sourceCodeFiles:
                        sourceCodeFiles.append(os.path.join(root, file))
            return sourceCodeFiles
        except FileNotFoundError:
            print("Source code directory not found!")
            return []

    def load_source_code_contents(self):
        contents = []
        for file_name in self.sourceCodeFiles:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    contents.append(file.read())
            except FileNotFoundError:
                print(f"Source code file {file_name} not found!")
            except UnicodeDecodeError:
                print("Unicode source error.")
        return contents

    def lemmatize_text(self, text):
        lemmatizer = WordNetLemmatizer()
        text = text.replace('_', ' ')  # Separate snake case when used
        text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)  # Separate camel case when used
        text = re.sub(r'[\(\)]', ' ', text)  # Remove parentheses from methods
        tokens = word_tokenize(text)
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(lemmatized_tokens)

    def vectorize(self):
        self.sourceCodeContents = [self.lemmatize_text(content) for content in self.sourceCodeContents]
        self.reportContents = self.lemmatize_text(self.reportContents)
        
        skVectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.95, min_df=2)
        all_documents = [self.reportContents] + self.sourceCodeContents
        tfidf_matrix = skVectorizer.fit_transform(all_documents)
        self.reportVector = tfidf_matrix[0:1]
        self.codeVectors = tfidf_matrix[1:]

    def cosineSimilarity(self):
        self.vectorize()
        self.similarities = cosine_similarity(self.reportVector, self.codeVectors)

    def get_all_similarities(self):
        self.cosineSimilarity()
        return self.similarities[0].tolist(), self.sourceCodeFiles

    def getClosestFile(self):
        self.cosineSimilarity()
        index = self.similarities.argmax()
        closestFile = self.sourceCodeFiles[index]
        closestScore = self.similarities[0][index]
        return closestFile, closestScore
    
    def getTop3ClosestFiles(self):
        self.cosineSimilarity()
        similarities_with_files = list(zip(self.similarities[0], self.sourceCodeFiles))
        top_3 = sorted(similarities_with_files, key=lambda x: x[0], reverse=True)[:3]
        return [(file, score) for score, file in top_3]

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
