import sys
import os
import json
import math
import matplotlib.pyplot as plt
import matplotlib.colors

path_dir_annotation = 'C:\\project\\kexxu\\dataset\\instancegroup\\ig-json-use'


def get_color(value):

    cmap = plt.cm.jet
    norm = matplotlib.colors.Normalize(vmin=0, vmax=0.1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    return sm.to_rgba(value)
    
def parse_export(list_line):
    list_message = []
    for i, line in enumerate(list_line):
        if line.strip() == "":
            continue
        str_type = line.split(' ')[0]
        line_json = line[len(str_type) + 1:]
        
        try:
            payload = json.loads(line_json)
        except:
            print(i)
            print(line_json) 
            exit()
        list_message.append({'type_message':str_type, 'payload':payload})
    return list_message

def create_stress(message_feature_0, message_feature_1):
    dict_0 = {}
    dict_1 = {}
    for feature in message_feature_0['payload']:
        dict_0[feature['Feature']] = feature['Value']

    for feature in message_feature_1['payload']:
        if not 'Value' in feature:
            return None
        dict_1[feature['Feature']] = feature['Value']
    
    duration_ms =  dict_1['timestamp_ms'] - dict_0['timestamp_ms']   
    dif_x = dict_1['pupil_pos_x'] - dict_0['pupil_pos_x']    
    dif_y = dict_1['pupil_pos_y'] - dict_0['pupil_pos_y']    
    movement_px = math.sqrt((dif_x * dif_x) + (dif_y * dif_y)) * 320
    return {'movement_px':movement_px, 'duration_ms':duration_ms}

def process(list_message):
    list_segment = []
    list_stress = []
    message_gps_last = None
    message_feature_last = None
    for message in list_message:
        if message['type_message'] == 'gps':
            if message_gps_last == None:
                message_gps_last = message
            else:
                lat_start = message_gps_last['payload']['Lat']
                long_start = message_gps_last['payload']['Long']
                lat_end = message['payload']['Lat']
                long_end = message['payload']['Long']

                if len(list_stress) == 0:
                    mean_stress = 0
                else:
                    summed_movement = 0
                    summed_duration = 0
                    for stress in list_stress:
                        summed_movement += stress['movement_px']
                        summed_duration += stress['duration_ms']
                    mean_stress = summed_movement / summed_duration
                    list_stress = []
                print(mean_stress)
                color_tuple = get_color(mean_stress)
                color_float = [color_tuple[0], color_tuple[1], color_tuple[2]]
                color_rgb = [int(color_tuple[0] * 255), int(color_tuple[1]) * 255, int(color_tuple[2] * 255)]
                list_segment.append({
                    'lat_start':lat_start,
                    'long_start':long_start,
                    'lat_end':lat_end,
                    'long_end':long_end,
                    'mean_stress':mean_stress,
                    'color_float':color_float,
                    'color_rgb':color_rgb
                })
                message_gps_last = message
        if message['type_message'] == 'feature':
            if message_feature_last == None:
                message_feature_last = message
            else:
                stress = create_stress(message_feature_last, message)
                if stress:
                    list_stress.append(stress)
                    message_feature_last = message
    return list_segment

    
list_name_file = os.listdir(path_dir_annotation)
list_list_segment = []
for name_file in list_name_file:
    path_file_source = os.path.join(path_dir_annotation, name_file)
    path_file_target = name_file
    print(name_file)
    with open(path_file_source, 'r') as file:
        list_line = file.readlines()
    list_message = parse_export(list_line)
    list_segment = process(list_message)
    result = {'list_segment':list_segment}
    with open(path_file_target, 'w') as file:
        json.dump(result,file)

    list_list_segment.append(list_segment)



for i, list_segment in enumerate(list_list_segment):
    for i, segement in enumerate(list_segment):
        x0 = segement['long_start']
        x1 = segement['long_end']
        y0 = segement['lat_start']
        y1 = segement['lat_end']
        color = segement['color_float']
        plt.plot([x0,x1], [y0, y1], color=color)
    plt.show()

    
        


