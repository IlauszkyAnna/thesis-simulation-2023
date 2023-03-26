#input
asteroidMass=int(input("Enter the mass of the asteroid in kg: "))
gravityTractorMass=int(input("Enter the mass of the gravity tractor in kg: "))
distance=int(input("Enter the distance between the asteroid and the GT in m: "))
timeLeft=int(input("Enter the time left in seconds: "))
timeForLevitatingLeft=int(input("Enter the time left for levitation in seconds: "))

#gravitational constant
G=6.67*(10**(-11))

#gravitational force between the asteroid and the GT
fGravitation=G*((asteroidMass*gravityTractorMass)/(distance**2))
print("The gravitational force between the asteroid and the GT:", fGravitation)

#acceleration of the asteroid
massTogether=asteroidMass+gravityTractorMass
aNEO=fGravitation/massTogether

#10 év = 315569260 másodperc
#1 év = 31556926 másodperc
#deflection: delta X
deflection=1.5*aNEO*timeForLevitatingLeft*((2*timeLeft)-timeForLevitatingLeft)
roundedDeflection=round(deflection,3)

print("The deflection after", timeLeft, "seconds is: ", roundedDeflection, "meters")
