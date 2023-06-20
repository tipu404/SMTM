# Imports
import os
import tarfile
import pandas as pd
import json
from multiprocessing import Process, Manager
from ..metric_functions import timer


@timer
def open_tar_file(input_path, max_files, chunk_size):
    count = 0
    chunk = []
    with tarfile.open(input_path, mode="r|xz") as tar:
        for member in tar:
            if count >= max_files:
                if chunk:  # yield remaining chunk if any left
                    yield pd.read_json('\n'.join(chunk), lines=True)
                break
            if member.isfile() and member.name.endswith(".jsonl"):
                file_obj = tar.extractfile(member)
                if file_obj is not None:
                    for line in file_obj:
                        chunk.append(line.decode('utf-8'))  # Add line to chunk
                        count += 1
                        if len(chunk) % chunk_size == 0:  # if chunk is full
                            yield pd.read_json('\n'.join(chunk), lines=True)  # yield chunk as dataframe
                            chunk = []  # reset chunk
        if chunk:  # yield the last chunk if any left
            yield pd.read_json('\n'.join(chunk), lines=True)



## Concurrent Multithreaded Queue Version


#@timer
#def open_tar_file(input_path, max_files, chunk_size, queue_dict, data_ready):
#    count = 0
#    key = 0
#    chunk = []
#    with tarfile.open(input_path, mode="r|xz") as tar:
#        for member in tar:
#            if count >= max_files:
#                break
#            if member.isfile() and member.name.endswith(".jsonl"):
#                file_obj = tar.extractfile(member)
#                if file_obj is not None:
#                    for line in file_obj:
#                        chunk.append(line.decode('utf-8'))
#                        count += 1
#                        if len(chunk) % chunk_size == 0:
#                            # Transform data first, then quickly update the shared dictionary
#                            df_chunk = pd.read_json('\n'.join(chunk), lines=True)
#                            counters = {"eda_counter": 1, "token_selector_counter": 1}
#                            with queue_dict.lock:  # Synchronize access to shared dictionary
#                                key += 1
#                                queue_dict[key] = [df_chunk, counters]
#                            data_ready.set()  # Signal that data is ready to be processed
#                            print(f"Added {len(chunk)} documents to queue. Total documents: {count}")
#                            chunk = []
#        if chunk:
#            # Transform data first, then quickly update the shared dictionary
#            df_chunk = pd.read_json('\n'.join(chunk), lines=True)
#            counters = {"eda_counter": 1, "token_selector_counter": 1}
#            with queue_dict.lock:
#                key += 1
#                queue_dict[key] = [df_chunk, counters]
#                print(f"Added {len(chunk)} documents to queue. Total documents: {count}")
#                chunk = []
