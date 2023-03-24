import PySimpleGUI as sg

	
sg.theme('Black')

layout = [[sg.Text('Enter the mass of the asteroid in kg:')],
		[sg.Input(key='asteroidMass')],
        [sg.Text('Enter the mass of the gravity tractor in kg:')],
		[sg.Input(key='gravityTractorMass')],
        [sg.Text('Enter the distance between the asteroid and the GT in m:')],
		[sg.Input(key='distance')],
        [sg.Text('Enter the time left in seconds:')],
		[sg.Input(key='timeLeft')],
        [sg.Text('Enter the time left for levitation in seconds:')],
		[sg.Input(key='timeForLevitatingLeft')],
		[sg.Button('Calculate')],
        [sg.Text('The deflection after'),sg.Text(key='-OUTPUT-'),sg.Text('seconds is:'),sg.Text(key='-OUTPUT-'), sg.Text('meters')]]

window = sg.Window('Asteroid deflection with Gravity Tractor', layout)


while True:
	event, values = window.read()
	print(event, values)
	
	
	if event == 'Calculate':
		# Update the "output" text element
		# to be the value of "input" element
		window['-OUTPUT-'].update(values['asteroidMass'])

    #megnezni hogy ez kell e
	if event == sg.WIN_CLOSED:
		break

window.close()
