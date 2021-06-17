#!/usr/bin/python3
"""
This module creates a windows to simulate
CONWAY'S GAME OF LIFE
"""

from traceback import print_tb
import PySimpleGUI as sg
import time
from PySimpleGUI.PySimpleGUI import Multiline


def InitMat(x, y):
    return [[0 for i in range(x)] for j in range(y)]


def printMat(TextArea, Mat):
    text = ""
    for row in Mat:
        for i in row:
            if i == 0:
                text += "_"
            else:
                text += "#"
        text += '\n'
    TextArea.update(text)


def cellsBorn(mat, cells):
    for cell in cells:
        mat[cell[0]][cell[1]] = 1


def nextStep(Mat0, Mat1):
    y = len(Mat0)
    x = len(Mat0[0])
    for i, row in enumerate(Mat0):
        for j, cell in enumerate(row):
            count = 0
            if cell == 0:
                for r_i in range(i-1, i + 2):
                    for c_i in range(j-1, j+2):
                        if c_i == x:
                            c_i = 0
                        if r_i == y:
                            r_i = 0
                        if c_i == -1:
                            c_i = x - 1
                        if r_i == -1:
                            r_i = y - 1
                        # print("r_i= {}".format(r_i))
                        # print("c_i= {}".format(c_i))
                        count += Mat0[r_i][c_i]
                if count == 3:
                    Mat1[i][j] = 1
                else:
                    Mat1[i][j] = 0
            else:
                for r_i in range(i-1, i + 2):
                    for c_i in range(j-1, j+2):
                        if c_i == x:
                            c_i = 0
                        if r_i == y:
                            r_i = 0
                        if c_i == -1:
                            c_i = x - 1
                        if r_i == -1:
                            r_i = y - 1
                        count += Mat0[r_i][c_i]
                count -= 1
                if count != 2 and count != 3:
                    Mat1[i][j] = 0
                else:
                    Mat1[i][j] = 1


layout = [[sg.Text("GAME OF LIFE")],
          [sg.Text('Screen size: '), sg.Input(
              '35, 45', size=(10, 1), key='-SIZE-'), sg.Button('CLEAR')],
          [sg.Text('alives: '), sg.Input(
              '(10,10),(10,11),(11,11),(11,12),(12,11)', size=(20, 1), key='-INPUT-')],
          [sg.Button("GO"), sg.Button("Stop")],
          [sg.Multiline(key='-ML-'+sg.WRITE_ONLY_KEY,
                        size=(30, 30), font=("Helvetica", 12))],
          [sg.Button("CLOSE"), sg.Text(key='-ITER-', size=(16, 1))]
          ]

# Create the window
window = sg.Window("GAME OF LIFE", layout, margins=(10, 10), finalize=True)

Mata = InitMat(30, 30)
Mate = InitMat(30, 30)

direction = 1

go = False
i = 0
while True:
    event, values = window.read(timeout=100)
    # End program if user closes window or
    # presses the OK button
    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break

    if event == "GO":
        try:
            alives = eval('['+values['-INPUT-']+']')
            print(alives)
            if any([type(i) != tuple for i in alives]):
                raise Exception("ups")
            cellsBorn(Mata, alives)
            go = True
            printMat(window['-ML-'+sg.WRITE_ONLY_KEY], Mata)

        except Exception as e:
            print(e)
            sg.popup('Alive cells has to be tuples separated by commas')

    if event == "CLEAR":
        try:
            y, x = eval('('+values['-SIZE-']+')')
            window['-ML-'+sg.WRITE_ONLY_KEY].set_size(size=(x, y))
            Mata = InitMat(x, y)
            Mate = InitMat(x, y)
            i = 0
            go = False
        except:
            sg.popup('Write x and y separated by a comma, example: 40,50')

    time.sleep(0.05)
    if go:
        if direction == 1:
            nextStep(Mata, Mate)
            printMat(window['-ML-'+sg.WRITE_ONLY_KEY], Mate)
            direction = 0

        else:
            nextStep(Mate, Mata)
            printMat(window['-ML-'+sg.WRITE_ONLY_KEY], Mata)
            direction = 1

        window['-ITER-'].update("iterations: {}".format(i))
        i += 1

window.close()
