import json, sys

class Client:
    file = 0
    data = 0

    end_points = 0
    switches = 0
    linksDemanded = 0

    possibleCircuits = 0
    links = 0

    duration = 0
    demands = 0

    simulationDemandSuccess = []
    results = []

    def __init__(self, _file: str) -> None:
        self.file = _file
        self.ReadJSON()
        self.RunDemands()
        self.PrintDemands()
        exit(0)
  
    def ReadJSON(self) -> None:
        try:
            f = open(self.file)
            self.data = json.loads(f.read())
            self.end_points = self.data["end-points"]
            self.switches = self.data["switches"]
            self.possibleCircuits = self.data["possible-circuits"]
            self.links = self.data["links"]
            self.duration = self.data["simulation"]["duration"]
            self.demands = self.data["simulation"]["demands"]
            self.simulationDemandSuccess = {x: False for x in range(len(self.data["simulation"]["demands"]))}
            f.close()

        except:
            print("The file cannot be opened.")
            self.data = 0
            self.end_points = 0
            self.switches = 0
            self.possibleCircuits = 0
            self.links = 0
            self.duration = 0
            self.demands = 0
            self.linksDemanded = 0


    def RunDemands(self) -> None:
        time = 1
        while (time <= self.duration):
            demand_num = 0
            for demand in self.demands:
                if (demand["start-time"] == time):
                    
                    circuit = self.FindCircuit(demand["end-points"])

                    if (circuit == []): # there is no existing route
                        self.results.append(["foglalás", demand["end-points"], time, "sikertelen"]) # unsuccessful demand
                        continue
                    
                    if self.IsCircuitSufficient(circuit, demand["demand"]) == False: # the capacity of the route is not sufficient
                        self.results.append(["foglalás", demand["end-points"], time, "sikertelen"]) # unsuccessful demand
                        continue

                    try:
                        self.DemandCircuit(circuit, demand["demand"])
                        self.results.append(["foglalás", demand["end-points"], time, "sikeres"]) # successful demand
                        self.simulationDemandSuccess[demand_num] = True
                    except:
                        self.results.append(["foglalás", demand["end-points"], time, "sikertelen"])

                if (demand["end-time"] == time) & (self.simulationDemandSuccess[demand_num]):
                    # FELSZABADITASSAL KELL FOLYTATNI !!!

                    circuit = self.FindCircuit(demand["end-points"])

                    if (circuit == []): # there is no existing route
                        self.results.append(["felszabadítás", demand["end-points"], time, "sikertelen"]) # unsuccessful undemand
                        continue

                    try:
                        self.UndemandCircuit(circuit, demand["demand"])
                        self.results.append(["felszabadítás", demand["end-points"], time, "sikeres"]) # successful undemand
                        self.simulationDemandSuccess[demand_num] = False
                    except:
                        self.results.append(["felszabadítás", demand["end-points"], time, "sikertelen"])
                
                demand_num += 1
            time += 1

    def FindCircuit(self, endPoints) -> list: # returns the first possible Circuit if it exists
        for circuit in self.possibleCircuits:
            if (circuit[0] == endPoints[0]) & (circuit[-1] == endPoints[1]):
                return circuit
        
        return []
    
    def IsCircuitSufficient(self, circuit, demand) -> bool: #checks if the circuit is sufficient for the demand
        for i in range(len(circuit)-1): # going on the circuit pointpairs to pointpairs
            for link in self.links: # finding the appropriate link
                if link["points"] == [circuit[i], circuit[i+1]]: # there must be a link...
                    if link["capacity"] - demand < 0: # the capacity is not sufficient for the demand
                        return False
                    
                    break
        
        return True # the whole circuit was sufficient for the demand

    def DemandCircuit(self, circuit, demand) -> None: #demands the circuit. Can only be run if the circuit is sufficient
        for i in range(len(circuit)-1): # going on the circuit pointpairs to pointpairs
            for link in self.links: # finding the appropriate link
                if link["points"] == [circuit[i], circuit[i+1]]: # there must be a link...
                    link["capacity"] -= demand
                    break

    def UndemandCircuit(self, circuit, demand) -> None:
        for i in range(len(circuit)-1): # going on the circuit pointpairs to pointpairs
            for link in self.links: # finding the appropriate link
                if link["points"] == [circuit[i], circuit[i+1]]: # there must be a link...
                    link["capacity"] += demand
                    
                    break


    def PrintDemands(self) -> None:
        request_num = 0
        for result in self.results:
            request_num += 1
            if (result[0] == "felszabadítás") & (result[3] == "sikeres"):
                print(f"{request_num}. igény {result[0]}: {result[1][0]}<->{result[1][1]} st:{result[2]}") #printing each demand
            else:
                print(f"{request_num}. igény {result[0]}: {result[1][0]}<->{result[1][1]} st:{result[2]} - {result[3]}") #printing each demand



if len(sys.argv) == 2:
    c = Client(sys.argv[1])
else:
    print("One argument requiered.")
    exit(-1)
