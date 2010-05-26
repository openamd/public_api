Application
-----------

  * Implement a basic query using alexandra ( http://github.com/dziegler/alexandra )

  * Change the schema keyspace name from HOPE2008 to HOPE2010

  * Document the following schema a la http://arin.me/blog/wtf-is-a-supercolumn-cassandra-data-model

    <Keyspace Name="HOPE2008">
       <!-- Holds Historical Locations and Users Facing each other -->
       <ColumnFamily ColumnType="Super"
                     CompareWith="UTF8Type"
                     CompareSubcolumnsWith="UTF8Type"
                     Name="LocationHistory"/>
       <ColumnFamily Name="Speakers"/>
       <ColumnFamily Name="Talks"/>
       <!-- Holds Pings and when Users face each other -->
       <ColumnFamily Name="UserInteractions"/>

       <ColumnFamily Name="ConferenceRegions"/>
       <ColumnFamily Name="TagReaderLocations"/>
       <!-- Holds Country, Cell Providers, Current Location and Interests -->
       <ColumnFamily Name="Users"/>
     </Keyspace>

API
---

  * Remove prefix /api/ from official api
  * Respond correctly for json, html requests