
import os
import argparse


parser = argparse.ArgumentParser(description="Converts a boblight configuration file to hyperion configuration file.")
parser.add_argument('boblight', nargs='?', default='boblight.conf',      help="boblight input  configuration file", metavar='BOBLIGHT')
parser.add_argument('hyperion', nargs='?', default='hyperion.conf.json', help="hyperion output configuration file", metavar='HYPERION')


HYPERION_TEMPLATE_FILE = 'hyperion.conf.json.template'


def assert_file_exists(filename):
	if not os.path.isfile(filename):
		print("ERROR: %s no such file." % filename)
		exit(1)


def generate_var(boblight, var):
	start = boblight.find(var) + len(var)
	end   = boblight.find('\n', boblight.find(var))
	scan  = boblight[start:end].strip().split(' ')
	return '\t\t"%s": { "minimum": %.4f, "maximum": %.4f},\n' % (var, int(scan[0]) / 100.0, int(scan[1]) / 100.0)


def boblight_to_hyperion(boblight, hyperion):
	boblight_config   = open(boblight, 'r').read()
	hyperion_template = open(HYPERION_TEMPLATE_FILE, 'r').read()
	hyperion_config   = open(hyperion, 'w')

	# Converts LEDS section
	leds_bob_list = boblight_config.split('[light]')
	leds = '"leds":\n[\n\t\n'
	for i in range(1,len(leds_bob_list)):
		leds += '\t{\n\t\t"index":%d,\n' % (i-1)
		leds += generate_var(leds_bob_list[i], 'hscan')
		leds += generate_var(leds_bob_list[i], 'vscan')
		leds += '\t},\n'
	leds = leds[:-2] + '],\n'

	# Prepares output configuration file
	hyperion_config.write(hyperion_template.replace('<<LEDS>>', leds))
	hyperion_config.close()
	

if __name__ == '__main__':
	# Parse arguments
	args = parser.parse_args()

	# Check validity
	assert_file_exists(args.boblight)
	assert_file_exists(HYPERION_TEMPLATE_FILE)

	# Convert config file
	boblight_to_hyperion(args.boblight, args.hyperion)




