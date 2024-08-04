class candidateElimination:
    def __init__(self, fileName, ct):
        self.data = self.getList(fileName)
        self.generalHypothesis = [list('?'*len(self.data[0][1:]))]
        self.specificHypothesis = []
        self.versionSpace = []
        # To find the index of target concept.
        for attribute in self.data[0]:
            if attribute == ct:
                self.ct = self.data[0].index(attribute)
                break
        self.targetConcept = [i[self.ct] for i in self.data[1:]]
        print(self.data)

    def getList(self, fileName):
        data = []
        with open(fileName, 'r') as file:
            for line in file:
                data.append([value.strip(' \' \n') for value in line.split(',')])
            return data

    def trainData(self, flag): 
    # flag - to show the steps

        for i in range(len(self.targetConcept)):

            if self.targetConcept[i] in ['1', 'yes', 'Yes', 'y']:

                if self.specificHypothesis == []:
                # When c(t) is 1, changes are made in specific hypothesis.
                    # Copying the first column with c(t) = 1.
                    self.specificHypothesis = self.data[i+1][1:].copy()
                    print(self.specificHypothesis)

                else:
                    if self.specificHypothesis != self.data[i+1]:
                        # If there is any change in values of the column, the value in specificHypothesis is changed to '?'.

                        for x, value in enumerate(self.specificHypothesis):
                            # print('value: ', value, 'list : ', self.data[i+1][x+1])
                            if value != '?' and value != self.data[i+1][x+1]:
                                self.specificHypothesis[x] = '?'
            else:
            # When c(t) is 0, changes are made in general hypothesis.
                self.generalHypothesis.clear() if self.generalHypothesis == list('?'*len(self.data[0][1:])) else None

                for value, x in zip(self.specificHypothesis, range(len(self.data)+1)):
                    newList = list('?'*(len(self.data[0][2:])))

                    if value != '?' and value != self.data[i+1][x+1]:
                        newList.insert(self.specificHypothesis.index(value), value)
                        # print(newList)
                        if newList != list('?'*(len(self.data[0][1:]))) and newList not in self.generalHypothesis:
                            self.generalHypothesis.append(newList)
            
            if flag:
                print(f'Instance {i+1}:\nTarget concept: {"Positive" if self.targetConcept[i] in ['1', 'yes', 'Yes', 'y'] else "Negative"}')
                print("\tSpecific Hypothesis: ", self.specificHypothesis)
                print("\tGeneral Hypothesis: ", self.generalHypothesis)
                print()

        temp = []
        # To remove the inconsistant hypothesis from generalHypothesis.
        if isinstance(self.generalHypothesis[0], list):
            for x in range(len(self.specificHypothesis)):
                for hypothesis in self.generalHypothesis:
                    if hypothesis[x] != '?' and hypothesis[x] == self.specificHypothesis[x] and hypothesis not in temp:
                        temp.append(hypothesis)
                        break

        self.generalHypothesis = temp.copy()

        # Finding the version space.
        for i, sHypothesis in enumerate(self.specificHypothesis):
            if sHypothesis != '?':
                for gHypothesis in self.generalHypothesis:
                    if gHypothesis[i] != sHypothesis:
                        temp = gHypothesis.copy()
                        temp[i] = sHypothesis
                        self.versionSpace.append(temp) if temp not in self.versionSpace else None
                        break
        
        return (self.specificHypothesis, self.generalHypothesis, self.versionSpace)

ce = candidateElimination("enjoySport.csv", "EnjoySport")
sh, gh, vs = ce.trainData(True)

print("\nFinal output:")
print("\tSpecific Hypothesis:\n\t\t", sh)
print("\tGeneral Hypothesis:\n\t\t", gh)
print("\tVersion Space:\n\t\t", vs)