import logging
import time

import argparse
import configparser
import io
import os
from collections import defaultdict


CONFIG_FILE = "cfg/main_cfg.cfg"


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def unique_config_sections(config_file):
    """Convert all config sections to have unique names.

    Adds unique suffixes to config sections for compability with configparser.
    """
    section_counters = defaultdict(int)
    output_stream = io.StringIO()
    with open(config_file) as fin:
        for line in fin:
            if line.startswith('['):
                section = line.strip().strip('[]')
                _section = section + '_' + str(section_counters[section])
                section_counters[section] += 1
                line = line.replace(section, _section)
            output_stream.write(line)
    output_stream.seek(0)
    return output_stream



def read_train_options(train_options):
    """
    parse train_options into a list of encoded intergers
    ex: "1,2" -> ["1_0", "2_0"]
    """
    return ["{}_0".format(int(i)) for i in train_options.split(",")]


def gen_log_dir(config_file):
    """
    Gen directory for log files. Create directory if neccesary
    """
    log_dir = config_file.split("/")[-1].split(".")[0]
    log_dir = "./logs/" + log_dir
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    return log_dir

if __name__ == "__main__":
    log_dir = gen_log_dir(CONFIG_FILE)
    log_file_name_1 = time.strftime("{}/%Y-%m-%d_%H:%M:%S_train-cfg.log".format(log_dir))
    # log_file_name_2 = time.strftime("./logs/%Y-%m-%d_%H:%M:%S_survival.log")
    main_log_file = setup_logger("main_log_file", log_file_name_1)
    main_log_file.info("Start")

    train_options = input("Insert options you want to train (eg: 1 or 1,2):")
    options_list = read_train_options(train_options)
    main_log_file.info("Options choosen in this run: " + ", ".join(options_list))

    unique_config_file = unique_config_sections(CONFIG_FILE)
    main_cfg_parser = configparser.ConfigParser()
    main_cfg_parser.read_file(unique_config_file)
    for option in options_list:
        running_text = "python "
        running_text += main_cfg_parser[option]["running_file"]
        unique_config_file = unique_config_sections(main_cfg_parser[option]["train_option"])
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read_file(unique_config_file)

        sub_log_file_name = time.strftime("{}/%Y-%m-%d_%H:%M:%S_{}.log".format(log_dir, option))
        sub_log_file = setup_logger("sub_log_file_{}".format(option), sub_log_file_name)
        sub_log_file.info("Start")
        for key in main_cfg_parser[option]:
            main_log_file.info("{}: {}".format(key, main_cfg_parser[option][key]))
        for sections in cfg_parser.sections():
            print(sections)
            for key in cfg_parser[sections]:
                sub_log_file.info("{}: {}".format(key, cfg_parser[sections][key]))
                if sections == "feed_args_0":
                    running_text += " --{} {}".format(key, cfg_parser[sections][key])
    print(running_text)
    os.system(running_text)


