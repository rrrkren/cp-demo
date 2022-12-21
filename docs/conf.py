# -*- coding: utf-8 -*-
#
# Confluent documentation build configuration file, created by
# sphinx-quickstart on Wed Dec 17 14:17:15 2014.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import re
from datetime import datetime
from docutils import nodes, utils
from sphinx.directives.code import CodeBlock
from sphinx.writers.html import HTMLTranslator

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.ifconfig', 'sphinxcontrib.httpdomain', 'sphinxcontrib.openapi']

# Setting configuration option for sphinxcontrib.httpdomain so that it does not
# complain when it encounters something that doesn't look quite like HTTP.
# Ref: https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/#additional-configuration
# - Added to account for "default" response block in OpenAPI/Swagger file from
#   metadata-service. "default" is a valid catch-all description of a response in
#   OpenAPI spec.
http_strict_mode = False
# And suppress warnings from Sphinx itself when it tries to apply HTTP syntax highlighting
# in the OpenAPI spec, but the lexer fails because of the "default" status code.
suppress_warnings = ['misc.highlighting_failure']


def _do_substitutions(config, content):
    def replacement(match):
        """Replace with either the substitution from config, or the original text if we don't have a substitution"""
        refname = match.group(1)
        return getattr(config, refname, match.group(0))

    return re.sub("\|(\w+)\|", replacement, content)


class CodeWithVarsDirective(CodeBlock):
    def run(self):
        config = self.state.document.settings.env.config

        self.content = [_do_substitutions(config, content) for content in self.content]
        return super(CodeWithVarsDirective, self).run()


def literal_with_vars_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    config = inliner.document.settings.env.app.config
    text = utils.unescape(text)

    substituted_text = _do_substitutions(config, text)
    retnode = nodes.literal(role=typ.lower(), classes=[typ])
    retnode += nodes.Text(substituted_text, substituted_text)
    return [retnode], []


class ConfluentHTMLTranslator(HTMLTranslator):
    def __init__(self, *args):
        super(ConfluentHTMLTranslator, self).__init__(*args)
        # By default, email addresses are automatically "obfuscated" via % encoding for @. It makes
        # the URL appear incorrect to users and doesn't really help since the email is easily
        # extracted and still valid anyway, so disable it.
        self.settings.cloak_email_addresses = False

def setup(app):
    def makeLink(role, rawtext, text, lineno, inliner, options={}, content=[]):
        tokens = text.split('|')
        # add link prefix per link macro
        if role == 'platform':
            linkPrefix = '/platform/' + platform_release + '/'
        if role == 'ccloud-cli':
            linkPrefix = '/ccloud-cli/' + ccloud_cli_release + '/'
        if role == 'connect-common':
            linkPrefix = '/connect/'
        if role == 'cloud':
            linkPrefix = '/cloud/' + cloud_release + '/'
        if role == 'confluent-cli':
            linkPrefix = '/confluent-cli/' + confluent_cli_release + '/'
        if role == 'kafka-javadoc':
            linkPrefix = 'https://kafka.apache.org/' + kafka_javadoc_version + '/javadoc/'
        if role == 'kafka-file':
            linkPrefix = 'https://github.com/apache/kafka/blob/' + kafka_branch + '/'
        elif role == 'ccloud-cta':
            linkPrefix = 'https://www.confluent.io/confluent-cloud/'
        linktext = tokens[0]
        if len(tokens) == 2:
            ref = linkPrefix + tokens[1]
        else:
            ref = linkPrefix + tokens[0]
            linktext = ref
        node = nodes.reference(rawtext, utils.unescape(linktext), refuri=ref, **options)
        return [node], []
    # add link macros
    app.add_role('confluent-cli', makeLink)
    app.add_role('cloud', makeLink)
    app.add_role('platform', makeLink)
    app.add_role('ccloud-cli', makeLink)
    app.add_role('connect-common', makeLink)
    app.add_role('kafka-javadoc', makeLink)
    app.add_role('kafka-file', makeLink)
    app.add_role('ccloud-cta', makeLink)
    app.add_config_value('cloud_docs', True, 'env')

    app.add_role('litwithvars', literal_with_vars_role)
    app.add_directive('codewithvars', CodeWithVarsDirective)

    app.set_translator('html', ConfluentHTMLTranslator)

    # Setup redirect pages to be generated after the rest of html page generation completes
    app.connect('build-finished', create_redirects)

    # Add the custom config values we want in the Sphinx config for substitutions
    for config_name in custom_config_names:
        app.add_config_value(config_name, '<set ' + config_name + '>', '')


# Even if it has a default, these options need to be specified
cloud_docs = True

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# Platform release
platform_release = 'current'
# Cloud release
cloud_release = 'current'
# Cloud CLI release
ccloud_cli_release = 'current'
#Confluent CLI release
confluent_cli_release = 'current'
# The short X.Y version.
version = '6.0'
# The full version, including alpha/beta/rc tags.
release = '6.0.11'
# Kafka version
kafka_branch = '2.6'
# Kafka Javadoc version
kafka_javadoc_version = '26'
# Kafka release we're tracking from upstream, so we can refer to it without the -cp version
kafka_upstream_release = '2.6.0'
# Kafka release (included in CP examples)
kafka_release = '6.0.11-ccs'
# Scala version used for CP packages
scala_version = '2.13'
# release post branch, used in ksqlDB, streams, examples
release_post_branch = release + '-post'
# CP preview release
preview = '5.4-preview'
# Version of ksqlDB, currently used for linking into ksqldb.io docs
ksqldb_version = '0.10.2'

