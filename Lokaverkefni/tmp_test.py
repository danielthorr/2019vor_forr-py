'''import PySimpleGUI as sg      
window = sg.Window('Simple data entry window')      
layout = [      
          [sg.Text('Please enter your Name, Address, Phone')],      
          [sg.Text('Name', size=(15, 1)), sg.InputText('1', key='_name_')],      
          [sg.Text('Address', size=(15, 1)), sg.InputText('2', key='_address_')],      
          [sg.Text('Phone', size=(15, 1)), sg.InputText('3', key='_phone_')],      
          [sg.Submit(), sg.Cancel()]      
         ]

event, values = window.Layout(layout).Read()

sg.Popup(event, values, values['_name_'], values['_address_'], values['_phone_'])'''
import PySimpleGUI
print(PySimpleGUI.__file__)