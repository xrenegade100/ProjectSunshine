import os
import time
from argparse import ArgumentParser
from pathlib import Path

import pandas

from analyzer import Analyzer
from app.common import util
from app.common.error_handler import handle_error, ErrorSeverity
from app.common.testing_list import TestingPackage
from app.model.input import Input
from app.model.project import Project
from app.nlp.pos_tagger_stanford import POSTaggerStanford
from app.nlp.splitter import Splitter
from app.service.result_writer import ResultWriter


class Main:

    def __init__(self):
        self.project = None
        self.files = []

        parser = ArgumentParser(util.get_config_setting('general', 'name'))
        parser.add_argument("-f", "--file", dest="arg_file", required=True,
                            help="Project Configuration file", metavar="FILE")
        args = parser.parse_args()

        if not os.path.exists(args.arg_file) or not os.path.isfile(args.arg_file):
            error_message = "Invalid Configuration File: \'%s\'" % str(args.arg_file)
            handle_error('Main', error_message, ErrorSeverity.Critical, True)

        self.project = Project(args.arg_file)
        self.__read_input()

    def __read_input(self):
        path_string = self.project.input_file
        input_data = pandas.read_csv(path_string)
        if len(input_data) == 0:
            error_message = "Input CSV file cannot be empty: \'%s\'" % str(path_string)
            handle_error('Main', error_message, ErrorSeverity.Critical, True)

        self.files = []
        file_extensions = util.get_supported_file_extensions()
        for i, item in input_data.iterrows():
            path = Path(item[0])
            path_string = str(path)

            if os.path.isdir(path_string):
                source_files = [p for p in path.rglob('*') if p.suffix in file_extensions]
                for file in source_files:
                    input_item = Input(str(file), item[1], item[2])
                    self.files.append(input_item)

            elif os.path.isfile(path_string):
                if path_string.lower().endswith(tuple(file_extensions)):
                    input_item = Input(path_string, item[1], item[2])
                    self.files.append(input_item)
            else:
                error_message = "Invalid files provided in input CSV file: \'%s\'" % str(path_string)
                handle_error('Main', error_message, ErrorSeverity.Critical, True)

        if len(self.files) == 0:
            error_message = "Invalid files provided in input CSV file: \'%s\'" % str(path_string)
            handle_error('Main', error_message, ErrorSeverity.Critical, True)

    def run_analysis(self):
        time_analysis_start = time.time()
        results = None
        tagger = POSTaggerStanford()
        splitter = Splitter()
        splitter.set_project(self.project)
        testing_package = TestingPackage()
        testing_package.set_project(self.project)
        for file in self.files:
            time_file_start = time.time()
            print("Analyzing: %s ..." % (file.path), end='', flush=True)
            a = Analyzer(self.project, file.path, file.type)
            results = ResultWriter()
            results.save_issues(a.analyze())
            time_file_end = time.time()
            print('done! (%s seconds)' %str(time_file_end - time_file_start))
        tagger.terminate()
        time_analysis_end = time.time()
        print("Analysis completed in " + str(time_analysis_end - time_analysis_start) + " seconds")


if __name__ == '__main__':
    main = Main()
    main.run_analysis()
