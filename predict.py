from os import path
import csv

PATH_THETA = "thetas.csv"
DEFAULT_FORMAT = "data,value\ntheta_0,0\ntheta_1,0\n"

def theta_create(pathing):
    try:
        fd = open(pathing, "w")
        fd.write(DEFAULT_FORMAT)
        fd.close()
    except Exception as e:
        print ("theta_create:", e)
        return (-1)
    return (0)

def theta_read(pathing):
    try:
        fd = open(pathing, "r", newline='')
        reader = csv.reader(fd, delimiter=',')
        header = next(reader)
        theta = [None] * 2
        theta[0] = float(next(reader)[1])
        theta[1] = float(next(reader)[1])
    except Exception as e:
        print ("theta_read:", e)
        print ("Fatal Error: unexpected csv format\n\nExpected:")
        print (DEFAULT_FORMAT)
        return (None)
    try:
        fd.close()
    except:
        pass
    return (theta)

def main():
    if not path.exists(PATH_THETA):
        print("File", PATH_THETA, "not found. Creating one...")
        if (theta_create(PATH_THETA) == -1):
            return (-1)
    theta = theta_read(PATH_THETA)
    if theta == None:
        return (-1)
    try:
        mileage = float(input("Enter mileage: "))
    except Exception as e:
        print("Input error: ", e)
        return (-1)
    print(theta[0] + theta[1] * mileage)
    return (0)

if __name__ == "__main__":
    main()
