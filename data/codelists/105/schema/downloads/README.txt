International Aid Transparency Initiative (IATI)
XML Schemas

IATI Support <support@iatistandard.org>
Version 1.05, 2014-10-06

This directory contains version 1.05 of the IATI XML
schemas, effective 2014-10-06 (subject to agreement).  More information about these schemas
is available at http://iatistandard.org

This directory contains the following files:

README.txt                      This file.

CHANGES.txt                     Change log.

iati-activities-schema.xsd      XML Schema for describing aid activities
                                (e.g. projects).

iati-organisations-schema.xsd    XML schema for describing aid
                                organisations and their budgets.

iati-common.xsd                 A supplementary schema with common
                                IATI markup.  Must be in the same
                                directory as the above.

xml.xsd                         A supplementary schema that must be in
                                the same directory as the above.

iati-registry-record-schema.xsd An application-specific extension
                                schema for importing documents into
                                the IATI registry.

tests/                          Unit tests for the schemas.

The tests include a series of short XML documents that should pass or
file when parsed against the schemas in this distribution.  The shell
scripts for running the tests rely on a Unix environment with the bash
shell and the xmllint utility, but the test documents will work with
any schema-aware XML parser. We will add unit tests as schema
development continues.

Acknowlegements
David Megginson <david.megginson@megginson.com> for his original work on
the IATI Schemas and continued support and involvment.

__end__
