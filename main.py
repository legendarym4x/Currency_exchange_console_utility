import json
import aiohttp
import asyncio
import platform
import sys
from datetime import datetime, timedelta
from time import time


class HttpError(Exception):
    pass


async def request(url: str):
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f'Connection error: {url}', str(err))


def formate_output(data: list):
    formatted_data = []
    for item in data:
        date_str = item['date']
        rates = item['exchangeRate']

        formatted_rates = {}
        for rate in rates:
            currency = rate['currency']
            if currency in ['EUR', 'USD']:
                sale_rate = rate.get('saleRate', rate['saleRateNB'])
                purchase_rate = rate.get('purchaseRate', rate['purchaseRateNB'])

                formatted_rates[currency] = {
                    'sale': sale_rate,
                    'purchase': purchase_rate
                }

        if formatted_rates:
            formatted_data.append({date_str: formatted_rates})
    return formatted_data


async def main(index_days):
    if 1 <= int(index_days) <= 10:
        today = datetime.now().date()
        dates = []
        for i in range(int(index_days)):
            d = (today - timedelta(days=i)).strftime("%d.%m.%Y")
            dates.append(d)
        print('Here is the course for the specified dates: ', dates)
        try:
            responses = await asyncio.gather(
                *[request(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}') for date in dates])
            formatted_responses = formate_output(responses)

            with open('rates.json', 'w') as file:
                json.dump(formatted_responses, file, indent=2)

            return formatted_responses
        except HttpError as err:
            print(err)
    else:
        print("The day index must be in the range 1 - 10")


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    start = time()
    res = asyncio.run(main(sys.argv[1]))
    print(res)
    print(time() - start)
