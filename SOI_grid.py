import shapefile

shp = shapefile.Reader('./Survey_of_India_fishnet/SoI_one-inch_number_letter')

shapeRecs = shp.shapeRecords()

# Number counter
numbers = []
for i, sr in enumerate(shapeRecs):
    if sr.record[4] not in numbers:
         numbers.append(sr.record[4])

# List of lists each containing records only of a single number
shapeRecsSingleNumber = []
for i, n in enumerate(numbers):
    shapeRecsSingleNumber.append([])
    for sr in shapeRecs:
        if sr.record[4] == numbers[i]:
            shapeRecsSingleNumber[i].append(sr)

# Sort lists within list based on coordinate attribute data
shapeRecordsSorted = []
for l in shapeRecsSingleNumber:
    lSorted = sorted(l, key=lambda x: (x.record[0], x.record[1]))
    shapeRecordsSorted.append(lSorted)

shapeRecordsSorted = [item for sublist in shapeRecordsSorted for item in sublist]
print(len(shapeRecordsSorted))

# Letter counter
letterGroups = [ ['D', 'C', 'B', 'A'], ['H', 'G', 'F', 'E',], ['L', 'K', 'J', 'I'], ['P', 'O', 'N', 'M']]
recordCounter = 0

for n in numbers:
    for letterGroup in letterGroups:
        subnumberCount = -4
        for r in range(4):
            subnumberCount += 4
            for l in letterGroup:
                letterGroupnumber = 5
                for r in range(4):
                    letterGroupnumber -= 1
                    subnumber = letterGroupnumber + subnumberCount
                    shapeRecordsSorted[recordCounter].record[5] = l
                    if len(str(subnumber)) == 2:
                        shapeRecordsSorted[recordCounter].record[6] = str(subnumber)
                    else:
                        shapeRecordsSorted[recordCounter].record[6] = '0' + str(subnumber)
                    recordCounter += 1

# Writer is pyshp 1.2 style, couldn't make 2.1 work
w = shapefile.Writer(shp.shapeType)
w.fields = list(shp.fields)

# https://gis.stackexchange.com/questions/102384/creating-records-in-output-shapefile-using-python
wRecords = []
wShapes = []
for sr in shapeRecordsSorted:
   wRecords.append(sr.record)
   wShapes.append(sr.shape)

# Check size, letters and number of letters
# def chunks(l, n):
#     n = max(1, n)
#     return (l[i:i+n] for i in range(0, len(l), n))
# recordsNested = []
# for r in chunks(wRecords, 256):
#     recordsNested.append(r)
# recordsNestedquestion = []
# for rN in recordsNested:
#     questions = []
#     questions.append(len(rN))
#     for r in rN:
#         if r[4] not in questions:
#              questions.append(r[4])
#     recordsNestedquestion.append(questions)
# for r in recordsNestedquestion:
#     print(len(r))

# Export to shp file
w._shapes.extend(wShapes)
w.records.extend(wRecords)
w.save('./Survey_of_India_output/Survey_of_India_output')
