from nptdms import TdmsFile

# Specify the path to your TDMS file
file_path = "C:\\Users\\louis\\PycharmProjects\\SVV\\B50\\DSE-Group16\\Stability\\wind_tunnel_test\\data\\data\\id_0_ts_1_aoa_-8_Vpp_0_fburst_X_dutycycle_X.tdms"

# Read the TDMS file
tdms_file = TdmsFile.read(file_path)

# Access groups and channels within the TDMS file
groups = tdms_file.groups()
channels = tdms_file["Group"]["Channel"]

# Access the data within a channel
data = channels[0].time_track()