import PySimpleGUI

PySimpleGUI.theme('BlueMono')



layout = [[PySimpleGUI.Text('Enter the mass of the asteroid in kg:'),PySimpleGUI.Input(key='-asteroidMass-')],
        [PySimpleGUI.Text('Enter the mass of the gravity tractor in kg:'), PySimpleGUI.Input(key='-gravityTractorMass-')],
        [PySimpleGUI.Text('Enter the distance between the asteroid and the GT in m:'), PySimpleGUI.Input(key='-distance-')],
        [PySimpleGUI.Text('Enter the time left in seconds:'), PySimpleGUI.Input(key='-timeLeft-')],
        [PySimpleGUI.Text('Enter the time left for levitation in seconds:'), PySimpleGUI.Input(key='-timeForLevitatingLeft-')],
		[PySimpleGUI.Button('Calculate')],
        [PySimpleGUI.Text('The deflection after'),PySimpleGUI.Text(key='-OUTPUT-',text_color='Red'),PySimpleGUI.Text('seconds is:'),PySimpleGUI.Text(key='-OUTPUT2-', text_color='Red'), PySimpleGUI.Text('meters')]]

window = PySimpleGUI.Window('Asteroid deflection with Gravity Tractor', layout, resizable=True, size=(600, 350))


#gravitational constant
G=6.67*(10**(-11))



while True:
	
	event, values = window.read()
	print(event, values)

	#
	#if event == '-asteroidMass-':
		#if values['-asteroidMass-'][-1] not in ('0123456789'):
			#PySimpleGUI.popup("Only digits allowed")
			#window['-OUTPUT-'].update(values['-asteroidMass-'][:-1])
	  	
	
	if event == 'Calculate':
		#gravitational force between the asteroid and the GT
		fGravitation=G*((int(values['-asteroidMass-'])*int(values['-gravityTractorMass-']))/(int(values['-distance-'])**2))

		#acceleration of the asteroid
		massTogether=int(values['-asteroidMass-'])+int(values['-gravityTractorMass-'])
		aNEO=fGravitation/massTogether

		#10 év = 315569260 másodperc
		#1 év = 31556926 másodperc
		#deflection: delta X
		deflection=1.5*aNEO*int(values['-timeForLevitatingLeft-'])*((2*int(values['-timeLeft-']))-int(values['-timeForLevitatingLeft-']))
		roundedDeflection=round(deflection,3)

		asd=int(values['-timeForLevitatingLeft-'])+6
		window['-OUTPUT-'].update(values['-timeLeft-'])
		window['-OUTPUT2-'].update(roundedDeflection)

	if event == PySimpleGUI.WIN_CLOSED:
		break

window.close()
