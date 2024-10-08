import shutil
import os
import markdown_parser

def main(source, destination, logging=False):
	if os.path.exists(destination):
		for item in os.listdir(destination):
			item_path = os.path.join(destination, item)
			if os.path.isdir(item_path):
				if logging:
					print(item_path)

				shutil.rmtree(item_path)
			else:
				if logging:
					print(item_path)

				os.remove(item_path)
	else:
		os.mkdir(destination)
	
	def recursive_copy(source, destination):
		if os.path.exists(source) and os.path.exists(destination):
			for item in os.listdir(source):
				source_path = os.path.join(source, item)
				destination_path = os.path.join(destination, item)
				if os.path.isdir(source_path):
					if logging:
						print(destination_path)

					os.mkdir(destination_path)
					recursive_copy(source_path, destination_path)
				else:
					if logging:
						print(destination_path)

					shutil.copy(source_path, destination_path)

	recursive_copy(source, destination)

def read_file(current_dir, path):
    file_path = os.path.join(current_dir, path)

    with open(file_path, 'r') as file:
        contents = file.read()
    return contents

def generate_html(template_path, markdown_path, current_dir, target_path):
	template_content = read_file(current_dir, template_path)
	markdown_content = read_file(current_dir, markdown_path)

	markdown_html = markdown_parser.markdown_to_html(markdown_content)
	markdown_title = markdown_parser.extract_title(markdown_content)

	template_content = template_content.replace("{{ Title }}", markdown_title).replace("{{ Content }}", markdown_html)

	with open(target_path, 'w') as file:
		file.write(template_content)

current_dir = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(current_dir, "..", "static")
public_dir = os.path.join(current_dir, "..", "public")

template_file_path = os.path.join(current_dir, "../template.html")
markdown_file_path = os.path.join(current_dir, "../content/index.md")

target_path = os.path.join(current_dir, "../public/index.html")


main(static_dir, public_dir, logging=False)
generate_html(template_file_path,markdown_file_path,current_dir,target_path)
