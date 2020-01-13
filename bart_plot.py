from data_storage import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('./map_weekday.png')

def plot_map(curated_train_list):
    print('plot_map hit')
    fig = plt.figure(figsize = (10, 10))
    zoom = 1.0
    w, h = fig.get_size_inches()
    fig.set_size_inches(w * zoom, h * zoom)
    plt.imshow(img)

    for i in curated_train_list:
        plt.plot(float(i[0][0]), float(i[0][1]), 'ko') # or i[1]
        # temp_points.remove()

    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
    print('not locked')


def parse_for_plot(train_list):
    coord_list = []
    for train in train_list:
        train_split = train.split('_')
        train_coord = find_coord(train_split[0], train_split[1])
        if not train_coord:
            continue
        try:
            coord_list.append((train_coord, NumberCars[train_split[2]]))
        except KeyError:
            pass

    return coord_list


def find_coord(stn, color):
    try:
        coord_dict = eval("{}Dict".format(color.title()))
    except NameError:
        return 0
    coord_key = "{}_{}".format(color.upper(), stn)
    try:
        station_coord = coord_dict[coord_key]
    except KeyError as error:  # Cases where there are anomaly line_station pair
        print(error)
        return 0

    return station_coord

