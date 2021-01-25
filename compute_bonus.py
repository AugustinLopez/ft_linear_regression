import csv
import math
import matplotlib.pyplot as plt

PATH_DATA="data.csv"
PATH_THETA="thetas.csv"
LEARNING_RATE=0.01
ITERATION=20000

def data_read(pathing):
    try:
        fd = open(pathing, "r", newline='')
        reader = csv.reader(fd, delimiter=',')
        mileage = []
        price = []
        next(reader)
        for row in reader:
            mileage.append(float(row[0]))
            price.append(float(row[1]))
        datapoint = [mileage, price]
    except Exception as e:
        print("data_read:", e)
        return None
    return datapoint

def normalize(maxi, mini, listing):
    if maxi == 0 or mini < 0:
        return None
    new =[]
    for i in range(len(listing)):
        new.append(listing[i] / maxi)
    return new

def gradient_descent(mileage, real_mileage, price, maxi, learning_rate, iteration):
    theta = [0,0]
    fig, ax = plt.subplots()
    plt.xlabel("Mileage")
    plt.ylabel("Price")
    fig.canvas.set_window_title("Mileage / Price")
    for iter in range(1, iteration):
        tmp = [0,0]
        for i in range(len(mileage)):
            tmp[0] += (theta[0] + theta[1] * mileage[i]) - price[i]
            tmp[1] += ((theta[0] + theta[1] * mileage[i]) - price[i]) * mileage[i]
        theta[0] = theta[0] - learning_rate * tmp[0] / len(mileage)
        theta[1] = theta[1] - learning_rate * tmp[1] / len(mileage)
        if iter == 1:
            ver = [0, maxi]
            line, = ax.plot(ver, [0,max(price)], color='g')
            plt.scatter(real_mileage, price)
        if iter % (iteration / 50) == 1:
            print(theta[0])
            hor = [theta[0], theta[0] + theta[1]]
            line.set_data(ver, hor)
            fig.canvas.draw()
            plt.pause(0.05)
    print("graph done!")
    plt.pause(2)
    return (theta)

def theta_create(pathing, theta):
    try:
        fd = open(pathing, "w")
        fd.write("data,value\ntheta_0,"+str(theta[0])+"\ntheta_1,"+str(theta[1])+"\n")
        fd.close()
    except Exception as e:
        print ("theta_create:", e)
        return (-1)
    return (0)

def data_add(pathing, mileage, price, theta):
    try:
        fd = open(pathing, "a")
    except:
        print("data_add:", e)
        return (-1)
    population = len(mileage)
    fd.write("population,"+str(population))
    average_mileage = 0
    average_price = 0
    for i in range(len(mileage)):
        average_mileage += mileage[i] / len(mileage)
        average_price += price[i] / len(price)
    fd.write("\nsmp.av_x,"+str(average_mileage)+"\nsmp.av_y,"+str(average_price))
    var_mileage = 0
    var_price = 0
    covariance = 0
    for i in range(len(mileage)):
        var_mileage += math.pow(mileage[i] - average_mileage, 2.0)
        var_price += math.pow(price[i] - average_price, 2.0)
        covariance += (mileage[i] - average_mileage) * (price[i] - average_price)
    var_price /= (len(price) - 1)
    var_mileage /= (len(mileage) - 1)
    covariance /= (len(mileage) - 1)
    dev_price = math.pow(var_price,0.5)
    dev_mileage = math.pow(var_mileage,0.5)
    correlation = covariance / (dev_price * dev_mileage)
    fd.write("\nsmp.std_x,"+str(dev_mileage)+"\nsmp.std_y,"+str(dev_price))
    fd.write("\nsmp.cor,"+str(correlation))
    xtheta_1 = covariance / var_mileage
    xtheta_0 = average_price - xtheta_1 * average_mileage
    fd.write("\nxtheta_0,"+str(xtheta_0)+"\nxtheta_1,"+str(xtheta_1))
    try:
        fd.close()
    except:
        pass
    return (0)

def main():
    datapoint = data_read(PATH_DATA)
    if datapoint is None:
        return (-1)
    if len(datapoint[0]) == 0:
        print("The dataset is empty.")
        return (0)
    maxi= max(datapoint[0])
    mini = min(datapoint[0])
    mileage = normalize(maxi, mini, datapoint[0])
    if mileage is None:
        print("Cannot normalize mileage data: negative value not supported (illogical)")
        return (-1)
    price = datapoint[1]
    theta = gradient_descent(mileage, datapoint[0], price, maxi, LEARNING_RATE, ITERATION)
    theta[1] = theta[1] / maxi
    theta_create(PATH_THETA, theta)
    data_add(PATH_THETA, datapoint[0], datapoint[1],theta)

if __name__ == "__main__":
    main()