from ReadSort import *
from matplotlib.figure import Figure


class CreatePlot:

    def __init__(self, collection, db_1, db_2, db_3, db_type):
        '''
        Constructor initializes fig variable, which is a figure plotted by plot_data method.
        :param collection: MongoDB collection
        :param db_1: 2016 database
        :param db_2: 2016 database
        :param db_3: 2016 database
        :param db_type: database type, passed by GUI, Traffic/Incidents
        '''

        self.fig = self.plot_data(collection, db_1, db_2, db_3, db_type)

    def return_top_value(self, collection, db, db_type):
        '''
        Method uses sorting methods from ReadSort class to return the highest value of
        a database given its type.
        :param collection: MongoDB collection
        :param db: database ID to be analyzed
        :param db_type: database type, Traffic/Incidents
        :return: data: the highest value of Traffic Volume or Incidents Total in a database
        '''

        # Importing ReadSort class and initializing data variable
        db_in = ReadSort(collection, db)
        data = ''

        # Data is equal to the highest value of a given database, depending on if it is Traffic/Incident
        if db_type == 'Traffic':
            db_in = db_in.sort_traffic()
            highest_row = db_in.nlargest(1, ['volume'])
            data = highest_row['volume']
        elif db_type == 'Incidents':
            db_in = db_in.sort_incidents()
            highest_row = db_in.nlargest(1, ['total'])
            data = highest_row['total']

        return int(data)

    def plot_data(self, collection, db_1, db_2, db_3, db_type):
        '''
        Method plots the highest value of data from all years into a figure.
        :param collection: MongoDB collection
        :param db_1: 2016 database
        :param db_2: 2016 database
        :param db_3: 2016 database
        :param db_type: database type, Traffic/Incidents, passed by GUI
        :return: fig: figure plotted by method
        '''

        # Getting names of x-axis data points which are the years represented
        n1 = db_1.replace(db_type, '')
        n2 = db_2.replace(db_type, '')
        n3 = db_3.replace(db_type, '')
        names = [n1, n2, n3]

        # Getting corresponding top values of the years represented for y-axis
        v1 = self.return_top_value(collection, db_1, db_type)
        v2 = self.return_top_value(collection, db_2, db_type)
        v3 = self.return_top_value(collection, db_3, db_type)
        values = [v1, v2, v3]

        # Creating figure
        fig = Figure(figsize=(10, 10))
        plt = fig.add_subplot(1, 2, 2)
        plt.scatter(names, values)
        plt.plot(names, values)

        # Setting labels
        plt.set_xlabel('Year')
        if db_type == 'Traffic':
            plt.set_ylabel('Maximum Traffic Volume')
        elif db_type == 'Incidents':
            plt.set_ylabel('Maximum Number of Incidents')

        return fig
