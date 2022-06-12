import car_app.database.DBManager as dbm 
import car_app.database.models.Country as ct

class CountryManager:
    
    @staticmethod
    def all_countries():
        with dbm.DBManager.session() as session:
            return session.query(ct.Country).order_by(ct.Country.name).all()
        
    @staticmethod
    def all_countries_as_dict():
        countries = CountryManager.all_countries()
        countries_list = []
        for country in countries:
            countries_list.append(ct.Country.to_dict(country))
        return countries_list