# Confluent CLI commands
confluent_acl = 'confluent local acl'
confluent_config = 'confluent local config'
confluent_consume = 'confluent local consume'
confluent_current = 'confluent local current'
confluent_demo = 'confluent local demo'
confluent_destroy = 'confluent local destroy'
confluent_list = 'confluent local list'
confluent_load = 'confluent local load'
confluent_log = 'confluent local log'
confluent_produce = 'confluent local produce'
confluent_start = 'confluent local start'
confluent_status = 'confluent local status'
confluent_stop = 'confluent local stop'
confluent_top = 'confluent local top'
confluent_unload = 'confluent local unload'
dash = ' --'

# Kafka server properties file
ak_props = 'server.properties'
# Control Center properties file
c3_props = 'control-center.properties'
# ksqlDB properties file
cksql_props = 'ksql-server.properties'
# Kafka REST properties
crest_props = 'kafka-rest.properties'
# Kafka Connect properties
kconnect_props = 'connect-distributed.properties'
# Schema Registry properties
sr_props = 'schema-registry.properties'

# Add custom configurations/substitutions you want here. They will be automatically registered for substitution by both
# the normal rst substitution mechanism (vis rst_prolog) and in other contexts, such as codewithvars blocks. If you add
# a name here, there should be a corresponding variable of the same name in this configuration file above this line.
custom_config_names = [
    "ccloud_cli_release",
    "confluent_cli_release",
    "confluent_acl",
    "confluent_config",
    "confluent_consume",
    "confluent_current",
    "confluent_demo",
    "confluent_destroy",
    "confluent_list",
    "confluent_load",
    "confluent_log",
    "confluent_produce",
    "confluent_start",
    "confluent_status",
    "confluent_stop",
    "confluent_top",
    "confluent_unload",
    "dash",
    "kafka_release",
    "kafka_upstream_release",
    "kafka_branch",
    "kafka_javadoc_version",
    "ksqldb_version",
    "release_post_branch",
    "scala_version",
    "ak_props",
    "c3_props",
    "cksql_props",
    "crest_props",
    "kconnect_props",
    "sr_props",
    "preview"
]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '**/includes', 'includes', 'images/source', '.hidden']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# Reused terms/content

rst_prolog = """
.. |ak-tm| replace:: Apache Kafka®
.. |ak| replace:: Kafka
.. |ansible| replace:: Ansible Playbooks for Confluent Platform
.. |avro-tm| replace:: Apache Avro®
.. |aws-long| replace:: Amazon Web Services
.. |aws| replace:: AWS
.. |az-long| replace:: Microsoft Azure
.. |az| replace:: Azure
.. |bmrr| replace:: Built-in Multi-Region Replication
.. |c-hub| replace:: Confluent Hub
.. |c3-short| replace:: Control Center
.. |c3| replace:: Confluent Control Center
.. |cadb-full| replace:: Confluent Auto Data Balancer
.. |cc-components| replace:: |cp| using only |cc| components
.. |ccloud| replace:: Confluent Cloud
.. |ccloud-ent| replace:: Confluent Cloud Enterprise
.. |ccloud-cluster-desc-basic| replace:: Basic clusters are designed for development use-cases.
.. |ccloud-cluster-desc-standard| replace:: Standard clusters are designed for production-ready features and functionality.
.. |ccloud-cluster-desc-dedicated| replace:: Dedicated clusters are designed for critical production workloads with high traffic or private networking requirements.
.. |ccs| replace:: Confluent Community software
.. |cc| replace:: Confluent Community
.. |cjms-full| replace:: Confluent JMS Client
.. |cjms| replace:: JMS Client
.. |cku-long| replace:: Confluent Unit for Kafka (CKU)
.. |cmetric-full| replace:: Confluent Metrics Reporter
.. |cmetric| replace:: Metrics Reporter
.. |cmqtt-full| replace:: Confluent MQTT Proxy
.. |co-long| replace:: Confluent Operator
.. |commercial-license| replace:: Commercially licensed
.. |commercial| replace:: This is a commercial component of |cp|.
.. |community-license| replace:: Community licensed
.. |community| replace:: This is a community component of |cp|.
.. |confluent-cli| replace:: Confluent CLI
.. |cos| replace:: Confluent Open Source
.. |co| replace:: Operator
.. |cpe| replace:: Confluent Enterprise
.. |cp| replace:: Confluent Platform
.. |cplus| replace:: C++ Client
.. |crep-full| replace:: Confluent Replicator
.. |crep| replace:: Replicator
.. |crest-long| replace:: Confluent REST Proxy
.. |crest| replace:: REST Proxy
.. |csa| replace:: Confluent Server Authorizer
.. |kcsu| replace:: CSU
.. |kcsu-long| replace:: Confluent Streaming Unit
.. |cs| replace:: Confluent Server
.. |dotnet| replace:: .NET Client
.. |gce-long| replace:: Google Compute Engine
.. |gce| replace:: GCE
.. |gcp-long| replace:: Google Cloud Platform
.. |gcp| replace:: GCP
.. |go| replace:: Go Client
.. |haproxy| replace:: HAProxy
.. |java| replace:: Java Client
.. |kacls-cli| replace:: Kafka Authorization management CLI
.. |kafka-version| replace:: 1.1.0
.. |kcat| replace:: kafkacat
.. |kconnect-long| replace:: Kafka Connect
.. |kconnect| replace:: Connect
.. |ksql-cloud| replace:: KSQL
.. |ksql-ui| replace:: ksqlDB web interface
.. |ksqldb| replace:: ksqlDB
.. |kstreams| replace:: Kafka Streams
.. |lambda| replace:: AWS Lambda
.. |ldap-auth-long| replace:: Confluent LDAP Authorizer
.. |ldap-auth| replace:: LDAP Authorizer
.. |mds-long| replace:: Metadata Service (MDS)
.. |mmaker| replace:: MirrorMaker
.. |mrrep| replace:: Multi-Region Clusters
.. |mqtt| replace:: MQTT Proxy
.. |python| replace:: Python Client
.. |rbac-long| replace:: role-based access control (RBAC)
.. |rbac-sa| replace:: service principal
.. |rbac| replace:: RBAC
.. |rest-utils-long| replace:: Confluent REST Utils
.. |rest-utils| replace:: REST Utils
.. |sr-ccloud| replace:: Confluent Cloud Schema Registry
.. |sr-long| replace:: Confluent Schema Registry
.. |sr| replace:: Schema Registry
.. |sv| replace:: Schema Validation
.. |streaming| replace:: Event Streaming Platform
.. |zk-full| replace:: Apache ZooKeeper™
.. |zk| replace:: ZooKeeper
"""

