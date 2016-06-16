# coding: utf-8

from ANA_DB.anadb import *
from initial import *


class Routine:
    # 使用する影響度ファイルを指定
    file_name = "data/coefficient4_reverse.csv"
    # センサ数を指定
    Initial.sensor = 54
    # はじめのセンサ位置を指定
    start_sensor = 1
    # 固定するセンサ番号を指定
    fix_sensor = 29

    def __init__(self):
        self.ana_db = AnaDb
        Initial.coefficient_file = Routine.file_name

    def start(self):
        # csvを作成
        # csvの作成
        file_name3 = "result/" + "300.csv"
        file_name5 = "result/" + "500.csv"
        file_name7 = "result/" + "700.csv"
        save_csv3 = open(file_name3, 'w')
        save_csv5 = open(file_name5, 'w')
        save_csv7 = open(file_name7, 'w')
        csv_writer3 = csv.writer(save_csv3)
        csv_writer5 = csv.writer(save_csv5)
        csv_writer7 = csv.writer(save_csv7)
        csv_list = ["Position", "min", "max"]
        csv_writer3.writerow(csv_list)
        csv_writer5.writerow(csv_list)
        csv_writer7.writerow(csv_list)

        # 10 cm間隔で簡易ANA/DBを実行
        for lum in range(0, 1):
            for pos in range(Routine.start_sensor, Routine.fix_sensor):
                min_a = 10000
                max_a = -1

                print(pos)

                for minmax in range(100, 1000, 50):
                    fixlum = 0
                    Initial.sensorConfig = []
                    Light.id = 1
                    if lum == 0:
                        fixlum = 300
                    elif lum == 1:
                        fixlum = 500
                    elif lum == 2:
                        fixlum = 700
                    Initial.sensorConfig.append([Routine.fix_sensor, fixlum])
                    Initial.sensorConfig.append([pos, minmax])

                    Initial.set()
                    self.ana_db = None
                    self.ana_db = AnaDb()
                    self.ana_db.start()

                    sensor_move = Initial.useSensorList[0].get_history()
                    sensor_fix = Initial.useSensorList[1].get_history()

                    for i in range(0, len(sensor_fix)):
                        if fixlum*0.93 < sensor_move[i] < fixlum*1.07 and minmax*0.93 < sensor_fix[i] < minmax*1.07:
                            if minmax < min_a:
                                min_a = sensor_fix[i]
                            if max_a < minmax:
                                max_a = sensor_fix[i]

                # CSVに最小と最大を書き込む
                csv_list = [str(10 * (Routine.fix_sensor - pos)), str(min_a), str(max_a)]
                if lum == 0:
                    csv_writer3.writerow(csv_list)
                elif lum == 1:
                    csv_writer5.writerow(csv_list)
                elif lum == 2:
                    csv_writer7.writerow(csv_list)
