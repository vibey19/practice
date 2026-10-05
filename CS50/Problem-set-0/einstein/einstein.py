def takeInput():
    mass = int(input("Enter mass: "))
    return mass

def calculateEnergy(mass):
    c = 300000000
    e = mass * c**2
    return e

def main():
    mass = takeInput()
    energy = calculateEnergy(mass)
    print(energy)
    
main()