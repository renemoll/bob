import logging


def bob_build(options, cwd):
	output_folder = determine_output_folder(options['build'])
	logging.debug("Determined output folder: %s", output_folder)

	def generate_build_env():
		steps = []
		if options['use-container']:
			steps += container_command(options['build']['target'], cwd)

		steps += build_system_command(options, output_folder)

		if options['build']['target'] == BuildTarget.Stm32:
			steps += build_stm32()

		return steps

	def build_project():
		steps = []

		if options['use-container']:
			steps += container_command(options['build']['target'], cwd)

		steps += build_project_command(output_folder)

		return steps

	return [
		generate_build_env(),
		build_project()
	]


def determine_output_folder(options):
	lookup = {
		BuildTarget.Stm32: 'stm32-',
		BuildTarget.Linux: 'linux64-',
		BuildTarget.Native: 'native-',
	}
	return lookup[options['target']] + str(options['config']).lower()


def container_command(target, cwd):
	if target == BuildTarget.Native:
		return []
	elif target == BuildTarget.Stm32:
		return ["docker",
			"run",
			"--rm",
			"-v", "{}:/work/".format(cwd),
			"renemoll/builder_arm_gcc"]
	elif target == BuildTarget.Linux:
		return ["docker",
			"run",
			"--rm",
			"-v", "{}:/work/".format(cwd),
			"renemoll/builder_clang"]

	raise ValueError("Unsupported container requested: '%s'", str(target))


def build_system_command(options, output_folder):
	cmd = ["cmake",
		"-B", "build/{}".format(output_folder),
		"-S", ".",
		"-DCMAKE_BUILD_TYPE={}".format(str(options['build']['config']))
		# "–warn-uninitialized"
	]

	if options['build']['target'] in (BuildTarget.Linux, BuildTarget.Stm32):
		cmd += [
			"-G", "Ninja",
		]

	return cmd


def build_stm32():
	return ["-DCMAKE_TOOLCHAIN_FILE=cmake/toolchain-stm32f767.cmake"]


def build_project_command(output_folder):
	return ["cmake", "--build", "build/{}".format(output_folder)]
