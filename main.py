import asyncio
import getpass
import yaml
from collector import Collector
from recorder import Recorder, Listener
from capturer import Capturer, Sleeper


def wait_username_and_password():
    username = input('username: ')
    password = getpass.getpass('password: ')
    return (username, password)

def construct_collector(config):
    collector = Collector(config['COLLECTOR'])
    return collector

def construct_listener(config, collector):
    record_config = config['RECORD']
    recorder = Recorder(record_config['RECORD_DIR'])
    listener = Listener(recorder, collector)
    return listener

def construct_sleeper(config, collector):
    status_config = config['STATUS']
    capturer = Capturer(status_config['PHOTO_DIR'], status_config['SCREEN_SHOT_DIR'])
    sleeper = Sleeper(status_config['SLEEP_TIME'], capturer, collector)
    return sleeper

def main():

    username, password = wait_username_and_password()
    
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    collector = construct_collector(config)
    collector.login(username, password)

    print(f'Welcome {username}')

    listener = construct_listener(config, collector)

    sleeper = construct_sleeper(config, collector)
    
    listener.start()
    
    sleeper.start()
    sleeper.join()
    
    listener.join()
    return

if __name__ == '__main__':
    main()
