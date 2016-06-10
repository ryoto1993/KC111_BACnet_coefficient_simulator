# coding: utf-8

from ANA_RC.anarc import *


class Routine:
    # センサ数を指定
    Initial.sensor = 54

    # はじめのセンサ位置を指定
    start_sensor = 0

    # 固定するセンサ番号を指定
    fix_sensor = 29

    # 方向を指定
    # 1:NE->SW, 2:SW->NE, 3:NW->SE, 4:SE->NW
    direction = 1
    direction_name = "NE->SW"

    # 使用する影響度ファイルを指定
    file_name = "data/coefficient4.csv"

    def __init__(self):
        self.anarc = AnaRc
        Initial.file_name = Routine.file_name

    def start(self):
        # csvを作成
        # csvの作成
        file_name3 = "result/" + str(Routine.fix_sensor) + "_" + Routine.direction_name + "_300.csv"
        file_name5 = "result/" + str(Routine.fix_sensor) + "_" + Routine.direction_name + "_500.csv"
        file_name7 = "result/" + str(Routine.fix_sensor) + "_" + Routine.direction_name + "_700.csv"
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
        for lum in range(0, 3):
            for pos in range(Routine.start_sensor, Routine.fix_sensor):
                min_a = 10000
                max_a = -1

                for minmax in range(200, 1000, 100):
                    fixlum = 0
                    print(pos)
                    Initial.sensorConfig = []
                    if lum == 0:
                        fixlum = 300
                    elif lum == 1:
                        fixlum = 500
                    elif lum == 2:
                        fixlum = 700
                    Initial.sensorConfig.append([Routine.fix_sensor, fixlum])
                    Initial.sensorConfig.append([pos, minmax])

                    Initial.set()
                    self.anarc = None
                    self.anarc = AnaRc()
                    self.anarc.start()

                    if(fixlum-20 < Initial.useSensorList[0].get_illuminance() < fixlum + 20 \
                        and minmax - 20 < Initial.useSensorList[1].get_illuminance() < minmax + 20):
                        print("say")
                        if minmax < min_a:
                            min_a = minmax
                        if max_a < minmax:
                            max_a = minmax

                # CSVに最小と最大を書き込む
                csv_list = [str(10 * (Routine.fix_sensor - pos)), str(min_a), str(max_a)]
                if lum == 0:
                    csv_writer3.writerow(csv_list)
                elif lum == 1:
                    csv_writer5.writerow(csv_list)
                elif lum == 2:
                    csv_writer7.writerow(csv_list)
