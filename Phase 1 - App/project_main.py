from pymongo import MongoClient
from WriteToDB import *
from ParseIncidents import *
from GUI import *


def main():

    # Open MongoDB Cluster and collection where data will be written
    cluster = MongoClient(
        "mongodb+srv://HunterKimmett:ENSF592@cluster0.s3zzo.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = cluster["ensf592project"]
    collection = db["p1"]
    collection.delete_many({})  # Clear the data in collection

    # Parsing the Incidents csv file to separate csv files for each year
    print('Parsing Incident .csv file...')
    ParseIncidents('Calgary-Traffic-App/Phase 1 - App/data/Traffic_Incidents.csv')

    # Writing data from Traffic csv files into MongoDB using WriteToDB class
    print('Done. Reading/writing Traffic .csv files to MongoDB...')
    WriteToDB(collection, 'Calgary-Traffic-App/Phase 1 - App/data/TrafficFlow2016_OpenData.csv', 'Traffic', 2016)
    WriteToDB(collection, 'Calgary-Traffic-App/Phase 1 - App/data/2017_Traffic_Volume_Flow.csv', 'Traffic', 2017)
    WriteToDB(collection, 'Calgary-Traffic-App/Phase 1 - App/data/Traffic_Volumes_for_2018.csv', 'Traffic', 2018)

    # Writing data from Incident csv files into MongoDB using WriteToDB class
    print('Done. Reading/writing Incident .csv files to MongoDB...')
    WriteToDB(collection, 'Calgary-Traffic-App/Phase 1 - App/data/Traffic_Incidents_2016.csv', 'Incidents', 2016)
    WriteToDB(collection, 'Calgary-Traffic-App/Phase 1 - App/data/Traffic_Incidents_2017.csv', 'Incidents', 2017)
    WriteToDB(collection, 'Calgary-Traffic-App/Phase 1 - App/data/Traffic_Incidents_2018.csv', 'Incidents', 2018)
    print('Done. Starting GUI...')

    # Running GUI
    root = tk.Tk()
    root.title('Calgary Traffic Analysis')
    app = GUI(root, collection)
    root.mainloop()


if __name__ == '__main__':
    main()
