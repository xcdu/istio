import os
import csv

def main():
    data_path = "post_fixed.csv"
    with open(data_path, encoding="utf8") as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        first_line = True
        train = True #(if false then test)
        valid_labels = ["General", "Configuration", "Telemetry", "Networking", "Security"]
        for row in data:
            if first_line:
                first_line = False
            else:
                if row[1] == '0' and row[7] in valid_labels:
                    if train: #part of the training data
                        #print(row[6])
                        f = open("train/" + row[7] + "/" + row[0] + ".txt", "w", encoding="utf-8")
                        f.write(row[6])
                        f.close()
                        train = not train
                    else: #part of the testing data
                        #print(row[6])
                        f = open("test/" + row[7] + "/" + row[0] + ".txt", "w", encoding="utf-8")
                        f.write(row[6])
                        f.close()
                        train = not train

if __name__ == '__main__':
        main()
