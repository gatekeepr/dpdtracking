import pickle
import os

WAREHOUSE_FILENAME = 'parcelWarehouse.pkl'

# load persistent object file
def loadParcelList():
    if os.path.getsize(WAREHOUSE_FILENAME) > 0:      
        with open(WAREHOUSE_FILENAME, 'rb') as input:
            return pickle.load(input)
    else:
        return list()

# store persistent object file
def saveParcelList(parcelList):
    with open(WAREHOUSE_FILENAME, 'wb') as output:
        pickle.dump(parcelList, output, pickle.HIGHEST_PROTOCOL)