# inside python 3.7.5 venv pip install pyshp==1.2
import shapefile

shp = shapefile.Reader('./Survey_of_India_updated_python/SoI_one-inch_number_letter')

records = shp.records()

# Number counter
numbers = []

for i, r in enumerate(records):
    if r[4] not in numbers:
         numbers.append(r[4])

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
                    records[recordCounter][5] = l
                    if len(str(subnumber)) == 2:
                        records[recordCounter][6] = str(subnumber)
                    else:
                        records[recordCounter][6] = '0' + str(subnumber)
                    recordCounter += 1

shp.records = records

# Writer is pyshp 1.2 style, couldn't make 2.1 work
w = shapefile.Writer(shp.shapeType)
w.fields = list(shp.fields)
w._shapes.extend(shp.shapes())

w.records.extend(shp.records)

w.save('./Survey_of_India_output/Survey_of_India_output')
