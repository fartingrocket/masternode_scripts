import bcolors
import requests
import sys
from datetime import datetime, timedelta, timezone
from lib.configurator import configurator


class updates:
    def __init__(self, ticker):
        self.config = configurator()
        self.config.load(ticker=ticker)
        self.avg_block_time = None
        self.last_block_height = None
        self.next_update_block_height = None
        self.remaining_blocks_to_update = None
        self.next_update_date_time = None

        if self.config.block_average in ({}, [], "", None) \
                or self.config.last_block in ({}, [], "", None)\
                or self.config.update_interval in ({}, [], "", None, 0) \
                or self.config.max_collateral_at_block in ({}, [], "", None, 0):
            print(f"{bcolors.FAIL}Some params needed to check for coin updates are not set correctly\n"
                  f"Cannot math. Abotring.{bcolors.END}\n")
            sys.exit(1)

    def start(self):
        date_time = datetime.now(timezone.utc)

        print("#"*(len(self.config.name)+8))
        print("### {} ###".format(self.config.name))
        print("#" * (len(self.config.name) + 8))

        print("\nDate : {}\tTime : {} UTC\n".format(date_time.date(),
                                                    date_time.time().isoformat(timespec='minutes')))

        self.get_avg_time_block()
        self.get_last_block()
        self.get_next_update_block_height()
        self.get_remaining_blocks_to_next_update()
        self.get_next_update_date_time()

    def get_avg_time_block(self):
        resp = requests.get(self.config.block_average)
        self.avg_block_time = timedelta(seconds=float(resp.json()))

    def get_last_block(self):
        resp = requests.get(self.config.last_block)
        self.last_block_height = resp.json()[0]["blocks"]

    def get_next_update_block_height(self):
        next_update = (1 + (self.last_block_height // self.config.update_interval)) * self.config.update_interval
        self.next_update_block_height = next_update

    def get_remaining_blocks_to_next_update(self):
        remaining = self.next_update_block_height - self.last_block_height
        self.remaining_blocks_to_update = remaining

    def get_next_update_event(self):
        if self.last_block_height > self.config.max_collateral_at_block:
            return "reward decrease"
        else:
            return "collateral update"

    def get_next_update_date_time(self):
        print("Avg block time = {} seconds".format(self.avg_block_time.seconds))
        print("Current block height = {}".format(self.last_block_height))
        print("Next update on block height = {}".format(self.next_update_block_height+1))
        print("Blocks remaining = {}".format(self.remaining_blocks_to_update))
        collateral_update_date_time = datetime.now(timezone.utc) + self.avg_block_time * self.remaining_blocks_to_update
        # We apply a delta of 1 second on the average block time
        time_delta = 2 * self.remaining_blocks_to_update * timedelta(seconds=1)
        # Then we calculate the upper and lower time limits
        upper_time = collateral_update_date_time + 0.5 * time_delta
        lower_time = collateral_update_date_time - 0.5 * time_delta
        # if the difference is too big we display a warning
        if upper_time.date().day != lower_time.date().day and time_delta.days >= 1:
            print(f"\n{bcolors.WARN}Note : Event is too far ahead or average block time is too big !{bcolors.END}")
            print("\nAssuming +/- 1 second on average block time")
            print("Next {} will occur :\n"
                  "\tBetween {} and {}\n".format(self.get_next_update_event(),
                                                 lower_time.date(),
                                                 upper_time.date()))

        elif upper_time.date().day != lower_time.date().day and time_delta.days < 1:
            print("\nAssuming +/- 1 second on average block time")
            print("Next {} will occur :\n"
                  "\tBetween {} at {} and {} at {} UTC\n".format(self.get_next_update_event(),
                                                                 lower_time.date(),
                                                                 lower_time.time().isoformat(timespec='minutes'),
                                                                 upper_time.date(),
                                                                 upper_time.time().isoformat(timespec='minutes')))

        else:
            print("\nAssuming +/- 1 second on average block time")
            print("Next {} will occur :\n"
                  "\tOn {} between {} and {} UTC\n".format(self.get_next_update_event(),
                                                           collateral_update_date_time.date(),
                                                           lower_time.time().isoformat(timespec='minutes'),
                                                           upper_time.time().isoformat(timespec='minutes')))
