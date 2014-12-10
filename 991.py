#-*-coding:utf-8-*-

import time
import click
from datetime import datetime
from beijing_bus import BeijingBus


@click.group()
def cli():
    pass


@click.command(help='build or re-build the cache')
def build_cache():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    BeijingBus.build_cache()
    click.secho('Done!', fg='green')


def echo_realtime_data(line, station_num):
    station = line.stations[station_num-1]
    realtime_data = line.get_realtime_data(station_num)
    click.clear()
    now = datetime.now().strftime('%H:%M:%S')
    title = '实时数据 [%s]  线路：%s  (每5秒自动刷新，更新于%s)' % (station.name, line.name, now)
    click.secho(title, fg='green', bold=True)
    click.echo()
    realtime_data = filter(lambda d: d['station_arriving_time'], realtime_data)
    realtime_data.sort(key=lambda d: d['station_arriving_time'])
    for i, data in enumerate(realtime_data):
        click.secho('公交%s：' % (i+1), bold=True, underline=True)
        click.echo('距离 %s 还有%s米' % (station.name, data['station_distance']))
        click.echo('预计 %s 到达' % data['station_arriving_time'].strftime('%H:%M'))
        click.echo('预计 %d 分钟后到达' % ((int(str((datetime.strptime(datetime.now().strftime('%H:%M'),'%H:%M')-datetime.strptime(data['station_arriving_time'].strftime('%H:%M'),'%H:%M')).seconds))-86400)*-1/60))
        click.echo()


@click.command()
def query():
    lines = BeijingBus.search_lines('991')
    line = lines[3]
    while True:
        echo_realtime_data(line, 16)
        time.sleep(5)
    

cli.add_command(build_cache)
cli.add_command(query)


if __name__ == '__main__':
    cli()
