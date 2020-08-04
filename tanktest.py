
Durm, Donald Delano. (JSC-CI531)[SGT, INC]
1:59 PM (1 minute ago)
to me

# -*- coding: utf-8 -*-

"""
Created on Thu Mar 26 10:42:04 2020



@author: Donnie
"""

import sys
import math 

 

class FlowPath():
    def __init__(self, name, flowpath_From, flowpath_To, dia, cd_user):
        self.__name  = name
        self.flowPath_From = flowpath_From
        self.flowPath_To = flowpath_To
        self.opening_Diameter = dia
        self.cd = cd_user

     

    @property
    def name(self):
        return self.__name

   

    @name.setter
    def name(self, name):
        self.__name = name   



    @property
    def opening_Diameter(self):
        return self.__opening_Diameter

   

    @opening_Diameter.setter
    def opening_Diameter(self, dia):
        self.__opening_Diameter = dia 

        

        

    @property
    def cd(self):
        return self.__cd

   

    @cd.setter
    def cd(self, number):
        self.__cd = number  

        

        

    @property
    def flowPath_From(self):
        return self.__flowPath_From

   

    @flowPath_From.setter
    def flowPath_From(self, flowpath):
        self.__flowPath_From = flowpath  

 

    @property
    def flowPath_To(self):
        return self.flowPath_To

      

    @flowPath_To.setter
    def flowPath_To(self, flowpath):
        self.flowPath_To = flowpath

       

          

 

# The graph nodes.
class Tank(object):
    def __init__(self, name):
        self.__name  = name
        self.__links = set()
        self.__flowPaths = set()

 

    @property
    def name(self):
        return self.__name

 

    @property
    def links(self):
        return set(self.__links)

   

    

    @property #psia
    def pressure(self):
        return self.__pressure

   

    @pressure.setter
    def pressure(self, number):
        self.__pressure = number

   

    

    @property #F
    def temperature(self):
        return self.__temperature

   

    @temperature.setter
    def temperature(self, number):
        self.__temperature = number

 

 

    @property #lbm
    def mass(self):
        return self.__mass

   

    @mass.setter
    def mass(self, number):
        self.__mass = number

 

 

    @property #lbm
    def mass_bank(self):
        return self.__mass_bank

   

    @mass_bank.setter
    def mass_bank(self, number):
        self.__mass_bank = number

 

 

    @property #ft^3
    def volume(self):
        return self.__volume

 

    @volume.setter
    def volume(self, number):
        self.__volume = number

 

 

 

    def get_flowPaths(self):
        return self.__flowPaths

 

    def add_flowPath(self, flowPathFrom, flowPathTo, dia, cd_user):
        flowpath = FlowPath(flowPathFrom.name + '-->' + flowPathTo.name, flowPathFrom, flowPathTo, dia, cd_user)
        self.__flowPaths.add(flowpath)

       

    def remove_flowPath(self, flowPath):
        self.__flowPaths.remove(flowPath)

 

 

 

    def get_links(self):
        return self.__links

 

    def add_link(self, other, dia, cd_user):
        self.__links.add(other)
        other.__links.add(self)

       

        #Add FlowPath - I tried to make Links an object, but that method had issues
        self.add_flowPath(self, other, dia, cd_user)

      

    def remove_link(self, other):
        self.__links.remove(other)
        other.__links.remove(self)

   


# The function to look for connected components.
def connected_tanks(tanks):
 

    # List of connected components found. The order is random.
    result = []

 

    # Make a copy of the set, so we can modify it.
    tanks = set(tanks)

 

    # Iterate while we still have nodes to process.
    while tanks:

 

        # Get a random node and remove it from the global set.
        n = tanks.pop()

 

        # This set will contain the next group of nodes connected to each other.
        group = {n}

 

        # Build a queue with this node in it.
        queue = [n]

 

        # Iterate the queue.
        # When it's empty, we finished visiting a group of connected nodes.
        while queue:
 

            # Consume the next item from the queue.
            n = queue.pop(0)

      

            # Fetch the neighbors.
            neighbors = n.links


            # Remove the neighbors we already visited.
            neighbors.difference_update(group)

 

            # Remove the remaining nodes from the global set.
            tanks.difference_update(neighbors)

 

            # Add them to the group of connected nodes.
            group.update(neighbors)

 

            # Add them to the queue, so we visit them in the next iterations.
            queue.extend(neighbors)

 

        # Add the group to the list of groups.
        result.append(group)

 

    # Return the list of groups.
    return result

 

