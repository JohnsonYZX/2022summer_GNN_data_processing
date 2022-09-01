import numpy as np
import os
from tqdm import tqdm
import sys

class Table:
    def __init__(self, video_name, output_name, cameras, time):
        self.video_name = video_name
        self.output_name = output_name
        self.cameras = cameras
        self.time = time
        self.data = np.zeros([time, cameras])
        self.collected = 0


requirement_file = open("data_requirement.txt", "rt")
data = []
while True:
    text = requirement_file.readline()
    if text == "":
        break
    else:
        words = text.split()
        video_name = words[0]
        output_name = words[1]
        cameras = int(words[2])
        time = int(words[3])
        data.append(Table(video_name, output_name, cameras, time))


file_names = os.listdir("data")
with tqdm(total=len(file_names), desc="processing data", unit="file", file=sys.stdout) as pbar:
    for file_name in file_names:
        file = open("data/" + file_name, "rt")
        text = file.readlines()
        if len(text) <= 2:
            continue
        last_words = text[-2].split()
        if len(last_words) < 4:
            last_words = text[-3].split()
        name = last_words[1]
        a = last_words[4]
        b = a.split(":")[1]
        max_time = round(int(last_words[4].split(":")[1]) / 1000)
        for table in data:
            if table.video_name != name or table.time > max_time:
                continue
            new_data = np.zeros([table.time, table.cameras])
            table.collected += 1
            file = open("data/" + file_name, "rt")
            t = 1
            views = 0
            count = 0
            last_time = -1
            while True:
                text = file.readline()
                words = text.split()
                if len(words) < 5:
                    break
                current_time = int(words[4].split(":")[1]) / 1000
                if current_time == last_time:
                    if round(current_time) != table.time:
                        new_data = np.zeros([table.time, table.cameras])
                        table.collected -= 1
                        break
                    view = round(views / count)
                    new_data[t - 1][view] += 1
                    break
                last_time = current_time
                if current_time > t:
                    view = int(views / count)
                    new_data[t - 1][view] += 1
                    if t == table.time:
                        break
                    t += 1
                    views = 0
                    count = 0
                views += int(words[3])
                count += 1
            table.data += new_data
        pbar.update(1)
print("done")
output_statistics = open("output_statistics.txt", "w")
for table in data:
    np.savetxt("output/" + table.output_name + "_" + str(table.time) + ".csv", table.data, delimiter=",", fmt="%i," * table.cameras)
    output_statistics.write(table.output_name + "_" + str(table.time) + ": " + str(table.collected) + "\n")
output_statistics.close()
print("saving done")
