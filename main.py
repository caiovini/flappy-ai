#!/usr/bin/env python3

from game import Game
import time
import os
import neat

HOST = '127.0.0.1'  # The server's hostname or IP address where game is running
PORT = 9021         # The port used by the server

def eval_genomes(genomes, config):

    game = Game(HOST , PORT)

    while(game.get_game_info()['state'] == 0): #State not initiated
          game.press_key_down('enter')

    for genome_id, genome in genomes:

        genome.fitness = 0
        info = game.get_game_info()

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        output = net.activate((info['birdHeight'] , info['pipes']['bottomPipeX'] , info['pipes']['bottomPipeY'], 
                                                    info['pipes']['topPipeX'] , info['pipes']['topPipeY']))
    
        if(output[0] > 0.5):
            print(info)
            game.press_key('up')
        else:
            time.sleep(0.1)  

        info = game.get_game_info()    

        if(info['state'] == 2): #State game over
            genome.fitness = -1
            game.press_key_down('home') 
            game.press_key_down('enter')    
        if(info['state'] == 1): #State initialized
            genome.fitness += info['timer'] + info['score'] * 3
            
        

def run(config_file):
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(eval_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':

    os.popen("java -jar desktop-1.0.jar")
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    