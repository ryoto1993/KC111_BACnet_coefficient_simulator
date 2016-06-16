# coding: utf-8

from ANA_RC.equipment import *
import csv


class Initial:
    # 照明の数
    light = 12
    # センサの数
    sensor = 66
    # 使用するセンサのリスト
    sensorConfig = []
    # 重み
    weight = 15
    # 使用する影響度ファイル
    file_name = "data/example.csv"

    # 設定用変数
    lightList = []
    sensorList = []
    useSensorList = []
    powerMeter = []

    @staticmethod
    def set():
        Initial.lightList = []
        Initial.sensorList = []
        Initial.useSensorList = []
        Initial.powerMeter = []

        f = open(Initial.file_name, 'r')
        reader = csv.reader(f)
        next(reader)  # ヘッダを読み飛ばす

        # 装置の準備
        for var in range(0, Initial.light):
            Initial.lightList.append(Light())
        for var in range(0, Initial.sensor):
            Initial.sensorList.append(Sensor())
            Initial.sensorList[var].set_influence(next(reader))

        Initial.powerMeter.append(PowerMeter())
        Initial.powerMeter[0].set_light_list(Initial.lightList)

        # 使用するセンサを設定
        for s in Initial.sensorConfig:
            Initial.sensorList[s[0]-1].set_target_illuminance(s[1])
            Initial.useSensorList.append(Initial.sensorList[s[0]-1])

        # 使用する照明を設定
        for l in Initial.lightList:
            l.set_sensor_list(Initial.useSensorList)
            l.set_weight(Initial.weight)
            l.set_power_meter(Initial.powerMeter[0])
