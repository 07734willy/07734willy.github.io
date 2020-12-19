from pygments.style import Style
from pygments.styles.colorful import ColorfulStyle
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic

class CodeStyle(Style):
	default_style = ColorfulStyle.default_style
	styles = {
		**ColorfulStyle.styles,

		Comment:  'italic #888',
	}
	
