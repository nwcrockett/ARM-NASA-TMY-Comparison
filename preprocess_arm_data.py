import os
import pandas as pd


def join_arm_data_files_together(directory_list):
    df_arm = pd.read_csv(directory_list[0])
    del(directory_list[0])
    df_arm = df_arm[['date_time', 'down_short_hemisp']]
    for item in directory_list:
        print(item)
        df_temp = pd.read_csv(item)
        df_temp = df_temp[['date_time', 'down_short_hemisp']]
        df_arm = pd.concat([df_arm, df_temp])

    os.chdir("/home/nelson/PycharmProjects/Arm_data_comparision")
    df_arm.reset_index(drop=True)

    df_arm.to_csv("processed_arm_data.csv")


if __name__ == "__main__":

    os.chdir("/media/nelson/LinuxExt/ARM data for Barrow/207121_extractedData/ascii-csv")
    direct = os.listdir()
    direct.sort()
    join_arm_data_files_together(direct)


