# Main libraries
import schedule, datetime, psycopg2, telebot, time, json, io, os, traceback
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Process
from telebot import types

# Project files
import config
import database
import classes
from path import *
from variables import *
#from bot import *