def calculate_mass(p, temp, vol):
    return ((p*vol*28.97)/(10.73*(temp)))      

 

def calculate_pressure(m, temp, vol):
    return ((m*(10.73*(temp)))/(vol*28.97))


 

 

def calculate_mdot(P_Upstream, P_Downstream, T_Upstream, T_Downstream, dia, cd):

 

    if abs(P_Upstream - P_Downstream) > 0.000000001:
       
        sign = (P_Upstream - P_Downstream) / abs(P_Upstream - P_Downstream)
        #print("Sign: " + str(sign))

       
        if P_Upstream < P_Downstream:
            dummy = P_Upstream
            dummy2 = T_Upstream
            P_Upstream = P_Downstream
            T_Upstream = T_Downstream
            P_Downstream = dummy
            T_Downstream = dummy2
            #print("In Dummy Switch")

       

        P_Ratio = P_Downstream/P_Upstream

        if P_Ratio >= .528:
            # Unchoked Flow
            mdot = 2.0544 * P_Upstream / math.sqrt(T_Upstream) * math.sqrt((pow(P_Ratio,1.42857)-pow(P_Ratio,1.71428)))
            #print("Unchoked")
        else:
            # Choked Flow
            mdot = 0.5317 * P_Upstream / pow(T_Upstream,0.5)
            print("Choked")

    
        print("modt Before: " + str(mdot))


        area = 3.14159 / 4.0 * pow(dia,2) * cd  
        

        mdot = sign * mdot * area
     

        #print("mdot: " + str(mdot))
 

    else:
        mdot = 0   

    return mdot

 

def pressure_equalization(P_Upstream, P_Downstream, V_Upstream, V_Downstream):
    return ((P_Upstream*V_Upstream+P_Downstream*V_Downstream)/(V_Upstream+V_Downstream))

 

def mass_equalization(P_Equalized,V_Equalized,T_eq):
    return ((P_Equalized*V_Equalized*28.97)/(10.73*(T_eq)))

 

