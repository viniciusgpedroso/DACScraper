# Constants
FIRST_SEMESTER = "01° Semestre"
FIRST_SEMESTER_ALT = "01� Semestre"
ELECTIVES_DETECTOR = "Disciplinas Eletivas"
FIRST_YEAR = "2013"  # Previous catalogs do not have the same structure
LAST_YEAR = "2020"

# REGEX
REGEX_CATALOG_YEAR = r'catalogo([0-9]{4})'
REGEX_PRE_REQ = r'<strong>Pré-Req.: <\/strong>(.*)<br>'
REGEX_SYLLABUS = r'<strong>Ementa: .*?>(.*?)(<\/p>|<br>)'
REGEX_CODE = r'(OF.*?)<br>'
REGEX_TITLE = r'- (.*)'
REGEX_ID = r'(\*?[A-Z]{2}[0-9]{1,3}|\*?[A-Z] [0-9]{1,3})'
REGEX_EMPHASIS_DETECTOR = r'([A-Z]{1,3}) -'
REGEX_COURSE_CODE_FROM_PROPOSAL_URL = r'sug([0-9]{1,3})'
REGEX_COURSE_NAME = r'Curso [0-9]{1,3} - (.*)'
REGEX_CREDITS_AMOUNT = r'([0-9]{1,2}) Cr'
REGEX_NUMERIC_ONLY = r'[^0-9]'
REGEX_REMOVE_PARENTHESES = r'\([^)]*\)'

# XPATH
XPATH_IDS = '//div[@class="div10b"]//@href'
XPATH_PARENT = "//div[@class='ancora']"
XPATH_TITLE = "self::*//a/text()"
XPATH_CODES = "self::*//following-sibling::p[1]"
XPATH_SYLLABUS = "self::*//following-sibling::div[@class='justificado']//p/text() | self::*//following-sibling::div[@class='justificado']/text()"
XPATH_COURSE_CODE = '//div[@class="texto"]//span/text()'
XPATH_COURSE = "//h2[contains(text(), 'Curso')]/text()"
XPATH_EMPHASIS = "//h1/text()"
XPATH_SEMESTER = '//div[@class="div100"]//a[contains(text(), "(")]/text() | //div[@class="div100"]//text()[contains(., "Semestre")]'
XPATH_SEMESTER += ' | //div[@class="div100"]//text()[contains(., "eletivos")]'
XPATH_ELECTIVES = '//strong[contains(text(),"Disciplinas Eletivas")]'
XPATH_ELECTIVES_DATA = '//following-sibling::br//following-sibling::text()[contains(.,"dentre")]'
XPATH_SUBJECTS = '/following-sibling::div//div[@class="div50b"]/a/text()'
