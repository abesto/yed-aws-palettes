#!/bin/sh
cat <<EOF
This script must be run from the yed-aws-palettes repository

It assumes the .graphml files have been manually imported from SVGs before the run.
The import cannot be automated due the fact that the yEd Software License Agreement explicitly
forbids the usage of yEd in any kind of automated process.

It further assumes that palette names have the form "AWS - \$CATEGORY.graphml" where "\$CATEGORY" is
a directory in "\$1", which is the extracted AWS Simple Icons SVG archive used for the initial import.

It works on the third and final assumption that the listing of the files in each category is in
the same order as the order of the symbols in the yED palettes (holds because yED lists the
files the same way we do).
EOF

svgdir="$1"
for category_dir in $svgdir/*; do
    category=$(basename "$category_dir")
    echo
    echo "Starting category $category"
    ls "$category_dir/" \
    | sort -f \
    | cut -f2 -d_ \
    | sed -e 's/\.svg$//' \
    | python ./add_tooltips.py "AWS - $category.graphml"
    echo "Done with category $category"
done
