import obd
from datetime import datetime
import json
import pygame
import requests
import time

#color
WHITE = (255, 255, 255)
SPRING_GREEN = (0, 255, 127)
STONE_GRAY = (0, 255, 0)
GREEN = (127, 255, 0)
LIGHT_GREEN = (152, 251, 152)
GREEN_YELLOW = (173, 255, 47)
TOMATO_COLOR = (255, 99, 71)
ORANGE = (255, 165, 0)
ORANGE_RED = (255, 69, 0)
GRAY= (230, 230, 230)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#commands
c1 = obd.commands.SPEED
c2 = obd.commands.RPM
c3 = obd.commands.ENGINE_LOAD
c4 = obd.commands.AMBIANT_AIR_TEMP
c5 = obd.commands.COOLANT_TEMP
c6 = obd.commands.INTAKE_TEMP
c7 = obd.commands.INTAKE_PRESSURE

#display params
rpm = 0
load = 0
speed = 0
air_temp = 0
cool_temp = 0
intake_temp = 0
intake_pressure = 0

one_word_url = 'https://v1.hitokoto.cn/?c=a&c=c&c=d&c=e&c=f&c=h&c=i&c=j&c=k&c=l&encode=json&&min_length=8&max_length=20'

#screen
screen = None

windows_debug = True

display_font = "wenquanyizenheimono"
number_font = "Digital Dismay"

if windows_debug:
    #display_font= "wenquanyizenheimono"
    display_font = "文泉驿正黑"
    rpm = 2389
    load = 9
    speed = 111
    air_temp = 18
    cool_temp = 98
    intake_temp = 43
    intake_pressure = 57


def get_text(text, color, size, alpha=255):
    text_surface = pygame.font.SysFont(display_font, size).render(str(text), True, color)
    text_surface.set_alpha(alpha)
    return text_surface


def get_number_text(text, color, size, alpha=255):
    text_surface = pygame.font.SysFont(number_font, size).render(str(text), True, color)
    text_surface.set_alpha(alpha)
    return text_surface


def get_number_text_stroke(text, color, size, mbSize, mbColor, alpha=255, mbAlpha=255):
    temp0 = get_number_text(text, color, size, alpha)
    temp1 = get_number_text(text, mbColor, size, mbAlpha)
    result = pygame.Surface((temp0.get_width() + mbSize * 2, temp0.get_height() + mbSize * 2))
    result.fill((0, 0, 0, 0))
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for d in range(mbSize):
                if i == 0 and j == 0:
                    continue
                result.blit(temp1, (mbSize + i * d, mbSize + j * d))
    result.blit(temp0, (mbSize, mbSize))
    return result


def rpm_tracker(obd_response):
    global rpm
    if not obd_response.is_null():
        rpm = int(obd_response.value.magnitude)


def load_tracker(obd_response):
    global load
    if not obd_response.is_null():
        load = int(obd_response.value.magnitude)


def speed_tracker(obd_response):
    global speed
    if not obd_response.is_null():
        speed = int(obd_response.value.magnitude)


def air_temp_tracker(obd_response):
    global air_temp
    if not obd_response.is_null():
        air_temp = int(obd_response.value.magnitude)


def cool_temp_tracker(obd_response):
    global cool_temp
    if not obd_response.is_null():
        cool_temp = int(obd_response.value.magnitude)


def intake_temp_tracker(obd_response):
    global intake_temp
    if not obd_response.is_null():
        intake_temp = int(obd_response.value.magnitude)


def intake_pressure_tracker(obd_response):
    global intake_pressure
    if not obd_response.is_null():
        intake_pressure = int(obd_response.value.magnitude)


def select_color_by_speed():
    global speed
    range_to_color = {
        range(0, 30): WHITE,
        range(30, 40): SPRING_GREEN,
        range(40, 50): STONE_GRAY,
        range(50, 60): GREEN,
        range(60, 70): GREEN_YELLOW,
        range(70, 80): YELLOW,
        range(80, 90): ORANGE,
        range(90, 100): TOMATO_COLOR,
        range(100, 115): ORANGE_RED,
        range(115, 299): RED
    }
    for item in range_to_color:
        if speed in item:
            return range_to_color[item]


