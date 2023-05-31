import click
import requests
import matplotlib.pyplot as plt
import datetime

API_KEY = 'f2ad09d76813a13c98e255db540b6dcf'


@click.command()
@click.option('--query', prompt='Enter the city name:', help='Enter the name of the city for weather information')
def process_query(query):
    city = query

    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast = data['list']

        dates = []
        temps = []
        humidities = []

        for day in forecast:
            date = datetime.datetime.strptime(day['dt_txt'], '%Y-%m-%d %H:%M:%S').date()
            if date not in dates:
                dates.append(date)
                temp = day['main']['temp']
                temps.append(temp)
                humidity = day['main']['humidity']
                humidities.append(humidity)

        # Set dark theme with darkest blue background
        plt.style.use('dark_background')
        plt.rcParams['axes.facecolor'] = '#000033'

        # Plot the graph with glowing lines
        plt.figure(figsize=(10, 6))
        plt.plot(dates, temps, color='orange', label='Temperature (°C)', linewidth=2, linestyle='-', marker='o', markersize=8, markerfacecolor='orange', markeredgecolor='orange', markeredgewidth=1, alpha=0.8)
        plt.plot(dates, humidities, color='white', label='Humidity (%)', linewidth=2, linestyle='-', marker='o', markersize=8, markerfacecolor='white', markeredgecolor='white', markeredgewidth=1, alpha=0.8)
        plt.xlabel('Date --------------->',color='#89CFF0',fontweight='bold')
        plt.ylabel('Value --------------->',color='#89CFF0',fontweight='bold')
        plt.title(f'Weather Forecast for {city}', fontweight='bold')
        plt.legend()
        plt.grid(False)

        # Rotate x-axis labels to be straight
        plt.xticks(rotation=0)

        # Add temperature values to the graph with arrows
        for i in range(len(dates)):
            plt.annotate(f'{temps[i]}', (dates[i], temps[i]), textcoords="offset points", xytext=(0,10), ha='center', va='bottom', color='orange', fontweight='bold', arrowprops=dict(arrowstyle='->', color='orange'))

        # Add humidity values to the graph with arrows
        for i in range(len(dates)):
            plt.annotate(f'{humidities[i]}', (dates[i], humidities[i]), textcoords="offset points", xytext=(0,10), ha='center', va='bottom', color='white', fontweight='bold', arrowprops=dict(arrowstyle='->', color='white'))

        plt.tight_layout()

        # Display the graph
        plt.show()

        click.echo()
        click.secho(f'Weather Forecast for {city}', bold=True)
        click.echo(f'-' * 45)
        click.echo('{:<10} {:<10} {:<2} {:<15}'.format('Date', 'Weather', 'Temp (°C)', 'Humidity (%)'))
        click.echo('-' * 45)

        for i in range(len(dates)):
            date = dates[i]
            weather = forecast[i]['weather'][0]['description']
            temp = temps[i]
            humidity = humidities[i]
            click.echo('{:<12} {:<18} {:<10} {:<15}'.format(date, weather, temp, humidity))

        click.echo()
        click.secho('Enjoy your week!', fg='green', bold=True)
        click.echo('🌍  Stay connected with the world through the weather!')

    else:
        click.echo('Error retrieving weather information. Please check the city name provided.')


if __name__ == '__main__':
    click.clear()
    click.secho('===================================================', fg='blue')
    click.secho('             Welcome to Weather Report             ', fg='blue', bold=True)
    click.secho('===================================================', fg='blue')
    click.echo()
    process_query()
