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
version = '1.1.1'
build.path += ['svg', 'md', 'tbl']
build.zoteroApiKey = myZoteroCredentials.zoteroApiKey
build.zoteroLibraryId = myZoteroCredentials.zoteroLibraryId
build.setStyle('modern')
build.tableTemplate = 'pandoc'
build.pdfHeader = 'Manuscript in preparation [v%s; %s; %s]' % (version, \
	time.strftime('%c'), git.commitHash().decode())
if '--snapshot' in sys.argv:
	git.snapshot('md/__main__.md', msg=sys.argv[-1])
else:
	#build.DOC('md/__main__.md', 'latest-manuscript.doc')
	build.PDF('md/__main__.md', 'latest-manuscript.pdf', lineNumbers=False)
	# build.zoteroApiKey = None
	# build.setStyle('letter-classic')
	# build.pdfHeader = 'Coverletter [v%s; %s; %s]' % (version,
	# 	time.strftime('%c'), git.commitHash())
	# build.PDF('md/__cover_letter__.md', 'coverletter-%s.pdf' % version,
	# 	lineNumbers=False)
	# build.DOC('md/__cover_letter__.md', 'coverletter-%s.doc' % version)
	# build.ODT('md/__cover_letter__.md', 'coverletter-%s.odt' % version)
