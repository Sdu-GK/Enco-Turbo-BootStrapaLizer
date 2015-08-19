import sublime, sublime_plugin

class minimize_cssCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		region = sublime.Region(0, self.view.size())
		content = self.view.substr(region)

		compact_split = content.split()
		temp_cl = ' '.join(compact_split)
		compact_content = temp_cl.replace(' {', '{').replace('{ ', '{').replace(' }', '}').replace('} ', '}').replace(' ;', ';').replace('; ', ';').replace(' :', ':').replace(': ', ':').replace(' ,', ',').replace(', ', ',').replace('*/ ', '*/')

		self.view.replace(edit, region, compact_content)


class expand_cssCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		self.view.run_command('minimize_css')

		region = sublime.Region(0, self.view.size())
		content = self.view.substr(region)
		content_arr = list(content)
		line_br = '\n'
		ident_chr = '\t'
		ident_str = ''
		prev_chr = ''
		is_comment = 0
		comment_closed = 0
		clean_content = ''

		for cur_chr in content_arr:

			if cur_chr == ';' and is_comment == 0:
				clean_content += cur_chr + line_br + ident_str

			elif cur_chr == '}' and is_comment == 0:
				if prev_chr == ';':
					clean_content += cur_chr + line_br
					ident_str = ident_str.replace(ident_chr, '', 1)
					clean_content += ident_str

				elif prev_chr == '}':
					clean_content += cur_chr
					ident_str = ident_str.replace(ident_chr, '', 1)
					clean_content += ident_str + line_br

				else:
					clean_content += line_br + ident_str + cur_chr + line_br
					ident_str = ident_str.replace(ident_chr, '', 1)
					clean_content += ident_str

			elif cur_chr == '{' and is_comment == 0:
				ident_str += ident_chr
				clean_content += ' ' + cur_chr + line_br + ident_str

			elif cur_chr == '/' and prev_chr == '*':
				clean_content += cur_chr + line_br  + ident_str
				is_comment = 0
				comment_closed = 1

			elif cur_chr == '*' and prev_chr == '/' and comment_closed == 1:
				clean_content += cur_chr
				is_comment = 0
				comment_closed = 0

			elif cur_chr == '*' and prev_chr == '/' and comment_closed == 0:
				clean_content += cur_chr
				is_comment = 1

			else:
				clean_content += cur_chr
				if is_comment == 0 and comment_closed == 1:
					comment_closed = 0

			prev_chr = cur_chr

		self.view.replace(edit, region, clean_content)
