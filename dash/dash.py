import obd
from datetime import datetime
import pygame
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

week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

#screen
screen = None

windows_debug = False

display_font = "wenquanyizenheimono"

if windows_debug:
    #display_font= "wenquanyizenheimono"
    display_font = "文泉驿正黑"
    rpm = 2389
    load = 8
    speed = 128
    air_temp = 38
    cool_temp = 98
    intake_temp = 43
    intake_pressure = 57


def get_number_text(text, color, size, alpha=255):
    text_surface = pygame.font.SysFont(display_font, size).render(str(text), True, color)
    text_surface.set_alpha(alpha)
    return text_surface


def get_text(text, color, size, alpha=255):
    text_surface = pygame.font.SysFont(display_font, size).render(str(text), True, color)
    text_surface.set_alpha(alpha)
    return text_surface

def get_number_text_stroke(text, color, size, mbSize, mbColor, alpha=255, mbAlpha=255):
    # 参数说明: text-要显示的文本 color-文本颜色 size-文本尺寸 mbSize-描边粗细 mbColor-描边颜色 alpha-文本不透明度 mbAlpha-描边不透明度
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
            air_temp_txt = get_number_text(str(air_temp), WHITE, 50)
            screen.blit(air_temp_txt, (55, 188))
        else:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 50)
            screen.blit(air_temp_txt, (49, 188))
    else:
        if air_temp < 10:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 50)
            screen.blit(air_temp_txt, (60, 188))
        else:
            air_temp_txt = get_number_text(str(air_temp), WHITE, 50)
            screen.blit(air_temp_txt, (32, 188))

    cool_temp_txt = get_number_text(str(cool_temp), WHITE, 50)
    screen.blit(cool_temp_txt, (153, 188))

    intake_temp_txt = get_number_text(str(intake_temp), WHITE, 50)
    screen.blit(intake_temp_txt, (270, 188))

    intake_pressure_txt = get_number_text(str(intake_pressure), WHITE, 50)
    screen.blit(intake_pressure_txt, (390, 188))

    if rpm < 1000:
        rpm_txt = get_number_text(str(rpm), WHITE, 80)
        screen.blit(rpm_txt, (22, 30))
    else:
        rpm_txt = get_number_text(str(rpm), WHITE, 70)
        screen.blit(rpm_txt, (10, 30))

    if load < 10:
        load_txt = get_number_text(str(load), WHITE, 100)
        screen.blit(load_txt, (209, 65))
    else:
        load_txt = get_number_text(str(load), WHITE, 90)
        screen.blit(load_txt, (185, 70))

    if speed < 10:
        speed_txt = get_number_text_stroke(str(speed), WHITE, 135, 4, select_color_by_speed())
        screen.blit(speed_txt, (341, 0))
    elif speed >= 10 and speed < 100:
        speed_txt = get_number_text_stroke(str(speed), WHITE, 115, 4, select_color_by_speed())
        screen.blit(speed_txt, (314, 5))
    else:
        speed_txt = get_number_text_stroke(str(speed), WHITE, 100, 4, select_color_by_speed())
        screen.blit(speed_txt, (290, 15))


def draw_rpm_screen():
    # rpm
    pygame.draw.rect(screen, GRAY, pygame.Rect(2, 5, 182, 150), 2)
    rpm_txt_render = get_text("RPM", WHITE, 35)
    screen.blit(rpm_txt_render, (55, 151))
    rpm_unit_render = get_text("r/min", WHITE, 25)
    screen.blit(rpm_unit_render, (114, 128))


def draw_load_screen():
    # load
    pygame.draw.rect(screen, GRAY, pygame.Rect(182, 70, 115, 115), 2)

    load_txt_render = get_text("Load", WHITE, 35)
    screen.blit(load_txt_render, (200, 34))
    load_unit_render = get_text("%", WHITE, 25)
    screen.blit(load_unit_render, (273, 156))


def draw_speed_screen():
    # speed
    pygame.draw.rect(screen, GRAY, pygame.Rect(295, 5, 183, 150), 2)
    speed_txt_render = get_text("Speed", WHITE, 35)
    screen.blit(speed_txt_render, (332, 152))
    speed_unit_render = get_text("Km/h", WHITE, 25)
    screen.blit(speed_unit_render, (406, 128))


def draw_more_info_screen():
    # more info
    pygame.draw.rect(screen, GRAY, pygame.Rect(2, 190, 476, 104), 2)

    pygame.draw.rect(screen, GRAY, pygame.Rect(2, 190, 122, 70), 2)
    txt1 = get_text("Ambient temp", WHITE, 18)
    screen.blit(txt1, (2, 240))
    pygame.draw.rect(screen, GRAY, pygame.Rect(122, 190, 120, 70), 2)
    txt2 = get_text("Coolant temp", WHITE, 18)
    screen.blit(txt2, (124, 240))
    pygame.draw.rect(screen, GRAY, pygame.Rect(240, 190, 120, 70), 2)
    txt3 = get_text("Intake temp", WHITE, 18)
    screen.blit(txt3, (248, 240))
    pygame.draw.rect(screen, GRAY, pygame.Rect(358, 190, 120, 70), 2)
    txt4 = get_text("Intake press", WHITE, 18)
    screen.blit(txt4, (366, 240))


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
    weekday_index = date.weekday()
    date_string = date.strftime("%Y-%m-%d %A %H:%M:%S")
    date_font = pygame.font.SysFont(display_font, 30)
    date_txt = date_font.render(date_string, True, WHITE)
    screen.blit(date_txt, (18, 260))

    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.2)

pygame.quit()