# The test code...
if __name__ == "__main__":

 

    # Define the Tanks
    tank1 = Tank("Tank 1")
    tank2 = Tank("Tank 2")
    tank3 = Tank("Tank 3")
    tank4 = Tank("Tank 4")
    tank5 = Tank("Tank 4")
    tank6 = Tank("Tank 5")
    tank7 = Tank("Tank 6")
    vacuum = Tank("Vacuum")

   

    # Define volumes of Tanks
    tank1.volume = 3450.0
    tank2.volume = 1947.86
    tank3.volume = 2190.0
    tank4.volume = 2190.0
    tank5.volume = 1108.25
    tank6.volume = 2261.0
    tank7.volume = 4405.0
    vacuum.volume = sys.maxint


    # Define temp of Tanks
    tank1.temperature = (72.0 + 460)
    tank2.temperature = (72.0 + 460)
    tank3.temperature = (72.0 + 460)
    tank4.temperature = (72.0 + 460)
    tank5.temperature = (72.0 + 460)
    tank6.temperature = (72.0 + 460)
    tank7.temperature = (72.0 + 460)
    vacuum.temperature = 0.0

   

    # Define pressure of Tanks
    tank1.pressure = 14.7
    tank2.pressure = 14.7
    tank3.pressure = 0.0
    tank4.pressure = 758.0 / 51.71
    tank5.pressure = 758.0 / 51.71
    tank6.pressure = 458.0 / 51.71
    tank7.pressure = 458.0 / 51.71
    vacuum.pressure = 0.0

   

    # Calcualte inital mass of Tanks
    tank1.mass = calculate_mass(tank1.pressure, tank1.temperature, tank1.volume)
    print(tank1.mass)
    tank2.mass = calculate_mass(tank2.pressure, tank2.temperature, tank2.volume)
    tank3.mass = calculate_mass(tank3.pressure, tank3.temperature, tank3.volume)
    tank4.mass = calculate_mass(tank4.pressure, tank4.temperature, tank4.volume)
    tank5.mass = calculate_mass(tank5.pressure, tank5.temperature, tank5.volume)
    tank6.mass = calculate_mass(tank6.pressure, tank6.temperature, tank6.volume)
    tank7.mass = calculate_mass(tank7.pressure, tank7.temperature, tank7.volume)
    vacuum.mass = 0.0

    

    

    # Define mass bank of Tanks
    tank1.mass_bank = 0.0
    tank2.mass_bank = 0.0
    tank3.mass_bank = 0.0
    tank4.mass_bank = 0.0
    tank5.mass_bank = 0.0
    tank6.mass_bank = 0.0
    tank7.mass_bank = 0.0
    vacuum.mass_bank = 0.0

   

    # Link up Tanks - I'm currently using the simplified model: T2 -- T1 -- T3
    tank1.add_link(tank2, 60, 1.0)      #  T4          T7
    tank1.add_link(tank3, 4.0, 0.59)    #  |            |
    #tank2.add_link(tank4)              # T2 -- T1  -- T3  --> Simlified Model: T2 -- T1 -- T3
    #tank2.add_link(tank5)              #  |           |
    #tank3.add_link(tank6)              # T5          T6
    #tank3.add_link(tank7)

   

    # Break up T3 and T1 Link
    #tank2.remove_link(tank3)

 

 

    # Put all the nodes/tanks together in one big set.
    tanks = {tank1, tank2, tank3, tank4, tank5, tank6, tank7}
   

    connected_Tanks = connected_tanks(tanks)

   

    # Find all the connected components.
    number = 1
    for components in connected_Tanks:
        names = sorted(tank.name for tank in components)
        names = ", ".join(names)
        print "Group #%i: %s" % (number, names)
        number += 1

   

    t = 0
    t_step = .12
    t_stop_time = 1

 

    print('(' + str(tank2.pressure) + ") -- (" + str(tank1.pressure) + ") -- (" + str(tank3.pressure) + ")")
    print('')

   

    total_mass = tank1.mass + tank2.mass + tank3.mass

  

    Data_Over_Time = list((list(),list() ,list() ))

   

 

   

    # Basic Run:
    while t < t_stop_time:
        #print('')
        for tank in sorted(tanks):
           # print('Tank: ' + tank.name)
            for flowPath in sorted(tank.get_flowPaths()):
            #for link in sorted(tank.get_links()):
                if abs(flowPath.flowPath_From.pressure - flowPath.flowPath_To.pressure) > 0.000000001: #Ignore transfering fluid when the pressure delta is small
                    print("")
                    print("t: " + str(t))
                    print(flowPath.name)
                    pathway = flowPath.name
                    mdot = calculate_mdot(flowPath.flowPath_From.pressure, flowPath.flowPath_To.pressure, flowPath.flowPath_From.temperature, flowPath.flowPath_To.temperature, flowPath.opening_Diameter, flowPath.cd)
                    P_eq = pressure_equalization(flowPath.flowPath_From.pressure,flowPath.flowPath_To.pressure,flowPath.flowPath_From.volume,flowPath.flowPath_To.volume)
                    M_eq = mass_equalization(P_eq,flowPath.flowPath_From.volume,flowPath.flowPath_From.temperature)
                    Max_Mass_Transfer = ((flowPath.flowPath_From.mass - M_eq))
                    sign = (flowPath.flowPath_From.pressure - flowPath.flowPath_To.pressure) / abs(flowPath.flowPath_From.pressure - flowPath.flowPath_To.pressure)
                    if Max_Mass_Transfer < abs(mdot):
                        mdot = Max_Mass_Transfer / t_step
                        #print("Hit Max Transfered: " + flowPath.flowPath_From.name + ": " + str(Max_Mass_Transfer))

                   
                    mdot = mdot * sign

                   

                    print(mdot)

                   

                    flowPath.flowPath_From.mass = flowPath.flowPath_From.mass - (mdot*t_step)
                    flowPath.flowPath_From.pressure = calculate_pressure(flowPath.flowPath_From.mass, flowPath.flowPath_From.temperature, flowPath.flowPath_From.volume)

 

                    flowPath.flowPath_To.mass = flowPath.flowPath_To.mass + (mdot*t_step)
                    flowPath.flowPath_To.pressure = calculate_pressure(flowPath.flowPath_To.mass, flowPath.flowPath_To.temperature, flowPath.flowPath_To.volume)

                   

                    #print(flowPath.flowPath_From.pressure)
                    #print(flowPath.flowPath_To.pressure)

                   

                    #flowPath.flowPath_To.mass_bank = 0
                    #print("")

                else:
                    flowPath.flowPath_From.mass_bank = 0

               

                print(str(flowPath.flowPath_From.pressure) + " --> " + str(flowPath.flowPath_To.pressure))
                print("Mass Balence: " +  str(total_mass - (tank1.mass + tank2.mass + tank3.mass)))

               

                #print(flowPath.flowPath_From.pressure)

    
        print('')
        t = t + t_step

   

    print(tank2.pressure)
    print(tank1.pressure)
    print(tank3.pressure)
