import csv
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
            print(str(theta[0]) + " ; " + str(theta[1]/maxi))
            hor = [theta[0], theta[0] + theta[1]]
            line.set_data(ver, hor)
            fig.canvas.draw()
            plt.pause(0.05)
    print("graph done!")
    plt.show()
    return (theta)

def theta_create(pathing, theta):
    try:
        fd = open(pathing, "w")
        fd.write("data,value\ntheta_0,"+str(theta[0])+"\ntheta_1,"+str(theta[1])+"\n")
        fd.write("population,"+str(population)+"\n")
        fd.write("learning rate,"+str(LEARNING_RATE)+"\n")
        fd.write("iteration,"+str(ITERATION)+"\n")
        fd.close()
    except Exception as e:
        print ("theta_create:", e)
        return (-1)
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
        print("negative value not supported (illogical in this context)")
        return (-1)
    price = datapoint[1]
    theta = gradient_descent(mileage, datapoint[0], price, maxi, LEARNING_RATE, ITERATION)
    theta[1] = theta[1] / maxi
    theta_create(PATH_THETA, theta)

if __name__ == "__main__":
    main()
