import os
from multiprocessing import Pool
from MainStatistics import MainStatistics
from StatisticsMerger import StatisticsMerger
import concurrent.futures as pool
import pprint

class AsynchStatisticsLoader:
    @staticmethod
    def make_statistics(vacancy_name, full_file_name):
        files_list = os.listdir(f'parsed_data')
        vacancy_tuple_array = []
        for a in files_list:
            vacancy_tuple_array.append((a, vacancy_name))

        with pool.ThreadPoolExecutor(max_workers=len(files_list)) as executer:
           results_array = executer.map(MainStatistics.make_statistics_dictionaries, vacancy_tuple_array)

        #with Pool(len(files_list)) as p:
            #results_array = p.map(MainStatistics.make_statistics_dictionaries, vacancy_tuple_array)

        StatisticsMerger.merge_statistics(full_file_name=full_file_name, statistics_objects_array=results_array)






