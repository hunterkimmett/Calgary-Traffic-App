import pandas as pd


class ReadSort:

    def __init__(self, collection, input_id):
        '''
        Constructor just initializes collection and the input_id to be used in
        other methods.
        :param collection: MongoDB collection to take data from
        :param input_id: MongoDB ID of the data to be taken
        '''
        self.collection = collection
        self.input_id = input_id

    def read_db(self):
        '''
        Reads the specified document on MongoDB and writes the data into a pandas dataframe.
        :return: df: pandas dataframe
        '''

        data_db = self.collection.find_one({'_id': self.input_id})
        df = pd.DataFrame(data_db['data'])
        return df

    def sort_traffic(self):
        '''
        Sorts traffic based on values in 'volume' column in a pandas dataframe, produced
        with read_db. Specific to Traffic type data.
        :return: df_sorted: pandas dataframe sorted by volume of traffic.
        '''

        df = self.read_db()
        df_sorted = df.sort_values('volume', ascending=False)
        return df_sorted

    def sort_incidents(self):
        '''
        Sorts traffic based on number of incidents at a location in a pandas dataframe,
        produced with read_db. Need to count and delete duplicates to find number of
        incidents. Specific to Incidents type data.
        :return: df_sorted: pandas dataframe sorted by total incidents.
        '''

        # Reading database and filtering out non-incident events, writing dataframe
        df = self.read_db()
        df_incidents = df[df['description'].str.contains('incident', case=False)]

        # Counting duplicates 'incident info' into 'total' column, sorting by incident info
        df_dups = df_incidents.groupby(['incident info']).size().reset_index(name='total')
        df_dups = df_dups.sort_values('incident info')

        # Dropping duplicates of 'incident info' in dataframe and sorting by incident info
        df_dropped = df_incidents.drop_duplicates(subset='incident info', keep='first')
        df_dropped = df_dropped.sort_values('incident info')

        # Merging dataframes with counted and dropped duplicates, creating new dataframe
        df_comb = df_dups.merge(df_dropped, how='inner')
        df_comb = df_comb[['incident info', 'description', 'start_dt', 'modified_dt', 'quadrant', 'longitude',
                           'latitude', 'location', 'count', 'total']]

        # Sorting and returning new dataframe by 'total' count
        df_sorted = df_comb.sort_values('total', ascending=False)
        return df_sorted
