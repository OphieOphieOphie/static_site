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

def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def generate_html_recursive(template_path, content_dir, public_dir, logging=False):
	template_content = read_file(template_path)

	for root, dirs, files in os.walk(content_dir):

		for file in files:
			if file.endswith('.md'):
				markdown_path = os.path.join(root, file)
				relative_path = os.path.relpath(markdown_path, content_dir)
				html_path = os.path.join(public_dir, os.path.splitext(relative_path)[0] + '.html')

				os.makedirs(os.path.dirname(html_path), exist_ok=True)

				markdown_content = read_file(markdown_path)
				markdown_html = markdown_parser.markdown_to_html(markdown_content)
				markdown_title = markdown_parser.extract_title(markdown_content)

				page_content = template_content.replace("{{ Title }}", markdown_title).replace("{{ Content }}", markdown_html)

				with open(html_path, 'w') as file:
					file.write(page_content)
				if logging:
					print(f"Generated: {html_path}")

current_dir = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(current_dir, "..", "static")
public_dir = os.path.join(current_dir, "..", "public")

template_path = os.path.join(current_dir, '..', 'template.html')
content_dir = os.path.join(current_dir, '..', 'content')
public_dir = os.path.join(current_dir, '..', 'public')

main(static_dir, public_dir, logging=False)
generate_html_recursive(template_path, content_dir, public_dir, logging=False)
