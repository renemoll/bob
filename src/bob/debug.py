
def bob_debug(options, cwd):
	"""
	Todo:
	- actually enter gdb
	- lldb?
	- make container optional
	"""
	def build_gdb():
		return [
			"docker",
			"run",
			"--rm",
			"-it",
			"-v", "{}:/work/".format(cwd),
			"renemoll/builder_arm_gcc",
			"/bin/bash"
		]

	return [build_gdb()]
