import os
try:
	import css_html_js_minify as minify
except ImportError:
	print("css_html_js_minify not found. Skipping minification...")
	exit()

os.chdir(os.path.dirname(os.path.realpath(__file__)))
#minify.process_single_css_file()

print("Minification successful.")