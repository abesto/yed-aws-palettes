yED Section Generator
=====================

This generator module will dynamically create yED sections for easily updating this
repository or on the fly.

Requirements
------------

This python generator requires [Pystache](https://github.com/defunkt/pystache) to
work, as the underlying files are generated from a mustache template.

```bash
pip install pystache
```

Running
-------

This example assumes that you have extracted the AWS Simple Icons (EPS, SVG) to the
directory `AWS_Simple_Icons_EPS-SVG`. Ensure the output directory is created before
running.

```bash
mkdir yED-AWS-Simple_Icons
./transform.py AWS_Simple_Icons_EPS-SVG yED-AWS-Simple_Icons
```
