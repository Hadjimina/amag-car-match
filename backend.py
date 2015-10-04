import tornado.web
import tornado.ioloop
import mysql.connector
import argparse
import mimetypes
import random

def hardcode_features(selected):
  sport = { 'feature': "sport", 'caption': "Sport Wagen" }
  family = { 'feature': "family", 'caption': "Familien Wagen" }
  offroader = { 'feature': "offroader", 'caption': "Offroader" }

  #price:
  minP = { 'feature': "grenzeLow", 'caption': 10000 }
  medP = { 'feature': "grenzeMed", 'caption': 20000 }
  maxP = { 'feature': "grenzeHigh", 'caption': 30000 }

  inStrArray = ""
  #sale_type:
  new = { 'feature': "new", 'caption': "Neu" }
  occ = { 'feature': "occ", 'caption': "Occasion" }
  demo = { 'feature': "demo", 'caption': "Demo" }

  #gear_type:
  gear = { 'feature': "gear", 'caption': "Geschaltet" }
  auto = { 'feature': "auto", 'caption': "Automat" }

  #brand:
  vw = { 'feature': "vw", 'caption': "VW" }
  audi = { 'feature': "audi", 'caption': "Audi" }
  skoda = { 'feature': "skoda", 'caption': "Skoda" }
  misc = { 'feature': "misc", 'caption': "Andere" }
  #!!!MISC = ANDERE !!!!

  #color:
  red = { 'feature': "red", 'caption': "Rot" }
  black = { 'feature': "black", 'caption': "Schwarz" }
  silver = { 'feature': "silver", 'caption': "Silver" }
  misc_color = { 'feature': "misc_color", 'caption': "Andere" }

  #fueltyp:
  gasoline = { 'feature': "gasoline", 'caption': "Benzin" }
  diesel = { 'feature': "diesel", 'caption': "Diesel" }
  hybrid = { 'feature': "hybrid", 'caption': "Hybrid" }
  elec = { 'feature': "elec", 'caption': "Elektrisch" }

  #Hash for every super Bubble with children to hashes which represent the feature Bubble
  carType = { 'feature': "type", 'caption': "Auto Kategorie" , 'children': [sport,family,offroader] }
  price = { 'feature': "price", 'caption': "Preis" , 'children': [minP,medP,maxP] }
  sale_type = { 'feature': "sale_type", 'caption': "Verkaufstyp" , 'children': [new,occ,demo] }
  gear_type = { 'feature': "gear_type", 'caption': "Schaltung" , 'children': [gear,auto] }
  brand = { 'feature': "brand", 'caption': "Marke" , 'children': [vw,audi,skoda,misc] }
  color = { 'feature': "color", 'caption': "Farbe" , 'children': [red,black,silver,misc_color] }
  fueltype = { 'feature': "fueltype", 'caption': "Treibstoff" , 'children': [gasoline,diesel,hybrid,elec] }

  categories = [carType, price, sale_type, brand, gear_type, color, fueltype]

  print(selected)
  
  result = []
  for category in categories:
    if not any(child['feature'] in selected for child in category['children']):
      result.append(category)
  
  return result

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, cnx):
        self.cnx = cnx

    def get(self, cmd):
        if cmd == 'index' or cmd == '':
            self.render("index.html")
        elif cmd == 'get_results':
            features = self.get_arguments('feature')
            print(features)

            query = "SELECT vehicle.vin, vehicle.price,vehicle.brand,vehicle.model_de,vehicle.model_year FROM `vehicle` INNER JOIN `gear_type` ON vehicle.gear_type=gear_type.id INNER JOIN `exterior_color` ON vehicle.exterior_color=exterior_color.id  WHERE "
