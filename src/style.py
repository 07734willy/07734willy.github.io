from pygments.style import Style
from pygments.styles.colorful import ColorfulStyle
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Text, Literal, Punctuation

class CodeStyle(Style):
	default_style = ColorfulStyle.default_style
	styles = {
		#**ColorfulStyle.styles,

		Keyword: "#62583e", #"#504834", #"#7e3a08",
		Keyword.Constant: "#B4B03D bold",
		String: "#B4B03D",
		Number: "#B4B03D",
		Operator: "#555",
		#Operator.Word: "#999 bold",
		Operator.Word: "#ac8854", #"#E9B770", #"#982239", #"#823b57", #"#a14222",
		Name.Builtin: "#999 bold",
		Name.Function: "#6C757A italic",
		Name.Function.Magic: "bold",
		Comment: "#555",
	}

class CodeLightStyle(Style):
	default_style = ColorfulStyle.default_style
	styles = {
		#**ColorfulStyle.styles,

		Keyword: "#E8CF98", #"#7e3a08",
		Keyword.Constant: "#a09e5c bold",
		String: "#a09e5c",
		Number: "#a09e5c",
		Operator: "#555",
		#Operator.Word: "#999 bold",
		Operator.Word: "#E9B770", #"#982239", #"#823b57", #"#a14222",
		Name.Builtin: "#999 bold",
		Name.Function: "#777 italic",
		Name.Function.Magic: "bold",
		Comment: "#555",
	}

class CodeDarkStyle(Style):
	default_style = ColorfulStyle.default_style
	styles = {
		#**ColorfulStyle.styles,

		Keyword: "#584314", #"#7e3a08",
		Keyword.Constant: "#a09e5c bold",
		String: "#a09e5c",
		Number: "#a09e5c",
		Operator: "#555",
		#Operator.Word: "#999 bold",
		Operator.Word: "#8d5c16", #"#982239", #"#823b57", #"#a14222",
		Name.Builtin: "#999 bold",
		Name.Function: "#777 italic",
		Name.Function.Magic: "bold",
		Comment: "#555",
	}
	
class OldCodeStyle(Style):
	default_style = ColorfulStyle.default_style
	styles = {
		#**ColorfulStyle.styles,

		Keyword: "#7e3a08",
		Keyword.Constant: "#a09e5c bold",
		String: "#a09e5c",
		Number: "#a09e5c",
		Operator: "#555",
		#Operator.Word: "#999 bold",
		Operator.Word: "#584314", #"#982239", #"#823b57", #"#a14222",
		Name.Builtin: "#999 bold",
		Name.Function: "#777 italic",
		Name.Function.Magic: "bold",
		Comment: "#555",
	}
