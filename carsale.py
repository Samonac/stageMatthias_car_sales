from flask import Flask, render_template, json, request, redirect
carsales = Flask(__name__)
jsnfile = 'data/carslist.json'

import glob

def getIdList():
    idList = []
    carsJSON = []
    for name in findjson():
        with open(name) as cr :
            #carsJSON = json.load(cr)
            
            print(name)
            #carsJSON = {**carsJSON, **json.load(cr)}
            
            carsJSON = carsJSON + json.load(cr)
            print(carsJSON)
    for carTemp in carsJSON:
        print('carTemp : ', carTemp)
        if carTemp['id'] not in idList:
            try :          
                idList.append(int(carTemp['id']))
            except Exception as err:
                print(err)
    print('idList : ', idList)

    return idList


def findjson() :
    list=[]
    #print('Named explicitly:')
    for name in glob.glob('./data/*.json'):
        list.append(name)
        #print(name)
    return list


@carsales.route("/") #For default route
def main():
    carsJSON = []
    for name in findjson():
        with open(name) as cr :
            #carsJSON = json.load(cr)
            
            print(name)
            #carsJSON = {**carsJSON, **json.load(cr)}
            
            carsJSON = carsJSON + json.load(cr)
            print(carsJSON)
    # for carTemp in carsJSON:
    #     print('carTemp : ', carTemp)
    #     if carTemp['id'] not in idList:
    #         idList.append(carTemp['id'])
    # print('idList : ', idList)
    return render_template("carslist.html", cars=carsJSON)



@carsales.route("/truck_id",methods=["GET","POST"])
def truck_id():
    status = ""
    truck_id = "null"
    car = {}
    with open(jsnfile, 'r') as m : 
        data = json.load(m) 
        details = request.form
        try:
            truck_id = request.args.get('search').lower()
        except Exception as e:
            print(e)
            truck_id = request.args.get('truck_id').lower()
        print(f"looking for {truck_id} in {json.dumps(data).lower()}")
        # found=False
        if truck_id in json.dumps(data).lower():
            # found=True
        # if found:
            statusTemp = "found"
            for jsonTemp in data:
                if truck_id in json.dumps(jsonTemp).lower():
                    car = jsonTemp
                    print("Found car : ", car)
        else:
            statusTemp = "not found"
        print(statusTemp)
    

    # car = {} 
    # car['id'] = "id"
    # car['name'] = "name"
    # car['year'] = "year"
    # car['price'] = "price"

    return render_template("addcar.html", car = car)
    # return render_template('truck_id.html',status = statusTemp, truck_id=truck_id)

@carsales.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        car = {} 
        idIndex = 1
        idList = getIdList()
        idMin = sorted(idList)[0]
        idMax = sorted(idList)[len(idList) - 1]
        # for idTemp in sorted(idList):
        print("idMin : ", idMin)
        print("idMax : ", idMax)
        while idIndex >= idMin and idIndex <= idMax and idIndex in idList:
            # print("loop incrementing idIndex : ", idIndex)
            idIndex += 1
        

        car['id'] = idIndex
        car['name'] = ""
        car['year'] = ""
        car['price'] = ""
        return render_template("addcar.html", car = car)
    if request.method == 'POST':
        id = request.form["id"]
        name = request.form["name"]
        year = request.form["year"]
        price = request.form["price"]
        with open(jsnfile) as cr:
            cars = json.load(cr)
        cars.append({"id": id, "name": name, "year": year, "price": price})
        with open(jsnfile, 'w') as cw:
            json.dump(cars, cw)
        return redirect('/')

@carsales.route('/updatecar/<string:id>',methods = ['GET','POST'])
def updatecar(id):
    with open(jsnfile) as cr:
        cars = json.load(cr)
    if request.method == 'GET':
        car = [x for x in cars if x['id'] == id][0]
        if car == None:
            car = {} 
            car['id'] = "id"
            car['name'] = "name"
            car['year'] = "year"
            car['price'] = "price"
        return render_template("addcar.html", car = car)
    if request.method == 'POST':
        for car in cars:
            if(car['id'] == id):
                car['name'] = request.form["name"]
                car['year'] = request.form["year"]
                car['price'] = request.form["price"]
                break
        with open(jsnfile, 'w') as cw:
            json.dump(cars, cw)
        return redirect('/')

@carsales.route('/deletecar/<string:id>')
def deletecar(id):
    with open(jsnfile) as cr:
        cars = json.load(cr)
    newcarlist = []
    for car in cars:
        if(car['id'] != id):
            newcarlist.append(car)
    with open(jsnfile, 'w') as cw:
        json.dump(newcarlist, cw)
    return redirect('/')

if(__name__ == "__main__"):
    carsales.run()
