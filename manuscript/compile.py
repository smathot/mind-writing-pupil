#!/usr/bin/env python3

"""
This file is part of P0009.1.

P0009.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0009.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0009.1.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from academicmarkdown import build, git
import myZoteroCredentials
import time
version = '2.2.3'
build.path += ['svg', 'md', 'tbl']
build.zoteroApiKey = myZoteroCredentials.zoteroApiKey
build.zoteroLibraryId = myZoteroCredentials.zoteroLibraryId
build.setStyle('naturecomm')
build.csl = 'plos.csl'
build.docxRef = None
build.tableTemplate = 'pandoc'
build.pdfHeader = 'Manuscript in preparation [v%s; %s; %s]' % (version, \
	time.strftime('%c'), git.commitHash().decode())
if '--snapshot' in sys.argv:
	git.exportFormats = 'pdf', 'docx'
	git.snapshot('md/__main__.md', msg=sys.argv[-1])
else:
	build.DOCX('md/__main__.md', 'latest-manuscript.docx')
	build.PDF('md/__main__.md', 'latest-manuscript.pdf', lineNumbers=True)
	build.zoteroApiKey = None
	build.pdfHeader = 'S1 Appendix [v%s; %s; %s]' % (version, \
		time.strftime('%c'), git.commitHash().decode())
	build.PDF('md/__supplementary__.md', 'latest-supplementary.pdf')
	build.DOCX('md/__supplementary__.md', 'latest-supplementary.docx')
	build.setStyle('letter-classic')
	build.pdfHeader = 'Coverletter [v%s; %s; %s]' % (version,
		time.strftime('%c'), git.commitHash().decode())
	build.PDF('md/__cover_letter__.md', 'coverletter-%s.pdf' % version)
	build.DOCX('md/__cover_letter__.md', 'coverletter-%s.docx' % version)
	build.PDF('md/__response_letter__.md', 'responseletter-%s.pdf' % version)
	build.DOCX('md/__response_letter__.md', 'responseletter-%s.docx' % version)
