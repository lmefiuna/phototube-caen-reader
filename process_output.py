#!/usr/bin/env python

import sys
import os
import csv
import numpy as np
from scipy import integrate
from wavedump_data_reader import read_wave_batch, CAEN_SAMPLING_PERIOD_SECONDS

filename = sys.argv[1]
filename_base = os.path.splitext(os.path.basename(filename))[0]
timestamp = int(filename_base.split("-")[0])
output_csv_file = sys.argv[2]


print(f"Processing {filename}")
with open(filename, "rb") as f:
    waves = read_wave_batch(f)

energies = np.array((), dtype=np.float64)
for wave in waves:
    energies = np.append(energies, -integrate.trapz(
        wave[1], wave[0], dx=CAEN_SAMPLING_PERIOD_SECONDS)/CAEN_SAMPLING_PERIOD_SECONDS)
average_energy = np.average(energies)
print(f"Average energy of batch: {average_energy}")

with open(output_csv_file, mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=("timestamp","average_energy"))
    if file.tell() == 0:
        writer.writeheader()
    
    writer.writerow({"timestamp": timestamp, "average_energy": average_energy})