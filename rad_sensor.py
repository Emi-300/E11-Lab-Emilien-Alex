from ast import arguments
import csv
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('/home/pi/cape_mca') # capemca.py directory

from capemca import CapeMCA
from capemca import find_all_mcas
from capemca import SPECTRUM_CHANNELS

devices = find_all_mcas()
print(f"Found {len(devices)} MCA device(s)")


if not devices:
    sys.exit(1)

#TODO - save spectra to file (CSV or binary)
#TODO - Parameters (filename, runtime, interval length)


#PARAMETERS

hasfile = False

try:
    file = open(f"data/{sys.argv[1]}.csv","w",newline=None)
except Exception as e:
    print("Unable to read file (remove the .csv from the name)")
    print("----------------------")
    print(e)
else:
    hasfile = True
    csvwriter = csv.writer(file,delimiter=',')
    csvwriter.writerow(["time","cps","totalCount","totalIntervals"] + [f"ch{ch}" for ch in range(SPECTRUM_CHANNELS)])


try:
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 120.0
except Exception as e:
    print("Unable to parse duration argument")
    print("----------------------")
    print(e)
    duration = 120

try:
    window = int(sys.argv[3]) if len(sys.argv) > 3 else 10.0 
except Exception as e:
    print("Unable to parse interval argument")
    print("----------------------")
    print(e)
    window = 10


spectra = []
read_times = []

with CapeMCA() as mca:
    try:
        start = time.time()
        reads = 0
        next_read = start

        while time.time() - start < duration:
            # Wait until the next window boundary
            now = time.time()
            if now < next_read:
                time.sleep(next_read - now)

            read_start = time.time()
            status = mca.read_status()
            spectrum = mca.read_spectrum()
            read_end = time.time()

            # Schedule next read from when this one started
            next_read = read_start + window

            spec_data = spectrum[1:]
            spec_total = sum(spec_data)
            nonzero = sum(1 for ch in spec_data if ch > 0)
            elapsed = read_start - start

            print(f"[{elapsed:6.1f}s] read {reads+1} "
                    f"(took {read_end - read_start:.2f}s): "
                    f"{status.cps} cps, "
                    f"totalCount={status.total_count:g}, "
                    f"intervals={status.total_intervals}")
            print(f"         spectrum: ch0={spectrum[0]}, specSum={spec_total}, "
                    f"nonzeroCh={nonzero}")

            active = [(ch, spectrum[ch]) for ch in range(1, SPECTRUM_CHANNELS)
                        if spectrum[ch] > 0]
            print(f"         channels: {active}")

            spectra.append(spec_data)
            read_times.append(elapsed)
            reads += 1

            if hasfile:
                csvwriter.writerow([elapsed, status.cps, status.total_count,
                                    status.total_intervals] + spec_data)

        print(f"\nCompleted {reads} reads in {time.time() - start:.2f}s "
                f"(window={window}s)")

    except Exception as e:
        print(f"\nError after {reads} reads: {e}")

print("Device closed, exiting.")