#SELECT * FROM `vehicle` INNER JOIN `exterior_color` ON vehicle.exterior_color=exterior_color.id  WHERE `exterior_color`.category = 'black'
            queryArray = []


            #TYPE
            if "sport" in features:
                typ = "`sport_score` >= 3"
                queryArray.append(typ)
            elif "family" in features:
                typ = "`family_score` >= 3"
                queryArray.append(typ)
            elif "offroader" in features:
                typ = " `offroad_score` >= 3"
                queryArray.append(typ)

            #PRICE

            #SALE TYPE
            if "new" in features:
                sale_typ = "`sale_type` = 'Neu'"
                queryArray.append(sale_typ)
            elif "occ" in features:
                sale_typ = "`sale_type` = 'Occ'"
                queryArray.append(sale_typ)
            elif "dem" in features:
                sale_typ = "`sale_type` = 'Demo'"
                queryArray.append(sale_typ)


            #GEAR TYPE
            if "gear" in features:
                gear_typ ="`gear_type`.category = 'Manual'"
                queryArray.append(gear_typ)
            elif "auto" in features:
                gear_typ ="`gear_type`.category = 'Automatic'"
                queryArray.append(gear_typ)

            #BRAND TYPE
            if "vw" in features:
                brand = "`brand` = 'VW'"
                queryArray.append(brand)
            elif "audi" in features:
                brand = "`brand` = 'Audi'"
                queryArray.append(brand)
            elif "skoda" in features:
                brand = "`brand` = 'SKODA'"
                queryArray.append(brand)
            elif "misc" in features:
                brand = "NOT `brand` = 'SKODA' AND NOT `brand` = 'Audi' AND NOT `brand` = 'VW'"
                queryArray.append(brand)


            #COLOR
            if "red" in features:
                color ="`exterior_color`.category = 'red'"
                queryArray.append(color)
            elif "black" in features:
                color ="`exterior_color`.category = 'black'"
                queryArray.append(color)
            elif "silver" in features:
                color ="`exterior_color`.category = 'silver'"
                queryArray.append(color)
            else:
                color ="NOT `exterior_color`.category = 'red' AND NOT `exterior_color`.category = 'black' AND NOT `exterior_color`.category = 'silver'"
                queryArray.append(color)


            #FUEL TYPE
            if "gasoline" in features:
                fuel_type = "`fuel_type` = 'B'"
                queryArray.append(fuel_type)
            elif "diesel" in features:
                fuel_type = "`fuel_type` = 'D'"
                queryArray.append(fuel_type)
            elif "hybrid" in features:
                fuel_type = "`fuel_type` = 'PH'"
                queryArray.append(fuel_type)
            elif "elec" in features:
                fuel_type = "`fuel_type` = 'E'"
                queryArray.append(fuel_type)
            
            #PRICE
            if "grenzeLow" in features:
                price = "`price_score` >= 4"
                queryArray.append(price)
            elif "grenzeLMed" in features:
                price = "`price_score`  >= 2"
                queryArray.append(price)
            elif "grenzeHigh" in features:
                price = "`price_score` = 1"
                queryArray.append(price)


            finalQuery = query + " AND ".join(queryArray)


            cursor = self.cnx.cursor()
            cursor.execute(finalQuery)

            results = []
            for vin, price, brand, caption, year in cursor:
                results.append({
                    'caption': caption,
                    'vin': vin,
                    'price': price, 
                    'brand': brand,
                    'year': year
                })

            if len(results) > 200:
                sap = random.sample(results, 200)
            else:
                sap = results
                
            self.write({"cars": sap, "count": len(results)})
        elif cmd == 'get_bullets':
            features = self.get_arguments('feature')
            
            self.write({'features': hardcode_features(features)[0:4]})
        else:
            self.send_error(404)

class ImageHandler(tornado.web.RequestHandler):
    def initialize(self, cnx):
        self.cnx = cnx
    
    def get(self, vin):
        cursor = self.cnx.cursor()
        cursor.execute("SELECT `name`, `image_data` FROM `vehicle_image` WHERE `vehicle_vin` = %s LIMIT 1", (vin, ))
        
        for (name, image_data) in cursor:
            self.set_header("Content-Type", mimetypes.guess_type(name)[0])
            self.write(image_data)
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)

    args = parser.parse_args()


    cnx = mysql.connector.connect(user='root', password='amaghackzurich',
                                  host='localhost',
                                  database='hackzurich')

    app = tornado.web.Application([
            (r"/feature/(.*)", tornado.web.StaticFileHandler, {"path": "/root/elio/feature/"}),
            (r"/image/(.*)", ImageHandler, {'cnx': cnx}),
            (r"/(.*)", MainHandler, {'cnx': cnx}),
        ],
        debug=True
    )
    app.listen(address='', port=args.port)
    tornado.ioloop.IOLoop.current().start()

    cnx.close()

if __name__ == "__main__":
    main()
