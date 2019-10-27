from flask import Flask, jsonify, request
from flask_api import status
from gameService import GameService
from flask_cors import CORS, cross_origin
from playerService import PlayerService
from client import Client
from queue import Queue
import binascii
import os
import copy

class Server():
  def __init__(self):
    self._gameService = GameService()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
    self._app = Flask(__name__)
    CORS(self._app, resources={r"/api/*": {"origins": "*"}})
    self.initApp()
    self._clients = {}

  def initApp(self):
    @self._app.route('/api/games')
    def sendGames():
      return jsonify(self._gameService.getGamesInfo())

    @self._app.route('/api/game/<name>')
    def sendGame(name):
      game = self._gameService.getGame(name)
      return jsonify(self._gameService.getGameInfo(game))

    @self._app.route('/api/player', methods = ['POST'])
    def receivePlayers():
      data = request.get_json()
      key = self.uniqueKey()
      game = copy.deepcopy(self._gameService.getGame(data['game']))
      self._clients[key] = Client(game, data['names'])
      return jsonify(key)

    @self._app.route('/api/player/validate/<name>')
    def validatePlayerName(name):
      return jsonify(PlayerService().validatePlayerName(name))
    
    @self._app.route('/api/params/', methods = ['POST'])
    def receiveParams():
      data = request.get_json()
      if data['key'] not in self._clients:
        return jsonify('Unknown key')
      return jsonify(
        self._clients[data['key']].validateParameters(
          data['numberOfChoices'],
          data['numberOfBlocks'],
        )
      )

    @self._app.route('/api/pick', methods = ['POST'])
    @cross_origin()
    def pickChoice():
      data = request.get_json()
      if data['key'] not in self._clients:
        return jsonify('Unknown key')
      self._clients[data['key']].pickChoice(data['playerName'], data['choiceName'])
      return ''
    
    @self._app.route('/api/block', methods = ['POST'])
    @cross_origin()
    def blockChoices():
      data = request.get_json()
      if data['key'] not in self._clients:
        return jsonify('Unknown key')
      self._clients[data['key']].blockChoices(data['choiceNames'])
      return ''

    @self._app.route('/api/player/choices/<key>/<player>')
    def getPlayerChoices(key, player):
      if key not in self._clients:
        return jsonify(None)
      return jsonify(self._clients[key].getChoicesForPlayer(player))

    @self._app.route('/api/results/<key>')
    def getResults(key):
      if key not in self._clients:
        return jsonify(None)
      return jsonify(self._clients[key].getResults())

    @self._app.route('/api/random/player/<key>')
    def getNextTurn(key):
      if key not in self._clients:
        return jsonify(None)  
      return jsonify(self._clients[key].getNextTurn())

  def run(self, port=5000):
    self._app.run(port=port, threaded=True)

  def uniqueKey(self):
    SIZE = 12
    key = binascii.hexlify(os.urandom(SIZE)).decode('utf-8')
    while key in self._clients:
      key = binascii.hexlify(os.urandom(SIZE)).decode('utf-8')
    return key


def createApp():
  server = Server()
  try:
    server.run(os.environ['PORT'])
  except KeyError:
    server.run()
