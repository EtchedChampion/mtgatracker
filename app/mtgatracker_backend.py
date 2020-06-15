import argparse
import os
import threading

from app import tasks, queues
from app.mtga_app import mtga_watch_app
from app.queues import all_die_queue, general_output_queue
from util import KillableTailer

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-i', '--log_file', default=None)
arg_parser.add_argument('-nf', '--no_follow', action="store_true", default=False)
arg_parser.add_argument('-f', '--read_full_log', action="store_true", default=False)
arg_parser.add_argument('-m', '--mouse_events', action="store_true", default=False)
arg_parser.add_argument('-p', '--port', default=8089, type=int)
args = arg_parser.parse_args()

print("process started with args: {}".format(args))

if args.log_file is None:  # assume we're on windows for now # TODO
    appdata_roaming = os.getenv("APPDATA")
    wotc_locallow_path = os.path.join(appdata_roaming, "..", "LocalLow", "Wizards Of The Coast", "MTGA")
    output_log = os.path.join(wotc_locallow_path, "output_log.txt")
    if not os.path.exists(output_log):
        output_log = None
    args.log_file = output_log

if __name__ == "__main__":
    print("starting block watch task server")
    block_watch_process = threading.Thread(target=tasks.block_watch_task,
                                           args=(queues.block_read_queue, queues.json_blob_queue,))
    block_watch_process.start()

    print("starting json watch task server")
    json_watch_process = threading.Thread(target=tasks.json_blob_reader_task,
                                          args=(queues.json_blob_queue, queues.json_blob_queue,))
    json_watch_process.start()

    print("starting action task server")
    action_process = threading.Thread(target=tasks.action_task,
                                      args=(queues.action_queue, queues.action_queue,))
    action_process.start()

    current_block = ""

    count = 0
    if not args.no_follow and all_die_queue.empty():
        print("starting to tail file: {}".format(args.log_file))
        if args.log_file:
            with open(args.log_file) as log_file:
                kt = KillableTailer(log_file, queues.all_die_queue)
                kt.seek_end()
                for line in kt.follow(delay=0):  # we don't want any delay because we need to act upon the last message
                    if line and (line.startswith("[UnityCrossThreadLogger]") or line.startswith("[Client GRE]")):
                        # this is the start of a new block (with title), end the last one
                        if "{" in current_block:  # try to speed up debug runs by freeing up json watcher task
                            # which is likely the slowest
                            last_idx = current_block.rindex("}")
                            # ^ After gamestate logs, there is garbage (non-json) in the same block; strip it out
                            # TODO: this is hella hacky and should be fixed
                            current_block = current_block[:last_idx + 1]
                            queues.block_read_queue.put(current_block)
                        current_block = line.strip() + "\n"
                    elif line and line.startswith("]") or line.startswith("}"):
                        current_block += line.strip() + "\n"
                        # this is the END of a block, end it and start a new one
                        if "{" in current_block:  # try to speed up debug runs by freeing up json watcher task
                            # which is likely the slowest
                            queues.block_read_queue.put(current_block)
                        current_block = ""
                    else:
                        # we're in the middle of a block somewhere
                        stripped = line.strip()
                        if stripped:
                            current_block += stripped + "\n"
                    if not all_die_queue.empty():
                        break
        else:
            general_output_queue.put({"error": "NoLogException",
                                      "msg": "No log file present. Please run MTGA at least once before launching MTGA Tracker.",
                                      "count": 1})

    queues.block_read_queue.put(None)

    block_watch_process.join()
    json_watch_process.join()
    while queues.json_blob_queue.qsize():
        queues.json_blob_queue.get()
