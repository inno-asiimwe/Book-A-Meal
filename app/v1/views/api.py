# -*- coding: utf-8 -*-
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

import os
import binascii

from instance.config import app_config


