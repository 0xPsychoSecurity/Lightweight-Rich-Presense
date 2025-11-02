import os
import sys
import time
import logging
import argparse
from pypresence import Presence

def parse_args():
    parser = argparse.ArgumentParser(description="Touge Rich Presence")
    parser.add_argument("--client-id", dest="client_id", help="Discord Application Client ID")
    parser.add_argument("--log-level", dest="log_level", default=os.getenv("LOG_LEVEL", "INFO"), help="Logging level (INFO, DEBUG, WARNING)")
    parser.add_argument("--large-image", dest="large_image", default=os.getenv("DISCORD_LARGE_IMAGE"), help="Discord Rich Presence large image asset key")
    parser.add_argument("--large-text", dest="large_text", default=os.getenv("DISCORD_LARGE_TEXT"), help="Hover text for the large image")
    parser.add_argument("--title", dest="title", default=os.getenv("DISCORD_TITLE"), help="Title text (maps to Rich Presence state)")
    return parser.parse_args()

args = parse_args()
LOG_LEVEL = str(args.log_level).upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format='%(asctime)s - %(levelname)s - %(message)s')

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID") or args.client_id
if not CLIENT_ID:
    try:
        CLIENT_ID = 1434347231808589897
    except EOFError:
        CLIENT_ID = None
if not CLIENT_ID:
    print("A Discord Application Client ID is required. Exiting.")
    sys.exit(1)

TEXT_STATE = args.title or "Aint Got No Gas Innit"
TEXT_DETAILS = "I Know Whats Wrong Widdit It"
BUTTONS = [{"label": "Enter the Touge", "url": "https://sllothtl.github.io/"}]

rpc = Presence(CLIENT_ID)

def connect_rpc():
    while True:
        try:
            rpc.connect()
            logging.info("Connected to Discord RPC")
            return
        except Exception as e:
            logging.error("RPC connect failed: %s", e)
            time.sleep(5)


def run():
    connect_rpc()
    start_time = int(time.time())
    while True:
        try:
            update_kwargs = {
                "state": TEXT_STATE,
                "details": TEXT_DETAILS,
                "start": start_time,
                "buttons": BUTTONS,
            }
            if args.large_image:
                update_kwargs["large_image"] = args.large_image
            if args.large_text:
                update_kwargs["large_text"] = args.large_text

            rpc.update(**update_kwargs)
            time.sleep(15)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error("Update failed: %s", e)
            try:
                rpc.connect()
                logging.info("Reconnected to Discord RPC")
            except Exception as re:
                logging.error("Reconnect failed: %s", re)
                time.sleep(30)

if __name__ == "__main__":
    print("Starting Touge Rich Presence... Press Ctrl+C to stop.")
    run()
