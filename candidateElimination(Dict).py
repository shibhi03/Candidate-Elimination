class Dictionary:
    def readData(self, fileName):
        dictionary = dict()
        with open(fileName, 'r') as file:
            keys = [key.strip(' \' \n') for key in file.readline().strip().split(',')]
            # print(keys)
            for line in file:
                for i, key in enumerate(keys):
                    dictionary[key] = list() if key not in dictionary else dictionary[key]
                    dictionary[key].append(line.strip().split(',')[i].strip(' \''))

        return dictionary
'''
data = {
    'c(t)': ['1', '0', '1', '0', '0'],
    'hair': ['blond', 'brown', 'blond', 'black', 'blond'],
    'body': ['thin', 'thin', 'plump', 'thin', 'plump'],
    'likesSimon': ['yes', 'no', 'yes', 'no', 'no'],
    'pose': ['arrogant', 'natural', 'goofy', 'arrogant', 'natural'],
    'smile': ['toothy', 'pleasent', 'pleasent', 'none', 'toothy'],
    'smart': ['no', 'yes', 'no', 'no', 'yes']
}
'''
class candidateElimination:
    def __init__(self, data):
        self.generalHypothesis = list('?'*(len(data)-1)) # Generates a list containing '?' equal to the number of columns
        self.specificHypothesis = list('0'*(len(data)-1)) # Generates a list containing '0'(null) equal to the number of columns
        self.versionSpace = []
        self.targetConcept = data[list(data)[0]]
        self.data = data

    def trainData(self, flag): # flag - to show the steps

        for i in range(len(self.targetConcept)):

            # Copying the rows excluding the 1st column.
            attributeList = [self.data[value][i] for value in list(self.data)[1:]]

            if self.targetConcept[i] in ['1', 'yes', 'Yes', 'y']:
                # When c(t) is 1, changes are made in specific hypothesis

                if self.specificHypothesis == list('0'*(len(self.data)-1)):
                    # Copying the first column with c(t) = 1.
                    self.specificHypothesis = attributeList

                else:
                    if self.specificHypothesis != attributeList:
                        # If there is any change in values of the column, the value in specificHypothesis is changed to '?'.

                        for x, value in enumerate(self.specificHypothesis):
                            # print('value: ', value, ' x: ', x)
                            if value != '?' and value != attributeList[x]:
                                self.specificHypothesis[x] = '?'
            else:
                # When c(t) is 0, changes are made in general hypothesis
                self.generalHypothesis.clear() if self.generalHypothesis == list('?'*(len(self.data)-1)) else None

                for value, x in zip(self.specificHypothesis, range(len(self.data))):
                    newList = list('?'*(len(self.data)-2))

                    if value != '?' and value != attributeList[x]:
                        newList.insert(self.specificHypothesis.index(value), value)
                        # print(newList)
                        if newList != list('?'*(len(self.data)-1)) and newList not in self.generalHypothesis:
                            self.generalHypothesis.append(newList)
            
            if flag:
                print(f'Instance {i+1}:\nTarget concept: {"Positive" if self.targetConcept[i] in ['1', 'yes', 'Yes', 'y'] else "Negative"}')
                print("\tSpecific Hypothesis: ", self.specificHypothesis)
                print("\tGeneral Hypothesis: ", self.generalHypothesis)
                print()

        temp = []
        if isinstance(self.generalHypothesis[0], list):
            for x in range(len(self.specificHypothesis)):
                for hypothesis in self.generalHypothesis:
                    if hypothesis[x] != '?' and hypothesis[x] == self.specificHypothesis[x] and hypothesis not in temp:
                        temp.append(hypothesis)
                        break

        self.generalHypothesis = temp.copy()

        for i, sHypothesis in enumerate(self.specificHypothesis):
            if sHypothesis != '?':
                for gHypothesis in self.generalHypothesis:
                    # print('\ng: ', gHypothesis, '\ns: ', sHypothesis)
                    if gHypothesis[i] != sHypothesis:
                        temp = gHypothesis.copy()
                        temp[i] = sHypothesis
                        # print('t: ', gHypothesis)
                        self.versionSpace.append(temp) if temp not in self.versionSpace else None
                        break
                # print('vs: ', versionSpace)
        
        return (self.specificHypothesis, self.generalHypothesis, self.versionSpace)

d = Dictionary()
data = d.readData("enjoySport.csv")

ce = candidateElimination(data)
sh, gh, vs = ce.trainData(True)

print("\nFinal output:")
print("\tSpecific Hypothesis:\n\t\t", sh)
print("\tGeneral Hypothesis:\n\t\t", gh)
print("\tVersion Space:\n\t\t", vs)