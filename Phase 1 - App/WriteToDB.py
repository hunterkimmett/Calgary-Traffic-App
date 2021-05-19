import pandas as pd


class WriteToDB:

    def __init__(self, collection, csv_in, data_type, year):
        '''
        Constructor takes input parameters to write csv data into a pandas dataframe
        using one of the writing methods, depending on the type of data. The id is a
        combination of the data type and its year.
        :param collection: MongoDB collection to write dataframe to.
        :param csv_in: .csv file to be read converted to a dataframe.
        :param data_type: Traffic or Incidents
        :param year: the year the data is from
        '''

        # If-else to decide which dataframe writing method to use, depending on data type
        if data_type == 'Traffic':
            self.data = self.write_traffic(csv_in)
        elif data_type == 'Incidents':
            self.write_incidents(csv_in)
            self.data = self.write_incidents(csv_in)
        else:
            self.data = 'Error'

        # Writing dataframe to MongoDB
        post = {'_id': data_type + str(year), 'data': self.data}
        collection.insert_one(post)

    def write_traffic(self, csv_in):
        '''
        Method writes data from csv_in into a pandas dataframe, and then into a dictionary.
        Specific to Traffic, headers must be standardized.
        :param csv_in: .csv file to be read
        :return: df_dict: pandas dataframe in dictionary form
        '''

        # Reading document and parsing the headers
        df = pd.read_csv(csv_in)
        headers = list(df.columns)

        # Standardizing headers so that they all are the same
        for i, s in enumerate(headers):
            s = s.lower()
            if s.__contains__('year'):
                headers[i] = 'year'
            elif s.__contains__('sec') or s.__contains__('seg'):
                headers[i] = 'secname'
            elif s.__contains__('length'):
                headers[i] = 'length'
            elif s.__contains__('volume'):
                headers[i] = 'volume'
            elif s.__contains__('geom') or s.__contains__('multiline'):
                headers[i] = 'the_geom'

        # Creating pandas dataframe based on headers with the same order
        df.columns = headers
        df = df[['secname', 'volume', 'the_geom', 'year']]

        # Converting dataframe to dictionary and returning the dictionary
        df_dict = df.to_dict('records')
        return df_dict

    def write_incidents(self, csv_in):
        '''
        Method writes data from csv_in into a pandas dataframe, and then into a dictionary.
        Specific to Incidents, formatting in csv file is already the same.
        :param csv_in: .csv file to be read
        :return: df_dict: pandas dataframe in dictionary form
        '''

        # Reading document and parsing the headers
        df = pd.read_csv(csv_in)
        headers = list(df.columns)

        # For simplicity making headers lowercase
        for i, s in enumerate(headers):
            headers[i] = s.lower()

        # Creating pandas dataframe based on headers with the same order
        df.columns = headers
        df = df[['incident info', 'description', 'start_dt', 'modified_dt', 'quadrant', 'longitude',
                 'latitude', 'location', 'count']]

        # Converting dataframe to dictionary and returning the dictionary
        df_dict = df.to_dict('records')
        return df_dict
