import machine
import neopixel
import time

# Matrix configuration
WIDTH = 8
HEIGHT = 8
NUM_LEDS = WIDTH * HEIGHT
DATA_PIN = 3 

np = neopixel.NeoPixel(machine.Pin(DATA_PIN), NUM_LEDS)

# Zigzag layout
def xy_to_index(x, y):
    if y % 2 == 0:
        return y * WIDTH + x
    else:
        return y * WIDTH + (WIDTH - 1 - x)

# Fill matrix with one color
def fill_matrix(r, g, b):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = xy_to_index(x, y)
            np[idx] = (r, g, b)
    np.write()

# Clear all LEDs
def clear():
    fill_matrix(0, 0, 0)

# Morse code dictionary
MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....', 'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',   'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',  'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--','4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..','9': '----.', '0': '-----',
    ' ': ' '
}

# Morse timing (in seconds)
DOT = 0.2
DASH = DOT * 3
SYMBOL_PAUSE = DOT
LETTER_PAUSE = DOT * 3
WORD_PAUSE = DOT * 7

# Flash a dot or dash
def flash(duration):
    fill_matrix(255, 255, 255)
    time.sleep(duration)
    clear()
    time.sleep(SYMBOL_PAUSE)

# Convert string to Morse code and flash it
def flash_morse(text):
    text = text.upper()
    for char in text:
        if char not in MORSE_CODE:
            continue
        code = MORSE_CODE[char]
        if code == ' ':
            time.sleep(WORD_PAUSE)
        else:
            for symbol in code:
                if symbol == '.':
                    flash(DOT)
                elif symbol == '-':
                    flash(DASH)
            time.sleep(LETTER_PAUSE)

# Change this to any string you want
MESSAGE = "SOS HELP"

# Main loop
while True:
    print("Flashing Morse for:", MESSAGE)
    flash_morse(MESSAGE)
    time.sleep(2)  # Pause before repeating