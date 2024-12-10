import os
from vectorizer import Vectorizor
import xml.etree.ElementTree as ET 

class VectorizerTest:
    def __init__(self, bugReportsDir, sourceCodeDir, xml):
        self.bugReportDir = bugReportsDir
        self.sourceCodeDir = sourceCodeDir
        self.xml = xml
        self.prefix = ".\\source_code\\swt-3.1\\src\\"
    def test(self):
        totalTest = 0
        passingTests = 0

        if not os.path.exists(self.bugReportDir) or not os.path.exists(self.sourceCodeDir):
            print("Bug report directory or source code directory does not exist.")
            return 0

        for root, dirs, files in os.walk(self.bugReportDir):
            for file in files:
                totalTest += 1
                v = Vectorizor(os.path.join(self.bugReportDir, file), self.sourceCodeDir)
                topFiles = v.getTop3ClosestFiles()

                tree = ET.parse(self.xml)
                root = tree.getroot()
                bug_id = os.path.splitext(os.path.basename(file))[0]
                bug = root.find(f".//bug[@id='{bug_id}']")
                correctFile = bug.find("./fixedFiles/file").text

                corFileM = self.normalize_path(correctFile)
                topFilesFix = [self.normalize_path(file, self.prefix) for file, _ in topFiles]

                if corFileM in topFilesFix:
                    passingTests += 1
                    print(f"{topFilesFix} {corFileM} {True}")
                else:
                    print(f"{topFilesFix} {corFileM} {False}")

        return (passingTests / totalTest)*100

                    
    def normalize_path(self, file_path, prefix_to_remove=None):
        if not isinstance(file_path, str):
            raise TypeError(f"Expected a string for file_path, but got {type(file_path).__name__}")
        
        normalized_path = os.path.normpath(file_path)
        
        if prefix_to_remove:
            prefix_to_remove = os.path.normpath(prefix_to_remove)
            if normalized_path.startswith(prefix_to_remove):
                normalized_path = normalized_path[len(prefix_to_remove):]
        
        normalized_path = normalized_path.replace(os.sep, '.').replace('/', '.')

        normalized_path = normalized_path.lstrip('.')
        substring_to_remove = "swt.swt-3.1.src."
        normalized_path = normalized_path.replace(substring_to_remove, "")
        
        return os.path.splitext(normalized_path.lower())[0]




# Convert XML into text file
def XMLParser(xmlFile, destDir):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    for bug in root.findall("bug"):
        id = bug.get("id")
        summary = bug.find("./buginformation/summary").text
        desc = bug.find("./buginformation/description").text
        file = bug.find("./fixedFiles/file").text

        filePath = os.path.join("bugReports", destDir,f"{id}.txt")
        with open(filePath, "w", encoding='utf-8') as f:
            f.write(f"Bug ID: {id}\n")
            f.write(f"Summary: {summary}\n")
            f.write(f"Description: {desc}\n")
            f.write(f"File: {file}\n")

if __name__ == "__main__":
    v = VectorizerTest("bugReports/SWT", os.path.join(".", "swt", "swt-3.1", "src"), "SWTBugRepository.xml")
    print(v.test())