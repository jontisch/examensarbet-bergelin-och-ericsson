from os import listdir
from os.path import isfile, join

CALIBRATION_OFFSET = 0.0013
SYSTEM_VOLTAGE = 3.3
PATH = "../BLE_0/"

def calc_power(data):
	start_time = abs(float(data[0].split(',')[0]))
	stop_time = abs(float(data[-1].split(',')[0]))
	vals = list()
	for i in data:
		if(len(i) > 1):
			r = i.split(',')
			vals.append([float(r[0]) + start_time, float(r[1]) + CALIBRATION_OFFSET])
	acc_area = 0
	for i in range(len(vals)-1):
		s_this, s_next = vals[i][0], vals[i+1][0]
		a_this, a_next = vals[i][1], vals[i+1][1]
		acc_area += (a_this+a_next)/2 * (s_next-s_this)
	print(acc_area * SYSTEM_VOLTAGE * 1000)

def get_csv_in_folder(path):
	files = [f for f in listdir(path) if isfile(join(path, f)) and '.csv' in f]
	return files

def parse_file(file):
	try:
		with open(file, "r") as f:
		    rows = f.read().split('\n')
		    return rows
	except:
		print("File can't be read, shutting down...")
		exit()

def main():
	files = get_csv_in_folder(PATH)
	for f in files:
		data = parse_file(PATH + f)
		print(f, end="\t")
		calc_power(data)

if( __name__ == '__main__'):
	main()