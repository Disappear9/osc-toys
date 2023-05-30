import asyncio
import logging
from typing import List
import settings
import time
from toys.estim.coyote.dg_interface import CoyoteInterface
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


ci = CoyoteInterface(
    device_uid=settings.COYOTE_UID, power_multiplier=1.28, safe_mode=True
)


async def start_channel_a():
    print(ci.patterns[settings.COYOTE_PATTERN])
    await ci.signal(
        power=int(settings.COYOTE_MAX_POWER_A * settings.MIN_POWER),
        pattern=ci.patterns[settings.COYOTE_PATTERN],
        duration=100000000,
        channel="a",
    )


async def start_channel_b():
    print(ci.patterns[settings.COYOTE_PATTERN])
    await ci.signal(
        power=int(settings.COYOTE_MAX_POWER_B * settings.MIN_POWER),
        pattern=ci.patterns[settings.COYOTE_PATTERN],
        duration=100000000,
        channel="b",
    )


async def serve_osc():
    dispatcher = Dispatcher()
    dispatcher.map(settings.COYOTE_ADDR_A, coyote_handler_a, "A")
    dispatcher.map(settings.COYOTE_ADDR_B, coyote_handler_b, "B")
    server = osc_server.AsyncIOOSCUDPServer(
        (settings.VRC_HOST, settings.VRC_OSC_PORT), dispatcher, asyncio.get_event_loop()
    )
    await server.create_serve_endpoint()


param_queue_a = []
param_queue_b = []
last_time_a = time.time()
cur_time_a = time.time()
last_time_b = time.time()
cur_time_b = time.time()


def get_avg(queue: List[float]) -> float:
    """
              ▲
              │
              │
              │                max_limit
          1.0 │               xx───────
              │              xx
              │             xx
              │            xx
              │           xx
              │          xx
    min_power │   ┌─────xx
              │   │       min_limit
              └───┴──────────────────────────►
              start_limit
    """
    s = 0.0
    for x in queue:
        s += x
    s /= len(queue)
    if s <= settings.MIN_LIMIT:
        # map [START_LIMIT, MIN_LIMIT] to MIN_OOWER
        s = settings.MIN_POWER
    elif s >= settings.MAX_LIMIT:
        # map [MAX_LIMIT, 1] to 1
        s = 1
    else:
        # map [MIN_LIMIT, MAX_LIMIT] to [MIN_POWER, 1]
        s = (s - settings.MIN_LIMIT) / (settings.MAX_LIMIT - settings.MIN_LIMIT) * (
            1 - settings.MIN_POWER
        ) + settings.MIN_POWER
    return s


def coyote_handler_a(addr, args, dis):
    """
    This function will calculate the avarage value of values from OSC
    within 1 second, and then set the power of the channel A by the result.
    """
    global param_queue_a, last_time_a, cur_time_a
    cur_time_a = time.time()
    # print("A: [{0}] ~ {1}".format(addr, dis))

    if dis < 0.1:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(ci.set_pwm(1, -1), loop=loop)
        return
    if cur_time_a - last_time_a > settings.WINDOW_SIZE:
        last_time_a = time.time()
        if len(param_queue_a) == 0 or not settings.CAN_UPDATE_POWER:
            param_queue_a.append(dis)
            return
        s = get_avg(param_queue_a)
        loop = asyncio.get_event_loop()
        if s < 0.1:
            asyncio.ensure_future(ci.set_pwm(1, -1), loop=loop)
        else:
            asyncio.ensure_future(
                ci.set_pwm(int(settings.COYOTE_MAX_POWER_A * s), -1), loop=loop
            )
        param_queue_a = []
    else:
        param_queue_a.append(dis)


def coyote_handler_b(addr, args, dis):
    """
    This function will calculate the avarage value of values from OSC
    within 1 second, and then set the power of the channel B by the result.
    """
    global param_queue_b, last_time_b, cur_time_b
    cur_time_b = time.time()
    # print("B: [{0}] ~ {1}".format(addr, dis))

    if dis < 0.1:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(ci.set_pwm(-1, 1), loop=loop)
        return
    if cur_time_b - last_time_b > settings.WINDOW_SIZE:
        last_time_b = time.time()
        if len(param_queue_b) == 0 or not settings.CAN_UPDATE_POWER:
            param_queue_b.append(dis)
            return
        s = get_avg(param_queue_b)
        loop = asyncio.get_event_loop()
        if s < 0.1:
            asyncio.ensure_future(ci.set_pwm(-1, 1), loop=loop)
        else:
            asyncio.ensure_future(
                ci.set_pwm(-1, int(settings.COYOTE_MAX_POWER_B * s)), loop=loop
            )
        param_queue_b = []
    else:
        param_queue_b.append(dis)


async def main():
    await ci.connect(retries=10)
    await asyncio.gather(start_channel_a(), start_channel_b(), serve_osc())
    await ci.stop()
    await ci.disconnect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