def blit_data_by_value():
    global rpm
    global load
    global speed
    global air_temp
    global cool_temp
    global intake_temp
    global intake_pressure

    if air_temp < 0:
        if air_temp > -10:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 61)
            screen.blit(air_temp_txt, (25, 178))
        else:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 61)
            screen.blit(air_temp_txt, (13, 178))
    else:
        if air_temp < 10:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 61)
            screen.blit(air_temp_txt, (52, 178))
        elif air_temp < 20:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 61)
            screen.blit(air_temp_txt, (31, 178))
        else:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 61)
            screen.blit(air_temp_txt, (38, 178))


    cool_temp_txt = get_number_text(str(cool_temp), WHITE, 61)
    screen.blit(cool_temp_txt, (157, 178))

    intake_temp_txt = get_number_text(str(intake_temp), WHITE, 61)
    screen.blit(intake_temp_txt, (275, 178))

    intake_pressure_txt = get_number_text(str(intake_pressure), WHITE, 61)
    screen.blit(intake_pressure_txt, (393, 178))

    if speed < 10:
        speed_txt = get_number_text_stroke(str(speed), WHITE, 160, 0, select_color_by_speed())
        screen.blit(speed_txt, (355, 0))
    elif speed >= 10 and speed < 100:
        speed_txt = get_number_text_stroke(str(speed), WHITE, 154, 2, select_color_by_speed())
        screen.blit(speed_txt, (320, 0))
    else:
        speed_txt = get_number_text_stroke(str(speed), WHITE, 154, 2, select_color_by_speed())
        screen.blit(speed_txt, (264, 0))

    if rpm < 1000:
        rpm_txt = get_number_text(str(rpm), WHITE, 120)
        screen.blit(rpm_txt, (17, 20))
    else:
        rpm_txt = get_number_text(str(rpm), WHITE, 100)
        screen.blit(rpm_txt, (7, 30))

    if load < 10:
        load_txt = get_number_text(str(load), WHITE, 120)
        screen.blit(load_txt, (216, 62))
    else:
        load_txt = get_number_text(str(load), WHITE, 120)
        screen.blit(load_txt, (190, 62))


def draw_rpm_screen():
    # rpm
    pygame.draw.rect(screen, GRAY, pygame.Rect(2, 5, 182, 150), 2)
    rpm_txt_render = get_text("RPM", GRAY, 34)
    screen.blit(rpm_txt_render, (55, 148))
    rpm_unit_render = get_text("r/min", GRAY, 25)
    screen.blit(rpm_unit_render, (116, 125))


def draw_load_screen():
    # load
    pygame.draw.rect(screen, GRAY, pygame.Rect(182, 70, 115, 115), 2)

    load_txt_render = get_text("Load", GRAY, 35)
    screen.blit(load_txt_render, (202, 34))
    load_unit_render = get_text("%", GRAY, 25)
    screen.blit(load_unit_render, (274, 156))


def draw_speed_screen():
    # speed
    pygame.draw.rect(screen, GRAY, pygame.Rect(295, 5, 183, 150), 2)
    speed_txt_render = get_text("Speed", GRAY, 35)
    screen.blit(speed_txt_render, (338, 146))
    speed_unit_render = get_text("Km/h", GRAY, 25)
    screen.blit(speed_unit_render, (410, 126))


def draw_more_info_screen():
    # more info
    pygame.draw.rect(screen, GRAY, pygame.Rect(2, 183, 476, 70), 2)

    pygame.draw.rect(screen, GRAY, pygame.Rect(2, 183, 122, 70), 2)
    txt1 = get_text("环境温度", GRAY, 22)
    screen.blit(txt1, (18, 226))
    pygame.draw.rect(screen, GRAY, pygame.Rect(122, 183, 120, 70), 2)
    txt2 = get_text("冷却液温度", GRAY, 22)
    screen.blit(txt2, (127, 226))
    pygame.draw.rect(screen, GRAY, pygame.Rect(240, 183, 120, 70), 2)
    txt3 = get_text("进气温度", GRAY, 22)
    screen.blit(txt3, (256, 226))
    pygame.draw.rect(screen, GRAY, pygame.Rect(358, 183, 120, 70), 2)
    txt4 = get_text("进气压力", GRAY, 22)
    screen.blit(txt4, (374, 226))


def request_one_word():
    rep = requests.get(one_word_url)
    rep.encoding = 'utf-8'
    one_word_data = json.dumps(rep.json())
    return json.loads(one_word_data)


def calc_one_word_from_position(one_word_from):
    pixel = 0
    for char in one_word_from:
        if pixel > 476 or pixel + 24 > 476:
            break
        if '\u4e00' <= char <= '\u9fa5':
            pixel += 24
        else:
            pixel += 14
    return {'position': 476 - pixel, 'word': one_word_from}


pygame.init()
if windows_debug:
    #screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((480, 320))
else:
    screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
    connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="9600", fast=False, timeout = 30)
    connection.watch(c1, callback=speed_tracker)
    connection.watch(c2, callback=rpm_tracker)
    connection.watch(c3, callback=load_tracker)
    connection.watch(c4, callback=air_temp_tracker)
    connection.watch(c5, callback=cool_temp_tracker)
    connection.watch(c6, callback=intake_temp_tracker)
    connection.watch(c7, callback=intake_pressure_tracker)
    connection.start()

pygame.mouse.set_visible(False)
one_word_json = request_one_word()
one_word = one_word_json['hitokoto']
one_word_from = one_word_json['from']
running =  True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.quit()
                pygame.quit()

    screen.fill(BLACK)
    blit_data_by_value()
    draw_speed_screen()
    draw_rpm_screen()
    draw_load_screen()
    draw_more_info_screen()

    #datetime
    date = datetime.now()
    time_string = date.strftime("%H:%M")
    time_txt = get_number_text(time_string, WHITE, 48)
    screen.blit(time_txt, (188, 0))

    #one word
    one_word_txt = get_text(one_word, WHITE, 24)
    screen.blit(one_word_txt, (0, 256))
    result = calc_one_word_from_position(one_word_from)
    one_word_from_txt = get_text(result['word'], WHITE, 24)
    screen.blit(one_word_from_txt, (result['position'], 286))

    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.2)

pygame.quit()
