from api_scripts.vk_utils import loop_listen, catch_events
import argparse
import constants

parser = argparse.ArgumentParser()
parser.add_argument('--token', type=str, help='VK API Token')
parser.add_argument('--admin-id', type=int, help='Admin id')
parser.add_argument('--debug', type=bool, default=False, help='Debug mode')
args = parser.parse_args()

if __name__ == '__main__':
    if args.token:
        constants.vk_api_token = args.token
    if args.admin_id:
        constants.admin_id = args.admin_id
    if args.debug:
        catch_events()
    else:
        loop_listen()