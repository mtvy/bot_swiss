# Main libraries
import schedule, datetime, psycopg2, telebot, time, json, io, os
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Process
from telebot import types

# Project files
import config, path
from variables import *