import pygame
from time import sleep as czekaj
from random import randint as losuj
import os
# --------------------------------------------------------------------------------------
class segment:
    def __init__(self, LED_size, screen = None, x = 0, y = 0):
        #                 off          on             selected       select
        self.colors = [(32, 56, 32), (16, 192, 0), (192, 192, 0), (128, 192, 0)]
        #          DARK GREEN      GREEN        GREEN GRAS      YELLOW
        self.currend_color = 1  # on
        self.currend_digit = None
        self.LEDs_x = 5
        self.LEDs_y = 7
        self.size_x = self.size_y = LED_size
        self.border_width = 1
        led_scale = 1
        self.radius = int(led_scale * (self.size_x - 2 * self.border_width) // 2)
        # self.border_color = (64, 64, 64)
        self.border_color = (0, 0, 0)
        # self.back_color = (48, 48, 48)
        self.back_color = (0, 0, 0)
        self.segment_width = self.LEDs_x * self.size_x
        self.segment_hight = self.LEDs_y * self.size_y
        # create LED display table
        # self.display_array = [[self.colors[0] for x in range(self.LEDs_x) ] for y in range(self.LEDs_y)]
        self.display_array = [[0 for x in range(self.LEDs_x) ] for y in range(self.LEDs_y)]
        if screen is not None: self.set_screen(screen, x, y)

    def set_screen(self, screen, x, y, show_it = True):
        self.screen = screen
        self.x_offset = x
        self.y_offset = y
        if show_it: self.show()
       
    def get_width(self):
        return self.segment_width

    def get_hight(self):
        return self.segment_hight

    def get_size(self):
        return (self.segment_width, self.segment_hight) # tuple
 
    def change_colors(self, color_off, color_on, color_selected, color_select):
        self.colors[0] = color_off
        self.colors[1] = color_on
        self.colors[3] = color_selected
        self.colors[2] = color_select

    def get_color(self, color_nr = None):
        if color_nr is None:
            return self.currend_color
        else:
            if 0 <= color_nr < 4:
                return self.colors[color_nr]
            else:
                return None
        
    def set_digit(self, digit, color = 1):
        shapes = (	
	                (0x3E, 0x45, 0x49, 0x51, 0x3E),	# 0
	                (0x00, 0x42, 0x7F, 0x40, 0x00),	# 1
	                (0x42, 0x61, 0x51, 0x49, 0x46),	# 2
	                (0x21, 0x41, 0x49, 0x4D, 0x3B),	# 3
	                (0x18, 0x14, 0x12, 0x7F, 0x10),	# 4
	                (0x27, 0x45, 0x45, 0x45, 0x39),	# 5
	                (0x3E, 0x49, 0x49, 0x49, 0x32),	# 6
	                (0x01, 0x01, 0x79, 0x05, 0x03),	# 7
	                (0x36, 0x49, 0x49, 0x49, 0x36),	# 8
	                (0x26, 0x49, 0x49, 0x49, 0x36),	# 9
	            )
        if 0 <= digit <= 9:
            self.currend_digit = digit
            x = 0
            for shape in shapes[digit]:
                mask = 0x01
                for y in range(self.LEDs_y):
                    if shape & mask:
                        self.display_array[y][x] = color
                    else:
                        self.display_array[y][x] = 0
                    mask <<= 1
                x += 1
        else:
            self.currend_digit = None
            self.clear()

    def show_digit(self, digit, color = 1):
        self.set_digit(digit, color)
        self.show()

    def get_digit(self):
        return self.currend_digit
    
    def digit_on(self):
        self.show_digit(self.get_digit())
        
    def show(self):
        for x in range(self.LEDs_x):
            for y in range(self.LEDs_y):
                color = self.display_array[y][x]
                position_x = self.x_offset + x * self.size_x
                position_y = self.y_offset + y * self.size_y
                # center = (position_x + self.border_width + self.radius, position_y + self.border_width + self.radius)
                center = (position_x + self.size_x // 2, position_y + self.size_y // 2)
                pygame.draw.rect(self.screen, self.back_color, pygame.Rect(position_x, position_y, self.size_x, self.size_y))
                pygame.draw.rect(self.screen, self.border_color, pygame.Rect(position_x, position_y, self.size_x, self.size_y),  self.border_width)
                pygame.draw.circle(self.screen, self.colors[color], center, self.radius)
                if color == 0:
                    color = self.back_color
                else:
                    color = self.colors[color]
                    # r = (2 * color[0]) % 256
                    # g = (2 * color[1]) % 256
                    # b = (2 * color[2]) % 256
                    r = color[0] // 2 + 127
                    g = color[1] // 2 + 127
                    b = color[2] // 2 + 127
                    color = (r,g,b)
                pygame.draw.circle(self.screen,color, center, self.radius, self.border_width + 1)
        pygame.display.flip()

    def clear(self):
        for x in range(self.LEDs_x):
            for y in range(self.LEDs_y):
                self.display_array[y][x] = 0
        self.show()
#
# --------------------------------------------------------------------------------------
#
# Gra ma na stałe 9 cyfr
#
def wylosuj():
    ile_losowan = losuj(5, 15)
    for i in range(ile_cyfr):
        cyferki[i] = i + 1
    for _ in range(ile_losowan):
        poz_1 = losuj(0, ile_cyfr - 2) #  -2 bo pozycje są liczone od 0. Norrmalnie by było od 1 do ilość cyfr -1 by losowanie było bez ostatniej
        while True:
            poz_2 = losuj(0, ile_cyfr - 2)
            if poz_2 > poz_1 + 1: break
            if poz_2 < poz_1 - 1: break
        cyferki[poz_1], cyferki[poz_1 + 1], cyferki[poz_2], cyferki[poz_2 + 1] = cyferki[poz_2], cyferki[poz_2 + 1], cyferki[poz_1], cyferki[poz_1 + 1]
    for i in range(ile_cyfr):
        panels[i].show_digit(cyferki[i], 1)
    swaps[0] = None
    swaps[1] = None
    swaps[2] = None
    swaps[3] = None
    return ile_losowan

def disp_info():
    if game_over:
        caption = '*** GAME OVER ***' + led_size*' ' + f'Shuffled {ile_losowan} times. Yours shift: {steps} '
        if ile_losowan < steps:
            caption =  caption + '- You lost'
        else:
            caption = caption + '- No way! You won'
        caption = caption + 40*' ' + 'Press Q for quit or N for naxt game'
    else: 
        caption = '*** Digit puzzle ***' + led_size*' ' + f'Shuffled {ile_losowan} times. Be better. Yours shift: {steps}'
    pygame.display.set_caption(caption)

LEFT_BUTTON = 1
RIGHT_BUTTON = 3
# --------------------------------------------------------------------------------------
os.system("cls")
print('''
Put the numbers in order from 1 to 9 by swapping them.
Swapping is made only by pairs.
You can by:
Left mouse button - select/deselect pair
Right mouse button - swap selected pair
n or r key - new game
ESC or q key - exit the game

Be better than the computer!!!
''')
# --------------------------------------------------------------------------------------
led_size = 18
ile_cyfr = 9
# --------------------------------------------------------------------------------------
panels = []
module_gap = led_size   # * "scale"
tmp_segment = segment(led_size)
segment_width, segment_hight = tmp_segment.get_size()
panel_width = ile_cyfr * (segment_width + module_gap) - module_gap # na końcu nie ma odstępu
panel_hight = segment_hight
screen_size = (panel_width, panel_hight)
del tmp_segment

pygame.init()
game_panel = pygame.display.set_mode(screen_size)

# pygame.display.set_caption('*** Gra w cyferki ***')

back_color = (0,0,0)
game_panel.fill(back_color)

y_pos = 0
for i in range(ile_cyfr):
    panels.append(None)
    panels[i] = segment(led_size)
    panels[i].set_digit(i + 1)
    panels[i].set_screen(game_panel, i * (segment_width + module_gap), y_pos)
cyferki = [n + 1 for n in range(ile_cyfr)] # set 1...9
status_left_button = False
status_right_button = False
mouse_button = 0
swaps = [None, None, None, None]
game_over = False
running = True
steps = 0
ile_losowan = wylosuj()
disp_info()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not (status_left_button or status_right_button):
                mouse_button = event.button
                if mouse_button == LEFT_BUTTON: status_left_button = True
                if mouse_button == RIGHT_BUTTON: status_right_button = True
            else:
                mouse_button = 0
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button = event.button
            if mouse_button == RIGHT_BUTTON:
                status_right_button = False
                if status_left_button:
                    mouse_button = 0
            if mouse_button == LEFT_BUTTON:
                status_left_button = False
                mouse_button = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or keys[pygame.K_q]: break
    if keys[pygame.K_r] or keys[pygame.K_n]:
        ile_losowan = wylosuj()
        disp_info()
        swaps = [None, None, None, None]
        game_over = False
        steps = 0
    if (mouse_button != 0) and not game_over:
        if mouse_button == RIGHT_BUTTON:
            if status_right_button:
                if not (swaps[0] is None or swaps[2] is None):
                    cyferki[swaps[0]], cyferki[swaps[1]], cyferki[swaps[2]], cyferki[swaps[3]] = \
                    cyferki[swaps[2]], cyferki[swaps[3]], cyferki[swaps[0]], cyferki[swaps[1]]
                    steps += 1
                    disp_info()
                    for i in range(ile_cyfr):
                        panels[i].show_digit(cyferki[i], 1)
                    swaps = [None, None, None, None]
                    game_over = True
                    for i in range(ile_cyfr):
                        if cyferki[i] != i + 1:
                            game_over = False
                            break
                    if game_over:
                        for i in range(ile_cyfr):
                            czekaj(0.7)
                            panels[i].clear()
                        disp_info()
        elif  mouse_button == LEFT_BUTTON:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_y = mouse_y // segment_hight + y_pos
            segment_nr = mouse_x // (segment_width + module_gap)
            mouse_x = mouse_x - segment_nr * (segment_width + module_gap)
            if (mouse_x <= segment_width) and (segment_nr < (ile_cyfr -1)):
                to_swaps = True
                for i in range(4):
                    if swaps[i] == segment_nr:
                        to_swaps = False
                        i = 2 * (i // 2)    # i = 0 -> 0
                                            # i = 1 -> 0
                                            # i = 2 -> 2
                                            # i = 3 -> 2
                        segment_nr = swaps[i]
                        swaps[i] = None
                        swaps[i + 1] = None
                        panels[segment_nr].show_digit(cyferki[segment_nr], 1)
                        panels[segment_nr + 1].show_digit(cyferki[segment_nr + 1], 1)
                if to_swaps:
                    for i in range(4):
                        if swaps[i] == segment_nr + 1:
                            to_swaps = False
                    if to_swaps:                        
                        if swaps[0] is None:
                            swaps[0] = segment_nr
                            panels[segment_nr].show_digit(cyferki[segment_nr], 2)
                            swaps[1] = segment_nr + 1
                            panels[segment_nr + 1].show_digit(cyferki[segment_nr + 1], 2)
                        elif swaps[2] is None:
                            swaps[2] = segment_nr
                            panels[segment_nr].show_digit(cyferki[segment_nr], 2)
                            swaps[3] = segment_nr + 1
                            panels[segment_nr + 1].show_digit(cyferki[segment_nr + 1], 2)
        mouse_button = 0
    pygame.display.flip()

pygame.quit()