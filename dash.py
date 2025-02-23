import obd
from datetime import datetime
import pygame
import time

#color
WHITE = (255, 255, 255)
GREEN = (127, 255, 0)
GRAY= (230, 230, 230)
RED = (255, 20, 60)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#commands
c1 = obd.commands.SPEED
c2 = obd.commands.RPM
c3 = obd.commands.ENGINE_LOAD
c4 = obd.commands.AMBIANT_AIR_TEMP
c5 = obd.commands.INTAKE_TEMP
c6 = obd.commands.INTAKE_PRESSURE
c7 = obd.commands.FUEL_PRESSURE


#display params
speed = 0
rpm = 0
load = 0
air_temp = 0
intake_temp = 0
intake_pressure = 0
fuel_pressure = 0

#screen
screen = None

windows_debug = False

wen_quan_font = "wenquanyizenheimono"

if windows_debug:
    #wen_quan_font= "wenquanyizenheimono"
    wen_quan_font = "文泉驿正黑"
    speed = 56
    rpm = 2389
    load = 9
    air_temp = 38
    intake_temp = 43
    intake_pressure = 57
    fuel_pressure = 358


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

    speed_txt_font = pygame.font.SysFont(wen_quan_font, 35)
    speed_txt_render = speed_txt_font.render("速度", True, GRAY)
    screen.blit(speed_txt_render, (60, 150))
    speed_unit_font = pygame.font.SysFont(wen_quan_font, 25)
    speed_unit_render = speed_unit_font.render("Km/h", True, GRAY)
    screen.blit(speed_unit_render, (120, 125))

    rpm_txt_font = pygame.font.SysFont(wen_quan_font, 35)
    rpm_txt_render = rpm_txt_font.render("转速", True, GRAY)
    screen.blit(rpm_txt_render, (350, 150))
    rpm_unit_font = pygame.font.SysFont(wen_quan_font, 25)
    rpm_unit_render = rpm_unit_font.render("r/min", True, GRAY)
    screen.blit(rpm_unit_render, (410, 125))

    load_txt_font = pygame.font.SysFont(wen_quan_font, 35)
    load_txt_render = load_txt_font.render("负载", True, GRAY)
    screen.blit(load_txt_render, (205, 60))
    load_unit_font = pygame.font.SysFont(wen_quan_font, 35)
    load_unit_render = load_unit_font.render("%", True, GRAY)
    screen.blit(load_unit_render, (268, 178))

    more_info_font = pygame.font.SysFont(wen_quan_font, 25)
    txt1 = more_info_font.render("环境温度", True, WHITE)
    screen.blit(txt1, (20, 245))
    txt2 = more_info_font.render("进气温度", True, WHITE)
    screen.blit(txt2, (135, 245))
    txt3 = more_info_font.render("进气压力", True, WHITE)
    screen.blit(txt3, (248, 245))
    txt4 = more_info_font.render("燃油压力", True, WHITE)
    screen.blit(txt4, (360, 245))


def speed_tracker(obd_response):
    global speed
    if not obd_response.is_null():
        speed = int(obd_response.value.magnitude)


def rpm_tracker(obd_response):
    global rpm
    if not obd_response.is_null():
        rpm = int(obd_response.value.magnitude)


def load_tracker(obd_response):
    global load
    if not obd_response.is_null():
        load = int(obd_response.value.magnitude)


def air_temp_tracker(obd_response):
    global air_temp
    if not obd_response.is_null():
        air_temp = int(obd_response.value.magnitude)


def intake_temp_tracker(obd_response):
    global intake_temp
    if not obd_response.is_null():
        intake_temp = int(obd_response.value.magnitude)


def intake_pressure_tracker(obd_response):
    global intake_pressure
    if not obd_response.is_null():
        intake_pressure = int(obd_response.value.magnitude)


def fuel_pressure_tracker(obd_response):
    global fuel_pressure
    if not obd_response.is_null():
        fuel_pressure = int(obd_response.value.magnitude)


def blit_date_by_value():
    global speed
    global rpm
    global load
    global air_temp
    global intake_temp
    global intake_pressure
    global fuel_pressure

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

    intake_temp_txt = more_info_font.render(str(intake_temp), True, WHITE)
    screen.blit(intake_temp_txt, (166, 275))

    intake_pressure_txt = more_info_font.render(str(intake_pressure), True, WHITE)
    screen.blit(intake_pressure_txt, (280, 275))

    fuel_pressure_txt = more_info_font.render(str(fuel_pressure), True, WHITE)
    screen.blit(fuel_pressure_txt, (384, 275))

    if speed < 10:
        speed_font = pygame.font.SysFont(wen_quan_font, 115)
        speed_txt = speed_font.render(str(speed), True, GREEN)
        screen.blit(speed_txt, (60, 10))
    elif speed >= 10 and speed < 100:
        speed_font = pygame.font.SysFont(wen_quan_font, 95)
        font_color = WHITE
        if speed < 70:
            font_color = GREEN
        elif speed >=70:
            font_color = BLUE
        speed_txt = speed_font.render(str(speed), True, font_color)
        screen.blit(speed_txt, (35, 20))
    else:
        speed_font = pygame.font.SysFont(wen_quan_font, 75)
        font_color = BLUE
        if speed >=100 and speed < 115:
            font_color = YELLOW
        elif speed >= 115:
            font_color = RED
        speed_txt = speed_font.render(str(speed), True, font_color)
        screen.blit(speed_txt, (25, 30))

    if rpm < 1000:
        rpm_font = pygame.font.SysFont(wen_quan_font, 80)
        rpm_txt = rpm_font.render(str(rpm), True, WHITE)
        screen.blit(rpm_txt, (310, 30))
    else:
        rpm_font = pygame.font.SysFont(wen_quan_font, 70)
        rpm_txt = rpm_font.render(str(rpm), True, WHITE)
        screen.blit(rpm_txt, (302, 30))

    if load < 10:
        load_font = pygame.font.SysFont(wen_quan_font, 70)
        load_txt = load_font.render(str(load), True, WHITE)
        screen.blit(load_txt, (218, 105))
    else:
        load_font = pygame.font.SysFont(wen_quan_font, 70)
        load_txt = load_font.render(str(load), True, WHITE)
        screen.blit(load_txt, (198, 105))


pygame.init()
if windows_debug:
    screen = pygame.display.set_mode((480, 320))
else:
    screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
    connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="9600", fast=False, timeout = 30)
    connection.watch(c1, callback=speed_tracker)
    connection.watch(c2, callback=rpm_tracker)
    connection.watch(c3, callback=load_tracker)
    connection.watch(c4, callback=water_temp_tracker)
    connection.watch(c5, callback=control_module_voltage_tracker)
    connection.watch(c6, callback=air_temp_tracker)
    connection.watch(c7, callback=intake_temp_tracker)
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
    blit_date_by_value()

    #datetime
    date = datetime.now()
    date_string = date.strftime("%Y年%m月%d日 %H:%M:%S")
    date_font = pygame.font.SysFont(wen_quan_font, 20)
    date_txt = date_font.render(date_string, True, GREEN)
    screen.blit(date_txt, (115, 220))

    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.2)

pygame.quit()
