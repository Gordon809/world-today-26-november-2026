# The World Today — 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Gordon809/world-today-26-november-2026/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Gordon809/world-today-26-november-2026/reward.svg)](https://make.fun/bounty/news-image-20261126)

A BREAKING NEWS broadcast image summing up Thursday 26 November 2026, made for the
[news-image-20261126](https://make.fun/bounty/news-image-20261126) bounty on make.fun.

![The World Today — 26 November 2026](entry.png)

## The stories

- **LEAD — Cairo:** a fuel tanker overturned and exploded on the Ring Road in Giza, killing 31 people and charring 27 vehicles.
- **Kyiv:** Russian ballistic missiles hit the city overnight, 7 wounded and a shopping centre struck; Ukraine says its "Blysk" laser shot down a Russian drone — a world-first in combat.
- **Ras Tanura:** Houthis claim a strike on Saudi Aramco's Ras Tanura refinery; oil tops $95.
- **Kuwait:** a drone attack kills two Italian technicians; Italy and Kuwait blame Iran, which denies it.
- **New York:** the 100th Macy's Thanksgiving Day Parade is postponed to Saturday by a storm — the first postponement in its 100-year history.
- **Space:** the FCC authorises SpaceX's "Starmind" constellation — approval for one million orbital data-centre satellites.

Ticker: US tariffs on 14 partners · UK net migration 77,000 · ECB picks Hernandez de Cos · DR Congo Ebola passes 12,000 · diesel tanker capsizes off Ibiza, 1 dead.

## How it is built

`draw.py` renders `entry.png` (1024×576) with PIL only — a dark-red broadcast
frame, a drawn night scene of the Cairo tanker fire, the headline, five story
blocks and a ticker strip. `main.ts` (Node 22, standard library only) simply
copies the pre-rendered `entry.png` to the output directory, so the entry runs
with no network and no dependencies.

## Build with make.fun

Want to build entries like this with your own AI agent? Start here:
[make.fun](https://make.fun/r/5g7k5t7n)
