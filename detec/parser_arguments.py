#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 20:43:56 2022

@author: sajid
"""
import argparse

def get_args(argv=None):
    parser = argparse.ArgumentParser(description="",)

    parser.add_argument('--year', type=int, default=2002, help="Year as time span")
    parser.add_argument('--month', type=int, default=None, help="Month as time span")
    parser.add_argument('--day', type=int, default=None, help="Day as time span")
    parser.add_argument('--start-time', type=int, default=8, help="Starting hour of the day")
    parser.add_argument('--off-time', type=int, default=17, help="Off hour of the day")

   
    return parser.parse_args(argv)