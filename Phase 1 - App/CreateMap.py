import folium
from ReadSort import *


class CreateMap:

    def __init__(self, collection, db_in, db_type):
        '''
        Constructor creates map.html file from inputs using either the get_traffic or
        get_incidents method depending on database type, whose returned values are used
        in create_map method to do the actual creation of the map file.
        :param collection: MongoDB collection
        :param db_in: database ID of database used to create map
        :param db_type: type of database, Traffic/Incidents
        '''

        # Initializing 3 local variables to be used
        loc = ''   # Location: latitude and longitude of high volume/incident area
        desc = ''  # Description: Info of the high volume/incident area
        tool = ''  # Tooltip for map

        # Get local variable values based on type of database
        if db_type == 'Traffic':
            loc, desc = self.get_traffic(collection, db_in)
            tool = 'Maximum Traffic'
        elif db_type == 'Incidents':
            loc, desc = self.get_incidents(collection, db_in)
            tool = 'Maximum Incidents'

        # Creating map
        self.create_map(loc, desc, tool)


    def get_traffic(self, collection, db_in):
        '''
        Method gets values for location of highest traffic volume from parameters input
        using ReadSort's sort_traffic method.
        :param collection: MongoDB collection
        :param db_in: database ID of database used to create map
        :return: loc, desc: location [lat,lon] and description of highest value
        '''

        # Importing ReadSort and getting dataframe
        rs = ReadSort(collection, db_in)
        df = rs.sort_traffic()

        # Getting row with highest value of volume
        highest_row = df.nlargest(1, ['volume'])

        # Assigning the value of secname and the_geom columns to desc and loc respectively
        desc = highest_row['secname'].item()
        loc = highest_row['the_geom'].item()

        # Formatting loc to remove non-numerical values, split into a list, and reformatting entries in list
        loc = loc.replace('MULTILINESTRING ((', '').replace('))', '')
        loc = loc.split(',')
        for i, s in enumerate(loc):
            loc[i] = s.strip().replace(' ', ', ')

        # Taking the first value of the list and splitting, then reversing order and returning variables
        loc_1 = loc[0].split(',')
        new_loc = loc_1[1] + ', ' + loc_1[0]
        return new_loc, desc

    def get_incidents(self, collection, db_in):
        '''
        Method gets values for location of highest incident total from parameters input
        using ReadSort's sort_traffic method.
        :param collection: MongoDB collection
        :param db_in: database ID of database used to create map
        :return: loc, desc: location [lat,lon] and description of highest value
        '''

        # Importing ReadSort and getting dataframe
        rs = ReadSort(collection, db_in)
        df = rs.sort_incidents()

        # Getting row with highest value of total
        highest_row = df.nlargest(1, ['total'])

        # Assigning the value of incident info and location columns to desc and loc respectively
        desc = highest_row['incident info'].item()
        loc = highest_row['location']
        loc = loc.item().strip('()')

        return loc, desc

    def create_map(self, loc, desc, tool):
        '''
        Creates map .html file with point at a location based on parameters using folium.
        :param loc: Location: latitude and longitude of high volume/incident area
        :param desc: Description: Info of the high volume/incident area
        :param tool: Tooltip for map
        :return:
        '''

        # Splitting and stripping location data
        loc = loc.split(',')
        for i, s in enumerate(loc):
            loc[i] = float(s.strip())

        # Latitude and longitude values
        lat = loc[0]
        lon = loc[1]

        # Creating map area, overview of Calgary
        m = folium.Map(location=[51.0265822, -114.0979545], zoom_start=10)

        # Placing marker at location with popup and tooltip
        folium.Marker([lat, lon], popup=desc, tooltip=tool).add_to(m)

        # Creating map.html file
        m.save('map.html')
