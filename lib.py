# Main libraries
import schedule, datetime, psycopg2, telebot, time, json, io, os, traceback
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Process
from telebot import types

# Project files
import config
from path import *
from variables import *
import database
#from bot import *