rst_prolog += '\n'.join([
    ".. |" + config_name + "| replace:: " + globals()[config_name] for config_name in custom_config_names
    ])

# -- Options for HTML output ----------------------------------------------

import sphinx_rtd_theme

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'canonical_url': 'https://docs.confluent.io/ansible/current/'
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = ['images/README.txt']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'Confluentdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'Confluent.tex', u'Confluent Platform Documentation',
   u'Confluent, Inc.', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'confluent', u'Confluent Cloud Documentation',
     [u'Confluent, Inc.'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'Confluent', u'Confluent Cloud Documentation',
   u'Confluent, Inc.', 'Confluent', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False

# Set of HTML redirects for legacy pages that should be created. The key is the HTML file that will
# be created (i.e. the page that *used* to exist). The value is the destination of the redirect. It
# can be either a relative path from the key's parent directory (for a redirect that is to another
# docs page, e.g. if you have moved the page) or absolute (for external links). For relative,
# internal links, we will try to preserve the anchor so you land in the same place in the page for
# moved pages. Format: '<old-filename>': '<relative-path-to-new-filename>'
redirects = {
}

_redirect_template = """
<html>
  <head>
    <meta http-equiv="refresh" content="1; url={dest}" />
    <script>
      window.location.href = "{dest}"{anchor}
    </script>
  </head>
</html>
"""

def create_redirects(app, exception):
    """
    Create HTML-based redirects from legacy paths to current files
    """

    if exception is not None:
        return

    if app.builder.name != 'html':
        return

    # src is the legacy page we need to turn into a redirect, dest is the target page that must
    # exist the current docs
    for src, dest in redirects.items():
        src_abs = os.path.join(app.outdir, src)

        is_absolute = dest.startswith('http://') or dest.startswith('https://')
        anchor = '' if is_absolute else ' + window.location.hash'

        redirect_contents = _redirect_template.format(dest=dest, anchor=anchor)

        if os.path.exists(src_abs):
            with open(src_abs, 'r') as fp:
                contents = fp.read()
            if contents != redirect_contents:
                raise RuntimeError("Source file for redirect already exists and has different contents: {}".format(src_abs))
            continue

        src_dir = os.path.dirname(src_abs)
        if not os.path.exists(src_dir):
            os.makedirs(src_dir)
        with open(src_abs, 'w') as fp:
            fp.write(redirect_contents)

        # This check has to be after creating the source file since relative paths may refer to
        # directories that don't exist until the source file is created
        dest_abs = os.path.join(os.path.dirname(src_abs), dest)
        if not is_absolute and not os.path.isfile(dest_abs):
            raise RuntimeError("Target redirect path does not exist: {}".format(dest_abs))

import requests
url = 'https://web-wp.confluent.io/wp-admin/admin-ajax.php?action=get_confluent_navigation'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
result = requests.get(url, headers=headers)
#print(result.content.decode())
html_context = {
    'confluent_navigation': result.content.decode()
}
