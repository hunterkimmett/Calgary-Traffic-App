import csv


class ParseIncidents:


    def __init__(self, csv_in):
        '''
        ParseIncidents class serves to parse values by year from a general Incidents file.
        The output is 3 separate .csv files for each year using the Incidents file in the constructor.
        '''

        self.parse_file(csv_in, '2016')
        self.parse_file(csv_in, '2017')
        self.parse_file(csv_in, '2018')

    def parse_file(self, csv_in, year):
        '''
        This method serves to read values for one specific year in a general csv file and write them
        into another. This is done based on the year the incident is reported in START_DT column.
        :param csv_in: Incidents file with many years
        :param year: the year to be parsed
        :return:
        '''

        with open(csv_in, 'r') as f_in, open('Traffic_Incidents_'+year+'.csv', 'w', newline='') as f_out:

            # Setting up reader and writer
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)

            # For every row, if row contains header or the year specified, write into new file
            for row in reader:
                if row[2].__contains__('START_DT') or row[2].__contains__(year):
                    writer.writerow(row[0:-1])
