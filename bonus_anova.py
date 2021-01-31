import csv
import math
# math is for math.pow(...,0.5)

PATH_DATA="data.csv"
PATH_THETA="thetas_bonus.csv"

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

def calculate_theta(mileage, price):
    if len(mileage) < 3:
        print("data_add: too little data")
        return None
    anova = {}
    population = len(mileage)
    average_mileage = 0
    average_price = 0
    for i in range(len(mileage)):
        average_mileage += mileage[i] / len(mileage)
        average_price += price[i] / len(price)
    var_mileage = 0
    var_price = 0
    covariance = 0
    for i in range(len(mileage)):
        var_mileage += math.pow(mileage[i] - average_mileage, 2.0) / (len(mileage) - 1)
        var_price += math.pow(price[i] - average_price, 2.0) / (len(price) - 1)
        covariance += (mileage[i] - average_mileage) * (price[i] - average_price) / (len(mileage) - 1)
    theta_1 = covariance / var_mileage
    theta_0 = average_price - theta_1 * average_mileage
    anova['population'] = population
    anova['average_x'] = average_mileage
    anova['average_y'] = average_price
    anova['std_x'] = math.pow(var_mileage, 0.5)
    anova['std_y'] = math.pow(var_price, 0.5)
    anova['correlation'] = covariance / (anova['std_x'] * anova['std_y'])
    anova['theta_0'] = theta_0
    anova['theta_1'] = theta_1
    return (anova)

def calculate_statistic(mileage, price, anova):
    anova['R'] = abs(anova['correlation'])
    anova['R^2'] = math.pow(anova['R'],2.0)
    anova['adjusted R^2'] = 1 - ((1 - anova['R^2'])*(anova['population'] - 1)/(anova['population'] - 2))
    SquaredSumError = 0
    SquaredSumRegr = 0
    for i in range(len(mileage)):
        regr = anova['theta_0'] + anova['theta_1'] * mileage[i]
        SquaredSumError += math.pow(regr - price[i], 2.0)
        SquaredSumRegr += math.pow(regr - anova['average_y'], 2.0)
    anova['SEE'] = math.pow(SquaredSumError / (anova['population'] - 2), 0.5)
    anova['F'] = SquaredSumRegr / SquaredSumError * (anova['population'] - 2)
    SquaredKm = (math.pow(anova['std_x'],2.0) * (anova['population'] - 1))
    anova['std_theta_1'] = math.pow((SquaredSumError / (anova['population'] - 2)) / SquaredKm, 0.5)
    tmp_0 = 1/anova['population'] + math.pow(anova['average_x'],2.0) / (math.pow(anova['std_x'],2.0) * (anova['population'] - 1))
    anova['std_theta_0'] = math.pow(math.pow(anova['SEE'], 2.0) * tmp_0, 0.5)
    anova['t_intercept'] = anova['theta_0'] / anova['std_theta_0']
    anova['t_slope'] = anova['theta_1'] / anova['std_theta_1']

def data_create(pathing, anova):
    try:
        fd = open(pathing, "w")
        fd.write("data,value\ntheta_0,"+str(anova['theta_0'])+"\ntheta_1,"+str(anova['theta_1'])+"\n")
        fd.write("population,"+str(anova['population'])+"\n")
        fd.write("average_x,"+str(anova['average_x'])+"\naverage_y,"+str(anova['average_y'])+"\n")
        fd.write("std_x,"+str(anova['std_x'])+"\nstd_y,"+str(anova['std_y'])+"\n")
        fd.write("correlation,"+str(anova['correlation'])+"\nR^2,"+str(anova['R^2'])+"\n")
        fd.write("adjusted R^2,"+str(anova['adjusted R^2'])+"\nSEE,"+str(anova['SEE'])+"\n")
        fd.write("F,"+str(anova['F'])+"\nstd_theta_0,"+str(anova['std_theta_0'])+"\n")
        fd.write("std_theta_1,"+str(anova['std_theta_1'])+"\n")
        fd.write("t_intercept,"+str(anova['t_intercept'])+"\nt_slope,"+str(anova['t_slope'])+"\n")
        print(anova)
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
    anova = calculate_theta(datapoint[0], datapoint[1])
    if anova is None:
        return (-1)
    calculate_statistic(datapoint[0], datapoint[1], anova)
    data_create(PATH_THETA, anova)

if __name__ == "__main__":
    main()
