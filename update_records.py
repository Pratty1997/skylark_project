import pymongo

class Add_Data:
    
    def __init__(self):
        try:
            self.connection=pymongo.MongoClient('localhost:27017')
            self.db=self.connection.skylark
            # Coordinate data of countries.
            self.records=self.db.records
            # Data of previous competitions
            self.data=self.db.data
            # New data addition requests
            self.new=self.db.new
            # Information change requests
            self.change=self.db.change

            # Coordinates
            self.coordinates={'EGYPT':[30.3697,28.3457],
                      'CAMEROON':[13.3697,6.3547],
                      'GHANA':[-1.3697,7.3547],
                      'NIGERIA':[7.3697,9.3547],
                      'IVORY COAST':[-5.3697,7.3547],
                      'DR CONGO':[24.3697,0.3547],
                      'ZAMBIA':[26.3697,-14.3547],
                      'TUNISIA':[9.3697,33.3547],
                      'SUDAN':[30.3697,15.3547],
                      'ALGERIA':[1.3697,28.3547],
                      'ETHIOPIA':[38.3697,8.3547],
                      'MOROCCO':[-8.3697,30.3547],
                      'SOUTH AFRICA':[24.3697,-28.3547],
                      'CONGO':[16.3697,0.3547],
                      'MALI':[-3.3697,16.3547],
                      'BURKINA FASO':[-1.3697,12.3547],
                      'SENEGAL':[-14.3697,15.3547],
                      'UGANDA':[32.3697,1.3547],
                      'GUINEA':[-10.3697,11.3547],
                      'LIBYA':[16.3697,28.3547],
                      'EQUATORIAL GUINEA':[10.3697,1.5],
                      'GABON':[12.3697,0.33547],
                      'UNITED ARAB REPUBLIC':[35.3697,30.3547],
                      'NIGERIA':[8.3697,9.3547],
                      'LIBYA':[18.3697,27.3547],
                      'ALGERIA':[4.3697,28.3547],
                      'ANGOLA':[18.3697,-12.3547]
                     }
            
            # ALL the previous records
            # Schema: KEY(Year of the competition) : (HOST,WINNER,RUNNER_UP,THIRD_PLACE);
            
            self.record={1957:['SUDAN','EGYPT','ETHIOPIA','SUDAN'],
                          1959:['UNITED ARAB REPUBLIC','UNITED ARAB REPUBLIC','SUDAN','ETHIOPIA'],
                          1962:['ETHIOPIA','ETHIOPIA','UNITED ARAB REPUBLIC','TUNISIA'],
                          1963:['GHANA','GHANA','SUDAN','UNITED ARAB REPUBLIC'],
                          1965:['TUNISIA','GHANA','TUNISIA','IVORY COAST'],
                          1968:['ETHIOPIA','CONGO','GHANA','IVORY COAST'],
                          1970:['SUDAN','SUDAN','GHANA','UNITED ARAB REPUBLIC'],
                          1972:['CAMEROON','CONGO','MALI','CAMEROON'],
                          1974:['EGYPT','ZAIRE','ZAMBIA','EGYPT'],
                          1976:['ETHIOPIA','N/A','N/A','N/A'],
                          1978:['GHANA','GHANA','UGANDA','NIGERIA'],
                          1980:['NIGERIA','NIGERIA','ALGERIA','MOROCCO'],
                          1982:['LIBYA','GHANA','LIBYA','ZAMBIA'],
                          1984:['IVORY COAST','CAMEROON','NIGERIA','ALGERIA'],
                          1986:['EGYPT','EGYPT','CAMEROON','IVORY COAST'],
                          1988:['MOROCCO','CAMEROON','NIGERIA','ALGERIA'],
                          1990:['ALGERIA','ALGERIA','NIGERIA','ZAMBIA'],
                          1992:['SENEGAL','IVORY COAST','GHANA','NIGERIA'],
                          1994:['TUNISIA','NIGERIA','ZAMBIA','IVORY COAST'],
                          1996:['SOUTH AFRICA','SOUTH AFRICA','TUNISIA','ZAMBIA'],
                          1998:['BURKINA FASO','EGYPT','SOUTH AFRICA','DR CONGO'],
                          2000:['GHANA','CAMEROON','NIGERIA','SOUTH AFRICA'],
                          2002:['MALI','CAMEROON','SENEGAL','NIGERIA'],
                          2004:['TUNISIA','TUNISIA','MOROCCO','NIGERIA'],
                          2006:['EGYPT','EGYPT','IVORY COAST','NIGERIA'],
                          2008:['GHANA','EGYPT','CAMEROON','GHANA'],
                          2010:['ANGOLA','EGYPT','GHANA','NIGERIA'],
                          2012:['GABON','ZAMBIA','IVORY COAST','MAIL'],
                          2013:['SOUTH AFRICA','NIGERIA','BURKINA FASO','MAIL'],
                          2015:['EQUITORIAL GUINEA','IVORY COAST','GHANA','DR CONGO'],
                          2017:['GABON','CAMEROON','EGYPT','BURKINA FASO'],
                          2019:['CAMEROON','','',''],
                          2021:['IVORY COAST','','',''],
                          2023:['GUINEA','','','']
                          }
        except Exception as e:
            print(e)

    def add_coordinates(self):
        for key,val in self.coordinates.items():
            # 200 :- OK
            insert={'_id':key,'coordinates':val}
            try:
                self.records.insert_one(insert)
                self.connection.close()
            except Exception as e:
                print(e)
                self.connection.close()

    def update_coordinates(self,country,coordinates):
        update={"_id":country,"coordinates":coordinates}
        match={"_id":country}
        self.records.update_one(match,{"$set":update},upsert=True)

    def add_records(self):
        for key,val in self.record.items():
            year=key
            host=val[0]
            winner=val[1]
            runner=val[2]
            third=val[3]
            insert={"_id":year,'host':host,'winner':winner,'runnerup':runner,'third':third}
            try:
                self.data.insert_one(insert)
                self.connection.close()
                print(insert)
            
            except Exception as e:
                print(e)
                self.connection.close()
                

    def add_new(self,year,host):
        # 200 for OK.
        # 400 for an error.
        insert={'year':year,'host':host}
        try:
            self.new.insert_one(insert)
            print("New request received.")
            self.connection.close()
            return 200
        except Exception as e:
            print(e)
            self.connection.close()
            return 400

    def change(self,info):
        # 200 :- OK
        # 400 :- Error
        insert={'message':info}
        try:
            self.change.insert_one(insert)
            self.connection.close()
            # Request for change in data placed successfully.
            return 200
        except Exception as e:
            self.connection.close()
            print(e)
            # Error occurred, couldn't place the request to change the data.
            return 400

    def find_record(self,year):
        find={'_id':int(year)}
        found=self.data.find_one(find)
        return found

    def find_by_country(self,country):
        find={'host':country}
        found=self.data.find(find)
        return found
    
    
    def send_data(self):
        country_data=self.records.find({})
        send=[]
        temp={}
        record=self.data.find({})
        for i in country_data:
            temp[i['_id']]=i['coordinates']
        for i in record:
            d={}
            d['host']=i['host']
            d['year']=i['_id']
            d['coordinates']=temp[i['host']]
            send.append(d)
        return send
    
# Test code.
a=Add_Data()
#a.send_data()
#print(a.add_coordinates())
a.add_records()
#a.update_coordinates("INDIA",[102.22,10.22])
"""resp=a.add_new(2025,"EGYPT")
if(resp==200):
    print("Hi, We've received your request for the new addition. We'll verify it, and add it. Thank you for contacting us. Greetings!")
"""
