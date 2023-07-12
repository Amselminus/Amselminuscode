def main():
    #file = "/workspaces/126971925/final_project/personal_information.csv"
    birth = "2004-01-16"
    #login_information = {"account_number" : }

    filenames = ["personal_information.csv", "login_information.csv"]
    for file in filenames:
        with open("/workspaces/126971925/final_project/" + file, "r") as f:
            lines = f.readlines()
        with open(file, "w") as f:
            for line in lines:
                information = line.split(",")
                #personal_information not deleted!!
                if file == "personal_information.csv":
                    if information[3] != birth:
                        f.write(line)
                #else:
                   # if information[0] != login_information["account_number"]:
                   #     f.write(line)

main()