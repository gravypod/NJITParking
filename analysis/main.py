import matplotlib as mpl

mpl.use("Agg")

import seaborn as sns; sns.set_context('talk'); sns.set_palette('muted', color_codes=True); sns.set(font_scale=4)

from pandas import read_csv, TimeGrouper, DataFrame, Timestamp
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MaxNLocator

import pytz

ZUR = pytz.timezone("Europe/Zurich")
EST = pytz.timezone("America/New_York")


def find_hourly_deck_usage(parking_data):
	# List of lots you want to look at
	parking_deck_names = ["Lot 10", "PARK", "Science & Tech Garage"]

	# A list of the average # of available spots, in each parking deck, in our dataset.
	hourly_averages = []

	for time, hourly_parking_data in parking_data.groupby(TimeGrouper("5min")):
		df = hourly_parking_data.groupby('deck').mean()

		# Metadata about this hour
		hour_average = {
			'hour': time.hour + (time.minute/60),
			'weekday': time.weekday(),
			'weekday_name': time.weekday_name,
			'entered': time
		}
		# Add in all of the decks
		hour_average.update({name: df[df.index == name].available.mean() for name in parking_deck_names})

		hourly_averages.append(hour_average)

	return DataFrame(hourly_averages)

def plot_hourly_capacity(parking_data):
	hourly_parking_deck_usage = find_hourly_deck_usage(parking_data)

	decks = ['PARK', 'Science & Tech Garage']

	fig, axs = plt.subplots(len(decks), sharex=True, figsize=(60, 42))

	weekday = Timestamp.now().weekday()
	for ax in axs:
		ax.axvline(weekday - (.5), linewidth=4, color='black')
		ax.axvline(weekday + (.5), linewidth=4, color='black')

	hlabels = [
		'12PM', '', '10PM', '', '8PM', '', '6PM', '', '4PM', '', '2PM', '', '12PM', '', '10AM', '', '8AM', '', '6AM', '', '4AM', '', '2AM', '', '12AM'
	]

	for deck, ax in zip(decks, axs):

		cm = plt.get_cmap('viridis')
		cNorm  = colors.Normalize(vmin=hourly_parking_deck_usage[deck].min() * 1.1, vmax=hourly_parking_deck_usage[deck].max() * 0.9)
		scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

		for (weekday, hour), block in hourly_parking_deck_usage.groupby(['weekday', 'hour']):
			h = (23 - hour)
			#print(hour, h) #, hlabels[h])
			block_patch = ax.add_patch(patches.Rectangle(
					(weekday - .5,  h),
					1, -5/60,
					color=scalarMap.to_rgba(block[deck].sum())
				)
			)



		ax.yaxis.set_major_locator(MaxNLocator(integer=True))


		ax.set_ylim(-1, 23)
		ax.set_yticks(list(range(-1, 24)))
		ax.set_yticklabels(hlabels)

		#ax.set_ylabel("Hour of Date")

		#ax.set_title(deck)

		div = make_axes_locatable(ax)
		cax = div.append_axes("right", size="5%", pad=0.05)
		color_bar = mpl.colorbar.ColorbarBase(cax, cmap=cm, norm=cNorm, orientation='vertical')
		color_bar.set_label('Spots in "{}"'.format(deck))


	ax = axs[-1]

	#ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
	ax.set_xlim(-0.4, 6.6)
	#ax.set_xlabel("Day of Week")
	ax.set_xticklabels(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"])

	#fig.suptitle("Parking Availability")
	plt.subplots_adjust(bottom=.03, left=0.08, hspace=0.07)
	fig.tight_layout()
	fig.savefig("hourly-deck-capacity.png", figsize=(32,40))

def main():
	parking_data = read_csv("parking.csv", parse_dates=['entered'], index_col=["entered"])
	parking_data.index = parking_data.index.tz_localize(ZUR).tz_convert(EST)
	plot_hourly_capacity(parking_data)

if __name__ == "__main__":
	main()
