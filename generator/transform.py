#!/usr/bin/env python

import argparse
import io
import os
import uuid
import xml.sax.saxutils

import pystache


class ReadableDir(argparse.Action):
    """
    Utility to ensure given argument is a directory, and is Readable
    """
    def __call__(self,parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("ReadableDir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError("ReadableDir:{0} is not a readable dir".format(prospective_dir))


def read_fully(filename):
    """
    Utility to read a file
    
    :param filename: filename to read
    :return: string of files content
    """
    with io.open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def create_mustache_category(filename):
    """
    Creates a Mustache parser object with the given file
    
    :param filename: filename to parse
    :return: Parser object from Mustache
    """
    return pystache.parse(read_fully(filename))


def get_args():
    """
    Collect args and validate them.
    :return: args dict
    """
    parser = argparse.ArgumentParser(description='Auto-generates yEd palette files from AWS Simple Icons')
    parser.add_argument('directory_in', metavar='icon_dir', action=ReadableDir, help='Directory to generate from.')
    parser.add_argument('directory_out', metavar='output_dir', action=ReadableDir, help='Directory to write generated files to.')

    return parser.parse_args()


def get_category_dirs(directory):
    """
    :param directory: directory to scan 
    :return: list of files that are directories
    """
    return [os.path.join(directory, d) for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))]


def get_svg_files(directory):
    """
    :param directory: directory to scan
    :return: list of files that are not a directory
    """
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and
            f.lower().endswith(u'.svg')]


def generate_mustache_args_node(svg_id, svg_filename):
    """
    Generate Mustache arguments for a node
    :param svg_id: ID of SVG
    :param svg_filename: Filename of SVG
    :return: Mustache arguments
    """
    return {
        'id': 'n{}'.format(svg_id),
        # Escaping is a noop for UUID, but here just in-case someone wants to change the
        # 'name' value - You need to escape it!
        'name': xml.sax.saxutils.escape(u'{}'.format(uuid.uuid4())),
        'tooltip': xml.sax.saxutils.escape(svg_filename),
        'resourceId': svg_id,
    }


def generate_mustache_args_resource(svg_id, svg_content):
    """
    Generate Mustache arguments for a SVG resource
    :param svg_id: ID of SVG
    :param svg_content: Content of SVG
    :return: Mustache arguments
    """
    return {
        'id': svg_id,
        'encodedContent': xml.sax.saxutils.escape(svg_content),
    }


def generate_mustache_args(svg_files):
    """
    Generate Mustache arguments
    :param svg_files: List of SVG files
    :return: Mustache arguments
    """
    args = {
        'nodes': [],
        'resources': [],
    }
    i = 0
    for svg_file in svg_files:
        svg_content = read_fully(svg_file)
        svg_name = os.path.splitext(os.path.basename(svg_file))[0]
        args['resources'].append(generate_mustache_args_resource(i, svg_content))
        args['nodes'].append(generate_mustache_args_node(i, svg_name))
        i += 1
    return args


def main():
    args = get_args()

    mustache_renderer = pystache.Renderer()
    # Grab current directory since our mustache template is relative to us
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    mustache_parsed_category = create_mustache_category(
        os.path.join(current_file_dir, u'category.graphml.mustache'))
    categories = get_category_dirs(args.directory_in)

    print(u'Importing {} categories...'.format(len(categories)))
    for category in categories:
        svg_files = get_svg_files(category)
        category_name = os.path.basename(category)
        if len(svg_files) == 0:
            print(u'No icons found in "{}"!'.format(category_name))
            continue

        mustache_vars = generate_mustache_args(svg_files)
        category_filename = 'AWS - {}.graphml'.format(category_name)
        category_file = os.path.join(args.directory_out, category_filename)
        with io.open(category_file, 'w', encoding='utf-8') as f:
            rendered = mustache_renderer.render(mustache_parsed_category, mustache_vars)
            f.write(rendered)
        print(u'Imported "{}" ({} icons)'.format(category_name, len(svg_files)))


if __name__ == "__main__":
    main()
