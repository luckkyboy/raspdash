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

wen_quan_font = "wenquanyizenheimono"

if windows_debug:
    #wen_quan_font= "wenquanyizenheimono"
    wen_quan_font = "文泉驿正黑"
    rpm = 2389
    load = 9
    speed = 89
    air_temp = 38
    cool_temp = 18
    intake_temp = 43
    intake_pressure = 57


def draw_screen():
    screen.fill(BLACK)
    # speed
    pygame.draw.rect(screen, GRAY, pygame.Rect(4, 5, 179, 150), 2)
    # rpm
    pygame.draw.rect(screen, GRAY, pygame.Rect(296, 5, 180, 150), 2)
    # load
    pygame.draw.rect(screen, GRAY, pygame.Rect(182, 100, 115, 115), 2)
    # more info
    pygame.draw.rect(screen, GRAY, pygame.Rect(15, 214, 450, 102), 2)

    rpm_txt_font = pygame.font.SysFont(wen_quan_font, 35)
    rpm_txt_render = rpm_txt_font.render("转速", True, GRAY)
    screen.blit(rpm_txt_render, (60, 150))
    rpm_unit_font = pygame.font.SysFont(wen_quan_font, 25)
    rpm_unit_render = rpm_unit_font.render("r/min", True, GRAY)
    screen.blit(rpm_unit_render, (120, 125))

    speed_txt_font = pygame.font.SysFont(wen_quan_font, 35)
    speed_txt_render = speed_txt_font.render("速度", True, GRAY)
    screen.blit(speed_txt_render, (350, 150))
    speed_unit_font = pygame.font.SysFont(wen_quan_font, 25)
    speed_unit_render = speed_unit_font.render("Km/h", True, GRAY)
    screen.blit(speed_unit_render, (410, 125))

    load_txt_font = pygame.font.SysFont(wen_quan_font, 35)
    load_txt_render = load_txt_font.render("负载", True, GRAY)
    screen.blit(load_txt_render, (205, 60))
    load_unit_font = pygame.font.SysFont(wen_quan_font, 35)
    load_unit_render = load_unit_font.render("%", True, GRAY)
    screen.blit(load_unit_render, (268, 178))

    more_info_font = pygame.font.SysFont(wen_quan_font, 20)
    txt1 = more_info_font.render("环境温度", True, WHITE)
    screen.blit(txt1, (30, 252))
    txt2 = more_info_font.render("冷却液温度", True, WHITE)
    screen.blit(txt2, (135, 252))
    txt3 = more_info_font.render("进气温度", True, WHITE)
    screen.blit(txt3, (257, 252))
    txt4 = more_info_font.render("进气压力", True, WHITE)
    screen.blit(txt4, (360, 252))


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

    more_info_font = pygame.font.SysFont(wen_quan_font, 30)
    if air_temp < 0:
        if air_temp > -10:
            air_temp_txt = more_info_font.render(str(air_temp), True, WHITE)
            screen.blit(air_temp_txt, (55, 275))
        else:
            air_temp_txt = more_info_font.render(str(air_temp), True, WHITE)
            screen.blit(air_temp_txt, (49, 275))
    else:
        if air_temp < 10:
            air_temp_txt = more_info_font.render(str(air_temp), True, WHITE)
            screen.blit(air_temp_txt, (60, 275))
        else:
            air_temp_txt = more_info_font.render(str(air_temp), True, WHITE)
            screen.blit(air_temp_txt, (52, 275))

    cool_temp_txt = more_info_font.render(str(cool_temp), True, WHITE)
    screen.blit(cool_temp_txt, (166, 275))

    intake_temp_txt = more_info_font.render(str(intake_temp), True, WHITE)
    screen.blit(intake_temp_txt, (280, 275))

    intake_pressure_txt = more_info_font.render(str(intake_pressure), True, WHITE)
    screen.blit(intake_pressure_txt, (380, 275))

    if rpm < 1000:
        rpm_font = pygame.font.SysFont(wen_quan_font, 80)
        rpm_txt = rpm_font.render(str(rpm), True, WHITE)
        screen.blit(rpm_txt, (22, 30))
    else:
        rpm_font = pygame.font.SysFont(wen_quan_font, 70)
        rpm_txt = rpm_font.render(str(rpm), True, WHITE)
        screen.blit(rpm_txt, (10, 30))

    if load < 10:
        load_font = pygame.font.SysFont(wen_quan_font, 70)
        load_txt = load_font.render(str(load), True, WHITE)
        screen.blit(load_txt, (218, 105))
    else:
        load_font = pygame.font.SysFont(wen_quan_font, 70)
        load_txt = load_font.render(str(load), True, WHITE)
        screen.blit(load_txt, (198, 105))

    if speed < 10:
        speed_font = pygame.font.SysFont(wen_quan_font, 130)
        speed_txt = speed_font.render(str(speed), True, select_color_by_speed())
        screen.blit(speed_txt, (347, 0))
    elif speed >= 10 and speed < 100:
        speed_font = pygame.font.SysFont(wen_quan_font, 115)
        speed_txt = speed_font.render(str(speed), True, select_color_by_speed())
        screen.blit(speed_txt, (317, 10))
    else:
        speed_font = pygame.font.SysFont(wen_quan_font, 100)
        speed_txt = speed_font.render(str(speed), True, select_color_by_speed())
        screen.blit(speed_txt, (294, 15))


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

    draw_screen()
    blit_data_by_value()

    #datetime
    date = datetime.now()
    weekday_index = date.weekday()
    date_string = date.strftime("%Y年%m月%d日 %H:%M:%S") + " " + week_days[weekday_index]
    date_font = pygame.font.SysFont(wen_quan_font, 25)
    date_txt = date_font.render(date_string, True, LIGHT_GREEN)
    screen.blit(date_txt, (55, 220))

    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.2)

pygame.quit()
